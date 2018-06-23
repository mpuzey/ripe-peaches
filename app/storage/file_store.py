import json

from app.storage.store import Store
from constants import ROOT_PATH


class FileStore(Store):

    def __init__(self, file_name):
        self.file_path = ROOT_PATH + '/app/storage/%s.json' % file_name

    def get(self, key):
        with open(self.file_path, 'r') as outfile:
            data = json.load(outfile)
            return data.get(key)

    def put(self, data):
        with open(self.file_path, 'w') as outfile:
            json.dump(data, outfile)

    def post(self, data):
        pass
