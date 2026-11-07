# Part 1B AI Movie Review Summarizer Harness Log

Record actual event timestamps when available and distinguish them from entry recording timestamps. 

## 1 Specification Context and Initial Generation

Record the approved constitution, specification, plan and tasks supplied to the coding agent; relevant prompts; and the initial-generation snapshot path.

Student entry:

Recorded 2026-11-01T20:39:40.022+05:30:
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

Student entry: 2026-11-01T20:45:40.022+05:30:
Provider: ollama
Model: llama3.2:latest
Endpoint: http://127.0.0.1:11434/v1
Credential status: no credential recorded/present
Application version: 0.1.0
Application input limit: 7000 tokens
Application output limit: 1200 tokens

## 3 Scoring Method and Acceptance Thresholds


Student entry: Student entry: 2026-11-01T20:55:40.022+05:30:

Structural: required fields, exact JSON keys, types, sentiment values, word/sentence limits, array limits, and failure envelopes.
Properties: deterministic requirements such as correct error types, expected sentiment etc.
Semantic: faithfulness, coverage, and uncertainty/usefulness.
Semantic scoring:
Faithfulness: 40%
Coverage: 35%
Uncertainty/usefulness: 25%
Each dimension is scored from 0–4.

## 4 Evaluation Runs and Outcomes

Student entries:

Recorded 2026-11-01T21:39:40.022+05:30:
The failed cases and evidence are saved in
`evidence/evaluation-results/2026-11-01T20-14-22.104+05-30/run.json`.
Dominant failures were Ollama schema/output compatibility (invalid sentiment
or five-field shape for six semantic cases) and two semantic judge failures
for POS-001 and MIX-001. There were no provider or judge service errors.
Token usage was not captured by the full runner; the report identifies the
instrumentation gap. No repair or rerun was performed.

## 5 Genuine Failures and Feedback

Student entries:

Recorded 2026-11-01T21:39:40.022+05:30:
No repair or revalidation occurred after this run. The smallest proposed next
experiment is one local NEG-001 diagnostic that preserves sanitized raw output,
parsed keys/sentiment, validation errors, and usage.

## 6 Repairs and Revalidation

Explain actual changes to code, prompts, parsers, validators or guardrails. Link before/after artifacts and rerun results. Verify whether the same dataset, checks and thresholds were retained, and disclose any legitimate reviewed specification revision.

Student entries:

Recorded 2026-11-01T21:45:07.1290560+05:30:
Second re-evaluation completed using local Ollama only. The repair added general-purpose evidence sufficiency and uncertainty
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


Student entry:

Decision supplied by the student: **ACCEPT**.

- Justification: the student supplied the ACCEPT decision; no further
  justification was recorded in the source instruction.
- Known limitations and residual risks: the final full Ollama evaluation
  passed structural checks `16/16` and property checks `16/16`, but semantic
  checks passed only `2/8` against the required `8/8`; the overall automated
  result was FAIL. The remaining semantic failures are documented in
  `../evaluation-results/2026-11-01T21-37-47.229+05-30/run.json` and the
  evidence-integrity report
  `workflow/2026-11-01T22-14-54.1542327+05-30-semantic-integrity-report.md`.
- Final evaluation and snapshot references: `../evaluation-results/2026-11-01T21-37-47.229+05-30/run.json` and
  `candidate-repair/2026-11-01T21-45-07.1290560+05-30/manifest.md`.
