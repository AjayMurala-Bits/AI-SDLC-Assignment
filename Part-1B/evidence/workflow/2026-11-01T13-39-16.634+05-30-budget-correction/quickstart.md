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
$env:MOVIE_REVIEW_MAX_TOKENS = "7000"
$env:MOVIE_REVIEW_JUDGE_MAX_TOKENS = "10000"
```

The proposal uses the same model for application and judge, with output
ceilings of 1200 and 2000 total output tokens respectively, including billed
reasoning and non-visible formatting tokens. Set `reasoning.effort=none` and
automatic retries are disabled. The judge receives the complete bounded review,
application output and rubric; count tokens and fail rather than truncate.
For `N` cases and
`N_semantic` semantic cases, the expected budget is `N + N_semantic` calls;
the minimum 15-case all-semantic budget is 30 calls. At the official standard
prices, the 15-case token-ceiling estimate is $0.40725 USD. Account access must
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
