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
- `MOVIE_REVIEW_MAX_INPUT_TOKENS` and `MOVIE_REVIEW_JUDGE_MAX_INPUT_TOKENS`:
  configured input ceilings used for cost estimation; values are `7000` and
  `10000` respectively.
- `MOVIE_REVIEW_MAX_OUTPUT_TOKENS` and
  `MOVIE_REVIEW_JUDGE_MAX_OUTPUT_TOKENS`: configured total output ceilings;
  values are `1200` and `2000` respectively. These include billed reasoning
  and non-visible formatting tokens. Count input tokens before each call and
  fail rather than truncate. Record all four values and
  `reasoning.effort=none` in sanitized evidence.
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
silently excluded. Each case result must link its stable `case_id` and `run_id`
to the input/fixture, application output, judge result when applicable, gate
results, and aggregate decision. The runner performs no scraping, website
access, login, or automatic action beyond the documented model request.
