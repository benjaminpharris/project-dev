#!/usr/bin/env python3
"""
Derive survey structure from the column names alone, then attach PDF text
at the BLOCK level (not the item level, which drifts between the sample
instrument and the deployed one).

The naming convention carries four independent signals:

    GS 0405 _ GSAD HASEXPER _n23
    ^^ ^^^^   ^^^^ ^^^^^^^^ ^^^^
    |  |      |    |        └─ version: r=revised, n=new, ext=institution ext
    |  |      |    └─ item mnemonic
    |  |      └─ section mnemonic (AD = advising)
    |  └─ block  (join key; stable across instrument versions)
    └─ instrument (GS = gradSERU core, INT = international module)

Block membership is recoverable two ways (numeric block, section mnemonic)
which lets each validate the other. Question kind is recoverable from block
cardinality plus the presence of a 'none of the above' sentinel.
"""

import re
import pandas as pd
from pathlib import Path

ITEM_RE = re.compile(r"^(?P<instrument>GS|INT)\d{4}")

DECOMP_RE = re.compile(r"""
    ^(?P<instrument>GS|INT)
     (?P<block_num>\d{4})
     (?P<block_suffix>[A-Z]?)
     _
     (?P<body>.*?)
     (?P<version>_(?:[rn]\d{2}|ext\d+))?
     (?P<option>_\d{1,3})?
    $
""", re.VERBOSE)

# Section mnemonic sits at the head of the body, after a GS/IS repeat.
MNEMONIC_RE = re.compile(r"^(?:GS|IS)(?P<mn>[A-Z]{2})")

SECTIONS = {
    "YP": "YOUR PROGRAM",
    "OS": "OVERALL SATISFACTION",
    "IE": "SELECTION AND ADMISSION",
    "FS": "FINANCIAL SUPPORT",
    "AD": "ADVISING",
    "RE": "RESEARCH EXPERIENCE",
    "TE": "TEACHING EXPERIENCE",
    "PC": "PROGRAM CLIMATE",
    "HW": "HEALTH AND WELL-BEING",
    "GA": "USE OF GENERATIVE AI TOOLS",
    "GG": "USE OF GENERATIVE AI TOOLS",
    "OB": "OBSTACLES TO COMPLETION",
    "CP": "CAREER PLANS",
    "DM": "DEMOGRAPHICS",
    "FP": "FUTURE PLANS",
    "IS": "INTERNATIONAL STUDENT EXPERIENCE",
}

# The six items whose body omits the section mnemonic. Cheaper to declare
# than to infer, and declaring them documents the exception.
MNEMONIC_OVERRIDE = {
    "GS0306_DBTCNCRN_n20": "FS",
    "GS0306_DBTINFLC_r23": "FS",
    "GS0701_SUPPENVR_r20": "PC",
    "GS0703_RLGSTLRN_n20": "PC",
    "GS0703_PLTCTLRN_n20": "PC",
    "GS0803_CPTOPCHOIC": "CP",
}

# 'None of the above' / 'Other, specify' sentinels mark a checkbox block.
SENTINEL_RE = re.compile(r"(NONEABVE|NOABV|NONE$|OTHER$|OTHR|NO$)", re.I)


def decompose(columns):
    rows = []
    for c in columns:
        if not ITEM_RE.match(c):
            rows.append({"code": c, "role": "admin_or_appended"})
            continue
        m = DECOMP_RE.match(c)
        g = m.groupdict()
        body = g["body"]

        if c in MNEMONIC_OVERRIDE:
            mn = MNEMONIC_OVERRIDE[c]
            item_mn = body
        elif g["instrument"] == "INT":
            mn = "IS"                                  # international module
            item_mn = re.sub(r"^IS", "", body)
        else:
            mm = MNEMONIC_RE.match(body)
            mn = mm.group("mn") if mm else None
            item_mn = body[len(mm.group(0)):] if mm else body

        ver = (g["version"] or "").lstrip("_")
        rows.append({
            "code": c,
            "role": "survey_item",
            "instrument": g["instrument"],
            "block": g["instrument"] + g["block_num"],
            "block_num": int(g["block_num"]),
            "block_suffix": g["block_suffix"] or "",
            "mnemonic": mn,
            "section": SECTIONS.get(mn),
            "item_mnemonic": item_mn,
            "version": ver,
            "version_kind": ("revised" if ver.startswith("r")
                             else "new" if ver.startswith("n")
                             else "extension" if ver.startswith("ext")
                             else ""),
            "version_year": (2000 + int(ver[1:3])) if re.match(r"^[rn]\d{2}$", ver) else pd.NA,
            "option_num": int(g["option"].lstrip("_")) if g["option"] else pd.NA,
        })
    return pd.DataFrame(rows)


def classify_blocks(df):
    items = df[df.role == "survey_item"].copy()
    size = items.groupby("block")["code"].transform("size")
    items["block_size"] = size

    has_sent = (items.assign(
                    s=items.item_mnemonic.str.contains(SENTINEL_RE, na=False)
                      | items.option_num.notna())
                .groupby("block")["s"].transform("any"))

    items["kind"] = [
        "standalone" if n == 1 else ("multiselect" if s else "matrix")
        for n, s in zip(items.block_size, has_sent)
    ]
    # Item order within block preserves questionnaire option order.
    items["item_order"] = items.groupby("block").cumcount() + 1
    return items


def attach_pdf(items, pdf_csv):
    """Join PDF text at block level; item text matched only where codes align."""
    pdf = pd.read_csv(pdf_csv)
    pdf["block"] = pdf["code"].str.extract(r"^((?:GS|INT)\d{4})")

    # One stem per block: the modal (longest) stem seen for that block.
    stems = (pdf.dropna(subset=["block"])
               .assign(L=pdf["question_stem"].astype(str).str.len())
               .sort_values("L", ascending=False)
               .groupby("block")
               .agg(stem_from_pdf=("question_stem", "first"),
                    section_from_pdf=("section", "first"),
                    pdf_page=("page", "first")))

    out = items.merge(stems, on="block", how="left")

    # Item label: exact code match first, then version-insensitive.
    norm = lambda s: s.str.replace(r"_(?:[rnRN]\d{2}|ext\d+)$", "", regex=True).str.upper()
    lut = dict(zip(norm(pdf["code"]), pdf["item_text"]))
    out["item_label_from_pdf"] = norm(out["code"]).map(lut)
    return out


def main():
    cols = [l.strip() for l in open("cols.txt") if l.strip()]
    df = decompose(cols)
    items = classify_blocks(df)
    full = attach_pdf(items, "/mnt/user-data/outputs/seru_data_dictionary.csv")

    full["needs_text"] = full["stem_from_pdf"].isna() | full["item_label_from_pdf"].isna()
    full["section_conflict"] = (
        full["section_from_pdf"].notna()
        & (full["section"] != full["section_from_pdf"])
    )

    print(f"columns            : {len(df)}")
    print(f"  survey items     : {len(items)}")
    print(f"  admin/appended   : {(df.role == 'admin_or_appended').sum()}")
    print(f"blocks             : {items.block.nunique()}")
    print(f"sections           : {items.section.nunique()}")
    print()
    print(items.kind.value_counts().to_string())
    print()
    print(f"stem from PDF      : {full.stem_from_pdf.notna().sum()}/{len(full)}")
    print(f"item label from PDF: {full.item_label_from_pdf.notna().sum()}/{len(full)}")
    print(f"needs manual text  : {int(full.needs_text.sum())}")
    print(f"section conflicts  : {int(full.section_conflict.sum())}")

    out = Path("/mnt/user-data/outputs")
    full.to_csv(out / "seru_schema.csv", index=False)
    return full


if __name__ == "__main__":
    main()
