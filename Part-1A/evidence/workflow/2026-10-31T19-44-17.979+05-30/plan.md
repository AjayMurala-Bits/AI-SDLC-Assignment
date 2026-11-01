# Implementation Plan: Movie Ticket Booking CLI

**Branch**: `001-movie-ticket-booking` | **Date**: 2026-10-31 | **Spec**: [spec.md](./spec.md)

**Input**: Approved feature specification from `specs/001-movie-ticket-booking/spec.md`

## Summary

Build a small Python command-line application for two fixed shows and ten seats
per show. Keep CLI parsing, booking rules, and local JSON persistence separate.
Use only the Python standard library at runtime. Ruff, Bandit, and unittest are
the mandatory quality gates, run together by one harness command.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: Python standard library at runtime; Ruff and Bandit as
development tools

**Storage**: One local JSON file containing version, next booking ID, and booking records

**Testing**: `unittest` discovery; Ruff lint; Bandit security scan

**Target Platform**: Local operator workstation with Python 3.11+

**Project Type**: Command-line application

**Performance Goals**: Each local command should complete promptly for the fixed
20-seat scope; no throughput or concurrency target is required.

**Constraints**: Offline operation, one operator, one running instance, fixed
shows/seats/price, deterministic results, no silent storage reset, no extra
features or runtime dependencies

**Scale/Scope**: Two shows, ten seats per show, one local operator, one JSON file

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Python CLI and Local JSON**: PASS — Python CLI and one local JSON store
  are defined.
- **II. Separated Responsibilities**: PASS — `cli.py`, `booking.py`, and
  `storage.py` have distinct responsibilities.
- **III. Deterministic and Atomic Booking**: PASS — validation precedes state
  changes, availability is deterministic, and multi-seat booking is all-or-none.
- **IV. Mandatory Quality Checks**: PASS — one `.harness/run_checks.ps1`
  command will run Ruff, Bandit, and unittest.
- **V. Honest Evidence and Acceptance**: PASS — initial/final code and each
  actual harness run are assigned separate evidence locations; student retains
  acceptance authority.

No violations or complexity exceptions are required.

## Project Structure

### Documentation (this feature)

```text
specs/001-movie-ticket-booking/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── cli.md
└── tasks.md                 # created later by $speckit-tasks
```

### Source Code (repository root)

```text
src/
└── movie_booking/
    ├── __init__.py
    ├── __main__.py          # module entry point
    ├── cli.py               # argument parsing and user-facing output
    ├── booking.py           # validation and booking state transitions
    ├── storage.py           # JSON read/write and storage errors
    └── models.py            # simple domain records/constants

tests/
├── test_booking.py          # pure booking rules and atomicity
├── test_storage.py          # valid, invalid, unreadable, and restart state
└── test_cli.py              # command contracts and clear errors

.harness/
└── run_checks.ps1           # single mandatory validation command

evidence/
└── harness-results/         # one non-overwriting folder per actual run
```

**Structure Decision**: Use one small `src/movie_booking` package. The CLI
depends on booking services, and booking services depend on the storage boundary;
storage does not handle CLI concerns. Tests are split by boundary and acceptance
behavior. The harness is isolated under `.harness/` and writes run evidence only
under `evidence/harness-results/`.

## CLI and Validation Plan

The user-facing commands are defined in [contracts/cli.md](./contracts/cli.md).
The planned harness command is:

```text
powershell -NoProfile -ExecutionPolicy Bypass -File .harness/run_checks.ps1
```

It will run Ruff, Bandit, and unittest in that order, capture exact commands,
timestamps, exit codes, stdout, stderr, and overall PASS/FAIL in a new evidence
folder. It will never overwrite an earlier run.

Acceptance-to-test mapping is defined in [quickstart.md](./quickstart.md).

## Phase 1 Design Decisions

- Store only canonical booking records and `next_booking_id`; derive seat
  availability from active bookings to avoid conflicting duplicated state.
- Use integer INR totals and canonical sorted seat lists for deterministic output.
- Treat malformed, missing-required-field, or unreadable JSON as an error; do not
  initialize or reset the file during a read failure.
- Keep cancellation records with status `cancelled`; cancelled seats become
  available because only active bookings reserve seats.

## Complexity Tracking

No constitution violations or unnecessary complexity are proposed.
