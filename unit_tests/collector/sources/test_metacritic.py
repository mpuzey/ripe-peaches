from mock import patch, MagicMock
import unittest
from collector.sources import metacritic
from unit_tests.collector.sources.meta_critic_html import get_reviews_html, get_first_review_html, \
get_review_without_full_review


class TestMetacritic(unittest.TestCase):

    @patch('collector.sources.metacritic.requests')
    def test__metacritic__get_reviews__WillReturnListOfReviews__WhenMetacriticRespondsWithPublicationScreenHTML(self, mock_requests):

        response = MagicMock()
        response.text = get_reviews_html()
        mock_requests.get.return_value = response
        expected_reviews = [
            {
                'artist': 'Yob',
                'date': 'Posted Jun 20, 2018',
                'publication_name': 'The Quietus',
                'release_name': 'Our Raw Heart',
                'score': '80',
                'link': 'http://thequietus.com/articles/24811-yob-our-raw-heart-album-review'
            }
        ]

        actual_reviews = metacritic.get_reviews('the-quietus')

        self.assertEqual(actual_reviews, expected_reviews)

    @patch('collector.sources.metacritic.requests')
    def test__metacritic__get_reviews__WillIncludeFirstReview_WhenMetacriticHTMLIncludesFirstReviewHTMLClass(self, mock_requests):

        response = MagicMock()
        response.text = get_first_review_html()
        mock_requests.get.return_value = response
        expected_reviews = [
            {
                'artist': 'Pusha T',
                'date': 'Posted Jun 21, 2018',
                'publication_name': 'The Quietus',
                'release_name': 'DAYTONA',
                'score': '80',
                'link': 'http://thequietus.com/articles/24834-pusha-t-daytona-album-review'
            }
        ]

        actual_reviews = metacritic.get_reviews('the-quietus')

        self.assertEqual(actual_reviews, expected_reviews)

    @patch('collector.sources.metacritic.requests')
    def test__metacritic__get_reviews__WillIncludeFirstReview_WhenMetacriticHTMLIncludesFirstReviewHTMLClass(self, mock_requests):

        response = MagicMock()
        response.text = get_review_without_full_review()
        mock_requests.get.return_value = response
        expected_reviews = [
            {
                'artist': 'Yob',
                'date': 'Posted Jun 20, 2018',
                'publication_name': 'The Quietus',
                'release_name': 'Our Raw Heart',
                'score': '80',
                'link': None
            }
        ]

        actual_reviews = metacritic.get_reviews('the-quietus')

        self.assertEqual(actual_reviews, expected_reviews)
