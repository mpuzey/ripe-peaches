from mock import patch
import unittest
from collector.review_scraper import ReviewScraper


class TestScraper(unittest.TestCase):

    @patch('collector.review_scraper.metacritic')
    def test__scraper__ReviewScraper__collect__WillReturnReviewsForEachPublicationInCuratedPublications__WhenCalled(self, mock_metacritic):

        mock_metacritic.get_reviews.side_effect = [[{'release_name': '1'}], [{'release_name': '2'}]]

        scraper = ReviewScraper(['publication1', 'publication2'])
        reviews = scraper.collect()


        self.assertEqual(reviews, [{'release_name': '1'}, {'release_name': '2'}])
