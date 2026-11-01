# Part-1B Movie Review Summarizer

This project contains the implementation and evaluation harness for the
approved movie-review summarizer specification.

- Ollama is the default local provider: `http://127.0.0.1:11434/v1` with
  model `llama3.2:latest`. No credential is required or stored.
- The existing OpenAI provider remains available by setting
  `MOVIE_REVIEW_PROVIDER=openai`, `MOVIE_REVIEW_MODEL=gpt-5.4-mini`, and
  supplying `OPENAI_API_KEY` privately. The key is never committed, printed,
  or stored in evidence.
- Offline tests and mock evaluation are not live model evidence.
- Live model execution is manual and external to Codex/VS Code PowerShell,
  using `.harness/run_evaluation.ps1 -Mode live` after dataset approval and
  freeze. The current local diagnostic uses Ollama only.
- Application and judge retries remain zero; the approved dataset, prompts,
  thresholds, and initial snapshot are unchanged.
- The initial-generation snapshot is preserved before any validation-driven
  repair.

