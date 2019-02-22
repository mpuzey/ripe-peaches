from src.aggregator.entities.data_worker import DataWorker

from src.common.crypto import calculate_hash
from constants import THUMBS_UP_THRESHOLD


class Aggregator(DataWorker):

    def __init__(self):
        self.releases = {}
        self.reviews = {}

    def work(self, aggregation_data):

        (artists, self.releases, self.reviews) = aggregation_data

        scores = {}

        for artist_id, artist in artists.items():
            score = self.__aggregate(artist)
            if score:
                scores.update(score)

        return scores

    def __aggregate(self, artist):

        artist_id = artist.get('id')
        artist_name = artist.get('name')

        score = {}
        releases = artist.get('releases')
        if not releases:
            return {}

        for release_id in releases:
            release = self.releases.get(release_id)
            release_name = release.get('name')
            review_ids = release.get('reviews')
            if not review_ids:
                continue

            aggregate_score = self.__aggregate_release_score(review_ids)

            score_id = calculate_hash(artist_name + release_name)

            score[score_id] = {
                'id': score_id,
                'release_id': release_id,
                'release_name': release_name,
                'artist_id': artist_id,
                'artist_name': artist_name,
                'score': aggregate_score,
                'reviews_counted': len(review_ids)
            }

        return score

    def __aggregate_release_score(self, review_ids):

        release_scores = [self.reviews.get(review_id).get('score') for review_id in review_ids]
        thumbs_up = [True for score in release_scores if score >= THUMBS_UP_THRESHOLD]
        aggregated_float = (sum(thumbs_up) / len(release_scores)) * 100

        return int(aggregated_float)
