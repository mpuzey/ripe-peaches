from app.use_cases.store import Store


class ReviewStore(Store):

    def __init__(self, storage_adapter):
        self.storage_adapter = storage_adapter

    def get(self):
        reviews = self.storage_adapter.get('reviews')
        return reviews

    def put(self, reviews):
        self.storage_adapter.put(reviews)