import uuid

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

        # store artists on the collector ?
        self.collector.collect(METACRITIC_PUBLICATIONS_SAMPLE, metacritic)
        self.collector.collect(AOTY_PUBLICATIONS_SAMPLE, aoty)
        reviews = self.collector.deliver()

        for raw_review in reviews:

            review = {
                'id': str(uuid.uuid4()),
                'score': raw_review.get('score'),
                'publication_name': raw_review.get('publication_name'),
                'date': raw_review.get('date'),
                'link': raw_review.get('link')
            }

            artist_name = raw_review.get('artist')
            release_name = raw_review.get('release_name')

            if not self.artists.get(artist_name):
                self.artists[artist_name] = {'id': str(uuid.uuid4())}

            if not self.artists.get(artist_name).get(release_name):
                self.artists[artist_name][release_name] = {
                    'id': str(uuid.uuid4()),
                    'reviews': []
                }

            self.artists[artist_name][release_name]['reviews'].append(review)

    def store_collection(self):

        #TODO nest child ids under parent and not other way round
        preexisting_artists = self.artist_store.put(self.artists)

        if preexisting_artists:
            for existing_artist in preexisting_artists:
                for artist in self.artists:
                    if existing_artist['name'] == artist['name']:
                        artist['id'] = existing_artist['id']

        release_bundle = []
        for artist in self.artists:
            releases = artist['releases']
            for release in releases:
                release['artist'] = artist['id']
                release_bundle.append(release)

        preexisting_releases = self.release_store.put(release_bundle)

        if preexisting_releases:
            for preexisting_release in preexisting_releases:
                for release in release_bundle:
                    if preexisting_release['title'] == release['title']:
                        release['id'] = preexisting_release

        review_bundle = []
        for release in release_bundle:
            reviews = release['reviews']
            for review in reviews:
                review['release'] = release['id']
                review_bundle.append(review)

        self.review_store.put(review_bundle)
