
import json
import time
from collections import Counter
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://quotes.toscrape.com/"
OUTPUT_DIR = Path(__file__).parent

HEADERS = {
    "User-Agent": "InternCircle-learning-project (student scraper)"
}


def scrape_quotes():
    """Collect quotes, authors and tags from the practice website."""
    url = BASE_URL
    quotes = []

    with requests.Session() as session:
        session.headers.update(HEADERS)

        while url:
            try:
                response = session.get(url, timeout=10)
                response.raise_for_status()
            except requests.RequestException as error:
                print(f"Could not fetch {url}: {error}")
                break

            soup = BeautifulSoup(response.text, "html.parser")

            for item in soup.select("div.quote"):
                text_element = item.select_one("span.text")
                author_element = item.select_one("small.author")

                # Skip incomplete quote records safely.
                if text_element is None or author_element is None:
                    continue

                quotes.append({
                    "text": text_element.get_text(strip=True),
                    "author": author_element.get_text(strip=True),
                    "tags": [
                        tag.get_text(strip=True)
                        for tag in item.select("a.tag")
                    ],
                })

            next_link = soup.select_one("li.next a")
            url = (
                urljoin(url, next_link["href"])
                if next_link and next_link.get("href")
                else None
            )

            if url:
                time.sleep(1)

    return quotes


def save_results(quotes):
    """Save scraped data in JSON and readable text files."""
    json_path = OUTPUT_DIR / "quotes.json"
    text_path = OUTPUT_DIR / "quotes.txt"

    with json_path.open("w", encoding="utf-8") as file:
        json.dump(quotes, file, indent=2, ensure_ascii=False)

    with text_path.open("w", encoding="utf-8") as file:
        for number, quote in enumerate(quotes, start=1):
            file.write(f"{number}. {quote['text']}\n")
            file.write(f"   Author: {quote['author']}\n")
            file.write(f"   Tags: {', '.join(quote['tags'])}\n\n")

    print(f"\nSaved {len(quotes)} quotes.")
    print(f"JSON file: {json_path.name}")
    print(f"Text file: {text_path.name}")


def print_summary(quotes):
    """Display basic statistics about the collected quotes."""
    if not quotes:
        print("No quotes were collected. Check your internet connection.")
        return

    authors = Counter(q["author"] for q in quotes)
    tags = Counter(tag for q in quotes for tag in q["tags"])

    print("\n--- Scraping Summary ---")
    print(f"Total quotes: {len(quotes)}")
    print(f"Most quoted author: {authors.most_common(1)[0][0]}")

    if tags:
        print(f"Most common tag: {tags.most_common(1)[0][0]}")
    else:
        print("No tags found.")


def main():
    print("Starting quote scraper...")
    quotes = scrape_quotes()

    # Save results even if a request failed after some pages.
    save_results(quotes)
    print_summary(quotes)


if __name__ == "__main__":
    main()
