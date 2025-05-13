from src.app.web.base_handler import BaseHandler


class ReviewsHandler(BaseHandler):

    def initialize(self, store):
        self.store = store

    def get(self):
        reviews = self.store.get()
        self.write({"reviews": reviews})


def parse_query(request):
    query_string = request.arguments
    search_text = query_string.get("text")[0].decode("utf-8")
    return search_text
