import unittest

from src.collector.controllers.review_scraper import ReviewScraper
from tests.bdd_tests.api.collector_service import service_starts
from tests.bdd_tests.test_data import get_artists_sample, get_review_list


class TestService(unittest.TestCase):

    def test__service__CollectorService__start__WillAddArtistsCatalogToCollector__WhenCalled(self):

        collector_instance = ReviewScraper()
        expected_artists = get_artists_sample()

        service_starts(collector_instance, get_review_list())

        self.assertEqual(collector_instance.artists, expected_artists)

    def test__service__CollectorService__store_collection__WillStoreArtists__WhenCalled(self):

        pass