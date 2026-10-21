
# Web Scraper for Quotes

## Project Overview
This project uses Python to collect quotes, authors and tags
from a public practice website and save the results as JSON
and readable text.

## Data Source
https://quotes.toscrape.com/

This website is designed for practicing web scraping.

## Technologies Used
- Python
- Requests
- BeautifulSoup
- JSON

## Features
- Sends HTTP requests with a timeout.
- Checks HTTP errors.
- Extracts quotes, authors and tags from HTML.
- Follows pagination to collect multiple pages.
- Waits one second between page requests.
- Saves data in quotes.json and quotes.txt.
- Displays the total number of quotes, most quoted author
  and most common tag.

## Requirements
Python 3.10 or later is recommended.

Install the libraries:
pip install requests beautifulsoup4

## How to Run
1. Open the project folder in VS Code.
2. Install the required libraries.
3. Run: python scraper.py
4. Check quotes.json and quotes.txt for the results.

## Responsible Scraping
The project uses the practice website intended for scraping
exercises. It uses a timeout, a descriptive User-Agent and
a one-second delay between page requests. It does not scrape
personal data or pages behind a login.

## Output Files
- scraper.py: scraper source code
- quotes.json: collected data in JSON format
- quotes.txt: readable quote records
- README.md: project documentation
