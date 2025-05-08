""" This module holds the tornado handler that displays data to the main screen of the
 application. Upon visiting the homepage of the site the user will see a list of recent releases
 and their aggregated review scores.
"""
from src.app.web.base_handler import BaseHandler


class ScoresHandler(BaseHandler):
    """ This homepage class is simply responsible for serving the static page the application runs
    on. """
    def initialize(self, store):
        self.store = store

    def get(self):
        scores = self.store.get_all()
        # Set CORS headers
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, content-type")
        self.set_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.write({'scores': scores})
        # self.render(os.path.join(PUBLIC_ROOT, 'index.html'))
        
    def options(self):
        # Respond to OPTIONS requests with CORS headers
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, content-type")
        self.set_header("Access-Control-Allow-Methods", "GET, OPTIONS") 
        self.set_status(204)
        self.finish()
