import unittest

from src.collector.entities.artist import Artist
from src.collector.entities.release import Release
from src.collector.entities.review import Review
from src.collector.use_cases.merge import merge_artist_dicts


class TestMergeArtistDicts(unittest.TestCase):

    def test__merge_artist_dicts__WillAddArtistReleaseAndReviewToArchive_WhenArtistNotSeenBefore(self):
        archived_artists = {
            'artist_id_123': Artist(
                id='artist_id_123',
                name='Deafheaven',
                releases=[]
            )
        }

        recently_review_artists = {
            'artist_id_456': Artist(
                id='artist_id_456',
                name='YOB',
                releases=[
                    Release(
                        id='release_id_123',
                        name='Clearing The Path',
                        reviews=[
                            Review(
                                id='review_id_123',
                                publication_name='pitchfork',
                                score=80,
                                date='',
                                link='')
                        ]
                    ),
                ]
            )
        }

        expected_artists = {
            'artist_id_123': Artist(
                id='artist_id_123',
                name='Deafheaven',
                releases=[]
            ),
            'artist_id_456': Artist(
                id='artist_id_456',
                name='YOB',
                releases=[
                    Release(
                        id='release_id_123',
                        name='Clearing The Path',
                        reviews=[
                            Review(
                                id='review_id_123',
                                publication_name='pitchfork',
                                score=80,
                                date='',
                                link='')
                        ]
                    ),
                ]
            )
        }

        actual_artists = merge_artist_dicts(archived_artists, recently_review_artists)

        assert actual_artists == expected_artists

    def test__merge_artist_dicts__WillAddArtistMultipleReleasesAndReviewToArchive_WhenArtistNotSeenBefore(self):
        archived_artists = {
            'artist_id_123': Artist(
                id='artist_id_123',
                name='Deafheaven',
                releases=[]
            )
        }

        recently_review_artists = {
            'artist_id_456': Artist(
                id='artist_id_456',
                name='YOB',
                releases=[
                    Release(
                        id='release_id_123',
                        name='Clearing The Path',
                        reviews=[
                            Review(
                                id='review_id_123',
                                publication_name='pitchfork',
                                score=80,
                                date='',
                                link='')
                        ]
                    ),
                    Release(
                        id='release_id_456',
                        name='Atma',
                        reviews=[
                            Review(
                                id='review_id_456',
                                publication_name='pitchfork',
                                score=80,
                                date='',
                                link='')
                        ]
                    )
                ]
            )
        }

        expected_artists = {
            'artist_id_123': Artist(
                id='artist_id_123',
                name='Deafheaven',
                releases=[]
            ),
            'artist_id_456': Artist(
                id='artist_id_456',
                name='YOB',
                releases=[
                    Release(
                        id='release_id_123',
                        name='Clearing The Path',
                        reviews=[
                            Review(
                                id='review_id_123',
                                publication_name='pitchfork',
                                score=80,
                                date='',
                                link='')
                        ]
                    ),
                    Release(
                        id='release_id_456',
                        name='Atma',
                        reviews=[
                            Review(
                                id='review_id_456',
                                publication_name='pitchfork',
                                score=80,
                                date='',
                                link='')
                        ]
                    )
                ]
            )
        }

        actual_artists = merge_artist_dicts(archived_artists, recently_review_artists)

        assert actual_artists == expected_artists

    def test__merge_artist_dicts__WillAddArtistReleaseAndMultipleReviewsToArchive_WhenArtistNotSeenBefore(self):
        pass

    def test__merge_artist_dicts__WillAddReleaseAndReviewToArchive_WhenReleaseNotSeenBefore(self):
        archived_artists = {
            'artist_id_123': Artist(
                id='artist_id_123',
                name='YOB',
                releases=[
                    Release(
                        id='release_id_123',
                        name='Clearing The Path',
                        reviews=[
                            Review(
                                id='review_id_123',
                                publication_name='pitchfork',
                                score=80,
                                date='',
                                link='')
                        ],
                    ),
                ]
            )

        }

        recently_review_artists = {
            'artist_id_123': Artist(
                id='artist_id_123',
                name='YOB',
                releases=[
                    Release(
                        id='release_id_456',
                        name='Atma',
                        reviews=[
                            Review(
                                id='review_id_456',
                                publication_name='pitchfork',
                                score=85,
                                date='',
                                link=''
                            )
                        ],
                    )
                ]
            )
        }

        expected_artists = {
            'artist_id_123': Artist(
                id='artist_id_123',
                name='YOB',
                releases=[
                    Release(
                        id='release_id_123',
                        name='Clearing The Path',
                        reviews=[
                            Review(
                                id='review_id_123',
                                publication_name='pitchfork',
                                score=80,
                                date='',
                                link='')
                        ],
                    ),
                    Release(
                        id='release_id_456',
                        name='Atma',
                        reviews=[
                            Review(
                                id='review_id_456',
                                publication_name='pitchfork',
                                score=85,
                                date='',
                                link=''
                            )
                        ],
                    )
                ]
            )
        }

        actual_artists = merge_artist_dicts(archived_artists, recently_review_artists)

        assert actual_artists == expected_artists

    def test__merge_artist_dicts__WillAddReviewToArchive_WhenReviewNotSeenBefore(self):
        archived_artists = {
            'artist_id_123': Artist(
                id='artist_id_123',
                name='YOB',
                releases=[
                    Release(
                        id='release_id_123',
                        name='Clearing The Path',
                        reviews=[
                            Review(
                                id='review_id_123',
                                publication_name='pitchfork',
                                score=80,
                                date='',
                                link='')
                        ],
                    ),
                ]
            )

        }

        recently_review_artists = {
            'artist_id_123': Artist(
                id='artist_id_123',
                name='YOB',
                releases=[
                    Release(
                        id='release_id_123',
                        name='Clearing The Path',
                        reviews=[
                            Review(
                                id='review_id_456',
                                publication_name='the needledrop',
                                score=70,
                                date='',
                                link=''
                            )
                        ]
                    )
                ]
            )
        }

        expected_artists = {
            'artist_id_123': Artist(
                id='artist_id_123',
                name='YOB',
                releases=[
                    Release(
                        id='release_id_123',
                        name='Clearing The Path',
                        reviews=[
                            Review(
                                id='review_id_123',
                                publication_name='pitchfork',
                                score=80,
                                date='',
                                link=''),
                            Review(
                                id='review_id_456',
                                publication_name='the needledrop',
                                score=70,
                                date='',
                                link=''
                            )
                        ]
                    )
                ]
            )
        }

        actual_artists = merge_artist_dicts(archived_artists, recently_review_artists)

        assert actual_artists == expected_artists

    def test__merge_artists_dicts__WillNotAddArtist__WhenSeenBefore(self):
        pass

    def test__merge_artists_dicts__WillNotAddRelease__WhenSeenBefore(self):
        pass

    def test__merge_artists_dicts__WillNotAddReview__WhenSeenBefore(self):
        pass
