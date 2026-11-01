"""Booking rules independent of the CLI and JSON storage."""

from __future__ import annotations

from typing import Any

from .models import ACTIVE, CANCELLED, SEAT_IDS, SHOW_IDS, TICKET_PRICE_INR


class BookingError(Exception):
    """Raised for invalid booking operations."""


def list_shows() -> tuple[str, ...]:
    return SHOW_IDS


def available_seats(store: dict[str, Any], show_id: str) -> list[str]:
    _validate_show(show_id)
    booked = {
        seat
        for booking in store["bookings"]
        if booking["show_id"] == show_id and booking["status"] == ACTIVE
        for seat in booking["seats"]
    }
    return [seat for seat in SEAT_IDS if seat not in booked]


def create_booking(
    store: dict[str, Any], show_id: str, seats: list[str]
) -> dict[str, Any]:
    _validate_show(show_id)
    if not seats:
        raise BookingError("At least one seat is required")
    if len(set(seats)) != len(seats):
        raise BookingError("Duplicate seats are not allowed")
    if any(seat not in SEAT_IDS for seat in seats):
        raise BookingError("Seat must be between A1 and A10")
    ordered_seats = sorted(seats, key=lambda seat: int(seat[1:]))
    available = set(available_seats(store, show_id))
    unavailable = [seat for seat in ordered_seats if seat not in available]
    if unavailable:
        raise BookingError(f"Seat(s) already booked or unavailable: {', '.join(unavailable)}")

    booking = {
        "booking_id": store["next_booking_id"],
        "show_id": show_id,
        "seats": ordered_seats,
        "total_inr": TICKET_PRICE_INR * len(ordered_seats),
        "status": ACTIVE,
    }
    store["bookings"].append(booking)
    store["next_booking_id"] += 1
    return booking


def get_booking(store: dict[str, Any], booking_id: int) -> dict[str, Any]:
    if not isinstance(booking_id, int) or isinstance(booking_id, bool) or booking_id < 1:
        raise BookingError("Booking ID must be a positive integer")
    for booking in store["bookings"]:
        if booking["booking_id"] == booking_id:
            return booking
    raise BookingError(f"Booking not found: {booking_id}")


def cancel_booking(store: dict[str, Any], booking_id: int) -> dict[str, Any]:
    booking = get_booking(store, booking_id)
    if booking["status"] == CANCELLED:
        raise BookingError("Booking is already cancelled")
    booking["status"] = CANCELLED
    return booking


def _validate_show(show_id: str) -> None:
    if show_id not in SHOW_IDS:
        raise BookingError("Show must be S1 or S2")
