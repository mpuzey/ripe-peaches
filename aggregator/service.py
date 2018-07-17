from app.gateways.artist_store import ArtistStore
from app.gateways.release_store import ReleaseStore
from app.gateways.review_store import ReviewStore
from app.db.file_adapter import FileAdapter


class AggregatorService:

    def __init__(self, aggregator):
        self.aggregator = aggregator
        self.artist_store = ArtistStore(FileAdapter('artists'))
        self.release_store = ReleaseStore(FileAdapter('releases'), None)
        self.review_store = ReviewStore(FileAdapter('reviews'))

    def start(self):

        aggregation_data = [
            self.artist_store.get(),
            self.release_store.get(),
            self.review_store.get()
        ]

        self.aggregator.work(aggregation_data)



if __name__ == "__main__":
    from aggregator.use_cases.aggregator import Aggregator
    aggregator = Aggregator()
    service = AggregatorService(aggregator)
    service.start()


