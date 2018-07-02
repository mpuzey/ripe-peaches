from collector.sources import metacritic, aoty
from constants import METACRITIC_PUBLICATIONS_SAMPLE, AOTY_PUBLICATIONS_SAMPLE
from app.gateways.review_store import ReviewStore
from app.db.file_adapter import FileAdapter


class CollectorService:

    def __init__(self, collector):
        self.collector = collector
        self.review_store = ReviewStore(FileAdapter('reviews'))

    def start(self):
        harvested_data = self.collector.collect(METACRITIC_PUBLICATIONS_SAMPLE, metacritic)
        harvested_data.extend(self.collector.collect(AOTY_PUBLICATIONS_SAMPLE, aoty))

        self.review_store.put(harvested_data)
