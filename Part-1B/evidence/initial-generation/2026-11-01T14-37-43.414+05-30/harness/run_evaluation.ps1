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

function Invoke-Evaluation {
    param([string]$SelectedMode)
    & python -m movie_review_summarizer.evaluation.runner --mode $SelectedMode --dataset $Dataset
    exit $LASTEXITCODE
}

if ($Mode -eq 'offline') {
    Write-Host 'Running OFFLINE MOCK evaluation only; this is not live model evidence.'
    Invoke-Evaluation -SelectedMode 'offline'
}

Write-Host 'Live evaluation requires an approved and frozen dataset.'
$key = Read-Host 'Enter the replacement OpenAI API key privately (input is hidden)' -AsSecureString
$bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($key)
try {
    $env:OPENAI_API_KEY = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)
    Write-Host 'Running LIVE evaluation through this external PowerShell session. The key is not saved.'
    Invoke-Evaluation -SelectedMode 'live'
}
finally {
    if ($bstr -ne [IntPtr]::Zero) {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
    }
    Remove-Item Env:OPENAI_API_KEY -ErrorAction SilentlyContinue
}

