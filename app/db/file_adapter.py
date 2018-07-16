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
        """ This API needs to take a dict, read existing keys from the file, updates existing documents
         if necessary and dumps the result to file."""

        existing_dataset = self.get()

        with open(self.file_path, 'w+') as outfile:

            for _, document in documents.items():

                id = document.get('id')
                if id in existing_dataset:

                    for key, value in existing_dataset[id].items():
                        if type(value) is list:
                            existing_dataset[id][key] = existing_dataset[id][key] + document[key]

            documents.update(existing_dataset)
            json.dump(documents, outfile)
