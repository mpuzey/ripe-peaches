import unittest

import tornado.web
from src.app.web.reviews_handler import ReviewsHandler
from mock import patch

from constants import PUBLIC_ROOT
from main import make_app
from src.app.web.scores_handler import ScoresHandler


class TestMain(unittest.TestCase):

    @patch('main.AggregatorService')
    @patch('main.CollectorService')
    @patch('main.ScoreStore')
    @patch('main.ReviewStore')
    @patch('main.tornado.web.Application')
    def test__main__make_app__WillInjectStoreIntoReviewsHandler__WhenCalled(self, mock_app, mock_review_store, mock_score_store, _, __):

        review_store_instance = mock_review_store.return_value
        score_store_instance = mock_score_store.return_value

        expected_arg = [
            (r'/', ScoresHandler, {'store': score_store_instance}),
            (r'/public/(.*)', tornado.web.StaticFileHandler, {'path': PUBLIC_ROOT}),
            ('/reviews', ReviewsHandler, {'store': review_store_instance})]

        make_app()

        mock_app.assert_called_with(expected_arg)

    @patch('main.MusicCataloger')
    @patch('main.start_aggregator_service')
    @patch('main.ReviewStore')
    @patch('main.tornado.web.Application')
    def \
            test__main__make_app__WillStartCataloger__WhenCalled(self, _, __, ___, mock_collector):

        make_app()
        collector_instance = mock_collector.return_value
        assert collector_instance.collect_reviews.called
        assert collector_instance.collect_releases.called

    @patch('main.AggregatorService')
    @patch('main.start_collector_service')
    @patch('main.ReviewStore')
    @patch('main.tornado.web.Application')
    def test__main__make_app__WillStartAggregatorService__WhenCalled(self, _, __, ___, mock_aggregator):

        make_app()
        aggregator_instance = mock_aggregator.return_value
        assert aggregator_instance.start.called

