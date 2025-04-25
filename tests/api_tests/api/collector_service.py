"""
The purpose of this module is to provide an API to test the collector service that is easy to use
in discrete tests and allows us to keep changes to tests to a minimum when functionality changes.
Instead where there are major refactors only the test API need change , where there are minor
refactors the tests and API need not. We should only need to add and change tests when there is new
functionality, a bug to fix or a missing scenario to cover.
"""

from mock import patch

from src.collector.use_cases.enricher import Enricher
from src.collector.web.spotify import Spotify
from src.collector.use_cases.music_catalog import MusicCatalog
from src.collector.use_cases.music_cataloger import MusicCataloger
from src.collector.controllers.music_release_collector import MusicReleaseCollector
from src.collector.service import CollectorService
from unittest.mock import MagicMock, AsyncMock
from src.entities.external_release import ExternalRelease


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
    
    # Correctly use the enriched_releases for get_release_from_album
    spotify.get_release_from_album = AsyncMock(side_effect=enriched_releases)
    
    enricher = Enricher(spotify)

    with patch('src.collector.service.FileAdapter') as mock_file_adapter, \
         patch('src.collector.service.aoty') as _, \
         patch('src.collector.service.metacritic') as _:

        service = CollectorService(music_cataloger, enricher)
        service.collect_reviews()

        return mock_file_adapter
