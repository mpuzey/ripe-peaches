"""
The purpose of this module is to provide an API to test the collector service that is easy to use
in discrete tests and allows us to keep changes to tests to a minimum when functionality changes.
Instead where there are major refactors only the test API need change , where there are minor
refactors the tests and API need not. We should only need to add and change tests when there is new
functionality, a bug to fix or a missing scenario to cover.
"""

from mock import patch

from src.collector.service import CollectorService


def collect_reviews(review_collector, collected_data):

    with patch('src.collector.service.FileAdapter') as mock_file_adapter, \
         patch('src.collector.service.aoty') as _, \
         patch('src.collector.service.metacritic') as __:

        review_collector.publication_reviews = collected_data

        collector_service = CollectorService(review_collector, None)
        collector_service.collect_reviews()

        return mock_file_adapter


def collect_releases(release_collector, collected_data):

    with patch('src.collector.service.FileAdapter') as mock_file_adapter, \
         patch('src.collector.service.spotify') as _:

        release_collector.raw_releases = collected_data

        collector_service = CollectorService(None, release_collector)
        collector_service.collect_releases()

        return mock_file_adapter
