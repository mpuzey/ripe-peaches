
class ReviewStore:

    def __init__(self, adapter):
        self.adapter = adapter

    def get(self):
        reviews = self.adapter.get('reviews')
        return reviews

    def put(self, reviews):
        json_blob = {'reviews': reviews}
        self.adapter.put(json_blob)