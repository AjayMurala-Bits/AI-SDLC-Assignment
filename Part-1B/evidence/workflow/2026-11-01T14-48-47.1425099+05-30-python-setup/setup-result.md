# Part-1B Python setup result

- Timestamp: `2026-11-01T14:48:47.1425099+05:30` (Asia/Kolkata)
- Scope: Part-1B only
- Existing initial snapshot: preserved and not modified
- Prior environment-failure evidence: preserved

## Host interpreter requested

```text
C:\Users\mail2\AppData\Local\Programs\Python\Python314\python.exe
```

The environment configuration tool recognized this path as Python `3.14.7`, but the execution sandbox could not access it. A PowerShell `Test-Path` returned `Access is denied`, and one explicit venv creation attempt could not invoke the path. No repeated retries were made.

## Attempted setup command

```powershell
$target = Join-Path (Get-Location) '.venv'
& 'C:\Users\mail2\AppData\Local\Programs\Python\Python314\python.exe' -m venv $target
```

Observed result:

```text
TARGET=D:\Ajay\WILP\Sem1\AI Augmented SDLC\Lab\Assignment\AI SDLC- Assignment\Part-1B\.venv
TARGET_EXISTS=False
The term 'C:\Users\mail2\AppData\Local\Programs\Python\Python314\python.exe' is not recognized ...
```

The PowerShell host did not propagate a reliable nonzero exit code, so this is recorded as **SETUP BLOCKED**, not successful setup. No Part-1B `.venv` was created by this attempt.

## Exact external PowerShell commands

Run these manually from an external PowerShell session where the host interpreter is accessible. The API key is not part of these commands and must be entered privately only if a later live workflow is approved.

```powershell
Set-Location 'D:\Ajay\WILP\Sem1\AI Augmented SDLC\Lab\Assignment\AI SDLC- Assignment\Part-1B'
$hostPython = 'C:\Users\mail2\AppData\Local\Programs\Python\Python314\python.exe'
& $hostPython --version
& $hostPython -m venv (Join-Path (Get-Location) '.venv')
$part1bPython = Join-Path (Get-Location) '.venv\Scripts\python.exe'
& $part1bPython -m pip install --upgrade pip
& $part1bPython -m pip install -r requirements.txt
```

Use the explicit interpreter for every local check; do not rely on PATH:

```powershell
$env:OPENAI_API_KEY = $null
$env:OPENAI_BASE_URL = 'http://127.0.0.1:9'
$env:PYTHONPATH = (Join-Path (Get-Location) 'src')
& $part1bPython -m unittest discover -s tests -v
& $part1bPython -m movie_review_summarizer.evaluation.runner --mode offline --dataset evals/dataset.json
```

The loopback base URL is a guard against accidental network use. Do not run `--mode live` for this validation.

