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
from mock import MagicMock


def collect_reviews(collected_data, enriched_releases):

    music_catalog = MusicCatalog()
    review_collector = MagicMock()
    review_collector.collect_reviews.return_value = collected_data

    release_collector = MusicReleaseCollector()
    music_cataloger = MusicCataloger(music_catalog, review_collector, release_collector)

    spotify = MagicMock()
    spotify.get_release_details.side_effect = enriched_releases
    enricher = Enricher(spotify)

    with patch('src.collector.service.FileAdapter') as mock_file_adapter, \
         patch('src.collector.service.aoty') as _, \
         patch('src.collector.service.metacritic') as _:

        service = CollectorService(music_cataloger, enricher)
        service.collect_reviews()

        return mock_file_adapter
