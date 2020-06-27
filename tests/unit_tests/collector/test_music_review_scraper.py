import unittest

from mock import MagicMock
from src.collector.entities.artist import Artist
from src.collector.entities.review import Review
from src.collector.entities.release import Release

from src.collector.controllers.music_review_collector import MusicReviewCollector
from src.collector.use_cases.music_review_cataloger import MusicReviewCataloger


class TestScraper(unittest.TestCase):

    def test__scraper__MusicReviewScraper__collect__WillBuildUpAListOfCuratedReviewsOnInstance__WhenCalledTwice(self):
        mock_metacritic = MagicMock()
        mock_metacritic.get_reviews.return_value = [
            {
                'release_name': 'Clearing The Path',
                'artist': 'YOB',
                'publication_name': 'pitchfork'
            }
        ]

        mock_aoty = MagicMock()
        mock_aoty.get_reviews.return_value = [
            {
                'release_name': 'Clearing The Path',
                'artist': 'YOB',
                'publication_name': 'melon'
            }
        ]

        cataloger = MusicReviewCataloger()
        scraper = MusicReviewCollector(cataloger)
        scraper.collect(mock_metacritic, publications=['pitchfork'])
        scraper.collect(mock_aoty, publications=['melon'])

        publication_reviews = scraper.catalog()
        expected_reviews = {
            'd92a4901abc2f02dfd347e0793ca3f1c223cbff321d30cdef2679ed13b1c58ae': Artist(
                id='d92a4901abc2f02dfd347e0793ca3f1c223cbff321d30cdef2679ed13b1c58ae',
                name='YOB',
                releases=[
                    Release(
                        id='137801a1514b811c49b2d27183e4b6fd8b7371d76cc4ff177c0a70d9700e196c',
                        name='Clearing The Path',
                        reviews=[
                            Review(
                                id='af9896e8834f324e2ad0aa281985cc9b13534ec3b2b81414f05df508ef0f2f0b',
                                publication_name='pitchfork',
                                score=None,
                                date=None,
                                link=None),
                            Review(
                                id='f36c160e4def4615f4ab216fa3a3f68bb98b29e649be9804a41e6199e9985f48',
                                publication_name='melon',
                                score=None,
                                date=None,
                                link=None)
                        ],
                        date=None,
                        type=None,
                        total_tracks=None,
                        spotify_url=None),
                ]
            )
        }

        self.assertEqual(expected_reviews, publication_reviews)
