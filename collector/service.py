from collector.scraper import Scraper
from app.storage.review_store import ReviewStore


class CollectorService:

    @staticmethod
    def start():
        scraper = Scraper()
        harvested_data = scraper.collect()
        store = ReviewStore()
        store.store_reviews(harvested_data)
