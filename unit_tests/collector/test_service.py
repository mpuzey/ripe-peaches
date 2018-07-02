from mock import MagicMock, call, patch
import unittest
from collector.service import CollectorService
from constants import METACRITIC_PUBLICATIONS_SAMPLE, AOTY_PUBLICATIONS_SAMPLE


class TestService(unittest.TestCase):

    @patch('collector.service.ReviewStore')
    @patch('collector.service.aoty')
    @patch('collector.service.metacritic')
    def test__service__CollectorService__start__WillCallScraperCollect__WhenCalled(self, mock_metacritic, mock_aoty, _):

        mock_collector = MagicMock()
        collector_instance = mock_collector.return_value
        collector_service = CollectorService(collector_instance)
        collector_service.start()

        calls = [call(METACRITIC_PUBLICATIONS_SAMPLE, mock_metacritic),
                 call(AOTY_PUBLICATIONS_SAMPLE, mock_aoty)]

        collector_instance.collect.assert_has_calls(calls)

    @patch('collector.service.ReviewStore')
    @patch('collector.service.aoty')
    @patch('collector.service.metacritic')
    def test__service__CollectorService__start__WillStoreReviews__WhenCalled(self, mock_metacritic, mock_aoty, mock_review_store):


        mock_collector = MagicMock()
        collector_instance = mock_collector.return_value

        mock_review_store_instance = mock_review_store.return_value

        collector_instance.collect.side_effect = [{'some_data': 'scooby'}], [{'some_data': 'doo'}]

        collector_service = CollectorService(collector_instance)
        collector_service.start()

        mock_review_store_instance.put.assert_called_with([{'some_data': 'scooby'}, {'some_data': 'doo'}])
