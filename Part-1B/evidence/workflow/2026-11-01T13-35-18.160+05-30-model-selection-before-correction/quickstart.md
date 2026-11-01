# Planning Quickstart: Movie Review Summarizer

This is a planning guide only. Application code and model calls are not part
of this step.

## Separate environment

Use the working Part-1A Python setup only as a reference. Create a separate
Part-1B environment and install only the dependencies declared for Part-1B.
Do not copy Part-1A evidence or environment files into Part-1B.

## Local configuration

Set the OpenAI API credential locally; never paste it into chat or save it in
source/evidence:

```powershell
$env:OPENAI_API_KEY = "<local-secret-not-recorded>"
$env:MOVIE_REVIEW_MODEL = "<selected-model>"
$env:MOVIE_REVIEW_MAX_TOKENS = "<application-token-ceiling>"
$env:MOVIE_REVIEW_JUDGE_MAX_TOKENS = "<judge-token-ceiling>"
```

The exact model and token ceilings must be selected before approval or paid
execution. The application and judge use the same selected model in this
minimal plan. Automatic retries are disabled. For `N` cases and
`N_semantic` semantic cases, the expected budget is `N + N_semantic` calls;
the minimum 15-case all-semantic budget is 30 calls. A maximum dollar cost is
reported only after model pricing and ceilings are configured.

## Planned commands

```powershell
$env:PYTHONPATH = (Join-Path (Get-Location) "src")
python -m movie_review_summarizer --input .\reviews.txt
powershell -NoProfile -ExecutionPolicy Bypass -File .\.harness\run_evaluation.ps1
```

The evaluation runner must preserve exact commands, configuration names (not
secret values), raw application/judge outputs, per-case gate results, failure
classifications, scores, and the aggregate decision under a new timestamped
`evidence/` folder.
