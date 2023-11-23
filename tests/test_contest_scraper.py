import unittest
import datetime
from unittest.mock import patch, MagicMock
from contest_scraper import ContestScraper

class TestContestScraper(unittest.TestCase):

    @patch('contest_scraper.requests.get') 
    def test_get_contests(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200

        with open('test_data.html', 'r') as file:
            mock_response.content = file.read()
        mock_get.return_value = mock_response

        scraper = ContestScraper(["codeforces"])
        result = scraper.get_contests()

        self.assertIsInstance(result, list) 
        self.assertGreater(len(result), 0)

    @patch('contest_scraper.parser.parse') 
    def test_parse_contest_data(self, mock_parse):
        mock_time = datetime.datetime(2023, 1, 1, 12, 0)
        mock_parse.return_value = mock_time

        data_ace = '{"title": "Sample Contest", "desc": "url: https://example.com", "time": {"start": "2023-01-01T12:00:00", "end": "2023-01-01T15:00:00"}}'

        scraper = ContestScraper(["codeforces"])
        result = scraper.parse_contest_data(data_ace)

        # Assertions
        self.assertEqual(result['name'], "Sample Contest")
        self.assertIn("example.com", result['url'])
        self.assertEqual(result['duration'], "0 minutes")

    def test_format_duration(self):
        scraper = ContestScraper(["codeforces"])

        self.assertEqual(scraper.format_duration(3661), "1 hour, 1 minute")
        self.assertEqual(scraper.format_duration(48 * 3600), "2 days")
        self.assertEqual(scraper.format_duration(0), "0 minutes")


if __name__ == '__main__':
    unittest.main()
