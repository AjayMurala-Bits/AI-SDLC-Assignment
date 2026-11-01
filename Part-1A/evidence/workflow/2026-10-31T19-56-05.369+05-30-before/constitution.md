<!--
Sync Impact Report
- Version change: 1.0.0 -> 1.0.0 (ratification recorded; no governance change)
- Modified principles: none
- Added sections: approval and ratification metadata
- Removed sections: none
- Follow-up TODOs: none
-->

# Movie Ticket Booking CLI Constitution

## Core Principles

### I. Python CLI and Local JSON
The application MUST use Python, expose its functions through a command-line
interface, and persist booking state in local JSON storage. The scope is limited
to the two predefined shows, their seats, bookings, and cancellations.

### II. Separated Responsibilities
Booking rules MUST remain separate from file-storage access and CLI handling.
Each boundary MUST be independently testable so that changes to presentation or
storage do not silently alter booking behaviour.

### III. Deterministic and Atomic Booking
The same inputs and stored state MUST produce the same result. Input MUST be
validated before any booking state changes. A seat MUST NOT be double-booked,
and a multi-seat request MUST either reserve every requested seat or reserve
none of them.

### IV. Mandatory Quality Checks
Every implementation MUST run one harness command covering syntax/lint checks,
security checks, and tests derived from the problem statement. Checks MUST
remain enabled and meaningful; failures MUST be reported rather than bypassed.

### V. Honest Evidence and Acceptance
The initial implementation and actual harness results MUST be preserved.
Checks MUST never be weakened and evidence MUST never be fabricated to obtain
PASS. The student alone makes the final acceptance decision.

## Technology Constraints

Use only the local Python CLI and JSON storage required by the problem
statement. Do not add a GUI, website, online payment, login, scheduling,
concurrency, or other excluded functionality without an explicit scope change.

## Quality and Evidence

Tests MUST cover valid operations, invalid input, isolation between shows,
atomic multi-seat failure, cancellation, persistence across restart, increasing
booking IDs, and invalid or unreadable storage. A failed check or repair MUST
remain traceable in the harness output and development record.

## Governance

This constitution governs the movie-booking work and supersedes conflicting
local practices. Amendments MUST state the reason, update the version, and be
reviewed before dependent specifications or code are changed. Versioning uses
semantic versioning: MAJOR for incompatible governance changes, MINOR for new
principles or material requirements, and PATCH for clarifications. Each
implementation review MUST verify compliance with these principles and the
problem statement. Approval is recorded below.

**Version**: 1.0.0 | **Ratified**: 2026-10-31 | **Last Amended**: 2026-10-31

**Approval**: Student approved constitution version 1.0.0 on 2026-10-31.
