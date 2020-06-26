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
                'release_name': '2',
                'artist': 'YOB',
                'publication_name': 'pitchfork'
            }
        ]

        cataloger = MusicReviewCataloger()
        scraper = MusicReviewCollector(cataloger)
        scraper.collect(mock_metacritic, publications=['publication1'])
        scraper.collect(mock_aoty, publications=['publication2'])

        publication_reviews = scraper.catalog()
        expected_reviews = {
            'd92a4901abc2f02dfd347e0793ca3f1c223cbff321d30cdef2679ed13b1c58ae': Artist(
                id='d92a4901abc2f02dfd347e0793ca3f1c223cbff321d30cdef2679ed13b1c58ae',
                name='YOB',
                releases=[
                    Release(
                        id='21560cc14bc7a778ae798a07e973b1164dc3717f2e863f3d9468a803bcb36abb',
                        name='Clearing The Path',
                        reviews=[
                            Review(
                                id='5d53f2cda49001c1663d8b0cae7a7836a841cbfd2f77d2030439ccd5331e3ba8',
                                publication_name='pitchfork',
                                score=None,
                                date=None,
                                link=None)
                    ],
                        date=None,
                        type=None,
                        total_tracks=None,
                        spotify_url=None),
                    Release(
                        id='21560cc14bc7a778ae798a07e973b1164dc3717f2e863f3d9468a803bcb36abb',
                        name='2',
                        reviews=[
                            Review(
                                id='5d53f2cda49001c1663d8b0cae7a7836a841cbfd2f77d2030439ccd5331e3ba8',
                                publication_name='pitchfork',
                                score=None,
                                date=None,
                                link=None)
                    ],
                        date=None,
                        type=None,
                        total_tracks=None,
                        spotify_url=None)
                ]
            )
        }

        self.assertEqual(publication_reviews, expected_reviews)
