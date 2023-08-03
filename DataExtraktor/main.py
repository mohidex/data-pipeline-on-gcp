from scrapers import ChalDalScraper


# Usage example:
if __name__ == "__main__":
    scraper = ChalDalScraper()
    for item in scraper.start():
        print(item)


