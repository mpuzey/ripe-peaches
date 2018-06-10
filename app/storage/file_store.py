import json
from app.storage.abstract_store import Store


class FileStore(Store):

    def get_recent_reviews(self):
        pass

    def store_reviews(self, reviews):

        json_blob = {'reviews': reviews}
        with open('reviews.json', 'w') as outfile:
            json.dump(json_blob, outfile)
