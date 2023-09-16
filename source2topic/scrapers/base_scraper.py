from abc import ABC, abstractmethod
from typing import Dict, Iterator, Union
from requests.models import Response
from models import Product


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
    def process_item(self, data: Union[str, dict]) -> Product:
        """
        Abstract method to process the scraped item from the data.

        Args:
            data (Union[str, dict]): The scraped item's data, which can be a string or a dictionary.

        Returns:
            Product: A processed Product object representing the scraped item's data.
        """
        pass

    @abstractmethod
    def parse(self, response: Response) -> Iterator[Union[Dict[str, str], str]]:
        """
        Abstract method to parse the HTTP response and yield scraped items.

        Args:
            response (Response): The HTTP response object containing the HTML content to be parsed.

        Yields:
            Iterator[Union[Dict[str, str], str]]: An iterator that yields dictionaries or strings representing scraped items.
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
            for item_html in self.parse(response):
                yield self.process_item(item_html)
