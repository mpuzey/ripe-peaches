from mock import MagicMock
import unittest
from collector.review_scraper import ReviewScraper


class TestScraper(unittest.TestCase):

    def test__scraper__ReviewScraper__collect__WillAddAListOfReviewsToInstanceContainingReviewsForEachPublicationInCuratedPublications__WhenCalledWithPublicationSources(self):
        mock_metacritic = MagicMock()
        mock_metacritic.get.side_effect = [[{'release_name': '1'}]]

        mock_aoty = MagicMock()
        mock_aoty.get.side_effect = [[{'release_name': '2'}]]

        scraper = ReviewScraper()
        scraper.collect(['publication1'], mock_metacritic)
        scraper.collect(['publication2'], mock_aoty)

        self.assertEqual(scraper.reviews, [{'release_name': '1'}, {'release_name': '2'}])
