# Part-1A: Movie Ticket Booking CLI

This folder contains the completed Part-1A implementation for a simple movie ticket booking command-line application.

## Completed work

- Created and approved the constitution, specification, technical plan, and task list.
- Implemented a Python CLI with local JSON storage.
- Supports two fixed shows (`S1`, `S2`) with ten seats per show at INR 200 per seat.
- Supports listing shows, viewing seats, booking seats, viewing bookings, and cancellation.
- Prevents double booking and rejects a multi-seat request unless all requested seats are available.
- Keeps CLI handling, booking logic, and storage separated under `src/`.
- Added specification-derived unit tests under `tests/`.
- Added the mandatory Ruff, Bandit, and unittest harness under `.harness/`.
- Preserved initial-generation, workflow, repair, harness-result, and final-generation evidence under `evidence/`.
- Completed a student-reported manual demonstration and recorded the final ACCEPT decision.

## Validation

The final mandatory harness run passed:

- Ruff: PASS
- Bandit: PASS
- unittest: PASS — 13 tests
- Overall: PASS

Run the documented harness from PowerShell with:

```powershell
Set-Location Part-1A
& .\.harness\run_checks.ps1
```

For direct CLI use:

```powershell
$env:PYTHONPATH = (Join-Path (Get-Location) "src")
python -m movie_booking --help
```

T008, shared test fixtures, is explicitly deferred because the approved requirements and existing tests do not require shared fixtures.

Demo video: [Part 1A - Movie Booking CLI.mp4](./Part%201A%20-%20Movie%20Booking%20CLI.mp4).
