from mock import patch, call
import unittest
from collector.review_scraper import ReviewScraper, CURATED_METACRITIC_PUBLICATIONS


class TestScraper(unittest.TestCase):

    @patch('collector.review_scraper.metacritic')
    def test__scraper__ReviewsScraper__collect__WillGetReviewsForEachPublicationInCuratedMetaCriticPublications__WhenCalled(self, mock_metacritic):

        calls = []

        for publication in CURATED_METACRITIC_PUBLICATIONS:
            calls.append(call(publication))

        scraper = ReviewScraper()
        scraper.collect()

        mock_metacritic.get_reviews.assert_has_calls(calls, any_order=True)

    @patch('collector.review_scraper.metacritic')
    def test__scraper__ReviewsScraper__collect__WillReturnReviewsForEachPublicationInCuratedPublications__WhenCalled(self, mock_metacritic):


        global METACRITIC_PUBLICATIONS
        pubs = METACRITIC_PUBLICATIONS

        METACRITIC_PUBLICATIONS = ['pub1', 'pub2']

        mock_metacritic.get_reviews.side_effect({'release_name': '1'}, {'release_name': '2'})

        scraper = ReviewScraper()
        reviews = scraper.collect()
        self.assertEqual(reviews, [])

        METACRITIC_PUBLICATIONS = pubs