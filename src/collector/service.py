from src.app.gateways.artist_store import ArtistStore
from src.app.gateways.release_store import ReleaseStore
from src.app.gateways.review_store import ReviewStore
from src.collector.use_cases import enricher
from src.collector.web import metacritic, aoty

from constants import METACRITIC_CURATED_PUBLICATIONS, AOTY_CURATED_PUBLICATIONS
from src.app.db.file_adapter import FileAdapter


class CollectorService:

    def __init__(self, music_cataloger):
        self.music_cataloger = music_cataloger
        self.review_store = ReviewStore(FileAdapter('reviews'))
        self.release_store = ReleaseStore(FileAdapter('releases'), self.review_store)
        self.artist_store = ArtistStore(FileAdapter('artists'))

    def collect_reviews(self):

        # TODO: the term "collect" is perhaps a bit overloaded. We describe the overall job of the service of going off
        #  to the internet and storing new reviews collecting and we call the controllers that physicaly fetch the data
        #  collectors as well
        self.music_cataloger.collect_reviews(metacritic, publications=METACRITIC_CURATED_PUBLICATIONS)
        self.music_cataloger.collect_reviews(aoty, publications=AOTY_CURATED_PUBLICATIONS)
        artists = self.music_cataloger.catalog_reviews()

        self.artist_store.put(artists)
        self.release_store.put(artists)

    def collect_releases(self):

        # We somehow need to get artist name and album name to pass in
        # We also need an instance of the spotify class
        releases = self.release_store.get()
        enriched_releases = enricher.add_release_dates(releases)
        self.release_store.put(releases)  # We can't pass releases yet! It takes artists
