from app.storage.file_store import FileStore


class ReviewStore:

    def __init__(self):
        self.file_store = FileStore('reviews')

    def get_reviews(self):
        reviews = self.file_store.get('reviews')
        return reviews

    def store_reviews(self, reviews):
        json_blob = {'reviews': reviews}
        self.file_store.put(json_blob)
