from mock import patch
import unittest
from collector.service import CollectorService


class TestService(unittest.TestCase):

    @patch('collector.service.ReviewStore')
    @patch('collector.service.Scraper')
    def test__service__CollectorService__start__WillCallScraperCollect__WhenCalled(self, mock_scraper, _):

        CollectorService.start()

        scraper_instance = mock_scraper.return_value
        assert scraper_instance.collect.called

    @patch('collector.service.ReviewStore')
    @patch('collector.service.Scraper')
    def test__service__CollectorService__start__WillStoreReviews__WhenCalled(self, mock_scraper, mock_store):

        CollectorService.start()
        scraper_instance = mock_scraper.return_value
        store_instance = mock_store.return_value

        test_data = {'some_data': 'scoob'}
        scraper_instance.collect.return_value = test_data

        store_instance.store_reviews.assert_called_with(test_data)
