import unittest

from src.collector.entities.artist import Artist
from src.collector.entities.release import Release
from src.collector.entities.review import Review
from src.collector.use_cases.merge import merge_artist_dicts


class TestMergeArtistDicts(unittest.TestCase):

    def test__merge_artist_dicts__WillAddArtistReleaseAndReviewToArchive_WhenArtistNotSeenBefore(self):
        archived_artists = {
            '8ba02ddc3c2b1c1887a7788f490e940f589bd600eed30734eefa29ec5c2b1440': Artist(
                id='8ba02ddc3c2b1c1887a7788f490e940f589bd600eed30734eefa29ec5c2b1440',
                name='Deafheaven',
                releases=[]
            )
        }

        recently_review_artists = {
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
                                score=80,
                                date='',
                                link='')
                        ],
                        date=None,
                        type=None,
                        total_tracks=None,
                        spotify_url=None),
                ]
            )
        }

        expected_artists = {
            '8ba02ddc3c2b1c1887a7788f490e940f589bd600eed30734eefa29ec5c2b1440': Artist(
                id='8ba02ddc3c2b1c1887a7788f490e940f589bd600eed30734eefa29ec5c2b1440',
                name='Deafheaven',
                releases=[]
            ),
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
                                score=80,
                                date='',
                                link='')
                        ],
                        date=None,
                        type=None,
                        total_tracks=None,
                        spotify_url=None),
                ]
            )
        }

        actual_artists = merge_artist_dicts(archived_artists, recently_review_artists)

        assert actual_artists == expected_artists

    def test__merge_artist_dicts__WillAddArtistMultipleReleasesAndReviewToArchive_WhenArtistNotSeenBefore(self):
        pass

    def test__merge_artist_dicts__WillAddArtistReleaseAndMultipleReviewsToArchive_WhenArtistNotSeenBefore(self):
        pass

    def test__merge_artist_dicts__WillAddReleaseAndReviewToArchive_WhenReleaseNotSeenBefore(self):
        archived_artists = {
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
                                score=80,
                                date='',
                                link='')
                        ],
                        date=None,
                        type=None,
                        total_tracks=None,
                        spotify_url=None),
                ]
            )

        }

        recently_review_artists = {
            'd92a4901abc2f02dfd347e0793ca3f1c223cbff321d30cdef2679ed13b1c58ae': Artist(
                id='d92a4901abc2f02dfd347e0793ca3f1c223cbff321d30cdef2679ed13b1c58ae',
                name='YOB',
                releases=[
                    Release(
                        id='1',
                        name='Atma',
                        reviews=[
                            Review(
                                id=1,
                                publication_name='pitchfork',
                                score=85,
                                date='',
                                link=''
                            )
                        ],
                    date=None,
                    type=None,
                    total_tracks=None,
                    spotify_url=None)
                ]
            )
        }

        expected_artists = {
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
                                score=80,
                                date='',
                                link='')
                        ],
                        date=None,
                        type=None,
                        total_tracks=None,
                        spotify_url=None),
                    Release(
                        id='1',
                        name='Atma',
                        reviews=[
                            Review(
                                id=1,
                                publication_name='pitchfork',
                                score=85,
                                date='',
                                link=''
                            )
                        ],
                        date=None,
                        type=None,
                        total_tracks=None,
                        spotify_url=None)
                ]
            )
        }

        actual_artists = merge_artist_dicts(archived_artists, recently_review_artists)

        assert actual_artists == expected_artists

    def test__merge_artist_dicts__WillAddReviewToArchive_WhenReviewNotSeenBefore(self):
        archived_artists = {
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
                                score=80,
                                date='',
                                link='')
                        ],
                        date=None,
                        type=None,
                        total_tracks=None,
                        spotify_url=None),
                ]
            )

        }

        recently_review_artists = {
            'd92a4901abc2f02dfd347e0793ca3f1c223cbff321d30cdef2679ed13b1c58ae': Artist(
                id='d92a4901abc2f02dfd347e0793ca3f1c223cbff321d30cdef2679ed13b1c58ae',
                name='YOB',
                releases=[
                    Release(
                        id='137801a1514b811c49b2d27183e4b6fd8b7371d76cc4ff177c0a70d9700e196c',
                        name='Clearing The Path',
                        reviews=[
                            Review(
                                id=1,
                                publication_name='the needledrop',
                                score=70,
                                date='',
                                link=''
                            )
                        ],
                        date=None,
                        type=None,
                        total_tracks=None,
                        spotify_url=None)
                ]
            )
        }

        expected_artists = {
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
                                score=80,
                                date='',
                                link=''),
                            Review(
                                id=1,
                                publication_name='the needledrop',
                                score=70,
                                date='',
                                link=''
                            )
                        ],
                        date=None,
                        type=None,
                        total_tracks=None,
                        spotify_url=None)
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
