from src.app.gateways.artist_store import ArtistStore
from src.app.gateways.release_store import ReleaseStore
from src.app.gateways.review_store import ReviewStore
from src.app.gateways.score_store import ScoreStore

from src.app.db.file_adapter import FileAdapter


class AggregatorService:

    def __init__(self, aggregator):
        self.aggregator = aggregator
        self.artist_store = ArtistStore(FileAdapter('artists'))
        self.release_store = ReleaseStore(FileAdapter('releases'), None)
        self.review_store = ReviewStore(FileAdapter('reviews'))
        self.score_store = ScoreStore(FileAdapter('scores'))

    def start(self):

        aggregation_data = [
            self.artist_store.get(),
            self.release_store.get(),
            self.review_store.get()
        ]

        print('aggregating scores for artist releases...')
        scores = self.aggregator.work(aggregation_data)
        print('finished aggregating scores!')

        self.score_store.put(scores)
