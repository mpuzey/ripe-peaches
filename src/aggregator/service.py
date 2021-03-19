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
        self.score_store = ScoreStore(FileAdapter('scores'), None)

    def start(self):

        aggregation_data = [
            self.artist_store.get_all(),
            self.release_store.get_all(),
            self.review_store.get_all()
        ]

        print('aggregating scores for artist releases...')
        scores = self.aggregator.work(aggregation_data)
        print('finished aggregating scores!')

        self.score_store.put(scores)
