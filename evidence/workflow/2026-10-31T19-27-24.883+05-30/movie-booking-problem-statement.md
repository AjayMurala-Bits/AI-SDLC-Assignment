# Movie Ticket Booking CLI Problem Statement

## Purpose

Build a simple command-line application for a small cinema counter to check seats, book tickets and cancel bookings. This is the proposed Part 1A application. Smart Todo is earlier practice work; its approval and test results do not establish approval or validation for this application.

## Problem statement

A cinema operator needs a small local tool to track seats for two predefined movie shows. The application lets the operator view shows and seat availability, book one or more seats, view a booking by ID, and cancel a booking. It prevents double booking, calculates the exact total using a fixed ticket price, and saves bookings in a local JSON file across restarts.

## Minimal scope

- Two predefined shows, identified as S1 and S2.
- Ten seats per show, named A1 through A10.
- Every ticket costs INR 200; no taxes, fees or discounts.
- Five operations: list shows, view seats, book seats, view booking, cancel booking.
- Booking all requested seats succeeds together, or the whole request fails.
- Booking IDs are increasing positive integers and are never reused.
- Cancellation releases seats for that show; retain the booking with status cancelled.
- One local operator and one running instance at a time.
- Python command line interface with local JSON storage.

## Expected behaviour to specify and test

1. Both shows initially have ten available seats.
2. Booking A1 and A2 for S1 costs INR 400 and makes those seats unavailable only for S1.
3. Booking A1 again for S1 is rejected; booking A1 for S2 remains possible.
4. A request containing an unavailable seat does not book any of its other seats.
5. Unknown shows, invalid seats, repeated seats in one request and empty seat selections are rejected without changing stored data.
6. Viewing a booking returns its show, seats, total and status.
7. Cancelling an active booking releases its seats; cancelling it again or using an unknown booking ID returns a clear error without changing data.
8. Restarting preserves bookings and the next booking ID.
9. Invalid or unreadable storage produces an error instead of silently resetting bookings.

## Exclusions

No login, customer personal information, graphical interface, website, online payment, refund processing, date/time scheduling, seat categories, movie administration or concurrent bookings.

## Development workflow

Use the lab sheet as the process reference: constitution, specification, clarification, plan, tasks, analysis, implementation and verification. Use reasonable defaults for minor choices and keep the feature scope above fixed unless the student requests a change.

Preserve the first movie-booking implementation, real harness runs and genuine repairs. Run syntax/lint, security and specification-derived tests using one harness command. The student writes the narrative log and reflections and makes the final acceptance decision.

## Status

Problem statement draft prepared from the selected movie-ticket-booking idea. No movie-booking implementation or validation has been performed. Review the constitution for this new scope and create fresh feature artifacts before implementation.
