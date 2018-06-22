import json

from app.storage.store import Store
from constants import ROOT_PATH


class FileStore(Store):

    def __init__(self, file_name):
        self.file_name = file_name

    def get(self):
        pass

    def put(self, data):
        file_path = ROOT_PATH + '/app/storage/%s.json' % self.file_name
        with open(file_path, 'w') as outfile:
            json.dump(data, outfile)

    def post(self, data):
        pass
