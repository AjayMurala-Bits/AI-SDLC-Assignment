import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from movie_booking.cli import main


class CliTests(unittest.TestCase):
    def invoke(self, path: Path, *args: str) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            result = main(list(args), store_path=path)
        return result, stdout.getvalue(), stderr.getvalue()

    def test_cli_commands_cover_booking_lifecycle(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bookings.json"
            result, output, error = self.invoke(path, "list-shows")
            self.assertEqual((result, output, error), (0, "S1\nS2\n", ""))
            result, output, _ = self.invoke(path, "view-seats", "S1")
            self.assertEqual(result, 0)
            self.assertIn("A1", output)
            result, output, _ = self.invoke(path, "book", "S1", "A1", "A2")
            self.assertEqual(result, 0)
            self.assertIn("total=INR 400", output)
            result, output, _ = self.invoke(path, "view-booking", "1")
            self.assertEqual(result, 0)
            self.assertIn("status=active", output)
            result, output, _ = self.invoke(path, "cancel", "1")
            self.assertEqual(result, 0)
            self.assertIn("status=cancelled", output)

    def test_cli_reports_invalid_input(self):
        with tempfile.TemporaryDirectory() as directory:
            result, output, error = self.invoke(Path(directory) / "bookings.json", "view-seats", "S3")
            self.assertEqual(result, 1)
            self.assertEqual(output, "")
            self.assertIn("Error:", error)


if __name__ == "__main__":
    unittest.main()
