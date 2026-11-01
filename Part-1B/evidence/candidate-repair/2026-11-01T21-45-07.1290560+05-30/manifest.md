# Second harness-driven repair snapshot

- Snapshot timestamp: 2026-11-01T21:45:07.1290560+05:30
- Scope: Part-1B only; first-generation and first-repair snapshots are unchanged.
- Provider used for re-evaluation: local Ollama `llama3.2:latest` at `http://127.0.0.1:11434/v1`.
- Frozen dataset and thresholds: unchanged; dataset SHA-256 remains `fdbf5bc8ca3f95539b19b10f0075955dcafee0549818615f64980a26e727f9f0`.
- Changed production files: `src/movie_review_summarizer/application.py`, `prompts/summarize.txt`.
- Changed validation files: `tests/test_application.py`, `.harness/focused_diagnostics.py`.
- Repair intent: generic evaluative-evidence preflight, uncertainty-safe handling of vague hedge-only text, balanced sentiment guardrail, and focused diagnostics through application orchestration with telemetry.
- No case IDs, benchmark labels, exact review phrases, credentials, judge changes, dataset changes, threshold changes, or OpenAI calls were added.

Evidence copied into this snapshot:

- `focused-diagnostic.json` is the final 8-case focused local Ollama run.
- `full-evaluation-run.json` is a copy of the unchanged full-run report; the original remains at `evidence/evaluation-results/2026-11-01T21-37-47.229+05-30/run.json`.

