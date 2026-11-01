# Data Model: Movie Review Summarizer

## ReviewInput

- `path`: local file path supplied to the CLI.
- `text`: UTF-8 review text, limited to 20,000 characters by default.
- The text is untrusted data and is never interpreted as commands.

## SuccessResult

- `summary`: non-empty string, at most 80 whitespace-separated words and 3
  sentences under the approved `.?!` counting rule.
- `sentiment`: one of `positive`, `negative`, `mixed`, `unclear`.
- `positive_aspects`: array of 0–5 strings, each at most 12 words.
- `negative_aspects`: array of 0–5 strings, each at most 12 words.
- `recommendation`: non-empty string, at most 30 words.
- No additional top-level fields are allowed.

## FailureResult

```json
{
  "error": {
    "type": "invalid_input | empty_input | insufficient_evidence | model_failure | invalid_model_output | evaluation_failure",
    "message": "observable human-readable application error"
  }
}
```

Semantic scores and aggregate PASS/FAIL decisions are evaluation entities, not
application output fields.

## EvaluationCase

- `id`: stable case identifier.
- `class`: `semantic`, `deterministic`, or `service-failure`.
- `input` or fixture reference.
- `requirements`: mapped requirement IDs.
- `expected_properties`: deterministic expectations and/or expected failure.
- `rubric`: semantic anchors when class is `semantic`.

## EvaluationResult

- Per-case structural, property, and semantic results.
- Semantic scores only for `semantic` cases.
- Service-failure classification and environment details separately recorded.
- Aggregate formula, `N_semantic`, `ceil(0.90 × N_semantic)`, mandatory failures,
  and overall PASS/FAIL.
