# Part-1B Movie Review Summarizer

This project contains the approved movie-review summarizer implementation and
evaluation harness.

- Ollama is the default local provider at `http://127.0.0.1:11434/v1` using
  `llama3.2:latest`. No credential is required or stored.
- The OpenAI provider remains available through private environment setup.
- Offline tests and mock evaluation are not live model evidence.
- Live execution uses the documented harness after dataset approval and freeze.
- Application and judge retries remain zero; prompts, thresholds, dataset and
  initial snapshot are preserved.
- Evidence is preserved under `evidence/`.
