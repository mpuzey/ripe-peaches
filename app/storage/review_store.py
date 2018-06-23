from app.storage.file_adapter import FileAdapter


class ReviewStore:

    def __init__(self):
        self.file_store = FileAdapter('reviews')

    def get_reviews(self):
        reviews = self.file_store.get('reviews')
        return reviews

    def store_reviews(self, reviews):
        json_blob = {'reviews': reviews}
        self.file_store.put(json_blob)
