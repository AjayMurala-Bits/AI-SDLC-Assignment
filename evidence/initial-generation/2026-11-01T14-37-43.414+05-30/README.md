# Part-1B Movie Review Summarizer

This project contains the implementation and evaluation harness for the
approved movie-review summarizer specification.

- Credentials are supplied privately through `OPENAI_API_KEY` and are never
  committed, printed, or stored in evidence.
- Offline tests and mock evaluation are not live model evidence.
- Live API execution is manual and external to Codex/VS Code PowerShell, using
  `.harness/run_evaluation.ps1 -Mode live` after dataset approval and freeze.
- The model is `gpt-5.4-mini`; application and judge retries are zero.
- The initial-generation snapshot is preserved before any validation-driven
  repair.

