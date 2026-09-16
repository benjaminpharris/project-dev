# VS Code notebook state investigation — 2026-09-12

The original failure was reproduced with the installed native Python environment locator (PET): a discovery refresh overlapping a successful interpreter-resolution request could omit `env_finance`. Python's discovery adapter interpreted the missing entry as deletion, and Jupyter disposed the active notebook controller while the Python kernel remained alive. Three single-request overlap trials reproduced the omission; a subsequent refresh rediscovered the environment.

The original session's Jupyter log recorded the controller deletion at 18:02:08 and `notebook controller is DISPOSED` at 18:09:32. Direct heartbeat and silent, history-free probes showed that its metadata and raw DataFrames survived. The standalone reproduction artifacts were in `/tmp` and did not survive the subsequent restart.

The first workaround attempt put `"python.locator": "js"` in the Default profile's settings. **That targeted the wrong profile.** This workspace is associated with the `Project-Dev` profile, whose settings are independent of Default settings. The profile shares extensions with Default, but does not share settings.

After `cachy-update`:

- VS Code changed from 1.136.2 to 1.137.0.
- The active Python extension remained 2026.4.0; Jupyter remained 2025.9.1.
- The Default-profile locator override survived the update.
- The Project-Dev profile had no locator override, and startup logs confirmed that the native PET locator still ran.

The corrected configuration is now in:

```text
/home/ben/.config/Code/User/profiles/-3d455735/settings.json
```

It contains `"python.locator": "js"`. The unintended Default-profile override was removed. Both edits were checked against their parsed originals to confirm that every other preference was preserved. Backups from this correction are in `/tmp/finance-kernel-profile-correction/` until the next cleanup or reboot.

The installed Python extension chooses its locator implementation during initialization. The corrected setting therefore requires the next extension startup to take effect. The investigation did not restart the user's kernel or reload the window.

The session started at 18:39 on the updated editor is distinct from the original failure. Kernel PID 17337 answered both heartbeat and shell requests and retained `metadata_df` with shape `(19, 1)` and `TICKERS`; its execution count was 3. At the time of inspection, its logs had **not** recorded the original controller-deletion error. The current UI stall's exact cause remains unconfirmed; finding the mis-targeted setting does not establish that both stalls have the same cause.

Verification after the next reload:

1. Confirm that the workspace still uses the Project-Dev profile and its locator preference remains `js`.
2. In the newly started extension host, confirm Python uses the JavaScript discovery path and does not start its bundled `python-env-tools/bin/pet server`.
3. Run the import and metadata cells, inspect Variables, then execute the raw-cache cell.
4. Recheck after leaving the notebook idle. A short successful run does not establish indefinite state persistence.

Evidence locations:

- Profile/workspace association: `/home/ben/.config/Code/User/globalStorage/storage.json`, under `profileAssociations` and `userDataProfiles`.
- Original logs: `/home/ben/.config/Code/logs/20260912T133215/window1/exthost/`.
- Post-update logs: `/home/ben/.config/Code/logs/20260912T183356/window1/exthost/`.
- Latest inspected Jupyter output: `output_logging_20260912T183937/1-Jupyter.log` under the post-update directory.

[VS Code documents profile-specific settings and workspace associations.](https://code.visualstudio.com/docs/configure/profiles#_folder-workspace-associations)
