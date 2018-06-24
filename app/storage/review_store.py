from app.storage.file_adapter import FileAdapter


class ReviewStore:

    def __init__(self):
        self.file_adapter = FileAdapter('reviews')

    def get(self):
        reviews = self.file_adapter.get('reviews')
        return reviews

    def put(self, reviews):
        json_blob = {'reviews': reviews}
        self.file_adapter.put(json_blob)
