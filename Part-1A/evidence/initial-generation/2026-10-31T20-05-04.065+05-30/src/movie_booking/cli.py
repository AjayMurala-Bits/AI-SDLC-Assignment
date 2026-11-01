"""Command-line interface for movie ticket booking."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from .booking import (
    BookingError,
    available_seats,
    cancel_booking,
    create_booking,
    get_booking,
    list_shows,
)
from .storage import StorageError, load_store, save_store

DEFAULT_STORE = "bookings.json"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Movie Ticket Booking CLI")
    commands = parser.add_subparsers(dest="command", required=True)

    commands.add_parser("list-shows", help="list the available shows")

    seats_parser = commands.add_parser("view-seats", help="view available seats")
    seats_parser.add_argument("show_id")

    book_parser = commands.add_parser("book", help="book one or more seats")
    book_parser.add_argument("show_id")
    book_parser.add_argument("seats", nargs="+")

    view_parser = commands.add_parser("view-booking", help="view a booking")
    view_parser.add_argument("booking_id", type=int)

    cancel_parser = commands.add_parser("cancel", help="cancel a booking")
    cancel_parser.add_argument("booking_id", type=int)
    return parser


def main(argv: Sequence[str] | None = None, store_path: Path | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    path = store_path or Path.cwd() / DEFAULT_STORE
    try:
        store = load_store(path)
        if args.command == "list-shows":
            for show_id in list_shows():
                print(show_id)
        elif args.command == "view-seats":
            print(" ".join(available_seats(store, args.show_id)))
        elif args.command == "book":
            booking = create_booking(store, args.show_id, args.seats)
            save_store(path, store)
            print(_format_booking(booking))
        elif args.command == "view-booking":
            print(_format_booking(get_booking(store, args.booking_id)))
        elif args.command == "cancel":
            booking = cancel_booking(store, args.booking_id)
            save_store(path, store)
            print(_format_booking(booking))
        return 0
    except (BookingError, StorageError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


def _format_booking(booking: dict[str, object]) -> str:
    seats = ", ".join(booking["seats"])
    return (
        f"Booking {booking['booking_id']}: show={booking['show_id']} "
        f"seats={seats} total=INR {booking['total_inr']} "
        f"status={booking['status']}"
    )
