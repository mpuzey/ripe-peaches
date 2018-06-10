from app.handlers.base_handler import BaseHandler
from app.sources import metacritic


class ReviewsHandler(BaseHandler):

    def initialize(self, store):
        self.store = store

    def get(self):
        reviews = metacritic.get_publication('consequence-of-sound')
        self.store.store_reviews(reviews)
        self.write({'reviews': reviews})


def parse_query(request):
    query_string = request.arguments
    search_text = query_string.get('text')[0].decode('utf-8')
    return search_text
