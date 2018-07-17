from mock import MagicMock, call, patch
import unittest
from collector.service import CollectorService
from tests.service_tests.test_data import get_artists_sample, get_review_list
from constants import METACRITIC_PUBLICATIONS_SAMPLE, AOTY_PUBLICATIONS_SAMPLE


class TestService(unittest.TestCase):

    @patch('collector.service.FileAdapter')
    @patch('collector.service.aoty')
    @patch('collector.service.metacritic')
    def test__service__CollectorService__start__WillCallCollectorCollect__WhenCalled(self, mock_metacritic, mock_aoty, _):

        mock_collector = MagicMock()
        collector_instance = mock_collector.return_value
        collector_service = CollectorService(collector_instance)
        collector_service.start()

        calls = [call(METACRITIC_PUBLICATIONS_SAMPLE, mock_metacritic),
                 call(AOTY_PUBLICATIONS_SAMPLE, mock_aoty)]

        collector_instance.collect.assert_has_calls(calls)

    @patch('collector.service.FileAdapter')
    @patch('collector.service.aoty')
    @patch('collector.service.metacritic')
    def test__service__CollectorService__start__WillAddArtistsCatalogToCollector__WhenCalled(self, mock_metacritic, mock_aoty, _):

        mock_collector = MagicMock()
        collector_instance = mock_collector.return_value
        collector_instance.artists = {}
        collector_instance.deliver.return_value = get_review_list()

        expected_artists = get_artists_sample()

        collector_service = CollectorService(collector_instance)
        collector_service.start()

        self.assertEqual(collector_instance.artists, expected_artists)

    @patch('collector.service.FileAdapter')
    @patch('collector.service.aoty')
    @patch('collector.service.metacritic')
    def test__service__CollectorService__store_collection__WillStoreArtists__WhenCalled(self,
                                                                                        mock_metacritic,
                                                                                        mock_aoty,
                                                                                        _):
        pass