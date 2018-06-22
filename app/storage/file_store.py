import json

from app.storage.abstract_store import Store
from constants import ROOT_PATH


class FileStore(Store):

    def get_recent_reviews(self):
        pass

    def store_reviews(self, reviews):

        json_blob = {'reviews': reviews}
        file_path = ROOT_PATH + '/app/storage/reviews.json'
        with open(file_path, 'w') as outfile:
            json.dump(json_blob, outfile)
