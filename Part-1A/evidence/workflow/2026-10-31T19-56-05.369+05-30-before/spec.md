# Feature Specification: Movie Ticket Booking CLI

**Feature Branch**: `001-movie-ticket-booking`

**Created**: 2026-10-31

**Status**: Approved

**Approval**: Student explicitly approved this specification on
2026-10-31T19:39:55.210+05:30 (Asia/Kolkata).

**Input**: User description: Create a short specification for the approved Movie Ticket Booking CLI.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - View Shows and Seats (Priority: P1)

As a cinema operator, I want to list the available shows and inspect each
show's seats so that I can see what can be booked.

**Why this priority**: Seat visibility is the starting point for every booking.

**Independent Test**: Start with empty booking state, list shows, and inspect
both shows' seats.

**Acceptance Scenarios**:

1. **Given** empty booking state, **When** the operator lists shows, **Then**
   S1 and S2 are shown.
2. **Given** empty booking state, **When** the operator views either show,
   **Then** seats A1 through A10 are shown as available.
3. **Given** a seat booked for S1, **When** the operator views both shows,
   **Then** that seat is unavailable only for S1.

### User Story 2 - Book Seats (Priority: P1)

As a cinema operator, I want to book one or more seats for a show so that the
operator can issue tickets with the exact total.

**Why this priority**: Booking is the primary business operation.

**Independent Test**: Book available seats, inspect the booking, and verify the
seat state and total.

**Acceptance Scenarios**:

1. **Given** A1 and A2 are available for S1, **When** they are booked, **Then**
   the booking succeeds, costs INR 400, and makes A1 and A2 unavailable for S1.
2. **Given** A1 is booked for S1, **When** A1 is booked again for S1, **Then**
   the request is rejected and no booking state changes.
3. **Given** A1 is booked for S1, **When** A1 is booked for S2, **Then** the
   S2 booking succeeds.
4. **Given** a multi-seat request contains an unavailable or invalid seat,
   **When** the request is submitted, **Then** none of its seats are booked.

### User Story 3 - View a Booking (Priority: P2)

As a cinema operator, I want to view a booking by ID so that I can confirm its
show, seats, total, and current status.

**Why this priority**: The operator needs a reliable booking record for lookup
and cancellation.

**Independent Test**: Create a booking, look it up by its returned ID, and
compare all displayed booking fields.

**Acceptance Scenarios**:

1. **Given** an existing booking ID, **When** it is viewed, **Then** its show,
   seats, exact total, and active status are returned.
2. **Given** an unknown booking ID, **When** it is viewed, **Then** a clear
   error is returned without changing stored data.

### User Story 4 - Cancel a Booking (Priority: P2)

As a cinema operator, I want to cancel an active booking so that its seats can
be booked again.

**Why this priority**: Cancellation corrects mistakes and returns seats to the
available inventory.

**Independent Test**: Book seats, cancel the booking, inspect the seats, and
look up the booking again.

**Acceptance Scenarios**:

1. **Given** an active booking, **When** it is cancelled, **Then** its seats
   become available and the booking remains viewable with cancelled status.
2. **Given** a cancelled booking, **When** it is cancelled again, **Then** a
   clear error is returned and the stored data is unchanged.
3. **Given** an unknown booking ID, **When** cancellation is requested, **Then**
   a clear error is returned and no seat is released.

### Edge Cases

- Unknown show IDs, invalid seat names, repeated seats, and empty selections are
  rejected before stored booking state changes.
- Booking IDs are positive, increasing, and never reused after cancellation.
- Restarting the application preserves bookings and the next booking ID.
- Invalid or unreadable local storage produces an error and never resets data.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide exactly two predefined shows, S1 and S2.
- **FR-002**: Each show MUST provide exactly ten seats named A1 through A10.
- **FR-003**: The system MUST support listing shows and viewing seat availability
  separately for each show.
- **FR-004**: The system MUST allow the operator to request a booking for one or
  more seats for one show.
- **FR-005**: Each ticket MUST cost exactly INR 200, with no tax, fee, discount,
  or other price adjustment.
- **FR-006**: A successful booking MUST return a positive, increasing booking ID,
  the selected show and seats, the exact total, and active status.
- **FR-007**: The system MUST reject an unavailable seat and MUST prevent double
  booking of the same seat for the same show.
- **FR-008**: The system MUST validate the complete request before changing
  bookings; all requested seats MUST be booked together or none MUST be booked.
- **FR-009**: The system MUST reject unknown shows, invalid seats, repeated seats,
  and empty seat selections without changing stored data.
- **FR-010**: The system MUST allow the operator to view a booking by ID with its
  show, seats, total, and status.
- **FR-011**: The system MUST cancel an active booking, release its seats for
  that show, and retain the booking with cancelled status.
- **FR-012**: The system MUST reject cancellation of an unknown or already
  cancelled booking without changing stored data.
- **FR-013**: The system MUST preserve bookings, cancellation status, released
  seats, and the next booking ID across application restarts.
- **FR-014**: The system MUST report invalid or unreadable local storage as an
  error instead of silently resetting bookings.
- **FR-015**: The application MUST be delivered as a Python command-line
  interface using local JSON storage, with booking rules separate from command
  handling and storage access.

### Key Entities *(include if feature involves data)*

- **Show**: One predefined show, identified by S1 or S2, with seats A1 through
  A10.
- **Seat**: A named place belonging to one show and having available or booked
  state.
- **Booking**: A positive non-reused ID, show, one or more seats, INR total, and
  active or cancelled status.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A fresh state shows exactly two shows and ten available seats for
  each show.
- **SC-002**: Every successful booking total equals 200 multiplied by its seat
  count, including a two-seat booking total of INR 400.
- **SC-003**: 100% of attempted double bookings and invalid multi-seat requests
  leave the prior booking state unchanged.
- **SC-004**: 100% of active cancellations release exactly the cancelled seats,
  retain a cancelled booking record, and allow those seats to be booked again.
- **SC-005**: After a restart, all previously stored booking records and the next
  booking ID match the state before restart.

## Assumptions

- The operator is local and unauthenticated; one operator and one running
  instance are in scope.
- The first booking ID is 1; subsequent IDs increase by one and are never reused.
- Errors are clear, human-readable command-line messages; no output format
  beyond the CLI is required.
- The local JSON file is the only persistence mechanism and is not silently
  recreated when it is invalid or unreadable.
- No feature is added beyond the stated scope without an explicit approved
  change to the problem statement.

## Scope Exclusions

This feature does not include login, customer personal information, a graphical
interface, a website, online payment, refunds, date/time scheduling, seat
categories, movie administration, concurrent bookings, or multiple operators.
