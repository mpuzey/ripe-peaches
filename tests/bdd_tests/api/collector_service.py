"""
The purpose of this module is to provide an API to test the collector service that is easy to use
in discrete tests and allows us to keep changes to tests to a minimum when functionality changes.
Instead where there are major refactors only the test API need change , where there are minor
refactors the tests and API need not. We should only need to add and change tests when there is new
functionality, a bug to fix or a missing scenario to cover.
"""

from mock import patch

from src.collector.service import CollectorService


def service_starts(collector_instance, collected_data):

    with patch('src.collector.service.ArtistStore') as mock_artist_store, \
         patch('src.collector.service.ReleaseStore') as mock_release_store, \
         patch('src.collector.service.aoty') as mock_aoty, \
         patch('src.collector.service.metacritic') as mock_metacritic:

        collector_instance.reviews = collected_data

        collector_service = CollectorService(collector_instance)
        collector_service.start()
