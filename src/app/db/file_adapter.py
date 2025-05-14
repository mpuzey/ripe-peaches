import json

from constants import ROOT_PATH
from src.app.db.storage_adapter import StorageAdapter


class FileAdapter(StorageAdapter):

    def __init__(self, file_name):
        self.file_path = ROOT_PATH + "/src/app/db/%s.json" % file_name

    def get(self, id):
        raise NotImplemented

    def get_all(self):
        """This API should return a full dict of keys from the file."""
        try:
            with open(self.file_path, "r") as outfile:
                data = json.load(outfile)
                return data
        except Exception as e:
            print("file path %s does not exist" % self.file_path)
            return {}

    def put(self, new_documents):
        """This API needs to take a dict, read existing keys from the file, updates existing documents
        if necessary and dumps the result to file."""

        existing_documents = self.get_all()

        documents = {}
        documents.update(existing_documents)

        with open(self.file_path, "w+") as outfile:

            for id, document in new_documents.items():

                if id in existing_documents:

                    documents = _merge_document(document, existing_documents)

            new_documents.update(documents)
            json.dump(new_documents, outfile)


def _merge_document(new_document, existing_documents):

    documents = {}
    documents.update(existing_documents)

    id = new_document.get("id")
    existing_document = existing_documents.get(id)

    for key, value in new_document.items():
        # Special handling for cover_url - prefer existing non-null value
        if key == "cover_url":
            if not existing_document.get(key) and value:
                # If existing is null/missing but new has a value, use the new value
                documents[id][key] = value
                print(f"Added new cover URL for {id}: {value}")
            elif (
                existing_document.get(key)
                and value
                and existing_document.get(key) != value
            ):
                # Both have values but they're different - keep existing and log
                print(
                    f"Keeping existing cover URL for {id}: {existing_document.get(key)} (new value was: {value})"
                )
        elif not existing_document.get(key):
            documents[id][key] = value

    for key, value in existing_document.items():
        if type(value) is list:
            existing_values = existing_documents[id][key]
            new_values = new_document[key]
            documents[id][key] = existing_values + list(
                set(new_values) - set(existing_values)
            )

        if key == "reviews_counted" or key == "score":
            documents[id][key] = new_document[key]

    return documents
