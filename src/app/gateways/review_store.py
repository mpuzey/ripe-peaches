from src.app.gateways.store import Store


class ReviewStore(Store):

    def __init__(self, storage_adapter):
        self.storage_adapter = storage_adapter

    def get(self, id):
        raise NotImplemented

    def get_all(self):
        reviews = self.storage_adapter.get()
        return reviews

    def put(self, reviews):
        self.storage_adapter.put(reviews)
