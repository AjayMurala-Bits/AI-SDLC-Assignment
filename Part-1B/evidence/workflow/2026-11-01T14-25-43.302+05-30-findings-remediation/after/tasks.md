---
description: "Dependency-ordered implementation and evaluation tasks for the approved movie review summarizer plan"
---

# Tasks: Movie Review Summarizer

**Input**: Design documents from `specs/001-movie-review-summarizer/`

**Prerequisites**: Approved `plan.md`, `spec.md`, `data-model.md`, `contracts/`,
`research.md`, `quickstart.md`, and the ratified constitution.

**Execution boundary**: Do not implement or make paid API calls until the
student approves the plan. All live application and evaluation API calls run
manually in the verified external PowerShell workflow with the key entered
privately. Codex reads the saved sanitized results afterward and does not retry
authentication in its own environment.

**Fixed evaluation configuration**: application input/output ceilings are
7,000/1,200 tokens; judge input/output ceilings are 10,000/2,000 tokens;
`reasoning.effort=none`; automatic retries are `0`. These ceilings include
billed reasoning and non-visible formatting tokens. Do not change the declared
scoring thresholds: semantic score `>= 0.80`, faithfulness `>= 3`, coverage
`>= 3`, zero unsupported claims, and at least `ceil(0.90 × N_semantic)` passing
semantic cases; mandatory structural, property, service, grounding, and
harness failures force overall FAIL.

## Phase 1: Setup

**Purpose**: Establish the implementation, prompt, dataset, and evidence
boundaries without making live calls.

- [ ] T001 Create the Part-1B Python package and dependency configuration under `src/`, `pyproject.toml`, and `requirements.txt` according to `plan.md`, without adding credentials or provider calls.
- [ ] T002 [P] Define the grounded summarization prompt and review-data boundary in `prompts/summarize.txt`, including JSON-only output and instruction-isolation requirements.
- [ ] T003 [P] Define the evaluation dataset contract in `evals/dataset.json` for stable unique case IDs, category, `semantic`/`deterministic`/`service-failure` class, original synthetic review text or a defined invalid-input fixture, requirement and acceptance-criterion references, expected success/failure outcome, expected deterministic properties, and semantic rubric fields; do not populate live results in this task.
- [ ] T004 [P] Create the evidence and runner directories under `evidence/`, `.harness/`, and `tests/`, preserving the no-secrets rule in `README.md`.

## Phase 2: Foundational

**Purpose**: Build shared contracts, configuration boundaries, and offline test
support before story implementation.

- [ ] T005 Implement the success and typed-failure schemas, including exact keys, enums, array bounds, word/sentence rules, and the 20,000-character input limit in `src/movie_review_summarizer/schema.py`.
- [ ] T006 Implement local configuration loading and the single provider adapter boundary in `src/movie_review_summarizer/provider.py`, using `OPENAI_API_KEY` and `MOVIE_REVIEW_MODEL` without printing or persisting secrets, with `MOVIE_REVIEW_MAX_INPUT_TOKENS=7000`, `MOVIE_REVIEW_MAX_OUTPUT_TOKENS=1200`, `MOVIE_REVIEW_JUDGE_MAX_INPUT_TOKENS=10000`, `MOVIE_REVIEW_JUDGE_MAX_OUTPUT_TOKENS=2000`, `reasoning.effort=none`, and zero retries.
- [ ] T007 [P] Add offline provider mocks and deterministic fixtures in `tests/fixtures/` and `tests/test_mocks.py`; ensure offline tests never contact the API and are labeled separately from live evaluation.
- [ ] T008 [P] Define the single-run evidence contract in `.harness/evidence_contract.md`, including sanitized configuration, exact commands, timestamps, raw outputs, judge context/results, metrics, failures, and aggregate decision without credentials.

## Phase 3: User Story 1 - Summarize supplied reviews (Priority: P1, MVP)

**Goal**: Read one local UTF-8 review file and produce a grounded five-field
JSON summary or a typed observable failure.

**Independent Test**: Offline mocked CLI runs produce schema-valid positive,
negative, and mixed summaries; a manual external run can later exercise the
real provider without changing the CLI contract.

### Tests for User Story 1

- [ ] T009 [P] [US1] Add offline unit tests for readable positive, negative, and mixed review inputs in `tests/test_application.py`, using mocks only and asserting no network access.
- [ ] T010 [P] [US1] Add schema tests for summary word/sentence limits, aspect bounds, sentiment enums, recommendation limits, exact top-level fields, and no markdown in `tests/test_schema.py`.

### Implementation for User Story 1

- [ ] T011 [US1] Implement UTF-8 file loading, 20,000-character validation, and input classification in `src/movie_review_summarizer/application.py`.
- [ ] T012 [US1] Implement one provider request per invocation and grounded response validation in `src/movie_review_summarizer/application.py` and `src/movie_review_summarizer/provider.py`.
- [ ] T013 [US1] Implement the JSON-only CLI entry point and typed exit behavior in `src/movie_review_summarizer/cli.py` and `src/movie_review_summarizer/__main__.py`.
- [ ] T014 [US1] Add offline end-to-end CLI tests with mocked provider responses in `tests/test_cli.py`, explicitly labeling them as offline and non-billing tests.

## Phase 4: User Story 2 - Handle unsafe or unusable input (Priority: P1)

**Goal**: Distinguish invalid input, insufficient evidence, adversarial review
content, malformed model output, and model/service failure.

**Independent Test**: Offline tests produce the declared failure types and show
that instruction-like review text cannot alter the task or schema.

- [ ] T015 [P] [US2] Add offline property tests for missing, unreadable, invalid-encoding, oversized, empty, whitespace-only, irrelevant, and insufficient inputs in `tests/test_properties.py`.
- [ ] T016 [P] [US2] Add offline adversarial-input tests proving embedded instructions, secret requests, and schema-changing text remain review data in `tests/test_properties.py` and `tests/fixtures/`.
- [ ] T017 [P] [US2] Add offline mocked failure tests for timeout, quota/unavailable service, malformed response, invalid JSON, and invalid failure classification in `tests/test_application.py`.
- [ ] T018 [US2] Map the failure cases to FR-001, FR-008 through FR-013, FR-021, and FR-022 in `evals/dataset.json`, including the explicit `service-failure` case.
- [ ] T019 [US2] Verify offline failure behavior and evidence boundaries with `tests/test_properties.py` and document that these tests do not establish live authentication, generation access, or billing.

## Phase 5: User Story 3 - Evaluate quality before acceptance (Priority: P1)

**Goal**: Run independent structural, property, and rubric-based semantic gates
over at least 15 varied cases and preserve a reproducible decision.

**Independent Test**: The evaluator consumes saved application outputs and
produces per-case gates, metrics, failures, threshold calculations, and an
aggregate PASS/FAIL without allowing judge output to override mandatory gates.

- [ ] T020 [P] [US3] Populate `evals/dataset.json` during implementation with at least 15 actual, original synthetic test inputs—not case descriptions—covering positive, negative, mixed, conflicting, vague/ambiguous, empty, irrelevant, malformed, boundary, missing-information, prompt-injection, and model/service-failure categories; give every case a unique ID and category, review text or a defined invalid-input fixture, FR/SC and acceptance-criterion references, expected success or failure outcome, and expected deterministic properties; for every `semantic` case also record expected sentiment, supported key points, prohibited unsupported claims, and quality-rubric criteria.
- [ ] T021 [P] [US3] Implement independent structural checks for exact fields, types, enums, limits, JSON-only output, and typed failure envelopes in `src/movie_review_summarizer/evaluation/structural.py` with tests in `tests/test_structural.py`.
- [ ] T022 [P] [US3] Implement independent deterministic property checks for requirement mappings, expected failures, instruction isolation, sentiment expectations, repeated-run safety, and the explicit FR-002 boundary that the provider performs no scraping, website access, login, or automatic action beyond the documented single model request in `src/movie_review_summarizer/evaluation/properties.py` with tests in `tests/test_evaluation_properties.py`.
- [ ] T023 [US3] Implement rubric-based semantic judging for faithfulness, coverage, uncertainty/usefulness, and unsupported claims in `src/movie_review_summarizer/evaluation/semantic.py`, applying the fixed formula `(0.40 × faithfulness + 0.35 × coverage + 0.25 × uncertainty/usefulness) / 4` and unchanged thresholds.
- [ ] T024 [US3] Implement the single evaluation runner in `.harness/run_evaluation.ps1` to load `evals/dataset.json`, verify the reviewed dataset version/hash before execution, execute the offline/mocked or manually authorized live mode, invoke the judge only for `semantic` cases, use zero retries, and preserve every case.
- [ ] T025 [US3] Add secure external PowerShell instructions in `specs/001-movie-review-summarizer/quickstart.md` and `.harness/run_evaluation.ps1` for private key entry, no key persistence/display, manual live execution, and explicit separation from offline mocks.
- [ ] T026 [US3] Implement timestamped evidence output under `evidence/evaluation-results/` containing sanitized configuration, prompts, raw application outputs, raw judge results, per-case structural/property/semantic gates, scores, failures, `N_semantic`, the approved integer-ceiling result `ceil(0.90 × N_semantic)` (smallest integer greater than or equal to the unrounded product), mandatory failures, aggregate PASS/FAIL, and the dataset version/hash; include stable `run_id`/`case_id` links or relative paths and hashes where applicable from input/fixture to application output, judge result, gates, and aggregate decision; freeze the reviewed dataset and reject or separately identify any dataset change before live evaluation.

## Phase 6: Repair, re-evaluation, and handoff

**Purpose**: Preserve provenance and require human review after evaluation.

- [ ] T027 Preserve the first complete source, prompt, tests, dataset, and harness in `evidence/initial-generation/` before any evaluation-driven repair, with a timestamped manifest and no secrets.
- [ ] T028 Run the offline test suite and then the manually authorized external live evaluation; record separate offline and live run identities in `evidence/` without repeating authentication from Codex.
- [ ] T029 Repair only evidenced failures in source, prompts, tests, or harness; preserve repair rationale and before/after artifacts in `evidence/workflow/` without changing thresholds.
- [ ] T030 Re-run the required offline tests and manually re-run live evaluation in external PowerShell after repairs; preserve raw outputs, judge results, metrics, failures, and timestamped aggregate evidence.
- [ ] T031 Preserve the final source, prompt, tests, dataset, harness, and configuration snapshot in `evidence/final-generation/` and link it to the final evaluation result.
- [ ] T032 Prepare the student review package in `evidence/` with reproducibility instructions, unresolved limitations, and a human acceptance decision; do not generate the narrative `evidence/harness-log.md` entry automatically.

## Dependencies and execution order

- Phase 1 precedes Phase 2; Phase 2 blocks all user-story work.
- US1 and US2 depend on the foundational schema, provider boundary, mocks, and evidence contract; they can proceed in parallel after Phase 2.
- US3 depends on the CLI contract and the offline behavior from US1/US2, but its structural and property components can proceed in parallel.
- Initial-generation preservation (T027) must occur before any evaluation-driven repair (T029).
- Live execution requires plan approval and must occur only in external PowerShell; saved results are read afterward by Codex.
- Final snapshot and human review follow re-evaluation.

## Parallel opportunities

- T002, T003, and T004 can run in parallel.
- T007 and T008 can run in parallel.
- T009 and T010 can run in parallel; T015 through T017 can run in parallel.
- T020 through T022 can run in parallel once the dataset contract is fixed.

## Implementation strategy

1. Complete setup and foundational contracts without live calls.
2. Deliver US1 as the MVP with offline mocks and schema tests.
3. Add US2 failure and adversarial coverage.
4. Add US3 evaluation gates, dataset, runner, and evidence preservation.
5. Preserve initial generation, repair only evidenced failures, re-evaluate,
   preserve the final snapshot, and wait for human acceptance.
