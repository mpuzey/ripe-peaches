import unittest

from mock import MagicMock

from src.collector.controllers.review_scraper import ReviewScraper


class TestScraper(unittest.TestCase):

    def test__scraper__ReviewScraper__collect__WillBuildUpAListOfCuratedReviewsOnInstance__WhenCalledTwice(self):
        mock_metacritic = MagicMock()
        mock_metacritic.get_reviews.return_value = [{'release_name': '1'}]

        mock_aoty = MagicMock()
        mock_aoty.get_reviews.return_value = [{'release_name': '2'}]

        scraper = ReviewScraper()
        scraper.collect(['publication1'], mock_metacritic)
        scraper.collect(['publication2'], mock_aoty)

        self.assertEqual(scraper.reviews, [{'release_name': '1'}, {'release_name': '2'}])
