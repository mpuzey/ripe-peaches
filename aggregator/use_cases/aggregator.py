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
                        release_scores = [int(reviews.get(review_id).get('score')) for review_id in review_ids]

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
        '''[e**2 for e in a_list if type(e) == types.IntType]'''
        return scores
