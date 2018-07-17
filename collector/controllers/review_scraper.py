from collector.entities.collector import Collector
from common.crypto import calculate_hash


class ReviewScraper(Collector):

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
                 'name': release_name,
                 'reviews': {}
                }

            self.artists[artist_id]['releases'][release_id]['reviews'][review_id] = review

        return self.artists
