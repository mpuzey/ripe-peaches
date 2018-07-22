import json

from constants import ROOT_PATH
from src.app.gateways.storage_adapter import StorageAdapter


class FileAdapter(StorageAdapter):

    def __init__(self, file_name):
        self.file_path = ROOT_PATH + '/src/app/db/%s.json' % file_name

    def get(self):
        """ This API should return a full dict of keys from the file. """
        try:
            with open(self.file_path, 'r') as outfile:
                data = json.load(outfile)
                return data
        except IOError:
            print('file path %s does not exist' % self.file_path)
            return {}

    def put(self, documents):
        """ This API needs to take a dict, read existing keys from the file, updates existing documents
         if necessary and dumps the result to file."""

        existing_documents = self.get()

        with open(self.file_path, 'w+') as outfile:

            for id, document in documents.items():

                if id in existing_documents:

                    update_lists(existing_documents, document)

            documents.update(existing_documents)
            json.dump(documents, outfile)


def update_lists(existing_data, new_data):

    id = new_data.get('id')
    for key, value in existing_data[id].items():
        if type(value) is list:
            existing_values = existing_data[id][key]
            existing_data[id][key] = list(set().union(existing_values, new_data[key]))

    return existing_data
