from src.collector.use_cases.music_parser import MusicParser

from src.common.crypto import calculate_hash


class MusicReviewParser(MusicParser):

    def __init__(self):
        super().__init__()
        self.artists = {}

    def parse(self, data):
        for raw_review in data:

            artist_id = super().build_artist(raw_review)

            release_id = self._build_release(artist_id, raw_review)

            self._build_review(raw_review, artist_id, release_id)

        return self.artists

    def _build_release(self, artist_id, raw_review):

        artist_name = raw_review.get('artist')
        release_name = self._format_release_name(raw_review.get('release_name'))

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
        release_name = self._format_release_name(raw_review.get('release_name'))
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

    @staticmethod
    def _format_release_name(name):

        formatted_name = name.replace('and', '&').title()

        return formatted_name
