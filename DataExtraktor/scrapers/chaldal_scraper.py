from .base_scraper import BaseScraper
from typing import Dict, Iterator
from .http import Request
from bs4 import BeautifulSoup

class ChalDalScraper(BaseScraper):
    # Implement the generate_requests method to yield the URLs to be scraped
    def generate_requests(self) -> Iterator[Request]:
        yield Request("https://example.com/page1", method="GET", headers=self.headers)
        yield Request("https://example.com/page2", method="GET", headers=self.headers)

    # Implement the parse method to parse the item from the HTML content
    def parse(self, html_content: str) -> Iterator[Dict[str, str]]:
        soup = BeautifulSoup(html_content, "html.parser")
        title = soup.select_one("h1").text.strip()
        price = soup.select_one(".price").text.strip()
        description = soup.select_one(".description").text.strip()

        yield {
            "title": title,
            "price": price,
            "description": description
        }
