from src.collector.entities.collector import Collector

from src.common.crypto import calculate_hash


class MusicReviewScraper(Collector):

    def __init__(self):
        self.reviews = []
        self.artists = {}

    def collect(self, publications, source):

        for publication in publications:
            print('scraping ' + publication)
            publication_reviews = source.get_reviews(publication)
            self.reviews.extend(publication_reviews)

        print('finished scraping!')

    def parse(self):
        for raw_review in self.reviews:

            artist_id = self._build_artist(raw_review)

            release_id = self._build_release(artist_id, raw_review)

            self._build_review(raw_review, artist_id, release_id)

        return self.artists

    def _build_artist(self, raw_review):

        artist_name = raw_review.get('artist')
        id = calculate_hash(artist_name)

        if not self.artists.get(id):
            self.artists[id] = {
                'id': id,
                'name': artist_name,
                'releases': {}
            }

        return id

    def _build_release(self, artist_id, raw_review):

        artist_name = raw_review.get('artist')
        release_name = _format_release_name(raw_review.get('release_name'))

        release_id = calculate_hash(artist_name + release_name)

        existing_release = self.artists.get(artist_id).get('releases').get(release_id)
        if not existing_release:
            self.artists[artist_id]['releases'][release_id] = {
                'id': calculate_hash(artist_name + release_name),
                'name': release_name,
                'reviews': {}
            }

        return release_id

    def _build_review(self, raw_review, artist_id, release_id):

        artist_name = raw_review.get('artist')
        release_name = _format_release_name(raw_review.get('release_name'))
        publication_name = raw_review.get('publication_name')

        review = {
            'score': raw_review.get('score'),
            'publication_name': publication_name,
            'date': raw_review.get('date'),
            'link': raw_review.get('link')
        }

        review_id = calculate_hash(artist_name + release_name + publication_name)
        review['id'] = review_id

        self.artists[artist_id]['releases'][release_id]['reviews'][review_id] = review


def _format_release_name(name):

    formatted_name = name \
        .replace('and', '&') \
        .replace('the', 'The')

    return formatted_name
