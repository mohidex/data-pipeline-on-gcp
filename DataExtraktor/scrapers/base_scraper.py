from abc import ABC, abstractmethod
from typing import Dict, Iterator

class BaseScraper(ABC):
    @abstractmethod
    def generate_requests(self) -> Iterator['Request']:
        """
        Abstract method to generate requests to be scraped.

        Returns:
            Iterator[Request]: An iterator that yields Request objects representing the URLs to be scraped.
        """
        pass

    @abstractmethod
    def process_item(self, item_html: str) -> Dict[str, str]:
        """
        Abstract method to process the scraped item from the HTML content.

        Args:
            item_html (str): The HTML content of the scraped item.

        Returns:
            Dict[str, str]: A dictionary containing the processed item's data.
        """
        pass

    @abstractmethod
    def parse(self, html_content: str) -> Iterator[Dict[str, str]]:
        """
        Abstract method to parse the HTML content and yield scraped items.

        Args:
            html_content (str): The HTML content to be parsed.

        Yields:
            Iterator[Dict[str, str]]: An iterator that yields dictionaries representing scraped items.
        """
        pass

    def start(self) -> Iterator[Dict[str, str]]:
        """
        Method to manage the overall scraping process.

        Returns:
            Iterator[Dict[str, str]]: An iterator that yields dictionaries representing scraped items.
        """
        for request in self.generate_requests():
            # Make the HTTP request using the Request object and get the response
            response = request()

            # Parse the HTML content of the response and yield scraped items
            for item in self.parse(response):
                yield item
