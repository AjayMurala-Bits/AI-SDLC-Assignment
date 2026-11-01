# Feature Specification: Movie Review Summarizer

**Feature Branch**: `001-movie-review-summarizer`

**Created**: 2026-11-01

**Status**: Draft

**Input**: User description: Create a small CLI that summarizes one movie's reviews from a local text file using an AI model and evaluates grounded structured output.

## User Scenarios & Testing

### User Story 1 - Summarize supplied reviews (Priority: P1)

As a movie viewer, I can provide a local text file of reviews and receive a concise JSON summary of what those reviews say.

**Why this priority**: This is the core user value.

**Independent Test**: Run the CLI with a normal review file and validate the success schema and grounded content.

**Acceptance Scenarios**:

1. **Given** a readable file containing relevant positive reviews, **When** the CLI runs, **Then** it returns valid JSON with positive sentiment and supported positive aspects.
2. **Given** relevant reviews with both praise and criticism, **When** the CLI runs, **Then** it returns mixed sentiment and represents both sides without unsupported claims.
3. **Given** a readable file with only irrelevant or too-little evidence, **When** the CLI runs, **Then** it reports insufficient evidence and does not produce a confident recommendation.

### User Story 2 - Handle unsafe or unusable input (Priority: P1)

As a user, I can distinguish invalid input, insufficient evidence, and model/service failures from a successful summary.

**Why this priority**: Clear failure handling prevents misleading results.

**Independent Test**: Run the CLI against empty, malformed, missing, and instruction-like inputs and check the documented failure types and unchanged evidence boundaries.

**Acceptance Scenarios**:

1. **Given** an empty or whitespace-only file, **When** the CLI runs, **Then** it returns an `empty_input` or `insufficient_evidence` failure and no success summary.
2. **Given** review text containing “ignore previous instructions” or similar text, **When** the CLI runs, **Then** that text is treated as review content and cannot change the summarization task.
3. **Given** an unavailable model service or malformed model response, **When** the CLI runs, **Then** it returns a distinct `model_failure` or `invalid_model_output` failure.

### User Story 3 - Evaluate quality before acceptance (Priority: P1)

As a student, I can evaluate outputs through independent structural, property, and semantic gates with thresholds defined before the run.

**Why this priority**: The assignment requires evidence that valid JSON is not mistaken for a faithful summary.

**Independent Test**: Run the 15-case evaluation dataset and inspect separate gate results, per-case evidence, and the final threshold decision.

**Acceptance Scenarios**:

1. **Given** output with missing fields or invalid values, **When** structural evaluation runs, **Then** the structural gate fails regardless of semantic score.
2. **Given** output that follows the schema but invents a movie fact, **When** property and semantic evaluation runs, **Then** the safety gate fails and overall evaluation cannot PASS.
3. **Given** all applicable gates pass their thresholds, **When** evaluation completes, **Then** it records the formula, thresholds, actual results, and a PASS/FAIL outcome for student review.

### Edge Cases

- Missing file, unreadable file, invalid text encoding, and an input above the declared size limit are input failures.
- Empty or whitespace-only input is not summarized.
- Reviews unrelated to a movie, or too vague to support a conclusion, produce `insufficient_evidence` rather than invented content.
- Conflicting reviews produce `mixed` sentiment and preserve both supported viewpoints.
- A single review is valid input but may receive `unclear` sentiment when evidence is weak.
- Embedded instructions, requests for secrets, or attempts to change the output format remain review data.
- A model timeout, quota error, unavailable service, or malformed response is reported separately from application and evaluation failures.

## Requirements

### Functional Requirements

- **FR-001**: The CLI MUST accept one path to a local UTF-8 text file containing reviews for one movie.
- **FR-002**: The CLI MUST make one summarization request per invocation and MUST NOT scrape reviews, access a website, require login, or perform automatic actions.
- **FR-003**: A successful result MUST be a JSON object with exactly these required fields: `summary`, `sentiment`, `positive_aspects`, `negative_aspects`, and `recommendation`.
- **FR-004**: In a successful result, `summary` MUST be a non-empty string of at most 80 words and at most 3 sentences.
- **FR-005**: `sentiment` MUST be one of `positive`, `negative`, `mixed`, or `unclear`.
- **FR-006**: `positive_aspects` and `negative_aspects` MUST be arrays of zero to five non-empty strings; each aspect MUST be at most 12 words.
- **FR-007**: `recommendation` MUST be a non-empty string of at most 30 words and MUST be conditional or explicitly state insufficient evidence when the reviews do not support a confident recommendation.
- **FR-008**: The success JSON MUST contain no additional top-level fields, null required values, markdown fences, or explanatory text outside JSON.
- **FR-009**: Empty, whitespace-only, irrelevant, or insufficient input MUST return a non-success result with failure type `empty_input` or `insufficient_evidence`; it MUST NOT invent aspects or a recommendation.
- **FR-010**: The application MUST return a failure object with `error.type` and `error.message` for invalid input, missing/unreadable files, model failures, malformed model output, and evaluation failures. Allowed failure types are `invalid_input`, `empty_input`, `insufficient_evidence`, `model_failure`, `invalid_model_output`, and `evaluation_failure`.
- **FR-011**: Review text MUST be treated as untrusted data. Text inside the review file MUST NOT override the task, request secrets, alter the schema, or become executable instructions.
- **FR-012**: Every factual statement, aspect, sentiment conclusion, and recommendation MUST be supported by the supplied reviews. Unsupported movie details MUST be omitted.
- **FR-013**: Conflicting supported opinions MUST be represented as `mixed` or `unclear`; the output MUST NOT silently select one side as universal fact.
- **FR-014**: The evaluation harness MUST provide three independent layers:
  - **Structural**: validate required fields, exact top-level keys, JSON types, enumerations, word/sentence limits, array limits, and failure-envelope rules.
  - **Properties**: check deterministic requirements such as error classification, no invented fields, instruction isolation, expected sentiment for unambiguous cases, and unchanged safety behaviour across repeated runs.
  - **Semantic**: score faithfulness, coverage of supported points, and appropriate uncertainty against the case rubric; valid JSON or keyword presence alone MUST NOT pass this layer.
- **FR-015**: The evaluation MUST use `evals/dataset.json` with at least 15 varied cases. Each case MUST include an ID, review input or input-fixture reference, requirement mapping, expected properties, and either a semantic rubric or an explicit expected failure type.
- **FR-016**: The 15 cases MUST cover positive, negative, mixed, boundary, ambiguity, missing information, empty/irrelevant input, malformed input, conflicting reviews, embedded adversarial instructions, and a model/service failure classification.
- **FR-017**: Semantic scoring MUST use three dimensions, each scored from 0 to 4: **faithfulness** (40%), **coverage** (35%), and **uncertainty/usefulness** (25%). Anchors MUST be applied consistently: 0 = absent or wholly wrong; 1 = mostly wrong with little usable evidence; 2 = partly correct but materially incomplete or overconfident; 3 = substantially correct, covers the important supported points, and handles uncertainty appropriately; 4 = fully faithful, complete for the case rubric, and appropriately cautious. The normalized score MUST be calculated exactly as `(0.40 × faithfulness + 0.35 × coverage + 0.25 × uncertainty/usefulness) / 4`.
- **FR-018**: Only cases whose expected outcome is a successful summary with a semantic rubric receive semantic scores. Cases expecting input rejection, insufficient-evidence handling, malformed input handling, or a typed service failure MUST be evaluated against their deterministic expected outcome and MUST NOT receive a semantic score. Each case MUST declare its evaluation class: `semantic`, `deterministic`, or `service-failure`.
- **FR-019**: Let `N_semantic` be the number of cases classified `semantic` in the dataset, excluding deterministic and service-failure cases. The required semantic pass count MUST be `ceil(0.90 × N_semantic)`. Service-failure cases MUST be counted and reported as mandatory service-gate outcomes; they MUST NOT be silently excluded or counted as passes. An unclassified service failure is an overall FAIL.
- **FR-020**: A semantic case can PASS only when its normalized score is at least `0.80`, faithfulness is at least `3`, coverage is at least `3`, and unsupported-claim count is zero. Any unsupported claim in any applicable case is a mandatory grounding failure and MUST cause overall FAIL, even if the 90% semantic pass count is met.
- **FR-021**: Any structural failure, safety/property failure, unsupported claim, invalid failure classification, service-gate failure, or evaluation-harness failure MUST be an overall FAIL regardless of average semantic score. Model/service failures MUST be reported separately from application and evaluation failures and MUST block overall PASS until resolved or explicitly classified as an environment/setup failure.
- **FR-022**: Typed failure results MUST describe observable application errors only, using the declared `error.type` and `error.message` fields. The application MUST NOT judge its own semantic correctness. Semantic scores, unsupported-claim findings, denominator calculations, and PASS/FAIL aggregation belong in the evaluation harness report.
- **FR-023**: Acceptance thresholds, score anchors, case classes, denominator definition, rounding rule, and the scoring formula MUST be recorded before evaluation outputs are collected and MUST NOT be weakened after observing results.
- **FR-024**: Prompts, model outputs, configuration, timestamps, per-case gate results, and overall results MUST be preserved under `evidence/`; secrets MUST NOT be stored in source or evidence.

### Key Entities

- **Review Input**: The UTF-8 text file supplied for one movie; its content is untrusted evidence.
- **Summary Result**: The five-field successful JSON object, or a typed failure object.
- **Evaluation Case**: One dataset item containing input, requirement mapping, expected deterministic properties, and semantic scoring guidance.
- **Evaluation Run**: A timestamped set of prompts, outputs, gate results, configuration, and overall decision.

## Success Criteria

### Measurable Outcomes

- **SC-001**: 100% of successful outputs in the evaluation dataset conform to the declared JSON schema and output limits.
- **SC-002**: 100% of empty, malformed, irrelevant, insufficient, and service-failure cases are classified with the correct failure type or documented environment classification.
- **SC-003**: 100% of adversarial-instruction cases preserve the summarization task and contain no instruction-following behaviour from review text.
- **SC-004**: At least `ceil(0.90 × N_semantic)` semantic cases achieve the declared score threshold, with zero unsupported claims in any case.
- **SC-005**: No overall evaluation is marked PASS when a mandatory structural, safety, property, service-classification, or evaluation-harness gate fails.
- **SC-006**: A reviewer can reproduce the evaluation decision from preserved prompts, outputs, configuration, timestamps, and results without relying on fabricated or backfilled evidence.

## Assumptions

- The user supplies one movie's reviews in a readable UTF-8 text file; review boundaries may be represented by paragraphs or line breaks and are not themselves a user-facing feature.
- A practical default input limit is 20,000 characters; exceeding it is `invalid_input` unless planning defines a justified alternative.
- The model/provider, credentials mechanism, timeout, and retry policy are intentionally deferred to planning.
- The evaluator may use a deterministic semantic judge or a documented human/AI rubric, but the three gate layers remain independent.
- The dataset is a specification artifact for the next workflow step; this step does not create its implementation or evaluation code.

## Important Ambiguities Deferred to Planning

- Model/provider and local versus remote access method.
- Exact CLI option spelling and the mechanism used to inject a controlled model/service failure during evaluation.
