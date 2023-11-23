from bs4 import BeautifulSoup
from dateutil import parser
import datetime
import requests
import logging
import html
import json
import re
import os


# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Platforms to scrape
PLATFORMS = ["codeforces", "topcoder", "atcoder", "codechef", "leetcode", "hackerrank", "hackerearth", "kickstart"]


class ContestScraper:
    def __init__(self, platforms, output_dir='output'):
        self.platforms = platforms
        self.base_url = "https://clist.by/"
        self.output_dir = output_dir
        self.create_output_dir()
        logging.info("ContestScraper initialized")

    def create_output_dir(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def format_duration(self, seconds):
            if seconds < 0:
                return "Invalid duration"

            days = seconds // (24 * 3600)
            hours = (seconds % (24 * 3600)) // 3600
            minutes = (seconds % 3600) // 60

            duration_parts = []
            if days > 0:
                duration_parts.append(f"{int(days)} day{'s' if days > 1 else ''}")
            if hours > 0:
                duration_parts.append(f"{int(hours)} hour{'s' if hours > 1 else ''}")
            if minutes > 0:
                duration_parts.append(f"{int(minutes)} minute{'s' if minutes > 1 else ''}")

            return ", ".join(duration_parts) if duration_parts else "0 minutes"

    def parse_contest_data(self, data_ace):
        try:
            # Cleaning and escaping problematic characters
            cleaned_data = re.sub(r'(?<="):\s*"(.*?)(?<!\\)"', lambda m: ':"' + m.group(1).replace('"', '\\"') + '"', html.unescape(data_ace))
            
            # Parsing JSON
            contest_data = json.loads(cleaned_data)

            # Calculating duration in seconds
            duration_seconds = (parser.parse(contest_data["time"]["end"]) - parser.parse(contest_data["time"]["start"])).total_seconds() if contest_data["time"].get("start") and contest_data["time"].get("end") else 0

            # Transforming to the API schema
            api_schema = {
                "name": contest_data.get("title", "Unknown"),
                "url": contest_data.get("desc", "Unknown").replace("url: ", ""),
                "start_time": parser.parse(contest_data["time"]["start"]).strftime('%Y-%m-%dT%H:%M:%S.%fZ') if contest_data["time"].get("start") else "-",
                "end_time": parser.parse(contest_data["time"]["end"]).strftime('%Y-%m-%dT%H:%M:%S.%fZ') if contest_data["time"].get("end") else "-",
                "duration": self.format_duration(duration_seconds),
                "type_": "Unknown", # Assuming type is unknown
                "in_24_hours": "Yes" if parser.parse(contest_data["time"]["start"]) - datetime.datetime.utcnow() <= datetime.timedelta(days=1) else "No",
                "status": "CODING" if contest_data["time"].get("start") and parser.parse(contest_data["time"]["start"]) <= datetime.datetime.utcnow() <= parser.parse(contest_data["time"]["end"]) else "BEFORE"
            }

            return api_schema
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return None


    def get_contests(self):
        logging.info("Starting to scrape contest data")
        response = requests.get(self.base_url)
        contests = []

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            contest_elements = soup.select('.contest.row:not(.subcontest) > div + div > i + a')

            for element in contest_elements:
                data_ace = element.get('data-ace')
                if data_ace:
                    contest_info = self.parse_contest_data(data_ace)
                    contests.append(contest_info)

        logging.info(f"Scraping completed, found {len(contests)} contests")
        return contests

    def save_contests_by_platform(self, contests):
        logging.info("Saving contests by platform")
        platform_contests = {platform: [] for platform in self.platforms}

        for contest in contests:
            if contest:  # Check if contest data is not None
                for platform in self.platforms:
                    if platform in contest['url']:
                        platform_contests[platform].append(contest)
                        break

        for platform, contests in platform_contests.items():
            file_path = os.path.join(self.output_dir, f"{platform}_contests.json")
            with open(file_path, "w") as file:
                json.dump(contests, file, indent=4, default=str)

        logging.info("Contests saved successfully")

    def run(self):
        logging.info("ContestScraper execution started")
        contests = self.get_contests()
        self.save_contests_by_platform(contests)
        logging.info("ContestScraper execution completed")


if __name__ == '__main__':
    scraper = ContestScraper(PLATFORMS)
    scraper.run()

