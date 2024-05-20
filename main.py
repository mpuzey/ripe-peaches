""" This is the main module for the application. It's in charge of creating and configuring the
tornado web server. """
import tornado.ioloop
import tornado.web

from src.app.service import start_app
from src.aggregator.service import AggregatorService
from src.aggregator.review_aggregator import ReviewScoresAggregator
from src.collector.use_cases.music_catalog import MusicCatalog
from src.collector.use_cases.music_cataloger import MusicCataloger
from src.collector.use_cases.enricher import Enricher
from src.collector.web.spotify import Spotify
from src.collector.controllers.music_release_collector import MusicReleaseCollector
from src.collector.controllers.music_review_collector import MusicReviewCollector
from src.collector.service import CollectorService


def start_all_services():
    run_jobs()
    start_app()


def run_jobs():
    start_collector_service()
    start_aggregator_service()


def start_collector_service():
    music_catalog = MusicCatalog()
    review_collector = MusicReviewCollector()
    release_collector = MusicReleaseCollector()
    music_cataloger = MusicCataloger(music_catalog, review_collector, release_collector)
    # spotify = Spotify()
    enricher = Enricher
    service = CollectorService(music_cataloger, enricher)
    service.collect_reviews()


def start_aggregator_service():
    aggregator = ReviewScoresAggregator()
    service = AggregatorService(aggregator)
    service.start()


if __name__ == '__main__':
    """ This function is the entry point for the application. """
    start_all_services()
