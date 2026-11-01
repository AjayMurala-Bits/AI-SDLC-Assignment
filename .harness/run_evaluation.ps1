[CmdletBinding()]
param(
    [ValidateSet('offline', 'live')]
    [string]$Mode = 'offline',
    [string]$Dataset = 'evals/dataset.json'
)

$ErrorActionPreference = 'Stop'
$partRoot = Split-Path -Parent $PSScriptRoot
Set-Location $partRoot
$env:PYTHONPATH = Join-Path $partRoot 'src'
$python = Join-Path $partRoot '.venv\Scripts\python.exe'
$env:MOVIE_REVIEW_PROVIDER = 'ollama'
$env:OLLAMA_BASE_URL = 'http://127.0.0.1:11434/v1'
$env:MOVIE_REVIEW_MODEL = 'llama3.2:latest'
$env:MOVIE_REVIEW_MAX_INPUT_TOKENS = '7000'
$env:MOVIE_REVIEW_MAX_OUTPUT_TOKENS = '1200'
$env:MOVIE_REVIEW_JUDGE_MAX_INPUT_TOKENS = '10000'
$env:MOVIE_REVIEW_JUDGE_MAX_OUTPUT_TOKENS = '2000'

if (-not (Test-Path -LiteralPath $python)) {
    throw "Part-1B venv interpreter is missing: $python"
}

function Invoke-Evaluation {
    param([string]$SelectedMode)
    & $python -m movie_review_summarizer.evaluation.runner --mode $SelectedMode --dataset $Dataset
    exit $LASTEXITCODE
}

if ($Mode -eq 'offline') {
    Write-Host 'Running OFFLINE MOCK evaluation only; this is not live model evidence.'
    Invoke-Evaluation -SelectedMode 'offline'
}

Write-Host 'Live evaluation requires an approved and frozen dataset.'
Write-Host 'Running LIVE evaluation against the local Ollama service. No OpenAI call is made.'
Invoke-Evaluation -SelectedMode 'live'

