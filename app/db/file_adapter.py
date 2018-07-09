import json

from app.gateways.storage_adapter import StorageAdapter
from constants import ROOT_PATH


class FileAdapter(StorageAdapter):

    def __init__(self, file_name):
        self.file_path = ROOT_PATH + '/app/db/%s.json' % file_name

    def get(self):
        """ This API should return a full dict of keys from the file. """
        with open(self.file_path, 'r') as outfile:
            data = json.load(outfile)
            return data

    def put(self, documents):
        """ This API needs to take a dict, read existing keys from the file, deduplicate documents if
        necessary, dump the result and return the deduplicated keys and their
        associated ids if there are any. """

        with open(self.file_path, 'wr+') as outfile:

            existing_dataset = json.load(outfile)

            for document in documents:

                id = document('id')
                if id in existing_dataset:
                    del documents[id]

            json.dump(documents, outfile)
