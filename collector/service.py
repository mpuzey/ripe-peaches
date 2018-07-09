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
        self.release_store = ReleaseStore(FileAdapter('releases'))
        self.artist_store = ArtistStore(FileAdapter('artists'))
        self.artists = {}

    def start(self):

        # store artists on the collector ?
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
            if not self.artists.get(artist_id):
                self.artists[artist_id] = {
                    'id': artist_id,
                    'name': artist_name,
                    'releases': {}
                }

            release_id = calculate_hash(artist_name + release_name)
            review_id = calculate_hash(artist_name + release_name + publication_name)
            review['id'] = review_id

            existing_release = self.artists.get(artist_id).get('releases').get(release_id)
            if not existing_release:
                self.artists[artist_id]['releases'][release_id] = {
                 'id': calculate_hash(artist_name + release_name),
                 'reviews': {}
                }

            self.artists[artist_id]['releases'][release_id]['reviews'][review_id] = review

    def store_collection(self):

            artist_documents = {}
            for _, artist in self.artists.items():
                release_ids = []
                for _, release in artist['releases'].items():
                    release_ids.append(release['id'])
                artist_document = {}
                artist_document.update(artist)
                artist_document['releases'] = release_ids
                artist_documents[artist_document['id']] = artist_document

            self.artist_store.put(artist_documents)

            review_documents = {}
            release_documents = {}

            # release store. Release store could use review store to store reviews too.

            for _, artist in self.artists.items():
                for release_id, release in artist['releases'].items():
                    review_ids = []
                    for review_id, review in release['reviews'].items():
                        review_ids.append(review_id)
                        review_documents[review_id] = review
                    release['reviews'] = review_ids
                    release_documents[release_id] = release

            self.release_store.put(release_documents)
            self.review_store.put(review_documents)
