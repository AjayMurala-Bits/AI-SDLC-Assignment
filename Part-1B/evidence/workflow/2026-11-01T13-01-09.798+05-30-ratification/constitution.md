<!--
Sync Impact Report
- Version change: 0.1.0 → 1.0.0 (student-approved ratification)
- Modified principles: replaced placeholder principles with AI review CLI, grounded claims, input safety, failure handling, and evaluation integrity.
- Added sections: Technical and Evidence Constraints; Quality and Evaluation Workflow.
- Removed sections: none; template placeholders were replaced.
- Follow-up TODOs: none.
-->

# AI Movie Review Summarizer Constitution

## Core Principles

### I. Simple CLI and Runtime Model
The application MUST be a simple Python command-line interface that reads
reviews from a local text file and invokes an AI model at runtime. The CLI
MUST expose clear success and failure results without adding features outside
the approved problem statement.

### II. Structured and Grounded Output
The summarizer MUST produce structured JSON that conforms to the approved
schema. Every claim, sentiment, theme, and limitation MUST be grounded only
in the supplied review text; the model MUST NOT invent facts or rely on
unstated outside knowledge.

### III. Review Text Is Data
Review content MUST be treated as untrusted data, never as instructions to
the application or model. Prompts MUST keep review text separate from system
and task instructions, and the application MUST preserve the intended task
when reviews contain instruction-like text.

### IV. Explicit Uncertainty and Service Failure
The application MUST explicitly report insufficient evidence when the
reviews do not support a requested conclusion. AI service failures,
malformed model responses, and invalid input MUST produce a clear failure
result and MUST NOT be presented as a successful summary.

### V. Independent Evaluation Gates
Evaluation MUST include independent schema checks, behavioural checks, and
semantic evaluation. Acceptance thresholds MUST be defined before evaluation
runs and MUST be applied consistently to the actual outputs.

## Technical and Evidence Constraints

- Actual prompts, model outputs, configuration, and evaluation results MUST be
  preserved with capture timestamps.
- Source code and evidence MUST contain no secrets, credentials, or API keys.
- Evidence MUST distinguish captured facts from student-authored narrative.
- Checks MUST NOT be weakened, skipped, or altered to obtain PASS, and
  failures MUST NOT be fabricated.

## Quality and Evaluation Workflow

- Tests and evaluation cases MUST be derived from the approved specification.
- Schema and behavioural checks MUST be independently executable from the
  semantic evaluator.
- A result is PASS only when all mandatory checks meet their pre-declared
  thresholds and the actual evidence is preserved.
- The student MUST review the evidence and make the final acceptance decision.

## Governance

This constitution governs Part-1B work and takes precedence over informal
implementation preferences. Amendments require a documented rationale,
preservation of the prior version, and explicit student approval before the
amended constitution is treated as ratified. Every workflow step MUST verify
that scope, grounding, security, evaluation, and evidence requirements remain
consistent with this constitution.

**Version**: 1.0.0 | **Ratified**: 2026-11-01 | **Last Amended**: 2026-11-01
