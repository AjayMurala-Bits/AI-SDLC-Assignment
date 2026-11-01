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
$runFolder = Join-Path $partRoot ('evidence\diagnostics\neg-001-ab-' + ((Get-Date -Format o) -replace ':', '-'))
Write-Host 'Running Experiment A: Ollama json_object mode; one NEG-001 request.'
& $python '.\.harness\neg_ab_diagnostic.py' --mode json_object --output (Join-Path $runFolder 'experiment-a-json-object.json')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'Running Experiment B: Ollama JSON Schema mode; one NEG-001 request.'
& $python '.\.harness\neg_ab_diagnostic.py' --mode json_schema --output (Join-Path $runFolder 'experiment-b-json-schema.json')
exit $LASTEXITCODE
