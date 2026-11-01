# Part 1B AI Movie Review Summarizer Harness Log

This is an AI-created blank template, not a record of completed work. The student supplies narrative entries based on actual observations. Link entries to preserved machine evidence. Do not include API keys or credentials.

Record actual event timestamps when available and distinguish them from entry recording timestamps. Use ISO 8601 with the timezone offset, for example +05:30 for Asia/Kolkata. If an event time is unknown, state "exact time not recorded" rather than inventing it. Preserve earlier entries and run results.

## 1 Specification Context and Initial Generation

Record the approved constitution, specification, plan and tasks supplied to the coding agent; relevant prompts; and the initial-generation snapshot path.

Student entry:

Machine-evidence entry recorded 2026-11-01T20:39:40.022+05:30:
The Ollama full evaluation run `2026-11-01T20-14-22.104+05-30` used provider
`ollama`, model `llama3.2:latest`, endpoint `http://127.0.0.1:11434/v1`, zero
retries and the approved token ceilings. No OpenAI call was made. The frozen
dataset SHA-256 remained
`fdbf5bc8ca3f95539b19b10f0075955dcafee0549818615f64980a26e727f9f0`.
Structural checks were `16/16` PASS, properties `8/16` PASS, semantic
`0/8` PASS against the required `8/8`, and overall result was FAIL. This is
not OpenAI-model acceptance and no human acceptance was recorded. Detailed
root-cause analysis: `evidence/workflow/2026-11-01T20-39-40.022+05-30-ollama-root-cause-analysis.md`.

## 2 Model and Evaluation Configuration

Record the provider, exact model identifier, relevant generation settings, prompt version and application version. If a separate evaluator model is used, record its configuration too. Link to configuration evidence without secrets.

Student entry:

## 3 Scoring Method and Acceptance Thresholds

Reference the approved schema, mandatory properties, semantic rubric, score calculation and thresholds established before evaluation. Explain how service failures and non-applicable checks are handled under the specification.

Student entry:

## 4 Evaluation Runs and Outcomes

For each actual run, add its run ID, event timestamp, recording timestamp, dataset version, command, structural results, property results, semantic scores, aggregate PASS/FAIL and evidence links. Distinguish service/setup failures from application/evaluation failures.

Student entries:

Machine-evidence entry recorded 2026-11-01T20:39:40.022+05:30:
The failed cases and evidence are preserved unchanged in
`evidence/evaluation-results/2026-11-01T20-14-22.104+05-30/run.json`.
Dominant failures were Ollama schema/output compatibility (invalid sentiment
or five-field shape for six semantic cases) and two semantic judge failures
for POS-001 and MIX-001. There were no provider or judge service errors.
Token usage was not captured by the full runner; the report identifies the
instrumentation gap. No repair or rerun was performed.

## 5 Genuine Failures and Feedback

Identify actual failed cases, generated outputs, failed requirement IDs, expected properties or rubric criteria, observed results and the evidence supplied back to the coding agent. Do not manufacture a failure. If no failures occurred, record that only after evaluation.

Student entries:

Machine-evidence entry recorded 2026-11-01T20:39:40.022+05:30:
No repair or revalidation occurred after this run. The smallest proposed next
experiment is one local NEG-001 diagnostic that preserves sanitized raw output,
parsed keys/sentiment, validation errors, and usage, followed by an adapter
structured-output compatibility check if needed. Thresholds, dataset and
prompts remain unchanged.

## 6 Repairs and Revalidation

Explain actual changes to code, prompts, parsers, validators or guardrails. Link before/after artifacts and rerun results. Verify whether the same dataset, checks and thresholds were retained, and disclose any legitimate reviewed specification revision.

Student entries:

Machine-evidence entry recorded 2026-11-01T21:45:07.1290560+05:30:
Second harness-driven repair and re-evaluation completed using local Ollama
only. The repair added general-purpose evidence sufficiency and uncertainty
guardrails, clarified dominant-versus-balanced sentiment, and routed focused
diagnostics through the application. The first repair snapshot, frozen dataset,
thresholds and prior evidence remain unchanged. Offline tests passed `24/24`.
The final focused run `2026-11-01T21-35-32.926+05-30` passed schema `8/8` and
properties `8/8`: [focused diagnostic](../diagnostics/focused-2026-11-01T21-33-45.9303600+05-30/focused.json).
The unchanged full Ollama re-evaluation `2026-11-01T21-37-47.229+05-30`
passed structural `16/16` and properties `16/16`, but semantic passed `2/8`
against required `8/8`, so overall result was FAIL. The failed semantic cases
were POS-001, CON-001, VAG-001, BND-001, INJ-001 and WEAK-001. No provider,
parser or judge service failure was recorded; this remains an application
grounding/coverage failure, not acceptance. Evidence: [full run](../evaluation-results/2026-11-01T21-37-47.229+05-30/run.json),
[repair report](workflow/2026-11-01T21-45-07.1290560+05-30-second-harness-repair-report.md),
and [candidate snapshot](candidate-repair/2026-11-01T21-45-07.1290560+05-30/manifest.md).
This checkpoint records repairing and re-evaluating only; no human acceptance
was recorded.

## 7 Final Human Decision

Record the student's explicit ACCEPT/REJECT decision, actual decision and recording timestamps, justification, known limitations and residual risks. Link final evaluation results and the final-generation snapshot. An automated PASS is not human acceptance.

Student entry:
