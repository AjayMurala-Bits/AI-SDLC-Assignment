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
$env:MOVIE_REVIEW_MODEL = "gpt-5.4-mini"
$env:MOVIE_REVIEW_MAX_TOKENS = "6000"
$env:MOVIE_REVIEW_JUDGE_MAX_TOKENS = "4000"
```

The proposal uses the same model for application and judge, with output
ceilings of 800 and 600 tokens respectively. Automatic retries are disabled.
For `N` cases and
`N_semantic` semantic cases, the expected budget is `N + N_semantic` calls;
the minimum 15-case all-semantic budget is 30 calls. At the official standard
prices, the 15-case token-ceiling estimate is $0.207 USD. Account access must
still be confirmed before paid execution.

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
