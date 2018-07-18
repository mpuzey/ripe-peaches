from aggregator.entities.data_worker import DataWorker
from common.crypto import calculate_hash


class Aggregator(DataWorker):

    def work(self, aggregation_data):

        (artists, releases, reviews) = aggregation_data

        scores = {}

        for artist_id, artist in artists.items():
            score = self.__aggregate(artist, releases, reviews)
            scores.update(score)

        return scores

    def __aggregate(self, artist, releases, reviews):

        artist_id = artist.get('id')
        artist_name = artist.get('name')

        score = {}
        for release_id in artist.get('releases'):
            release = releases.get(release_id)
            release_name = release.get('name')

            aggregate_score = self.__aggregate_release_score(release, reviews)

            score_id = calculate_hash(artist_name + release_name)

            score[score_id] = {
                'id': score_id,
                'release_id': release_id,
                'release_name': release_name,
                'artist_id': artist_id,
                'artist_name': artist_name,
                'score': aggregate_score
            }

        return score

    def __aggregate_release_score(self, release, reviews):

        review_ids = release.get('reviews')
        release_scores = [int(reviews.get(review_id).get('score')) for review_id in review_ids]
        aggregated_score = sum(release_scores) / len(release_scores)

        return aggregated_score
