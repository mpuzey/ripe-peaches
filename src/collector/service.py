from src.app.gateways.artist_store import ArtistStore
from src.app.gateways.release_store import ReleaseStore
from src.app.gateways.review_store import ReviewStore
from src.collector.web import metacritic, aoty

from constants import METACRITIC_CURATED_PUBLICATIONS, AOTY_PUBLICATIONS
from src.app.db.file_adapter import FileAdapter


class CollectorService:

    def __init__(self, collector):
        self.collector = collector
        self.review_store = ReviewStore(FileAdapter('reviews'))
        self.release_store = ReleaseStore(FileAdapter('releases'), self.review_store)
        self.artist_store = ArtistStore(FileAdapter('artists'))

    def start(self):

        # self.collector.collect(METACRITIC_CURATED_PUBLICATIONS, metacritic)
        self.collector.collect(AOTY_PUBLICATIONS, aoty)
        artists = self.collector.parse()

        self.artist_store.put(artists)
        self.release_store.put(artists)
