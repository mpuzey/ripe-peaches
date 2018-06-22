from app.storage.file_store import FileStore


class ReviewStore:

    def __init__(self):
        self.file_store = FileStore('reviews')

    def get_recent_reviews(self):
        pass

    def store_reviews(self, reviews):
        json_blob = {'reviews': reviews}
        self.file_store.put(json_blob)
