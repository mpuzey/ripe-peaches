from collector.web import metacritic, aoty
from constants import METACRITIC_PUBLICATIONS_SAMPLE, AOTY_PUBLICATIONS_SAMPLE
from app.gateways.review_store import ReviewStore
from app.gateways.release_store import ReleaseStore
from app.gateways.artist_store import ArtistStore
from app.db.file_adapter import FileAdapter


class CollectorService:

    def __init__(self, collector):
        self.collector = collector
        self.review_store = ReviewStore(FileAdapter('reviews'))
        self.release_store = ReleaseStore(FileAdapter('releases'))
        self.artist_store = ArtistStore(FileAdapter('artists'))
        self.artists = {}

    def start(self):

        self.collector.collect(METACRITIC_PUBLICATIONS_SAMPLE, metacritic)
        self.collector.collect(AOTY_PUBLICATIONS_SAMPLE, aoty)
        reviews = self.collector.deliver()

        for raw_review in reviews:

            review = {
                'score': raw_review.get('score'),
                'publication_name': raw_review.get('publication_name'),
                'date': raw_review.get('date'),
                'link': raw_review.get('link')
            }

            artist_name = raw_review.get('artist')
            release_name = raw_review.get('release_name')

            if not self.artists.get(artist_name):
                self.artists[artist_name] = {}

            if not self.artists.get(artist_name).get(release_name):
                self.artists[artist_name][release_name] = {'reviews': []}

            self.artists[artist_name][release_name]['reviews'].append(review)

    def store_collection(self):
        self.artist_store.put(self.artists)

        # TODO: store documents against ids
        # for artist in self.artists:
        #     releases = artist['releases']
        #     self.release_store.put(releases)
        #
        #     for release in releases:
        #         self.review_store.put(release.get('reviews'))
