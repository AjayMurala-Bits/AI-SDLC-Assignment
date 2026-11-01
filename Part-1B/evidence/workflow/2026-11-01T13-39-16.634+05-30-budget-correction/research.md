# Research: Movie Review Summarizer Plan

**Status**: Provider/access choice complete; model and cost-budget details are
still unresolved. No model calls have been made.

## Decision: OpenAI API with local credential

**Rationale**: The user selected OpenAI API access without assuming Codex
subscription access. The API key remains in the user's local environment or
credential store and is never pasted into chat, source, or evidence.

**Configuration boundary**: `OPENAI_API_KEY` supplies authentication and
`MOVIE_REVIEW_MODEL` selects both the application and judge model. The current
process has the API-key variable present, but the model variable is absent.
No credential values are printed or stored. Exact model, token ceilings, and
pricing must be selected before approval or paid execution.

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
latency, rate-limit, and variability risk. The judge may miss unsupported
claims and is not a correctness guarantee. Judge outputs must be captured and
cannot override structural/property/safety gates. Non-empty unsupported-claim
findings are mandatory grounding failures.

## Remaining implementation choices

Automatic retries are fixed at zero. The exact model name, token ceilings,
and pricing are not yet selected and block plan approval until documented
without secrets.

## Proposed model for review

The current proposal is `gpt-5.4-mini` for both the application and the
separate judge call. Official documentation lists Structured Outputs support
and standard text pricing of $0.75 per million input tokens and $4.50 per
million output tokens. Use 7,000 input/1,200 total-output tokens for
application calls and 10,000 input/2,000 total-output tokens for judge calls,
with zero retries. The total-output ceilings include billed reasoning and
non-visible formatting tokens; use `reasoning.effort=none` for this simple
task. One model for both roles is simple but can create correlated blind
spots; the judge is not an independent correctness guarantee.

The account model-list check returned sanitized HTTP 401 with
`invalid_api_key` / `Incorrect API key provided`, so this is an authentication
failure and access to the proposal remains unverified.

