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

    def put(self, new_documents):
        """ This API needs to take a dict, read existing keys from the file, updates existing documents
         if necessary and dumps the result to file."""

        existing_documents = self.get()

        documents = {}
        documents.update(existing_documents)

        with open(self.file_path, 'w+') as outfile:

            for id, document in new_documents.items():

                if id in existing_documents:

                    documents = merge_document(document, existing_documents)

            documents.update(new_documents)
            json.dump(new_documents, outfile)


def merge_document(new_document, existing_documents):

    documents = {}
    documents.update(existing_documents)

    id = new_document.get('id')
    for key, value in existing_documents[id].items():
        if type(value) is list:
            existing_values = existing_documents[id][key]
            documents[id][key] = list(set().union(existing_values, new_document[key]))

    return documents
