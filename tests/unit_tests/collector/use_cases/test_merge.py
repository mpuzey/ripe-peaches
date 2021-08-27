import unittest

from src.collector.entities.artist import Artist
from src.collector.entities.release import Release
from src.collector.entities.review import Review
from src.collector.use_cases.merge import merge_artist_dicts
from tests.unit_tests.collector.use_cases.test_merge_helper import ArtistDictionaryBuilder


class TestMergeArtistDicts(unittest.TestCase):

    # TODO: does this test really prove anything test__merge_artist_dicts__WillAddArtistMultipleReleasesAndReviewToArchive_WhenArtistNotSeenBefore doesn't prove?
    def test__merge_artist_dicts__WillAddArtistReleaseAndReviewToArchive_WhenArtistNotSeenBefore(self):

        artist_dict_builder = ArtistDictionaryBuilder()
        # TODO: should the builder set some existing state up?
        archived_artists = artist_dict_builder.add_artist('artist_id_123', 'Deafheaven').artist_dict()

        recently_reviewed_artists = artist_dict_builder\
            .reset()\
            .add_artist('artist_id_456', 'YOB')\
            .add_release('release_id_123', 'Clearing The Path')\
            .add_review('review_id_123', 'pitchfork', 80, 'Posted Feb 12, 2021')\
            .artist_dict()

        expected_artists = artist_dict_builder.add_artist('artist_id_123', 'Deafheaven').artist_dict()

        actual_artists = merge_artist_dicts(archived_artists, recently_reviewed_artists)

        # TODO need to compare dicts properly
        assert actual_artists == expected_artists

    def test__merge_artist_dicts__WillAddArtistMultipleReleasesAndReviewToArchive_WhenArtistNotSeenBefore(self):

        artist_dict_builder = ArtistDictionaryBuilder()
        archived_artists = artist_dict_builder.add_artist('artist_id_123', 'Deafheaven').artist_dict()

        recently_reviewed_artists = artist_dict_builder \
            .reset() \
            .add_artist('artist_id_456', 'YOB') \
            .add_release('release_id_123', 'Clearing The Path') \
            .add_review('review_id_123', 'pitchfork', 80, 'Posted Feb 12, 2021') \
            .add_release('release_id_456', 'Atma') \
            .add_review('review_id_456', 'pitchfork', 80, 'Posted Feb 13, 2021') \
            .artist_dict()

        expected_artists = artist_dict_builder.add_artist('artist_id_123', 'Deafheaven').artist_dict()

        actual_artists = merge_artist_dicts(archived_artists, recently_reviewed_artists)

        # TODO need to compare dicts properly
        assert actual_artists == expected_artists

    def test__merge_artist_dicts__WillAddArtistReleaseAndMultipleReviewsToArchive_WhenArtistNotSeenBefore(self):
        pass

    def test__merge_artist_dicts__WillAddReleaseAndReviewToArchive_WhenReleaseNotSeenBefore(self):

        artist_dict_builder = ArtistDictionaryBuilder()
        archived_artists = artist_dict_builder \
            .add_artist('artist_id_456', 'YOB') \
            .add_release('release_id_123', 'Clearing The Path') \
            .add_review('review_id_123', 'pitchfork', 80, 'Posted Feb 12, 2021') \
            .artist_dict()

        recently_reviewed_artists = artist_dict_builder \
            .reset() \
            .add_artist('artist_id_456', 'YOB') \
            .add_release('release_id_456', 'Atma') \
            .add_review('review_id_456', 'pitchfork', 80, 'Posted Feb 13, 2021') \
            .artist_dict()

        expected_artists = artist_dict_builder \
            .add_release('release_id_123', 'Clearing The Path') \
            .add_review('review_id_123', 'pitchfork', 80, 'Posted Feb 12, 2021') \
            .artist_dict()

        actual_artists = merge_artist_dicts(archived_artists, recently_reviewed_artists)

        # TODO need to compare dicts properly
        assert actual_artists == expected_artists

    def test__merge_artist_dicts__WillAddReviewToArchive_WhenReviewNotSeenBefore(self):

        artist_dict_builder = ArtistDictionaryBuilder()
        archived_artists = artist_dict_builder \
            .add_artist('artist_id_456', 'YOB') \
            .add_release('release_id_123', 'Clearing The Path') \
            .add_review('review_id_123', 'pitchfork', 80, 'Posted Feb 12, 2021') \
            .artist_dict()

        recently_reviewed_artists = artist_dict_builder \
            .reset() \
            .add_artist('artist_id_456', 'YOB') \
            .add_release('release_id_123', 'Clearing The Path') \
            .add_review('review_id_456', 'the needledrop', 80, 'Posted Feb 13, 2021') \
            .artist_dict()

        builder = artist_dict_builder.add_review('review_id_123', 'pitchfork', 80, 'Posted Feb 12, 2021')
        expected_artists = builder.artist_dict()
        # TODO expected releases is empty here

        actual_artists = merge_artist_dicts(archived_artists, recently_reviewed_artists)

        # TODO need to compare dicts properly
        assert actual_artists == expected_artists

    def test__merge_artists_dicts__WillNotAddArtist__WhenSeenBefore(self):
        pass

    def test__merge_artists_dicts__WillNotAddRelease__WhenSeenBefore(self):
        pass

    def test__merge_artists_dicts__WillNotAddReview__WhenSeenBefore(self):
        pass
