from src.aggregator.aggregator import MusicAggregator
from src.entities.artist import Artist

from src.common.crypto import calculate_hash
from config import THUMBS_UP_THRESHOLD


class ReviewScoresAggregator(MusicAggregator):

    def aggregate_artists(self, artists):

        scores = {}

        for artist_id, artist in artists.items():
            artist_release_scores = self.__aggregate_artist(artist)
            if artist_release_scores:
                scores.update(artist_release_scores)

        return scores

    def __aggregate_artist(self, artist: Artist):

        artist_id = artist.id
        artist_name = artist.name

        artist_release_scores = {}
        releases = artist.releases
        if not releases:
            return {}

        for release in releases:
            release_name = release.name
            reviews = release.reviews
            review_ids = [review.id for review in reviews]
            if not review_ids:
                continue

            aggregate_score = self.__aggregate_release_score(reviews)

            score_id = calculate_hash(artist_name + release_name)

            artist_release_scores[score_id] = {
                'id': score_id,
                'release_id': release.id,
                'release_name': release_name,
                'artist_id': artist_id,
                'artist_name': artist_name,
                'score': aggregate_score,
                'reviews_counted': len(review_ids)
            }

        return artist_release_scores

    @staticmethod
    def __aggregate_release_score(reviews):

        release_scores = [review.score for review in reviews]
        thumbs_up = [True for score in release_scores if score >= THUMBS_UP_THRESHOLD]
        aggregated_float = (sum(thumbs_up) / len(release_scores)) * 100

        return int(aggregated_float)
