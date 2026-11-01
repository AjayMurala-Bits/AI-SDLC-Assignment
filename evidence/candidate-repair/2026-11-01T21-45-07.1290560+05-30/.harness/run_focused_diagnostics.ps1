[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$partRoot = Split-Path -Parent $PSScriptRoot
Set-Location $partRoot
$python = Join-Path $partRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $python)) { throw "Part-1B venv interpreter is missing: $python" }
$env:PYTHONPATH = Join-Path $partRoot 'src'
$env:MOVIE_REVIEW_PROVIDER = 'ollama'
$env:OLLAMA_BASE_URL = 'http://127.0.0.1:11434/v1'
$env:MOVIE_REVIEW_MODEL = 'llama3.2:latest'
$env:MOVIE_REVIEW_MAX_INPUT_TOKENS = '7000'
$env:MOVIE_REVIEW_MAX_OUTPUT_TOKENS = '1200'
$env:MOVIE_REVIEW_JUDGE_MAX_INPUT_TOKENS = '10000'
$env:MOVIE_REVIEW_JUDGE_MAX_OUTPUT_TOKENS = '2000'
$runFolder = Join-Path $partRoot ('evidence\diagnostics\focused-' + ((Get-Date -Format o) -replace ':', '-'))
Write-Host 'Running focused Ollama diagnostics only; no judge or full evaluation is invoked.'
& $python '.\.harness\focused_diagnostics.py' --output (Join-Path $runFolder 'focused.json')
exit $LASTEXITCODE
