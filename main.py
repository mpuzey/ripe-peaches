""" This is the main module for the application. It's in charge of creating and configuring the
tornado web server. """
import tornado.ioloop
import tornado.web
from src.aggregator.service import AggregatorService
from src.aggregator.use_cases.aggregator import Aggregator
from src.app.gateways.review_store import ReviewStore
from src.app.gateways.score_store import ScoreStore
from src.app.web.reviews_handler import ReviewsHandler
from src.app.web.scores_handler import ScoresHandler
from src.collector.controllers.music_review_scraper import MusicReviewScraper
from src.collector.controllers.music_release_scraper import MusicReleaseScraper
from src.collector.service import CollectorService

from constants import PUBLIC_ROOT
from src.app.db.file_adapter import FileAdapter


def make_app():
    """ This function returns an Application instance loaded with the necessary request handlers
    for the app.
    """

    start_collector_service()
    start_aggregator_service()

    review_store = ReviewStore(FileAdapter('reviews'))
    score_store = ScoreStore(FileAdapter('scores'))

    return tornado.web.Application([
        (r'/', ScoresHandler, {'store': score_store}),
        (r'/public/(.*)', tornado.web.StaticFileHandler, {'path': PUBLIC_ROOT}),
        (r'/reviews', ReviewsHandler, {'store': review_store})
    ])


def start_collector_service():
    # review_collector = MusicReviewScraper()
    release_collector = MusicReleaseScraper()
    service = CollectorService(None, release_collector)
    # service.collect_reviews()
    service.collect_releases()


def start_aggregator_service():
    aggregator = Aggregator()
    service = AggregatorService(aggregator)
    service.start()


if __name__ == '__main__':
    """ This function is the entry point for the application. """
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
