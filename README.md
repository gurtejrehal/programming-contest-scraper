
# Programming Contest Scraper and API

This project consists of a Python-based web scraper (`ContestScraper`) for programming contests from various platforms and a Flask API to serve the scraped data.

## Features

- **Contest Scraper**: Scrape programming contest information from multiple platforms and save it in JSON format.
- **Flask API**: Serve the scraped contest data through a RESTful API.

## API Schema

The Flask API provides the following endpoint:

- `GET /contests/<platform>`: Retrieve contest data for a specific platform.

The response is a JSON object with the following structure:

```json
{
  "contests": [
    {
      "name": "Contest Name",
      "url": "Contest URL",
      "start_time": "Start Time in ISO 8601 Format",
      "end_time": "End Time in ISO 8601 Format",
      "duration": "Duration in human-readable format (e.g., 3 hours, 30 minutes)",
      "type": "Type of the contest",
      "in_24_hours": "Yes or No, indicating if the contest starts within 24 hours",
      "status": "Current status (e.g., 'CODING', 'BEFORE')"
    },
    ...
  ]
}
```

Replace `<platform>` in the endpoint with the desired platform name (e.g., `codeforces`, `hackerrank`).

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Flask
- Other dependencies listed in `requirements.txt`

### Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/gurtejrehal/programming-contest-scraper.git
   cd programming-contest-scraper
   ```

2. Install the required packages:

   ```sh
   pip install -r requirements.txt
   ```

### Usage

1. Run the scraper to collect contest data:

   ```sh
   python contest_scraper.py
   ```

   This will scrape the contest data and save it in the `output` directory.

2. Start the Flask server:

   ```sh
   flask run
   ```

   The API will be available at `http://127.0.0.1:5000/`.

### API Endpoints

- **Get Contest Data**: `GET /contests/<platform>`

   Replace `<platform>` with the platform name to retrieve its contests (e.g., `codeforces`, `hackerrank`).

### Example

To get contests from Codeforces:

```sh
curl http://127.0.0.1:5000/contests/codeforces
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## Developer

- **Gurtej Rehal**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
