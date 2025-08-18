"""This is the main module for the application. It's in charge of creating and configuring the
tornado web server."""

import tornado.ioloop
import tornado.web

from constants import PUBLIC_ROOT
from src.app.db.file_adapter import FileAdapter
from src.app.gateways.review_store import ReviewStore
from src.app.gateways.score_store import ScoreStore
from src.app.web.reviews_handler import ReviewsHandler
from src.app.web.scores_handler import ScoresHandler


def start_app():
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()


def make_app():
    """This function returns an Application instance loaded with the necessary request handlers
    for the app.
    """
    # Initialize stores
    review_store = ReviewStore(FileAdapter("reviews"))
    score_store = ScoreStore(FileAdapter("scores"), FileAdapter("releases"))

    return tornado.web.Application(
        [
            (r"/", ScoresHandler, {"store": score_store}),
            (r"/public/(.*)", tornado.web.StaticFileHandler, {"path": PUBLIC_ROOT}),
            (r"/reviews", ReviewsHandler, {"store": review_store}),
        ]
    )


if __name__ == "__main__":
    """This function is the entry point for the application."""
    start_app()
