""" This is the main module for the application. It is in charge of creating and configuring the
tornado web server app. """
import tornado.ioloop
import tornado.web
from app.storage.review_store import ReviewStore

from app.handlers.reviews_handler import ReviewsHandler


def make_app():
    """ This function returns an Application instance which holds the request handlers for the app.
    """
    store = ReviewStore()

    return tornado.web.Application([
        (r'/reviews', ReviewsHandler, {'store': store})
    ])


if __name__ == '__main__':
    """ This function is the entry point for the application. """
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
