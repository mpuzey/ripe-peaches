from src.app.gateways.store import Store
from typing import Dict
from src.collector.entities.artist import Artist


class ReleaseStore(Store):

    def __init__(self, storage_adapter, review_store):
        self.storage_adapter = storage_adapter
        self.review_store = review_store

    def get(self, id):
        raise NotImplemented

    def get_all(self):
        releases = self.storage_adapter.get()
        return releases

    def put(self, artists: Dict[str, Artist]):

        review_documents = {}
        release_documents = {}

        for _, artist in artists.items():
            for release in artist.releases:
                review_ids = []
                for review in release.reviews:
                    review_ids.append(review.id)
                    review_documents[review.id] = review.__dict__
                release.reviews = review_ids
                release_documents[release.id] = release.__dict__

        self.storage_adapter.put(release_documents)
        if review_documents:
            self.review_store.put(review_documents)
