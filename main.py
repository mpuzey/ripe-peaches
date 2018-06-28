""" This is the main module for the application. It's in charge of creating and configuring the
tornado web server. """
import tornado.ioloop
import tornado.web

from app.gateways.review_store import ReviewStore
from app.db.file_adapter import FileAdapter
from app.web.reviews_handler import ReviewsHandler
from app.web.scores_handler import ScoresHandler
from collector.review_scraper import ReviewScraper
from collector.service import CollectorService
from constants import PUBLIC_ROOT


def make_app():
    """ This function returns an Application instance loaded with the necessary request handlers
    for the app.
    """
    collector = ReviewScraper()
    store = ReviewStore(FileAdapter('reviews'))

    service = CollectorService(collector, store)
    service.start()

    return tornado.web.Application([
        (r'/', ScoresHandler),
        (r'/public/(.*)', tornado.web.StaticFileHandler, {'path': PUBLIC_ROOT}),
        (r'/reviews', ReviewsHandler, {'store': store})
    ])


if __name__ == '__main__':
    """ This function is the entry point for the application. """
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
