from .base_scraper import BaseScraper
from typing import Dict, Iterator
from .http import Request
from bs4 import BeautifulSoup

class ChalDalScraper(BaseScraper):

    # Implement the generate_requests method to yield the URLs to be scraped
    def generate_requests(self) -> Iterator[Request]:
        yield Request("http://books.toscrape.com/catalogue/category/books/mystery_3/index.html", method="GET")
        yield Request("http://books.toscrape.com/catalogue/category/books/travel_2/index.html", method="GET")

    # Implement the parse method to parse the item from the HTML content
    def parse(self, html_content: str) -> Iterator[Dict[str, str]]:
        soup = BeautifulSoup(html_content.text, "html.parser")
        return soup.find_all(class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
    
    def process_item(self, item_html: str) -> Dict[str, str]:
        name = item_html.article.h3.text
        price = item_html.article.find('p', class_='price_color').text
        return {
            'name': name,
            'price': price
        }
