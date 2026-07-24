#!/usr/bin/env python3
"""
gradSERU 2025 instrument -> per-section data dictionary.

Uses the PDF font layer instead of flat text. The instrument encodes its
own structure typographically:

    24pt bold            -> section header
    10pt bold, x0~36     -> question stem (wraps; continuation stays bold)
    10pt regular, x0~42  -> matrix item label / response option
    14pt Courier 'o'     -> radio grid (marks a matrix, gives column count)
    (CODE) in parens     -> variable name for the item on that row
    10pt italic          -> display logic / instructions

Output: one DataFrame per section, plus a combined long-format frame.
Nothing here is expected to be perfect — the goal is a high-recall draft
with provenance (page, y-position) on every row so it can be checked
against the PDF and hand-corrected quickly.
"""

import re
import pdfplumber
import pandas as pd
from pathlib import Path

PDF = Path("/mnt/user-data/uploads/gradSERU_2025_Survey_Instrument_sample.pdf")

CODE_RE = re.compile(r"""
    \b(
        (?:GS|INT)\d{4}[A-Z]?(?:_[A-Za-z][A-Za-z0-9]*)*
      | (?:GS|CP)[A-Z]{6,}(?:_[A-Za-z0-9]+)*
    )\b
""", re.VERBOSE)

LOGIC_VARS = {"ONLINE_MOD", "LEVEL_GRAD", "INTL_MOD", "PROGRAM_TEXT1"}
LOGIC_RE = re.compile(r"\b(" + "|".join(LOGIC_VARS) + r")\b")

NOISE_RE = re.compile(
    r"^\s*((Display|spl) This (Question|Choice|Item|Section)|Carry Forward|"
    r"Skip To|Page \d+ of \d+|q://)", re.IGNORECASE)

STEM_MIN_X = 40      # stems start at the left margin (~36)
RADIO_SIZE = 13.5    # the 'o' glyphs render at 14pt


def build_lines(page):
    """Group chars into visual lines carrying font metadata."""
    buckets = {}
    for ch in page.chars:
        buckets.setdefault(round(ch["top"] / 3.0) * 3, []).append(ch)

    out = []
    for top in sorted(buckets):
        chs = sorted(buckets[top], key=lambda c: c["x0"])
        text = "".join(c["text"] for c in chs)
        if not text.strip():
            continue
        n = len(chs)
        out.append({
            "top": top,
            "x0": min(c["x0"] for c in chs),
            "size": max(c["size"] for c in chs),
            "bold": sum("Bold" in c["fontname"] for c in chs) / n,
            "italic": sum("Italic" in c["fontname"] for c in chs) / n,
            "text": re.sub(r"\s+", " ", text).strip(),
        })
    return out


def clean(t):
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"^[▢▼⊗]\s*", "", t)
    t = t.replace("⊗", "")
    t = re.sub(r"_{4,}", "", t)
    return t.strip(" .,;-")


def strip_code(t):
    t = CODE_RE.sub("", t)
    t = re.sub(r"\(\s*\)", "", t)
    return clean(t)


def is_radio(ln):
    """A row of the response grid."""
    return ln["size"] >= RADIO_SIZE and set(ln["text"].replace(" ", "")) <= {"o", "○"}


def is_header(ln):
    return ln["size"] >= 16 and ln["bold"] > 0.5


def is_stem(ln):
    """Bold body text at the left margin starts (or continues) a stem."""
    return (ln["bold"] >= 0.5 and 9 <= ln["size"] <= 12
            and ln["x0"] < STEM_MIN_X and not NOISE_RE.match(ln["text"]))


def is_scale_row(ln, grid_x0=None):
    """Response anchors sit right of the item column, above the radio grid.

    Multi-line anchor headers ("Very / dissatisfied (1)") wrap leftward, so
    a fixed x cutoff misses their first line. When the radio grid's left
    edge is known, use that as the boundary instead.
    """
    if ln["bold"] >= 0.5:
        return False
    bound = (grid_x0 - 30) if grid_x0 else 150
    if ln["x0"] < min(bound, 150):
        return False
    t = ln["text"]
    if re.fullmatch(r"[\s\(\)\d]+", t):            # a bare '(1) (2) (3)' row
        return True
    numbered = len(re.findall(r"\(\d{1,2}\)", t))
    if numbered >= 2:
        return True
    return bool(re.fullmatch(
        r"(?:Very|Not|Slightly|Extremely|Strongly|Somewhat|Never|Sometimes|"
        r"Often|Fair|Good|Poor|More|Less|No|Yes|dis|un)?\s*"
        r"[A-Za-z/\- ]{2,26}(?:\s*\(\d{1,2}\))?", t.strip()))


def parse():
    pdf = pdfplumber.open(PDF)
    records, logic = [], []

    section = "FRONT MATTER"
    stem = None
    stem_page = stem_top = None
    last_stem_top = -999
    scale_buf = []
    grid_x0 = None
    inline_row = None
    pending_stem = []          # accumulates wrapped bold lines
    carry_item = []            # regular-text lines awaiting their code

    def flush_stem():
        nonlocal stem, pending_stem, last_stem_top
        if pending_stem:
            stem = clean(" ".join(pending_stem))
            pending_stem = []
            last_stem_top = -999

    for pno, page in enumerate(pdf.pages, start=1):
        if pno <= 2:           # cover + TOC
            continue
        for ln in build_lines(page):
            txt = ln["text"]

            for lm in LOGIC_RE.finditer(txt):
                logic.append({"variable": lm.group(1), "page": pno,
                              "section": section, "context": clean(txt)[:90]})

            if is_header(ln):
                flush_stem()
                name = clean(txt).upper()
                # 'INTERNATIONAL STUDENT' / 'EXPERIENCE' wrap across lines
                if section == "INTERNATIONAL STUDENT" and name == "EXPERIENCE":
                    section = "INTERNATIONAL STUDENT EXPERIENCE"
                else:
                    section = name
                stem, carry_item = None, []
                continue

            if is_radio(ln):
                flush_stem()
                grid_x0 = ln["x0"] if grid_x0 is None else min(grid_x0, ln["x0"])
                continue

            if is_scale_row(ln, grid_x0):
                scale_buf.append(clean(txt))
                if len(scale_buf) > 6:
                    scale_buf = scale_buf[-6:]
                continue

            if NOISE_RE.match(txt):
                carry_item = []
                continue

            if is_stem(ln):
                # A standalone question carries its code inline, inside the
                # bold line: "GS0401_GSADPRIMRYAD Do you currently have...".
                inline = [c for c in CODE_RE.findall(txt) if c not in LOGIC_VARS]
                if inline:
                    # A bold section intro may already be buffered; it is
                    # preamble, not this question's stem — discard it.
                    pending_stem = []
                    body = strip_code(txt)
                    records.append({
                        "section": section,
                        "code": inline[0],
                        "question_stem": body,
                        "item_text": "",
                        "page": pno,
                        "y": round(ln["top"]),
                        "stem_page": pno,
                        "n_codes_on_line": len(inline),
                        "response_options": "",
                        "_inline": True,
                    })
                    stem, stem_page, stem_top = body, pno, ln["top"]
                    last_stem_top = ln["top"]
                    inline_row = records[-1]   # allow bold wrap to extend it
                    carry_item = []
                    scale_buf = []
                    grid_x0 = None
                    continue

                # A vertical gap or a page change means this bold line
                # starts a NEW stem rather than continuing the previous one.
                if (inline_row is not None and not pending_stem
                        and ln["top"] - last_stem_top <= 26):
                    inline_row["question_stem"] = clean(
                        inline_row["question_stem"] + " " + clean(txt))
                    last_stem_top = ln["top"]
                    stem = inline_row["question_stem"]
                    continue

                if pending_stem and (ln["top"] - last_stem_top > 26):
                    flush_stem()
                    stem_page, stem_top = pno, ln["top"]
                if not pending_stem:
                    stem_page, stem_top = pno, ln["top"]
                pending_stem.append(clean(txt))
                last_stem_top = ln["top"]
                carry_item = []
                scale_buf = []
                grid_x0 = None
                continue

            # Non-bold line: close any open stem, then treat as item text.
            flush_stem()
            inline_row = None

            codes = CODE_RE.findall(txt)
            codes = [c for c in codes if c not in LOGIC_VARS]
            label = strip_code(txt)

            if not codes:
                if label:
                    carry_item.append(label)
                    if len(carry_item) > 3:
                        carry_item = carry_item[-3:]
                continue

            # This line owns one or more codes. Item text = any wrapped
            # lines above it plus whatever remains on this line.
            item = clean(" ".join(carry_item + ([label] if label else [])))
            carry_item = []

            for code in codes:
                records.append({
                    "section": section,
                    "code": code,
                    "question_stem": stem or "",
                    "item_text": item,
                    "page": pno,
                    "y": round(ln["top"]),
                    "stem_page": stem_page,
                    "n_codes_on_line": len(codes),
                    "response_options": " | ".join(scale_buf),
                })

    pdf.close()
    return pd.DataFrame(records), pd.DataFrame(logic)


def main():
    df, logic_df = parse()

    # The first item in each matrix can absorb fragments of the anchor
    # header sitting directly above it (the grid position that bounds those
    # anchors isn't known until the first radio row is seen). Strip any
    # leading run of anchor words from the item label.
    ANCHOR_HEAD = re.compile(
        r"^(?:\s*(?:Very|Not|No|Slightly|Extremely|Strongly|Somewhat|Never|"
        r"Sometimes|Often|Fair|Good|Poor|Yes|To a|at all|all|small|large|"
        r"moderate|applicable|extent|competent|well|helpful|interested|true|"
        r"satisfied|dissatisfied|agree|disagree|Decreased|Increased|change|"
        r"\(\d{1,2}\))\b[,\s]*)+", re.IGNORECASE)

    def strip_anchor_head(t):
        if not t:
            return t
        out = ANCHOR_HEAD.sub("", t).strip(" .,;-")
        # Only accept the strip if it leaves a real label behind.
        return out if len(out) >= 8 else t

    df["item_text_raw"] = df["item_text"]
    df["item_text"] = df["item_text"].map(strip_anchor_head)

    # Flag rows whose label still carries anchor-header contamination.
    # These are almost always the FIRST item of a matrix block; the label
    # is present but preceded by scale words. Cheap to fix by hand.
    ANCHOR_WORDS = {"very", "not", "slightly", "extremely", "strongly",
                    "poor", "fair", "good", "applicable", "extent", "all",
                    "moderate", "large", "small", "dissatisfied", "satisfied",
                    "competent", "true", "agree", "disagree", "helpful"}

    def contaminated(t):
        if not isinstance(t, str) or not t:
            return False
        head = t.split()[:6]
        hits = sum(w.lower().strip("(),") in ANCHOR_WORDS for w in head)
        return hits >= 2

    df["anchor_bleed"] = df["item_text"].map(contaminated)

    # Item type: a stem with several coded rows beneath it is a matrix.
    counts = df.groupby(["section", "question_stem"])["code"].transform("size")
    df["item_type"] = counts.map(lambda n: "matrix_item" if n > 1 else "standalone")
    # Standalone questions carry the text in the stem, not the item.
    df.loc[(df["item_type"] == "standalone") & (df["item_text"] == ""),
           "item_text"] = df["question_stem"]

    df["q_prefix"] = df["code"].str.extract(r"^((?:GS|INT)\d{4})")
    df["needs_review"] = (
        (df["question_stem"].str.len() < 15)
        | ((df["item_text"].str.len() < 3) & (df["item_type"] == "matrix_item"))
        | df["code"].duplicated(keep=False)
        | df["anchor_bleed"]
    )

    sections = {s: g.reset_index(drop=True) for s, g in df.groupby("section", sort=False)}

    print(f"total coded rows : {len(df)}")
    print(f"unique codes     : {df['code'].nunique()}")
    print(f"sections         : {len(sections)}")
    print(f"flagged for review: {int(df['needs_review'].sum())}")
    print()
    for s, g in sections.items():
        print(f"  {s:<36} {len(g):>4} items  "
              f"{g['question_stem'].nunique():>3} stems  "
              f"{int(g['needs_review'].sum()):>3} flagged")

    out = Path("/mnt/user-data/outputs")
    out.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(out / "seru_data_dictionary.xlsx") as xw:
        cols = ["code", "question_stem", "item_text", "response_options",
                "item_type", "q_prefix", "page", "y", "anchor_bleed",
                "needs_review"]
        df[["section"] + cols].to_excel(xw, sheet_name="ALL", index=False)
        for s, g in sections.items():
            tab = re.sub(r"[^A-Za-z0-9 ]", "", s)[:31] or "UNTITLED"
            g[cols].to_excel(xw, sheet_name=tab, index=False)
        if not logic_df.empty:
            logic_df.to_excel(xw, sheet_name="display_logic", index=False)
        df[df["needs_review"]][["section"] + cols].to_excel(
            xw, sheet_name="REVIEW", index=False)

    df.to_csv(out / "seru_data_dictionary.csv", index=False)
    return df, sections


if __name__ == "__main__":
    main()
