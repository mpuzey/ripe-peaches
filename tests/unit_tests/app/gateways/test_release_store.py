import unittest
from unittest.mock import MagicMock

from src.app.gateways import release_store
from tests.unit_tests.collector.use_cases.test_merge_helper import ArtistDictionaryBuilder

from deepdiff import DeepDiff


class TestReleaseStore(unittest.TestCase):
    def test__release_store__ReleaseStore__put__WillStoreReleases__WhenValidArtistDictReceived(self):

        mock_file_adapter = MagicMock()
        mock_review_store = MagicMock()
        store = release_store.ReleaseStore(mock_file_adapter, mock_review_store)
        artist_dict_builder = ArtistDictionaryBuilder()
        arist_dict = artist_dict_builder \
            .reset() \
            .add_artist('artist_id_123', 'Future') \
            .add_release('release_id_123', 'We Don\'T Trust You') \
            .add_review('review_id_123', '57-the-needle-drop', 70, '2024-03-20') \
            .add_release('release_id_345', 'We Still Don\'T Trust You') \
            .add_review('review_id_345', '57-the-needle-drop', 30, '2024-03-20') \
            .artist_dict()

        expected_releases = {
            'release_id_123': {
                'date': None,
                'id': 'release_id_123',
                'name': 'We Don\'T Trust You',
                'reviews': ['review_id_123'],
                'spotify_url': None,
                'total_tracks': None,
                'type': None
            },
            'release_id_345': {
                'date': None,
                'id': 'release_id_345',
                'name': 'We Still Don\'T Trust You',
                'reviews': ['review_id_345'],
                'spotify_url': None,
                'total_tracks': None,
                'type': None
            }
        }

        store.put(arist_dict)

        actual_releases = mock_file_adapter.put.call_args.args
        DeepDiff(expected_releases, actual_releases)

    def test__release_store__ReleaseStore__put__WillStoreReviews__WhenSimilarReleasesReceived(self):

        mock_file_adapter = MagicMock()
        mock_review_store = MagicMock()
        store = release_store.ReleaseStore(mock_file_adapter, mock_review_store)
        artist_dict_builder = ArtistDictionaryBuilder()
        arist_dict = artist_dict_builder \
            .reset() \
            .add_artist('artist_id_123', 'Future') \
            .add_release('release_id_123', 'We Don\'T Trust You') \
            .add_review('review_id_123', '57-the-needle-drop', 70, '2024-03-20') \
            .add_release('release_id_345', 'We Still Don\'T Trust You') \
            .add_review('review_id_345', '57-the-needle-drop', 30, '2024-03-20') \
            .artist_dict()

        expected_reviews = {
            'review_id_123':
                {
                    'date': '2024-03-20',
                    'id': 'review_id_123',
                    'link': '',
                    'publication_name': '57-the-needle-drop',
                    'score': 70
                },
            'review_id_345':
                {
                    'date': '2024-03-20',
                    'id': 'review_id_345',
                    'link': '',
                    'publication_name': '57-the-needle-drop',
                    'score': 30
                }
        }

        store.put(arist_dict)

        actual_reviews = mock_review_store.put.call_args.args
        DeepDiff(expected_reviews, actual_reviews)

