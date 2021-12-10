import unittest

from mock import call

from tests.api_tests import in_memory_test_data
from tests.api_tests import store_time_test_data
from tests.api_tests.api.collector_service import collect_reviews


class TestService(unittest.TestCase):

    def test__service__CollectorService__collect_reviews__WillStoreArtistsReleasesAndReviews__WhenCalled(self):

        mock_file_adapter = collect_reviews(in_memory_test_data.get_publication_reviews(),
                                            in_memory_test_data.get_enriched_releases())

        calls = [call(store_time_test_data.get_artists()),
                 call(store_time_test_data.get_releases()),
                 call(store_time_test_data.get_reviews())]

        mock_file_adapter_instance = mock_file_adapter.return_value
        mock_file_adapter_instance.put.assert_has_calls(calls)
