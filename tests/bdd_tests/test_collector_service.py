import unittest

from mock import call

from src.collector.controllers.music_review_collector import MusicReviewCollector
from src.collector.use_cases.music_review_cataloger import MusicReviewCataloger
from src.collector.controllers.music_release_collector import MusicReleaseCollector
from tests.bdd_tests import in_memory_test_data
from tests.bdd_tests import store_time_test_data
from tests.bdd_tests.api.collector_service import collect_reviews, collect_releases


class TestService(unittest.TestCase):

    def test__service__CollectorService__store_reviews__WillStoreArtistsReleasesAndReviews__WhenCalled(self):

        review_collector = MusicReviewCollector(MusicReviewCataloger())

        mock_file_adapter = collect_reviews(review_collector, in_memory_test_data.get_raw_reviews())

        calls = [call(store_time_test_data.get_artists()),
                 call(store_time_test_data.get_releases()),
                 call(store_time_test_data.get_reviews())]

        mock_file_adapter_instance = mock_file_adapter.return_value
        mock_file_adapter_instance.put.assert_has_calls(calls)

    def test__service__CollectorService__store_releases__WillStoreArtistsReleases__WhenCalled(self):
        release_collector = MusicReleaseCollector()

        mock_file_adapter = collect_releases(release_collector, in_memory_test_data.get_raw_releases())

        calls = [call(store_time_test_data.get_spotify_artists()),
                 call(store_time_test_data.get_spotify_releases())]

        mock_file_adapter_instance = mock_file_adapter.return_value
        mock_file_adapter_instance.put.assert_has_calls(calls)
