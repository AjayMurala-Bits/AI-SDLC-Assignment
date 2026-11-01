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
- `MOVIE_REVIEW_MODEL`: selected model name; record the value in configuration
  evidence only if it is non-secret.
- The runner must fail clearly when required configuration is missing and must
  classify provider timeouts, quota errors, and unavailable services as model /
  service failures.

## Evaluation runner

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\.harness\run_evaluation.ps1
```

The runner loads `evals/dataset.json`, executes the application, runs
structural and property checks independently, invokes the semantic judge only
for `semantic` cases, and writes a new timestamped evidence folder. It must
not let judge output override structural, property, grounding, or service
failure gates.
