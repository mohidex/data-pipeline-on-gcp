import config
from scrapers import ChalDalScraper
from publisher import GooglePubSubClient


def main():
    client = GooglePubSubClient(
        project_id=config.PROJECT_ID,
        topic_id=config.TOPIC_ID,
        credentials_path=config.CREDENTIALS_PATH
    )
    scraper = ChalDalScraper()
    for item in scraper.start():
        msg = client.publish_message(item.to_dict())
        print(msg)


if __name__ == "__main__":
    main()


