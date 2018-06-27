""" This module holds the tornado handler that displays data to the main screen of the
 application. Upon visiting the homepage of the site the user will see a list of recent releases
 and their aggregated review scores.
"""
import os
from app.handlers.base_handler import BaseHandler
from constants import PUBLIC_ROOT


class ScoresHandler(BaseHandler):
    """ This homepage class is simply responsible for serving the static page the application runs
    on. """
    def get(self):
        self.render(os.path.join(PUBLIC_ROOT, 'index.html'))
