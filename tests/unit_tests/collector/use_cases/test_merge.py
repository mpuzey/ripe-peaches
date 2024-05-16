import unittest

from src.collector.entities.artist import Artist
from src.collector.use_cases.merge import merge_artist_dicts
from tests.unit_tests.collector.use_cases.test_merge_helper import ArtistDictionaryBuilder


class TestMergeArtistDicts(unittest.TestCase):

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

        assert actual_artists == expected_artists

    def test__merge_artist_dicts__WillAddArtistReleaseAndMultipleReviewsToArchive_WhenArtistNotSeenBefore(self):
        artist_dict_builder = ArtistDictionaryBuilder()
        archived_artists = artist_dict_builder.add_artist('artist_id_123', 'Deafheaven').artist_dict()

        recently_reviewed_artists = artist_dict_builder \
            .reset() \
            .add_artist('artist_id_456', 'YOB') \
            .add_release('release_id_123', 'Clearing The Path') \
            .add_review('review_id_123', 'pitchfork', 80, 'Posted Feb 12, 2021') \
            .add_release('release_id_456', 'Clearing The Path') \
            .add_review('review_id_456', '7-popmatters', 85, 'Posted Feb 13, 2021') \
            .artist_dict()

        expected_artists = artist_dict_builder.add_artist('artist_id_123', 'Deafheaven').artist_dict()

        actual_artists = merge_artist_dicts(archived_artists, recently_reviewed_artists)

        assert actual_artists == expected_artists

    def test__merge_artist_dicts__WillAddReleaseAndReviewToArchive_WhenReleaseNotSeenBefore(self):

        artist_dict_builder = ArtistDictionaryBuilder()
        archived_artists = artist_dict_builder \
            .add_artist('artist_id_456', 'YOB') \
            .add_release('release_id_123', 'Clearing The Path') \
            .add_review('review_id_123', 'pitchfork', 80, 'Posted Feb 12, 2021') \
            .artist_dict()

        recently_reviewed = artist_dict_builder \
            .reset() \
            .add_artist('artist_id_456', 'YOB') \
            .add_release('release_id_456', 'Atma') \
            .add_review('review_id_456', 'pitchfork', 80, 'Posted Feb 13, 2021') \
            .artist_dict()

        expected_artists = artist_dict_builder \
            .add_release('release_id_123', 'Clearing The Path') \
            .add_review('review_id_123', 'pitchfork', 80, 'Posted Feb 12, 2021') \
            .artist_dict()

        actual_artists = merge_artist_dicts(archived_artists, recently_reviewed)

        assert actual_artists == expected_artists

    def test__merge_artist_dicts__WillAddReviewToArchive_WhenReviewNotSeenBefore(self):

        artist_dict_builder = ArtistDictionaryBuilder()
        archived_artists_builder = artist_dict_builder \
            .add_artist('artist_id_456', 'YOB') \
            .add_release('release_id_123', 'Clearing The Path') \
            .add_review('review_id_123', 'pitchfork', 80, 'Posted Feb 12, 2021')
        archived_artists = archived_artists_builder.artist_dict()

        recently_reviewed_builder = ArtistDictionaryBuilder() \
            .add_artist('artist_id_456', 'YOB') \
            .add_release('release_id_123', 'Clearing The Path') \
            .add_review('review_id_456', 'the needledrop', 80, 'Posted Feb 13, 2021')
        recently_reviewed_artists = recently_reviewed_builder.artist_dict()

        expected_artists = archived_artists_builder \
            .add_review('review_id_456', 'the needledrop', 80, 'Posted Feb 13, 2021') \
            .artist_dict()

        actual_artists = merge_artist_dicts(archived_artists, recently_reviewed_artists)

        assert actual_artists == expected_artists

    def test__merge_artists_dicts__WillNotAddArtist__WhenSeenBefore(self):
        artist_dict_builder = ArtistDictionaryBuilder()
        archived_artists_builder = artist_dict_builder \
            .add_artist('artist_id_456', 'YOB')
        archived_artists = archived_artists_builder.artist_dict()

        recently_reviewed_builder = ArtistDictionaryBuilder() \
            .add_artist('artist_id_456', 'YOB')
        recently_reviewed_artists = recently_reviewed_builder.artist_dict()

        actual_artists = merge_artist_dicts(archived_artists, recently_reviewed_artists)

        assert actual_artists == archived_artists

    def test__merge_artists_dicts__WillNotAddRelease__WhenSeenBefore(self):
        artist_dict_builder = ArtistDictionaryBuilder()
        archived_artists_builder = artist_dict_builder \
            .add_artist('artist_id_456', 'YOB') \
            .add_release('release_id_123', 'Clearing The Path')
        archived_artists = archived_artists_builder.artist_dict()

        recently_reviewed_builder = ArtistDictionaryBuilder() \
            .add_artist('artist_id_456', 'YOB') \
            .add_release('release_id_123', 'Clearing The Path')
        recently_reviewed_artists = recently_reviewed_builder.artist_dict()

        actual_artists = merge_artist_dicts(archived_artists, recently_reviewed_artists)

        assert actual_artists == archived_artists

    def test__merge_artists_dicts__WillNotAddReview__WhenSeenBefore(self):
        artist_dict_builder = ArtistDictionaryBuilder()
        archived_artists_builder = artist_dict_builder \
            .add_artist('artist_id_456', 'YOB') \
            .add_release('release_id_123', 'Clearing The Path') \
            .add_review('review_id_123', 'pitchfork', 80, 'Posted Feb 12, 2021')
        archived_artists = archived_artists_builder.artist_dict()

        recently_reviewed_builder = ArtistDictionaryBuilder() \
            .add_artist('artist_id_456', 'YOB') \
            .add_release('release_id_123', 'Clearing The Path') \
            .add_review('review_id_123', 'the pitchfork', 80, 'Posted Feb 12, 2021')
        recently_reviewed_artists = recently_reviewed_builder.artist_dict()

        actual_artists = merge_artist_dicts(archived_artists, recently_reviewed_artists)

        assert actual_artists == archived_artists

    def test__merge_artists_dicts__WillHandleTwoReleasesUnderTheSameArtist__WhenNewArtist(self):
        archived_artists = {}

        recently_reviewed_builder = ArtistDictionaryBuilder() \
            .add_artist('artist_id_456', 'Future') \
            .add_release('release_id_123', 'We Don\'T Trust You') \
            .add_review('review_id_123', 'pitchfork', 50, '2024-03-20') \
            .add_release('release_id_456', 'We Still Don\'T Trust You') \
            .add_review('review_id_456', 'the pitchfork', 60, '2024-04-09') \
            .add_review('review_id_456', 'popmatters', 45, '2024-04-09')
        recently_reviewed_artists = recently_reviewed_builder.artist_dict()

        expected_artists = recently_reviewed_artists

        actual_artists = merge_artist_dicts(archived_artists, recently_reviewed_artists)

        assert actual_artists == expected_artists

    def test__merge_artists_dicts__WillHandleTwoReleasesUnderTheSameArtist__WhenArchivedArtist(self):
        artist_dict_builder = ArtistDictionaryBuilder()
        archived_artists = artist_dict_builder.add_artist('artist_id_123', 'Future').artist_dict()

        recently_reviewed_artists = ArtistDictionaryBuilder() \
            .add_artist('artist_id_123', 'Future') \
            .add_release('release_id_123', 'We Don\'T Trust You') \
            .add_review('review_id_123', 'pitchfork', 50, '2024-03-20') \
            .add_release('release_id_456', 'We Still Don\'T Trust You') \
            .add_review('review_id_123', 'the pitchfork', 60, '2024-04-09') \
            .add_review('review_id_456', 'popmatters', 45, '2024-04-09') \
            .artist_dict()

        expected_artists = recently_reviewed_artists

        actual_artists = merge_artist_dicts(archived_artists, recently_reviewed_artists)

        assert actual_artists == expected_artists

    def test__merge_artists_dicts__WillHandleHangingReleaseIDMissingFromReleaseStore__WhenArchivedArtistIncludesReleaseID(self):
        artist_dict_builder = ArtistDictionaryBuilder()

        artist = Artist(id='artist_id_123', name='Future', releases=[None])

        archived_artists = artist_dict_builder.set_artist(artist).artist_dict()

        recently_reviewed_artists = ArtistDictionaryBuilder() \
            .add_artist('artist_id_123', 'Future') \
            .add_release('release_id_123', 'We Don\'T Trust You') \
            .add_review('review_id_123', 'pitchfork', 50, '2024-03-20') \
            .artist_dict()

        expected_artists = recently_reviewed_artists.copy()

        actual_artists = merge_artist_dicts(archived_artists, recently_reviewed_artists)

        assert actual_artists == expected_artists
