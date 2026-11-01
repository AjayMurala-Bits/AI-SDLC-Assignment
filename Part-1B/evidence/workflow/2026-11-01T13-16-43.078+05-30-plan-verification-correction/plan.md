# Implementation Plan: Movie Review Summarizer

**Branch**: `001-movie-review-summarizer` | **Date**: 2026-11-01 | **Spec**: [spec.md](./spec.md)

**Input**: Approved and clarified feature specification.

**Status**: Corrected verification draft; not ready for approval.

The provider/access method is selected, but the exact model name, token
budgets, and provider pricing needed for a maximum dollar estimate are not
yet selected. No model calls have been made.

## Summary

Build a small Python CLI that reads one local review text file, makes one
runtime model request, and writes either the approved five-field JSON success
object or a typed observable failure object. Keep the application, schema
checks, property checks, and semantic evaluator separate. Use one PowerShell
evaluation runner and preserve all raw and aggregate evidence.

## Technical Context

**Language/Version**: Python; use the working Part-1A Python setup as a
reference only. Create a separate Part-1B environment and record its actual
version during implementation.

**Primary Dependencies**: Python OpenAI API client, with `OPENAI_API_KEY`
and `MOVIE_REVIEW_MODEL` supplied locally through environment variables or a
credential store. The application model and judge model are both the exact
non-secret value of `MOVIE_REVIEW_MODEL`; no exact model is currently
configured. Secrets MUST never be copied into source or evidence.

**Storage**: Local input text files and timestamped JSON/text evidence; no
application database.

**Testing**: `unittest` for application/schema/property tests; independent
structural and property checks must be directly executable without a semantic
judge.

**Target Platform**: Windows PowerShell development environment, with CLI
paths and commands documented relative to Part-1B.

**Project Type**: Python command-line application and evaluation harness.

**Performance Goals**: One model request per application invocation and no
automatic retries; no application performance target beyond completing a
normal local run without unbounded retries.

**Constraints**: One UTF-8 local input file, 20,000-character default limit,
no secrets in source/evidence, no scraping/login/database/automatic actions,
and no paid model calls during planning.

**Scale/Scope**: One movie per invocation and at least 15 evaluation cases;
small local assignment-scale dataset.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Simple CLI and runtime model**: PASS — one Python CLI and one model request.
- **Structured and grounded output**: PASS — schema and review-only grounding
  are specified before implementation.
- **Review text is data**: PASS — prompts keep review content separate from
  task instructions and test adversarial text.
- **Explicit uncertainty and service failure**: PASS — typed observable
  failures and separate service-gate reporting are required.
- **Independent evaluation gates**: PASS — structural, property, and semantic
  layers remain independent, with fixed thresholds.
- **Evidence/no secrets/integrity**: PASS — raw prompts, outputs,
  configuration, timestamps, failures, and decisions are preserved; no keys or
  fabricated results are allowed.
- **Student acceptance**: PASS — the harness reports results but does not
  decide final acceptance.

## Proposed Design

### CLI and application boundaries

- `src/movie_review_summarizer/cli.py`: parse an input path and emit JSON only.
- `src/movie_review_summarizer/application.py`: load/validate input, call the
  provider adapter once, validate the model response, and map observable
  failures to the approved error types.
- `src/movie_review_summarizer/provider.py`: one narrow OpenAI API adapter;
  model name comes from `MOVIE_REVIEW_MODEL` and credentials stay local.
- `src/movie_review_summarizer/schema.py`: success/failure shape and limit
  validation shared by the application and structural evaluator.
- `prompts/summarize.txt`: task instructions that explicitly mark review text
  as data and require grounded JSON.

The application does not calculate semantic scores or decide whether its own
summary is faithful. That work belongs to the evaluation harness.

### Model calls, failures, and cost boundary

- For a dataset of `N` cases and `N_semantic` cases classified `semantic`, the
  expected budget is `N` application calls plus `N_semantic` judge calls. With
  the minimum 15-case dataset and all cases semantic, this is 15 application
  calls plus 15 judge calls, or 30 total calls.
- Automatic retry limit is zero for both application and judge calls. A later
  manual rerun is a separate preserved run and is not silently folded into a
  prior result.
- Every case remains in the result set. An application-call failure is an
  observable typed model/service failure; an unexpected one fails the overall
  result. A deterministic expected service-failure case may pass only its
  explicitly defined failure classification. A judge-call failure is a service
  failure, is not a semantic pass, and forces overall FAIL. Malformed judge
  output is an evaluation failure, is not a semantic pass, and forces overall
  FAIL. No failed case is excluded from a denominator.
- The harness must record configured application and judge token ceilings and
  provider pricing before any paid run. Maximum cost is calculated as
  `N * application_cost_for_configured_ceiling + N_semantic * judge_cost_for_configured_ceiling`.
  A dollar maximum cannot be stated yet because the exact model, token
  ceilings, and pricing are not selected; this is a readiness blocker, not a
  reason to guess a cost.

### Evaluation layers

- **Structural**: parse JSON and enforce exact success keys, types, enums,
  array bounds, word/sentence limits, and typed failure-envelope shape.
- **Properties**: apply deterministic expected outcomes from each dataset case,
  including error type, sentiment for unambiguous cases, instruction
  isolation, no invented fields, and service-failure classification.
- **Semantic**: score only cases classified `semantic` using the approved
  faithfulness/coverage/uncertainty rubric and formula. Required pass count is
  `ceil(0.90 * N_semantic)`; unsupported claims and mandatory gate failures
  always force overall FAIL.

### Simple semantic-evaluation approach and limitations

The preferred plan is one rubric-based OpenAI judge result per semantic case, using
the saved review input, application JSON, and case rubric. The judge returns
only the three 0–4 scores plus an unsupported-claim finding; the harness
computes the formula and thresholds. This adds one additional model call per
semantic case, so a 15-case dataset may require up to 15 judge calls in
addition to application calls, with provider cost, latency, and possible rate
limits. Judge outputs can vary and may miss subtle unsupported claims; they
must therefore be preserved, repeated-run differences reported, and never
override structural/property/safety checks. If the chosen provider cannot be
used, the harness must report a model/service failure rather than silently
excluding semantic cases or substituting a PASS.

The judge must return an `unsupported_claims` array identifying each claim and
missing review evidence, or an explicit empty array. Any non-empty finding is a
mandatory grounding failure and forces overall FAIL regardless of the 90%
semantic threshold. Malformed or missing judge output cannot establish that
the array is empty and therefore fails. The judge may miss subtle claims and
is not a correctness guarantee; its output never overrides structural,
property, grounding, or service-failure gates.

### Evidence and repair boundary

- `.harness/run_evaluation.ps1` is the single evaluation entry point.
- `evidence/` receives a new timestamped run folder containing exact commands,
  raw application stdout/stderr and JSON output, raw judge request context and
  response, per-case structural/property/semantic results, failure
  classifications, scores, and aggregate decision. Sanitized configuration
  records provider, exact model when configured, rubric version/hash,
  thresholds, token ceilings, retry limit, and settings; it records secret
  presence only and never secret values.
- The first complete source, prompts, tests, dataset, and harness must be
  copied to `evidence/initial-generation/` before the first evaluation-driven
  repair. A final snapshot is kept separately.
- Automated evidence remains separate from any student-authored narrative
  `evidence/harness-log.md`; no narrative entry is generated by the plan.

## Project Structure

### Documentation (this feature)

```text
specs/001-movie-review-summarizer/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── contracts/
```

### Source Code (repository root)

```text
src/
└── movie_review_summarizer/
    ├── __init__.py
    ├── __main__.py
    ├── cli.py
    ├── application.py
    ├── provider.py
    └── schema.py

prompts/
└── summarize.txt

tests/
├── test_application.py
├── test_schema.py
└── test_properties.py

evals/
└── dataset.json

.harness/
└── run_evaluation.ps1

evidence/
├── workflow/
├── initial-generation/
├── evaluation-results/
└── final-generation/
```

**Structure Decision**: Use one `src/` package, a separate prompt file,
independent unit/property tests, one dataset, and one PowerShell evaluation
runner. Provider-specific implementation and dependency files are added only
after the access method is selected.

## Complexity Tracking

No constitution violations or extra architectural components are proposed.

## Readiness blockers before plan approval

1. Select and record the exact application/judge model in local configuration.
2. Select and record application/judge token ceilings and current provider
   pricing so the harness can calculate a maximum evaluation cost.
3. Confirm the local model configuration is present before any paid run.
