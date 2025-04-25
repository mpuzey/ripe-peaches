import unittest

from src.entities.artist import Artist
from src.entities.release import Release
from src.entities.review import Review
from src.collector.use_cases.merge import merge_artist_dicts, merge_releases
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
            .reset() \
            .add_artist('artist_id_456', 'YOB') \
            .add_release('release_id_123', 'Clearing The Path') \
            .add_review('review_id_123', 'pitchfork', 80, 'Posted Feb 12, 2021') \
            .add_release('release_id_456', 'Atma') \
            .add_review('review_id_456', 'pitchfork', 80, 'Posted Feb 13, 2021') \
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
    
    def test__merge_releases__WillPreserveEnrichmentData__WhenMergingReleasesWithSameID(self):
        """Test that enrichment data like dates are preserved when merging releases"""
        # Create a release with enrichment data (date, type, etc.)
        enriched_release = Release(
            id='release_123',
            name='Test Album',
            reviews=[],
            date='2023-05-15',
            type='album',
            total_tracks=12,
            spotify_url='https://spotify.com/album/123'
        )
        
        # Create the same release but without enrichment data (as if from new review)
        new_review = Review(
            id='review_456',
            publication_name='Pitchfork',
            score=85,
            date='2023-05-20',
            link='https://pitchfork.com/reviews/123'
        )
        
        unenriched_release = Release(
            id='release_123',
            name='Test Album',
            reviews=[new_review],
            date=None,
            type=None,
            total_tracks=None,
            spotify_url=None
        )
        
        # Merge the releases
        merged_releases = merge_releases([enriched_release], [unenriched_release])
        
        # Check that enrichment data was preserved
        self.assertEqual(len(merged_releases), 1)
        self.assertEqual(merged_releases[0].id, 'release_123')
        self.assertEqual(merged_releases[0].date, '2023-05-15')  # Original date preserved
        self.assertEqual(merged_releases[0].type, 'album')  # Original type preserved
        self.assertEqual(merged_releases[0].total_tracks, 12)  # Original tracks preserved
        self.assertEqual(merged_releases[0].spotify_url, 'https://spotify.com/album/123')  # Original URL preserved
        self.assertEqual(len(merged_releases[0].reviews), 1)  # New review was added
    
    def test__merge_releases__WillUpdateMissingEnrichmentData__WhenNewReleaseHasIt(self):
        """Test that missing enrichment data is updated when new release has it"""
        # Create a release without enrichment data
        unenriched_release = Release(
            id='release_123',
            name='Test Album',
            reviews=[],
            date=None,
            type=None,
            total_tracks=None,
            spotify_url=None
        )
        
        # Create the same release but with enrichment data
        enriched_release = Release(
            id='release_123',
            name='Test Album',
            reviews=[],
            date='2023-05-15',
            type='album',
            total_tracks=12,
            spotify_url='https://spotify.com/album/123'
        )
        
        # Merge the releases
        merged_releases = merge_releases([unenriched_release], [enriched_release])
        
        # Check that enrichment data was added
        self.assertEqual(len(merged_releases), 1)
        self.assertEqual(merged_releases[0].id, 'release_123')
        self.assertEqual(merged_releases[0].date, '2023-05-15')
        self.assertEqual(merged_releases[0].type, 'album')
        self.assertEqual(merged_releases[0].total_tracks, 12)
        self.assertEqual(merged_releases[0].spotify_url, 'https://spotify.com/album/123')
    
    def test__merge_releases__WillNotAddDuplicateReleases__WhenMergingReleasesWithSameID(self):
        """Test that duplicate releases are not added when merging"""
        # Create two identical releases
        release1 = Release(
            id='release_123',
            name='Test Album',
            reviews=[],
            date='2023-05-15',
            type='album',
            total_tracks=12,
            spotify_url='https://spotify.com/album/123'
        )
        
        release2 = Release(
            id='release_123',
            name='Test Album',
            reviews=[],
            date='2023-05-15',
            type='album',
            total_tracks=12,
            spotify_url='https://spotify.com/album/123'
        )
        
        # Merge the releases
        merged_releases = merge_releases([release1], [release2])
        
        # Check that there's only one release in the result
        self.assertEqual(len(merged_releases), 1)
        self.assertEqual(merged_releases[0].id, 'release_123')
    
    def test__merge_releases__WillAddNewReleases__WhenMergingReleasesWithDifferentIDs(self):
        """Test that new releases are added when merging"""
        # Create two different releases
        release1 = Release(
            id='release_123',
            name='Test Album 1',
            reviews=[],
            date='2023-05-15',
            type='album',
            total_tracks=12,
            spotify_url='https://spotify.com/album/123'
        )
        
        release2 = Release(
            id='release_456',
            name='Test Album 2',
            reviews=[],
            date='2023-06-20',
            type='album',
            total_tracks=10,
            spotify_url='https://spotify.com/album/456'
        )
        
        # Merge the releases
        merged_releases = merge_releases([release1], [release2])
        
        # Check that both releases are in the result
        self.assertEqual(len(merged_releases), 2)
        release_ids = [r.id for r in merged_releases]
        self.assertIn('release_123', release_ids)
        self.assertIn('release_456', release_ids)
    
    def test__merge_releases__WillCombineReviews__WhenMergingReleasesWithSameID(self):
        """Test that reviews are combined when merging releases with the same ID"""
        review1 = Review(
            id='review_123',
            publication_name='Pitchfork',
            score=85,
            date='2023-05-20',
            link='https://pitchfork.com/reviews/123'
        )
        
        review2 = Review(
            id='review_456',
            publication_name='NME',
            score=90,
            date='2023-05-25',
            link='https://nme.com/reviews/456'
        )
        
        release1 = Release(
            id='release_123',
            name='Test Album',
            reviews=[review1],
            date='2023-05-15',
            type='album',
            total_tracks=12,
            spotify_url='https://spotify.com/album/123'
        )
        
        release2 = Release(
            id='release_123',
            name='Test Album',
            reviews=[review2],
            date='2023-05-15',
            type='album',
            total_tracks=12,
            spotify_url='https://spotify.com/album/123'
        )
        
        # Merge the releases
        merged_releases = merge_releases([release1], [release2])
        
        # Check that both reviews are in the result
        self.assertEqual(len(merged_releases), 1)
        self.assertEqual(len(merged_releases[0].reviews), 2)
        review_ids = [r.id for r in merged_releases[0].reviews]
        self.assertIn('review_123', review_ids)
        self.assertIn('review_456', review_ids)
    
    def test__merge_releases__WillNotDuplicateReviews__WhenMergingReleasesWithSameReviews(self):
        """Test that reviews are not duplicated when merging releases with the same reviews"""
        review = Review(
            id='review_123',
            publication_name='Pitchfork',
            score=85,
            date='2023-05-20',
            link='https://pitchfork.com/reviews/123'
        )
        
        release1 = Release(
            id='release_123',
            name='Test Album',
            reviews=[review],
            date='2023-05-15',
            type='album',
            total_tracks=12,
            spotify_url='https://spotify.com/album/123'
        )
        
        release2 = Release(
            id='release_123',
            name='Test Album',
            reviews=[review],
            date='2023-05-15',
            type='album',
            total_tracks=12,
            spotify_url='https://spotify.com/album/123'
        )
        
        # Merge the releases
        merged_releases = merge_releases([release1], [release2])
        
        # Check that there's only one review in the result
        self.assertEqual(len(merged_releases), 1)
        self.assertEqual(len(merged_releases[0].reviews), 1)
        self.assertEqual(merged_releases[0].reviews[0].id, 'review_123')
