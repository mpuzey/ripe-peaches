from collector.scraper import Scraper
from app.storage.review_store import ReviewStore


class CollectorService:

    @staticmethod
    def start():
        store = ReviewStore()
        scraper = Scraper()
        harvested_data = scraper.collect()
        store.store_reviews(harvested_data)
