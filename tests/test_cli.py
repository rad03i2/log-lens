import contextlib
import io
from pathlib import Path
import tempfile
import unittest

from log_lens.cli import main


class CliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "app.log"
        self.path.write_text("INFO started\nERROR timeout\nWARNING slow\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_search_json(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = main(["search", str(self.path), "--level", "error", "--json"])
        self.assertEqual(code, 0)
        self.assertIn('"level": "ERROR"', out.getvalue())

    def test_no_match_returns_one(self):
        with contextlib.redirect_stdout(io.StringIO()):
            code = main(["search", str(self.path), "--contains", "missing"])
        self.assertEqual(code, 1)

    def test_summary(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = main(["summary", str(self.path)])
        self.assertEqual(code, 0)
        self.assertIn("Lines: 3", out.getvalue())


if __name__ == "__main__":
    unittest.main()
