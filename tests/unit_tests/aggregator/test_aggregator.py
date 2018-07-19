import unittest

from src.aggregator.use_cases.aggregator import Aggregator
from tests.unit_tests.aggregator import test_data


class TestAggregator(unittest.TestCase):

    def test__aggregator__Aggregator__work__WillReturnDictOfAggregatedReleaseScores__WhenCalledWithValidAggregationData(self):

        sample_aggregation_data = [
            test_data.get_artist_sample(),
            test_data.get_release_sample(),
            test_data.get_review_sample()
        ]

        expected_aggregated_scores = {
            '0227438fc7af5cd3e37464870b4fce85fae7a4f3ddebe80594b0181db2c31a4f':
                {
                    'id': '0227438fc7af5cd3e37464870b4fce85fae7a4f3ddebe80594b0181db2c31a4f',
                    'release_id': '0227438fc7af5cd3e37464870b4fce85fae7a4f3ddebe80594b0181db2c31a4f',
                    'release_name': "I'll Tell You What!",
                    'artist_id': '6d36d7e180b92eacd41f75ec53c4c4681f965c36db1dc7770e64e0f4e3166ab4',
                    'artist_name': 'Rp Boo',
                    'score': 70.0
                },
            '0c0f12aab588d760168fc6a42fd2ec424c531bc9fe3bb9516559bcb55599b304':
                {
                    'id': '0c0f12aab588d760168fc6a42fd2ec424c531bc9fe3bb9516559bcb55599b304',
                    'release_id': '0c0f12aab588d760168fc6a42fd2ec424c531bc9fe3bb9516559bcb55599b304',
                    'release_name': 'Closer Apart',
                    'artist_id': '7fd24a70ad382f7019780298658cc417995ee63c2b1e0a73c09ce2864e81da16',
                    'artist_name': 'Okzharp',
                    'score': 90.0
                }
        }

        aggregator = Aggregator()
        actual_aggregated_scores = aggregator.work(sample_aggregation_data)

        self.assertEqual(expected_aggregated_scores, actual_aggregated_scores)
