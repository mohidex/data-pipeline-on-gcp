from .base_scraper import BaseScraper
from typing import Dict, Iterator, Union
from .http import Request
from requests.models import Response
from bs4 import BeautifulSoup
from models import Product


class ChalDalScraper(BaseScraper):

    # Implement the generate_requests method to yield the URLs to be scraped
    def generate_requests(self) -> Iterator[Request]:
        url = "https://catalog.chaldal.com/searchOld"
        form_data = {
            "apiKey": "e964fc2d51064efa97e94db7c64bf3d044279d4ed0ad4bdd9dce89fecc9156f0",
            "storeId": 1,
            "warehouseId": 8,
            "pageSize": 100,
            "currentPageIndex": 0,
            "metropolitanAreaId": 1,
            "query": "",
            "productVariantId": -1,
            "canSeeOutOfStock": "false",
            "filters": [],
            "maxOutOfStockCount": {"case": "Some", "fields": [5]},
            "shouldShowAlternateProductsForAllOutOfStock": {"case": "Some", "fields": [True]}
        }
        req =  Request(url=url, method="POST", json=form_data)
        n_pages = req().json()['nbPages']
        for i in range(2):
            form_data.update({"currentPageIndex": i})
            yield Request(url=url, method="POST", json=form_data)

    def parse(self, response: Response) -> Iterator[Union[Dict[str, str], str]]:
        json_data = response.json()
        yield from json_data["hits"]
    
    def process_item(self, data: Union[str, dict]) -> Product:
        name = data.get("name")
        price = data.get("mrp")
        key = data.get("slug")
        return Product(
            key=key,
            name=name,
            price=price,
            source="Chaldal"
        )
