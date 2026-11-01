# Validation setup evidence

- Capture time: 2026-10-31T20:12:40.950+05:30 (Asia/Kolkata).
- The previous failed run remains unchanged at `../../harness-results/2026-10-31T20-07-39.033+05-30/`.
- Added `requirements-dev.txt` declaring the approved Ruff and Bandit gates.
- Updated the harness to use the project-local `.venv\Scripts\python.exe` and invoke Ruff, Bandit, and unittest through that interpreter.
- The project-local environment could not be created because the configured Python path was absent and no usable Python executable or installer was found.
- No new harness result was run after this setup change.
- Before/after harness copies are `harness-before.ps1` and `harness-after.ps1` in this folder.
