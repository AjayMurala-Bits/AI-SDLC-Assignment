# Data Model: Movie Ticket Booking CLI

## Constants

- Shows: `S1`, `S2`
- Seats per show: `A1` through `A10`
- Ticket price: integer `200` INR
- Initial booking ID: `1`

## JSON Store Format

```json
{
  "version": 1,
  "shows": ["S1", "S2"],
  "next_booking_id": 1,
  "bookings": [
    {
      "id": 1,
      "show_id": "S1",
      "seats": ["A1", "A2"],
      "total_inr": 400,
      "status": "active"
    }
  ]
}
```

## Entities and Rules

### Show

- `show_id`: one of `S1` or `S2`.
- Seats are the fixed names `A1` through `A10`.
- Availability is derived from seats in active bookings for that show.

### Booking

- `id`: positive integer, unique and never reused.
- `show_id`: valid show identifier.
- `seats`: non-empty, unique, valid seat names in canonical order.
- `total_inr`: `200 * len(seats)`.
- `status`: `active` or `cancelled`.

## State Transitions

```text
no booking --valid all-available request--> active booking
active booking --cancel--> cancelled booking + seats available
active booking --invalid or conflicting request--> unchanged state
cancelled booking --cancel again--> unchanged state + clear error
```

## Store Validation

The store MUST contain the expected version and show list, a positive next ID,
and valid booking records. Missing, malformed, or unreadable JSON MUST produce
an error and MUST NOT silently create or reset the store.
