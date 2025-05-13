"""
The purpose of this module is to provide an API to test the collector service that is easy to use
in discrete tests and allows us to keep changes to tests to a minimum when functionality changes.
Instead where there are major refactors only the test API need change , where there are minor
refactors the tests and API need not. We should only need to add and change tests when there is new
functionality, a bug to fix or a missing scenario to cover.
"""

from mock import patch
import asyncio
from copy import deepcopy

from src.collector.use_cases.enricher import Enricher
from src.collector.web.spotify import Spotify
from src.collector.use_cases.music_catalog import MusicCatalog
from src.collector.use_cases.music_cataloger import MusicCataloger
from src.collector.controllers.music_release_collector import MusicReleaseCollector
from src.collector.service import CollectorService
from unittest.mock import MagicMock, AsyncMock
from src.entities.external_release import ExternalRelease
from src.entities.artist import Artist
from src.entities.release import Release
from src.entities.review import Review

from tests.api_tests import store_time_test_data


def collect_reviews(collected_data, enriched_releases):

    music_catalog = MusicCatalog()
    review_collector = MagicMock()
    review_collector.collect_reviews.return_value = collected_data

    release_collector = MusicReleaseCollector()
    music_cataloger = MusicCataloger(music_catalog, review_collector, release_collector)

    # Create a mock for spotify that can handle async calls
    spotify = MagicMock()
    
    # Mock the enrichment source that gets created when Enricher calls spotify(session)
    enrichment_source = AsyncMock()
    spotify.return_value = enrichment_source
    
    # Create mock album data to return from get_album
    mock_album_data_yob = {
        'name': 'Our Raw Heart',
        'release_date': '2019-02-15',
        'album_type': 'album',
        'total_tracks': 12,
        'external_urls': {'spotify': 'https://spotify.com'}
    }
    
    mock_album_data_sleep = {
        'name': 'The Sciences',
        'release_date': '2019-01-15',
        'album_type': 'album',
        'total_tracks': 10,
        'external_urls': {'spotify': 'https://spotify.com'}
    }
    
    # Set up get_album to return appropriate album data
    enrichment_source.get_album = AsyncMock(side_effect=[mock_album_data_yob, mock_album_data_sleep])
    
    # Mock the spotify class's get_release_from_album method with AsyncMock
    spotify.get_release_from_album = AsyncMock(side_effect=enriched_releases)
    
    # Create a mock enricher that doesn't actually perform async operations
    mock_enricher = MagicMock(spec=Enricher)
    mock_enricher.add_release_dates = AsyncMock()
    
    # Convert store_time_test_data to proper Artist objects
    artists_dict = store_time_test_data.get_artists()
    releases_dict = store_time_test_data.get_releases()
    reviews_dict = store_time_test_data.get_reviews()
    
    artist_objects = {}
    for artist_id, artist_data in artists_dict.items():
        release_objects = []
        for release_id in artist_data['releases']:
            release_data = releases_dict.get(release_id)
            
            # Create review objects
            review_objects = []
            for review_id in release_data['reviews']:
                review_data = reviews_dict.get(review_id)
                review = Review(
                    id=review_data['id'],
                    publication_name=review_data['publication_name'],
                    date=review_data['date'],
                    link=review_data['link'],
                    score=review_data['score']
                )
                review_objects.append(review)
            
            release = Release(
                id=release_data['id'],
                name=release_data['name'],
                reviews=review_objects,
                date=release_data['date'],
                type=release_data['type'],
                total_tracks=release_data['total_tracks'],
                spotify_url=release_data['spotify_url']
            )
            release_objects.append(release)
            
        artist = Artist(
            id=artist_data['id'],
            name=artist_data['name'],
            releases=release_objects
        )
        artist_objects[artist_id] = artist
    
    # Set the return value to use actual Artist objects
    mock_enricher.add_release_dates.return_value = artist_objects
    
    # Also create a mock for the music_cataloger to return artists with reviews
    mock_music_cataloger = MagicMock()
    mock_music_cataloger.catalog_reviews.return_value = artist_objects
    
    with patch('src.collector.service.FileAdapter') as mock_file_adapter, \
         patch('src.collector.service.aoty') as _, \
         patch('src.collector.service.metacritic') as _:

        service = CollectorService(mock_music_cataloger, mock_enricher)
        service.collect_reviews()

        return mock_file_adapter
