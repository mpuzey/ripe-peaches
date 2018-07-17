from app.use_cases.store import Store


class ReleaseStore(Store):

    def __init__(self, storage_adapter, review_store):
        self.storage_adapter = storage_adapter
        self.review_store = review_store

    def get(self):
        releases = self.storage_adapter.get()
        return releases

    def put(self, artists):

        review_documents = {}
        release_documents = {}

        for _, artist in artists.items():
            for release_id, release in artist['releases'].items():
                review_ids = []
                for review_id, review in release['reviews'].items():
                    review_ids.append(review_id)
                    review_documents[review_id] = review
                release['reviews'] = review_ids
                release_documents[release_id] = release

        self.storage_adapter.put(release_documents)
        self.review_store.put(review_documents)
