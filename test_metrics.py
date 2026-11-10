import unittest
from collect_metrics import parse_sacct


class TestSlurmMetrics(unittest.TestCase):

    def test_parse_completed_job(self):
        sample = "12345|COMPLETED|00:00:02|00:00.664||0:0"

        rows = parse_sacct(sample)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["job_id"], "12345")
        self.assertEqual(rows[0]["state"], "COMPLETED")
        self.assertEqual(rows[0]["exit_code"], "0:0")

    def test_empty_output(self):
        self.assertEqual(parse_sacct(""), [])


if __name__ == "__main__":
    unittest.main()
