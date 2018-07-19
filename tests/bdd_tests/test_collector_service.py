import unittest
from mock import call, patch

from src.collector.controllers.review_scraper import ReviewScraper
from tests.bdd_tests.api.collector_service import service_starts
from tests.bdd_tests import in_memory_test_data
from tests.bdd_tests import store_time_test_data


class TestService(unittest.TestCase):

    def test__service__CollectorService__store_collection__WillStoreArtists__WhenCalled(self):

        collector_instance = ReviewScraper()
        calls = [call(store_time_test_data.get_artists()),
                 call(store_time_test_data.get_releases()),
                 call(store_time_test_data.get_reviews())]

        mock_file_adapter = service_starts(collector_instance, in_memory_test_data.get_reviews())

        mock_file_adapter_instance = mock_file_adapter.return_value
        mock_file_adapter_instance.put.assert_has_calls(calls)

    @patch('src.collector.service.ReleaseStore')
    @patch('src.collector.service.ArtistStore')
    def test__service__CollectorService__start__WillAddArtistsCatalogToCollector__WhenCalled(self,
                                                                                             mock_artist_store,
                                                                                             mock_release_store):

        collector_instance = ReviewScraper()
        expected_artists = in_memory_test_data.get_artists()

        service_starts(collector_instance, in_memory_test_data.get_reviews())

        self.assertEqual(collector_instance.artists, expected_artists)
