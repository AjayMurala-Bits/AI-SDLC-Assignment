# CLI Contract: Movie Ticket Booking CLI

The CLI is invoked as `python -m movie_booking <command> ...`. Successful
commands write human-readable results to standard output. Invalid input,
unknown IDs, conflicts, and storage failures write a clear error and return a
non-zero exit code. No interactive prompts are required.

## Commands

| Command | Arguments | Required result |
|---|---|---|
| `list-shows` | none | Lists exactly `S1` and `S2`. |
| `view-seats` | `<show_id>` | Lists `A1`–`A10` with availability for that show. |
| `book` | `<show_id> <seat> [<seat> ...]` | Validates all seats, creates one active booking, and prints ID, seats, and total. |
| `view-booking` | `<booking_id>` | Prints show, seats, total, and status. |
| `cancel` | `<booking_id>` | Cancels an active booking, releases its seats, and prints the cancelled ID. |

## Error Contract

- Unknown show, invalid seat, repeated seat, empty seat list, unavailable seat,
  unknown booking ID, or repeated cancellation is rejected.
- A rejected request leaves the JSON store unchanged.
- Invalid or unreadable JSON is reported as a storage error and never replaced.

## Determinism

Show IDs, seat lists, and booking records are displayed in canonical order.
Booking IDs and totals are derived from the stored state and fixed price.
