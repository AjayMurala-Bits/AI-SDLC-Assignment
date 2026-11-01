# Research: Movie Review Summarizer Plan

**Status**: Complete for planning; OpenAI API with local credential selected.

## Decision: OpenAI API with local credential

**Rationale**: The user selected OpenAI API access without assuming Codex
subscription access. The API key remains in the user's local environment or
credential store and is never pasted into chat, source, or evidence.

**Configuration boundary**: `OPENAI_API_KEY` supplies authentication and
`MOVIE_REVIEW_MODEL` selects the model. The exact model name and timeout remain
implementation configuration choices and must be recorded without secrets.

## Decision: Keep provider access behind one adapter

**Rationale**: The application must remain a simple CLI and the provider/access
method is not known. A single adapter keeps the rest of the code and tests
independent from provider SDK details.

**Alternatives considered**: Direct provider calls throughout the CLI were
rejected because they would make service failures, tests, and later provider
changes harder to isolate.

## Decision: Use independent structural and property checks

**Rationale**: JSON validity, exact fields, limits, typed failures, and
deterministic safety rules can be checked without a model judge. These checks
must remain mandatory even if semantic evaluation is unavailable.

**Alternatives considered**: One LLM judge for all checks was rejected because
it could hide schema or safety failures behind a high quality score.

## Decision: Rubric-based semantic evaluation

**Rationale**: Semantic quality needs meaning-level assessment for faithfulness,
coverage, uncertainty, and unsupported claims. A judge can apply the approved
0–4 anchors per semantic case, while the harness computes the fixed formula and
thresholds.

**Limitations**: Each semantic case adds a judge call and possible cost,
latency, rate-limit, and variability risk. Judge outputs must be captured and
cannot override structural/property/safety gates.

## Remaining implementation choices

The exact model name, SDK version, timeout, retry policy, and controlled
service-failure injection mechanism remain implementation details. They must be
documented before execution and must not alter approved thresholds.
