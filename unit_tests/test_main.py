from mock import patch
import unittest

from main import make_app
from app.handlers.reviews_handler import ReviewsHandler


class TestMain(unittest.TestCase):

    @patch('main.FileStore')
    @patch('main.tornado.web.Application')
    def test__main__make_app__WillInjectAFileStoreIntoReviewsHandler__WhenCalled(self, mock_app, mock_store):

        store_instance = mock_store.return_value
        expected_args = [('/reviews', ReviewsHandler, {'store': store_instance})]

        make_app()

        mock_app.assert_called_with(expected_args)
