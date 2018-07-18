from mock import patch
import unittest
import tornado.web

from main import make_app
from app.web.reviews_handler import ReviewsHandler
from app.web.scores_handler import ScoresHandler
from constants import PUBLIC_ROOT


class TestMain(unittest.TestCase):

    @patch('main.CollectorService')
    @patch('main.ReviewStore')
    @patch('main.tornado.web.Application')
    def test__main__make_app__WillInjectStoreIntoReviewsHandler__WhenCalled(self, mock_app, mock_store, _):

        store_instance = mock_store.return_value
        expected_arg = [
            (r'/', ScoresHandler),
            (r'/public/(.*)', tornado.web.StaticFileHandler, {'path': PUBLIC_ROOT}),
            ('/reviews', ReviewsHandler, {'store': store_instance})]

        make_app()

        mock_app.assert_called_with(expected_arg)

    @patch('main.CollectorService')
    @patch('main.start_aggregator_service')
    @patch('main.ReviewStore')
    @patch('main.tornado.web.Application')
    def test__main__make_app__WillStartCollector__WhenCalled(self, _, __, ___, mock_collector):

        make_app()
        collector_instance = mock_collector.return_value
        assert collector_instance.start.called

    @patch('main.AggregatorService')
    @patch('main.start_collector_service')
    @patch('main.ReviewStore')
    @patch('main.tornado.web.Application')
    def test__main__make_app__WillStartAggregatorService__WhenCalled(self, _, __, ___, mock_aggregator):

        make_app()
        aggregator_instance = mock_aggregator.return_value
        assert aggregator_instance.start.called

