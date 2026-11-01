$ErrorActionPreference = "Continue"
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repoRoot
$started = Get-Date
$runName = $started.ToString("yyyy-MM-ddTHH-mm-ss.fffzzz").Replace(":", "-")
$runDir = Join-Path $repoRoot (Join-Path "evidence\harness-results" $runName)
New-Item -ItemType Directory -Path $runDir -Force | Out-Null
$env:PYTHONPATH = (Join-Path (Get-Location) "src")

$steps = @(
    [ordered]@{ Name = "ruff"; FilePath = "ruff"; Arguments = @("check", "src", "tests") },
    [ordered]@{ Name = "bandit"; FilePath = "bandit"; Arguments = @("-r", "src") },
    [ordered]@{ Name = "unittest"; FilePath = "python"; Arguments = @("-m", "unittest", "discover", "-s", "tests", "-v") }
)
$results = @()
foreach ($step in $steps) {
    $stepDir = Join-Path $runDir $step.Name
    New-Item -ItemType Directory -Path $stepDir -Force | Out-Null
    $command = "$($step.FilePath) " + ($step.Arguments -join " ")
    Set-Content -Path (Join-Path $stepDir "command.txt") -Value $command -Encoding utf8
    $process = Start-Process -FilePath $step.FilePath -ArgumentList $step.Arguments -RedirectStandardOutput (Join-Path $stepDir "stdout.txt") -RedirectStandardError (Join-Path $stepDir "stderr.txt") -NoNewWindow -PassThru -Wait
    Set-Content -Path (Join-Path $stepDir "exit-code.txt") -Value ([string]$process.ExitCode) -Encoding utf8
    $results += [ordered]@{ name = $step.Name; command = $command; exit_code = $process.ExitCode }
}

$ended = Get-Date
$passed = ($results | Where-Object { $_.exit_code -ne 0 }).Count -eq 0
$summary = [ordered]@{
    run_start = $started.ToString("yyyy-MM-ddTHH:mm:ss.fffzzz")
    run_end = $ended.ToString("yyyy-MM-ddTHH:mm:ss.fffzzz")
    timezone = "Asia/Kolkata"
    python_path = $env:PYTHONPATH
    overall = if ($passed) { "PASS" } else { "FAIL" }
    commands = $results
}
$summary | ConvertTo-Json -Depth 5 | Set-Content -Path (Join-Path $runDir "summary.json") -Encoding utf8
Write-Output $summary.overall
if ($passed) { exit 0 } else { exit 1 }
