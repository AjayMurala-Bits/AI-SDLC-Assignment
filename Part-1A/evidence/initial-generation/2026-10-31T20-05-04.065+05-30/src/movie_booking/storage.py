"""Validated JSON persistence for booking state."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

from .models import (
    ACTIVE,
    BOOKING_STATUSES,
    CANCELLED,
    SEAT_IDS,
    SHOW_IDS,
    STORE_VERSION,
    TICKET_PRICE_INR,
)


class StorageError(Exception):
    """Raised when booking storage cannot be read, written, or validated."""


def empty_store() -> dict[str, Any]:
    return {
        "version": STORE_VERSION,
        "shows": list(SHOW_IDS),
        "next_booking_id": 1,
        "bookings": [],
    }


def load_store(path: Path) -> dict[str, Any]:
    if not path.exists():
        return empty_store()
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise StorageError(f"Unable to read storage: {path}") from exc
    validate_store(data)
    return data


def save_store(path: Path, data: dict[str, Any]) -> None:
    validate_store(data)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            delete=False,
        ) as handle:
            temporary_name = handle.name
            json.dump(data, handle, indent=2, sort_keys=True)
            handle.write("\n")
        os.replace(temporary_name, path)
    except OSError as exc:
        if temporary_name:
            try:
                os.unlink(temporary_name)
            except OSError:
                pass
        raise StorageError(f"Unable to write storage: {path}") from exc


def validate_store(data: Any) -> None:
    if not isinstance(data, dict):
        raise StorageError("Storage root must be an object")
    if data.get("version") != STORE_VERSION:
        raise StorageError("Unsupported storage version")
    if data.get("shows") != list(SHOW_IDS):
        raise StorageError("Storage shows are invalid")
    next_id = data.get("next_booking_id")
    if not isinstance(next_id, int) or isinstance(next_id, bool) or next_id < 1:
        raise StorageError("next_booking_id must be a positive integer")
    bookings = data.get("bookings")
    if not isinstance(bookings, list):
        raise StorageError("bookings must be a list")

    booking_ids: set[int] = set()
    active_seats: dict[str, set[str]] = {show_id: set() for show_id in SHOW_IDS}
    maximum_id = 0
    for booking in bookings:
        if not isinstance(booking, dict):
            raise StorageError("Each booking must be an object")
        booking_id = booking.get("booking_id")
        if (
            not isinstance(booking_id, int)
            or isinstance(booking_id, bool)
            or booking_id < 1
            or booking_id in booking_ids
        ):
            raise StorageError("Booking IDs must be unique positive integers")
        booking_ids.add(booking_id)
        maximum_id = max(maximum_id, booking_id)
        show_id = booking.get("show_id")
        if show_id not in SHOW_IDS:
            raise StorageError("Booking show is invalid")
        seats = booking.get("seats")
        if not isinstance(seats, list) or not seats:
            raise StorageError("Booking seats must be a non-empty list")
        if any(seat not in SEAT_IDS for seat in seats) or len(set(seats)) != len(seats):
            raise StorageError("Booking seats are invalid")
        expected_seats = sorted(seats, key=lambda seat: int(seat[1:]))
        if seats != expected_seats:
            raise StorageError("Booking seats must be ordered")
        if booking.get("total_inr") != TICKET_PRICE_INR * len(seats):
            raise StorageError("Booking total is invalid")
        status = booking.get("status")
        if status not in BOOKING_STATUSES:
            raise StorageError("Booking status is invalid")
        if status == ACTIVE:
            if active_seats[show_id].intersection(seats):
                raise StorageError("Active seat bookings overlap")
            active_seats[show_id].update(seats)
        elif status != CANCELLED:
            raise StorageError("Booking status is invalid")
    if next_id <= maximum_id:
        raise StorageError("next_booking_id must exceed existing booking IDs")
