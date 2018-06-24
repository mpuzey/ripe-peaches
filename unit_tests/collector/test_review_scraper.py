from mock import MagicMock
import unittest
from collector.review_scraper import ReviewScraper


class TestScraper(unittest.TestCase):

    def test__scraper__ReviewScraper__collect__WillReturnReviewsForEachPublicationInCuratedPublications__WhenCalled(self):
        mock_metacritic = MagicMock()
        mock_metacritic.get.side_effect = [[{'release_name': '1'}], [{'release_name': '2'}]]

        scraper = ReviewScraper()
        reviews = scraper.collect(['publication1', 'publication2'], mock_metacritic)

        self.assertEqual(reviews, [{'release_name': '1'}, {'release_name': '2'}])
