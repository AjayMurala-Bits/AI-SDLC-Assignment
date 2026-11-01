Work only inside Part-1B.

Use speckit-plan with the approved constitution and clarified specification.
Keep the Python CLI and implementation simple.

Plan:
- Source under src/, prompts under prompts/, tests under tests/.
- Evaluation cases in evals/dataset.json.
- One evaluation runner under .harness/.
- Independent schema and property checks.
- Semantic evaluation using the approved rubric and scoring formula.
- Timestamped raw outputs, per-case results, scores, failures and
  aggregate decisions under evidence/.
- Separate model/service failures from application/evaluation failures.
- Preserve initial generation before evaluation-driven repairs.

Before finalizing the plan, ask me which model provider and access
method I can use. Do not assume my Codex subscription provides API access.
Never ask me to paste API keys into chat.

Explain a simple semantic-evaluation approach and its limitations.
If proposing an LLM judge, explain its additional calls/cost and keep
schema/property checks independent. Do not change approved thresholds.

Use the working Python setup from Part-1A as an environment reference,
but keep Part-1B dependencies and evidence separate.

Preserve this prompt and planning artifacts with actual timestamps.
Do not create application code, run paid model calls, record plan
approval, or generate my narrative harness log.

Ensure to log harness-log.md when required
