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

    def put(self, documents, dedupe_field=None):
        """ This API needs to take a dict, read existing keys from the file, deduplicate documents if
        necessary, dump the result and return the deduplicated keys and their
        associated ids if there are any. """
        duplicated_documents = []

        with open(self.file_path, 'wr+') as outfile:

            existing_dataset = json.load(outfile)
            existing_documents = existing_dataset.values()

            if dedupe_field:
                for document in documents:
                    for existing_document in existing_documents:
                        if existing_document[dedupe_field] == document[dedupe_field]:

                            duplicated_documents.append({
                                document[dedupe_field]: existing_document.get('id')
                            })
                            del documents[dedupe_field]

            existing_documents.update(documents)
            json.dump(documents, outfile)

        return duplicated_documents
