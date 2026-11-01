# Python host-path correction and project-local setup

- Capture time: 2026-10-31T20:20:37.589+05:30 (Asia/Kolkata).
- Earlier discovery record: the previous sandbox discovery reported no usable Python. That conclusion was incorrect because sandbox access blocked the supplied path.
- Correction: `C:\Users\mail2\AppData\Local\Programs\Python\Python314\python.exe` exists and reports Python 3.14.7 when accessed with the required permission.
- Project-local environment: `.venv` creation succeeded.
- Dependency installation: `requirements-dev.txt` installation succeeded with exit code 0.
- Installed versions: pip 26.2.1, Ruff 0.17.3, Bandit 1.9.4.
- Harness setup now resolves `.venv\Scripts\python.exe` explicitly for all three mandatory gates.
- No application source or tests were repaired after the new Ruff findings.
