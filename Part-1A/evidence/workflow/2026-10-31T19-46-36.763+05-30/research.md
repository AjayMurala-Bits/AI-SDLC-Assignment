# Research Notes: Movie Ticket Booking CLI

## Decision: Python standard library at runtime

- **Rationale**: The approved constitution requires Python and the feature is a
  small local CLI. The standard library keeps the runtime dependency-free.
- **Alternatives considered**: A web framework or third-party CLI framework was
  rejected because the scope excludes a website and does not need extra behavior.

## Decision: JSON file with canonical booking records

- **Rationale**: The problem statement requires local JSON persistence. Storing
  bookings and the next ID, while deriving availability, avoids duplicated seat
  state and makes deterministic checks straightforward.
- **Alternatives considered**: A database was rejected as unnecessary for two
  shows and one local operator.

## Decision: unittest, Ruff, and Bandit in one harness command

- **Rationale**: These are the mandated validation tools. A single harness entry
  point makes the quality gate repeatable and preserves actual evidence.
- **Alternatives considered**: pytest and additional coverage tools were rejected
  because they are outside the requested dependency set.
