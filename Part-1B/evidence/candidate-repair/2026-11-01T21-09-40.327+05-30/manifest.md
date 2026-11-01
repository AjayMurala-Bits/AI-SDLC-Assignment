# Candidate repair manifest

Timestamp: 2026-11-01T21:09:40.327+05:30 (Asia/Kolkata)

This candidate preserves the original application snapshot and frozen dataset.
It contains only the repaired production prompt/adapter and the focused test
and diagnostic harness additions used for validation.

Changed production files:

- `src/movie_review_summarizer/provider.py` — Ollama application requests now
  use the unchanged `success_schema()` through JSON Schema response format.
- `prompts/summarize.txt` — generic sentiment decision rules and grounding
  constraints were made explicit; no case-specific wording was added.

Validation additions:

- `tests/test_ollama_provider.py` — offline assertion that the exact existing
  schema is sent to the Ollama adapter.
- `.harness/focused_diagnostics.py` and
  `.harness/run_focused_diagnostics.ps1` — local-only focused diagnostics; no
  judge or full evaluation invocation.

Unchanged by this candidate: dataset, dataset lock/hash, acceptance
thresholds, judge, initial-generation snapshot, OpenAI adapter, historical
run artifacts and previous diagnostic evidence.
