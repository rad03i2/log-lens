import unittest
from log_lens.core import LogLensError, filter_records, iter_records, parse_line, summarize


class CoreTests(unittest.TestCase):
    def test_parse_level_and_timestamp(self):
        row = parse_line(3, "2026-09-21T10:20:30Z ERROR database unavailable\n")
        self.assertEqual(row.level, "ERROR")
        self.assertEqual(row.timestamp, "2026-09-21T10:20:30Z")
        self.assertEqual(row.number, 3)

    def test_aliases_are_normalized(self):
        self.assertEqual(parse_line(1, "WARNING slow").level, "WARN")
        self.assertEqual(parse_line(2, "FATAL stop").level, "CRITICAL")

    def test_filters_combine(self):
        rows = iter_records(["INFO ready", "ERROR timeout API", "ERROR disk"])
        result = list(filter_records(rows, level="error", contains="api", ignore_case=True))
        self.assertEqual([r.number for r in result], [2])

    def test_regex_filter(self):
        rows = iter_records(["INFO id=12", "INFO id=abc"])
        result = list(filter_records(rows, regex=r"id=\d+$"))
        self.assertEqual(len(result), 1)

    def test_invalid_regex_is_domain_error(self):
        with self.assertRaises(LogLensError):
            list(filter_records(iter_records(["x"]), regex="["))

    def test_summary(self):
        data = summarize(iter_records(["INFO ok", "ERROR bad", "plain line"]))
        self.assertEqual(data["total_lines"], 3)
        self.assertEqual(data["levels"], {"ERROR": 1, "INFO": 1, "UNCLASSIFIED": 1})


if __name__ == "__main__":
    unittest.main()
