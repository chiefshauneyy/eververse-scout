import unittest
from datetime import datetime, timezone
from bot import EVERVERSE_URL, make_message

class MessageTests(unittest.TestCase):
    def test_message_has_correct_link(self):
        message = make_message(datetime(2026, 11, 15, 17, 15, tzinfo=timezone.utc))
        self.assertIn(EVERVERSE_URL, message)
        self.assertIn("November 15, 2026", message)

if __name__ == "__main__":
    unittest.main()
