# CLI Contract: Movie Review Summarizer

## Invocation

From the Part-1B root:

```powershell
$env:PYTHONPATH = (Join-Path (Get-Location) "src")
python -m movie_review_summarizer --input .\reviews.txt
```

The exact option spelling remains a small implementation detail, but the CLI
must accept one local review-file path and emit JSON only on stdout. Errors use
the typed failure shape and a non-zero exit code.

## Runtime configuration

- `OPENAI_API_KEY`: required locally; never print or save it.
- `MOVIE_REVIEW_MODEL`: exact selected model name used by both application and
  judge; record it in sanitized configuration evidence only if non-secret.
- `MOVIE_REVIEW_MAX_TOKENS` and `MOVIE_REVIEW_JUDGE_MAX_TOKENS`: configured
  token ceilings used for cost estimation. Proposed values are `6000` and
  `4000` input tokens respectively, with output ceilings of `800` and `600`;
  record the final values in sanitized configuration evidence.
- The runner must fail clearly when required configuration is missing and must
  classify provider timeouts, quota errors, and unavailable services as model /
  service failures. Automatic retries are disabled (`0`).

## Evaluation runner

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\.harness\run_evaluation.ps1
```

The runner loads `evals/dataset.json`, executes the application, runs
structural and property checks independently, invokes the semantic judge only
for `semantic` cases, and writes a new timestamped evidence folder. It must
not let judge output override structural, property, grounding, or service
failure gates. Malformed judge output, judge-call failure, and unexpected
application-call failure remain recorded cases and force overall FAIL; none is
silently excluded.
