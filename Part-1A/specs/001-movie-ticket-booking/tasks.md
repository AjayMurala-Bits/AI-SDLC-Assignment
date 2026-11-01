---

description: "Ordered implementation tasks for the Movie Ticket Booking CLI"
---

# Tasks: Movie Ticket Booking CLI

**Input**: Design documents from `specs/001-movie-ticket-booking/`

**Prerequisites**: Approved `plan.md`, `spec.md`, `research.md`, `data-model.md`,
`contracts/cli.md`, and `quickstart.md`.

**Strategy**: Build the smallest working CLI incrementally, write the requested
tests with each story, and keep every validation result genuine and recoverable.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish the planned project layout and validation entry point.

- [X] T001 Create the package skeleton in `src/movie_booking/__init__.py` and `src/movie_booking/__main__.py`.
- [X] T002 Create the test modules `tests/test_booking.py`, `tests/test_storage.py`, and `tests/test_cli.py` using `unittest`.
- [X] T003 [P] Add the single validation entry point in `.harness/run_checks.ps1` that sets `$env:PYTHONPATH = (Join-Path (Get-Location) "src")` as an absolute path, passes it to test subprocesses, and runs Ruff, Bandit, and unittest in order.
- [X] T004 [P] Confirm `src/`, `tests/`, `.harness/`, `evidence/initial-generation/`, `evidence/final-generation/`, and `evidence/harness-results/` are present without adding application behavior.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Implement shared domain and storage boundaries before story work.

- [X] T005 Implement fixed show, seat, price, booking, and status definitions in `src/movie_booking/models.py` for FR-001, FR-002, FR-005, and the data model constraints.
- [X] T006 Implement JSON load/save, schema validation, and storage errors in `src/movie_booking/storage.py` for FR-013 and FR-014; never silently reset invalid or unreadable storage.
- [X] T007 Implement validation helpers and deterministic booking state transitions in `src/movie_booking/booking.py` for FR-006 through FR-012; validate the full request before any state change.
- [D] T008 [P] Add shared test fixtures and temporary-store helpers in `tests/test_storage.py` and `tests/test_booking.py` without changing production behavior. **Deferred**: existing `setUp` and per-test `TemporaryDirectory()` usage already provide isolation and cover the approved requirements; no shared helper is necessary.

**Checkpoint**: Storage and booking boundaries are independently testable; no
CLI story begins until invalid input and atomicity can be verified.

---

## Phase 3: User Story 1 - View Shows and Seats (Priority: P1) 🎯 MVP

**Goal**: List S1/S2 and show A1-A10 availability independently per show.

**Independent Test**: With a fresh store, list shows and view seats for both
shows; all twenty seats are available.

### Tests for User Story 1

- [X] T009 [P] [US1] Add fresh-state and show-isolation tests in `tests/test_booking.py` for FR-001 through FR-003 and acceptance scenarios US1-AS1 through US1-AS3.
- [X] T010 [P] [US1] Add `list-shows` and `view-seats` command contract tests in `tests/test_cli.py` for `contracts/cli.md`.

### Implementation for User Story 1

- [X] T011 [US1] Implement `list-shows` and `view-seats <show_id>` in `src/movie_booking/cli.py` using the booking and storage boundaries.
- [X] T012 [US1] Wire `python -m movie_booking` dispatch in `src/movie_booking/__main__.py` and return clear non-zero errors for invalid show IDs.

**Checkpoint**: US1 can be demonstrated and tested without booking, lookup, or
cancellation features.

---

## Phase 4: User Story 2 - Book Seats (Priority: P1)

**Goal**: Book one or more available seats with exact INR pricing and atomic
failure behavior.

**Independent Test**: Book S1 A1/A2 for INR 400, reject a conflicting request,
and confirm S2 A1 remains available.

### Tests for User Story 2

- [X] T013 [P] [US2] Add booking tests in `tests/test_booking.py` for FR-004 through FR-009 and acceptance scenarios US2-AS1 through US2-AS4: success, INR 200 per seat, double-booking prevention, show isolation, invalid inputs, and all-or-none multi-seat requests.
- [X] T014 [P] [US2] Add `book <show_id> <seat>...` CLI contract tests in `tests/test_cli.py` for successful output and non-zero error handling.

### Implementation for User Story 2

- [X] T015 [US2] Implement booking creation and exact total calculation in `src/movie_booking/booking.py`, preserving deterministic seat order and never reusing IDs.
- [X] T016 [US2] Implement the `book` command in `src/movie_booking/cli.py` and persist successful changes through `src/movie_booking/storage.py` only after complete validation.

**Checkpoint**: US1 and US2 work independently, including atomic rejection and
exact pricing.

---

## Phase 5: User Story 3 - View a Booking (Priority: P2)

**Goal**: Retrieve a booking by ID with show, seats, total, and status.

**Independent Test**: Create a booking, view its ID, and verify every returned
field; unknown IDs return a clear error without mutation.

### Tests for User Story 3

- [X] T017 [P] [US3] Add booking lookup tests in `tests/test_booking.py` for FR-010 and acceptance scenarios US3-AS1 and US3-AS2.
- [X] T018 [P] [US3] Add `view-booking <booking_id>` CLI contract tests in `tests/test_cli.py` for active records and unknown IDs.

### Implementation for User Story 3

- [X] T019 [US3] Implement booking lookup in `src/movie_booking/booking.py` and the `view-booking` command in `src/movie_booking/cli.py`.

**Checkpoint**: US3 is independently testable against a persisted active
booking.

---

## Phase 6: User Story 4 - Cancel a Booking (Priority: P2)

**Goal**: Cancel active bookings, release seats, and retain cancelled records.

**Independent Test**: Cancel an active booking, re-view it as cancelled, confirm
its seats are available, and reject repeat/unknown cancellation.

### Tests for User Story 4

- [X] T020 [P] [US4] Add cancellation tests in `tests/test_booking.py` for FR-011 and FR-012 and acceptance scenarios US4-AS1 through US4-AS3, including seat release, retained cancelled status, repeat cancellation, and unknown ID.
- [X] T021 [P] [US4] Add `cancel <booking_id>` CLI contract tests in `tests/test_cli.py` for success and clear errors.

### Implementation for User Story 4

- [X] T022 [US4] Implement cancellation state transition in `src/movie_booking/booking.py` and the `cancel` command in `src/movie_booking/cli.py`.
- [X] T023 [US4] Add restart/persistence coverage in `tests/test_storage.py` for FR-013 and FR-014, including next ID preservation and invalid/unreadable store errors.

**Checkpoint**: All four user stories are independently demonstrable and map
to the approved acceptance criteria.

---

## Phase 7: Evidence, Validation, and Repair

**Purpose**: Preserve the first implementation, run genuine gates, repair only
when needed, and retain both initial and final versions.

- [X] T024 Preserve the first complete implementation in `evidence/initial-generation/` before any repair or check-driven modification.
- [X] T025 [P] Review `.harness/run_checks.ps1` and all source/test paths for the approved one-command gates; do not weaken or bypass Ruff, Bandit, or unittest.
- [X] T026 Run `powershell -NoProfile -ExecutionPolicy Bypass -File .harness/run_checks.ps1` (which sets the absolute `src` path for test subprocesses) and save start/end timestamps, exact commands, exit codes, stdout, stderr, and PASS/FAIL in a new folder under `evidence/harness-results/`.
- [X] T027 If a genuine validation failure occurs, repair the smallest responsible source/test/harness file, preserve the failed run, and document the repair without fabricating PASS evidence.
- [X] T028 Re-run the unchanged mandatory gates after any repair, saving another non-overwriting run folder under `evidence/harness-results/`.
- [X] T029 Preserve the final validated implementation separately in `evidence/final-generation/` and leave `evidence/harness-log.md` for the student-authored narrative.
- [X] T030 Run the scenarios in `specs/001-movie-ticket-booking/quickstart.md` and compare results with the approved acceptance criteria before student acceptance.

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: T001-T004; no story behavior yet.
- **Foundational (Phase 2)**: T005-T008 depends on setup and blocks story work.
- **US1 (Phase 3)**: T009-T012 depends on foundational work and is the MVP.
- **US2 (Phase 4)**: T013-T016 depends on US1 CLI wiring and shared booking logic.
- **US3 (Phase 5)**: T017-T019 depends on persisted booking creation from US2.
- **US4 (Phase 6)**: T020-T023 depends on booking records from US2 and lookup from US3.
- **Evidence/validation (Phase 7)**: T024 follows the first complete implementation;
  T025-T030 follow the desired story scope and preserve every actual result.

### User Story Dependencies

- **US1**: Foundational only; MVP.
- **US2**: Foundational plus shared CLI entry point from US1.
- **US3**: US2 booking record available.
- **US4**: US2 booking record and US3 lookup available.

### Parallel Opportunities

- T003, T004, and T008 can proceed in parallel after the basic layout exists.
- T009/T010, T013/T014, T017/T018, and T020/T021 are parallel test tasks within their stories.
- Different story test preparation can be parallelized after shared foundations,
  but implementation remains ordered where it shares `cli.py` or `booking.py`.

## Independent Test Criteria

- **US1**: Fresh state lists S1/S2 and ten available seats per show; booking in
  one show does not alter the other.
- **US2**: A1/A2 for S1 yields INR 400; conflicts and invalid mixed requests
  leave state unchanged.
- **US3**: A known ID returns show/seats/total/status; unknown ID does not mutate.
- **US4**: Cancellation releases seats, retains cancelled status, and rejects
  repeated or unknown cancellation.

## MVP Scope

The MVP is US1: listing shows and viewing seat availability. US2 is the next
increment because booking is the core business value; US3 and US4 follow without
adding features outside the approved specification.

## Implementation Strategy

Deliver setup and foundations first, then complete each user story with tests
before implementation and an independent checkpoint. Preserve the first complete
implementation before any repair. Run and preserve actual validation evidence,
repair only genuine failures, preserve the final version, and leave the final
acceptance decision to the student.
