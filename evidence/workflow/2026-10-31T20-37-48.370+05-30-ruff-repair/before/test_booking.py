import copy
import unittest

from movie_booking.booking import (
    BookingError,
    available_seats,
    cancel_booking,
    create_booking,
    get_booking,
)
from movie_booking.storage import empty_store


class BookingTests(unittest.TestCase):
    def setUp(self):
        self.store = empty_store()

    def test_shows_start_with_ten_seats_and_are_independent(self):
        self.assertEqual(len(available_seats(self.store, "S1")), 10)
        self.assertEqual(len(available_seats(self.store, "S2")), 10)
        create_booking(self.store, "S1", ["A1"])
        self.assertNotIn("A1", available_seats(self.store, "S1"))
        self.assertIn("A1", available_seats(self.store, "S2"))

    def test_successful_booking_has_exact_price(self):
        booking = create_booking(self.store, "S1", ["A3", "A1"])
        self.assertEqual(booking["booking_id"], 1)
        self.assertEqual(booking["seats"], ["A1", "A3"])
        self.assertEqual(booking["total_inr"], 400)
        self.assertEqual(booking["status"], "active")

    def test_double_booking_and_multi_seat_failure_are_atomic(self):
        create_booking(self.store, "S1", ["A1"])
        before = copy.deepcopy(self.store)
        with self.assertRaises(BookingError):
            create_booking(self.store, "S1", ["A2", "A1"])
        self.assertEqual(self.store, before)

    def test_invalid_inputs_are_rejected(self):
        for show_id, seats in (("S3", ["A1"]), ("S1", ["A11"]), ("S1", ["A1", "A1"]), ("S1", [])):
            with self.subTest(show_id=show_id, seats=seats):
                with self.assertRaises(BookingError):
                    create_booking(self.store, show_id, seats)

    def test_view_and_cancel_booking(self):
        create_booking(self.store, "S1", ["A1"])
        self.assertEqual(get_booking(self.store, 1)["status"], "active")
        cancel_booking(self.store, 1)
        self.assertEqual(get_booking(self.store, 1)["status"], "cancelled")
        self.assertIn("A1", available_seats(self.store, "S1"))
        with self.assertRaises(BookingError):
            cancel_booking(self.store, 1)

    def test_unknown_booking_ids_are_rejected_without_mutation(self):
        before = copy.deepcopy(self.store)
        with self.assertRaises(BookingError):
            get_booking(self.store, 99)
        with self.assertRaises(BookingError):
            cancel_booking(self.store, 99)
        self.assertEqual(self.store, before)


if __name__ == "__main__":
    unittest.main()
