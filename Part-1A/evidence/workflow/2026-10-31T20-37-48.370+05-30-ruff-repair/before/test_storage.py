import json
import tempfile
import unittest
from pathlib import Path

from movie_booking.booking import create_booking
from movie_booking.storage import StorageError, empty_store, load_store, save_store


class StorageTests(unittest.TestCase):
    def test_round_trip_preserves_bookings_and_ids(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bookings.json"
            store = empty_store()
            create_booking(store, "S1", ["A1"])
            save_store(path, store)
            loaded = load_store(path)
            self.assertEqual(loaded, store)
            next_booking = create_booking(loaded, "S1", ["A2"])
            self.assertEqual(next_booking["booking_id"], 2)

    def test_invalid_json_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bookings.json"
            path.write_text("{not json", encoding="utf-8")
            with self.assertRaises(StorageError):
                load_store(path)

    def test_invalid_store_shape_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bookings.json"
            path.write_text(json.dumps({"version": 1}), encoding="utf-8")
            with self.assertRaises(StorageError):
                load_store(path)

    def test_unreadable_store_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(StorageError):
                load_store(Path(directory))


if __name__ == "__main__":
    unittest.main()
