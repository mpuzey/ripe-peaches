from collector.web import metacritic, aoty
from constants import METACRITIC_PUBLICATIONS_SAMPLE, AOTY_PUBLICATIONS_SAMPLE
from app.gateways.review_store import ReviewStore
from app.gateways.release_store import ReleaseStore
from app.gateways.artist_store import ArtistStore
from app.db.file_adapter import FileAdapter
from common.crypto import calculate_hash


class CollectorService:

    def __init__(self, collector):
        self.collector = collector
        self.review_store = ReviewStore(FileAdapter('reviews'))
        self.release_store = ReleaseStore(FileAdapter('releases'), self.review_store)
        self.artist_store = ArtistStore(FileAdapter('artists'))

    def start(self):

        self.collector.collect(METACRITIC_PUBLICATIONS_SAMPLE, metacritic)
        self.collector.collect(AOTY_PUBLICATIONS_SAMPLE, aoty)
        reviews = self.collector.deliver()

        for raw_review in reviews:

            publication_name = raw_review.get('publication_name')
            review = {
                'score': raw_review.get('score'),
                'publication_name': publication_name,
                'date': raw_review.get('date'),
                'link': raw_review.get('link')
            }

            artist_name = raw_review.get('artist')
            release_name = raw_review.get('release_name')

            artist_id = calculate_hash(artist_name)
            if not self.collector.artists.get(artist_id):
                self.collector.artists[artist_id] = {
                    'id': artist_id,
                    'name': artist_name,
                    'releases': {}
                }

            release_id = calculate_hash(artist_name + release_name)
            review_id = calculate_hash(artist_name + release_name + publication_name)
            review['id'] = review_id

            existing_release = self.collector.artists.get(artist_id).get('releases').get(release_id)
            if not existing_release:
                self.collector.artists[artist_id]['releases'][release_id] = {
                 'id': calculate_hash(artist_name + release_name),
                 'name': release_name,
                 'reviews': {}
                }

            self.collector.artists[artist_id]['releases'][release_id]['reviews'][review_id] = review

    def store_collection(self):

            self.artist_store.put(self.collector.artists)

            self.release_store.put(self.collector.artists)
