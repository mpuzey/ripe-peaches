import uuid

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

            if not self.artists.get(artist_name):
                self.artists[artist_name] = {'id': calculate_hash(artist_name)}

            if not self.artists.get(artist_name).get(release_name):
                self.artists[artist_name][release_name] = {
                    'id': calculate_hash(artist_name + release_name),
                    'reviews': []
                }

            review['id']: calculate_hash(artist_name + release_name + publication_name)

            self.artists[artist_name][release_name]['reviews'].append(review)

    def store_collection(self):

        artist_documents = {}
        for artist in self.artists:
            release_ids = []
            for release in artist['releases']:
                release_ids.append(release['id'])
            artist['releases'] = release_ids
            artist_documents[artist['id']] = artist

        self.artist_store.put(artist_documents)

        review_documents = {}
        release_documents = {}

        # release store. Release store could use review store to store reviews too.

        for artist in self.artists:
            for release in artist['releases']:
                review_ids = []
                for review in release['reviews']:
                    review_ids.append(review['id'])
                release['reviews'] = review_ids
                release_documents[release['id']] = release

        self.release_store.put(release_documents)
        self.review_store.put(review_documents)
