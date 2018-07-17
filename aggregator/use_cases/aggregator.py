from aggregator.entities.data_worker import DataWorker
from common.crypto import calculate_hash


class Aggregator(DataWorker):

    def work(self, aggregation_data):

        (artists, releases, reviews) = aggregation_data

        scores = {}

        for key, value in artists.items():
            artist_name = value.get('name')
            release_ids = value.get('releases')
            if release_ids:
                for release_id in release_ids:
                    release = releases.get(release_id)
                    release_name = release.get('name')
                    review_ids = release.get('reviews')
                    if review_ids:
                        release_scores = []
                        for review_id in review_ids:
                            review = reviews.get(review_id)
                            release_scores.append(int(review.get('score')))

                        score_id = calculate_hash(artist_name + release_name)
                        aggregated_score = sum(release_scores) / len(release_scores)

                        scores[score_id] = {
                            'id': score_id,
                            'release_id': release_id,
                            'release_name': release_name,
                            'artist_id': key,
                            'artist_name': artist_name,
                            'score': aggregated_score

                        }

        return scores
