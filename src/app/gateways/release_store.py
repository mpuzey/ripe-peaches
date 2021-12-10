from src.app.gateways.store import Store
from typing import Dict
from src.collector.entities.artist import Artist
from src.collector.entities.release import Release


class ReleaseStore(Store):

    def __init__(self, storage_adapter, review_store):
        self.storage_adapter = storage_adapter
        self.review_store = review_store

    def get(self, id):
        raise NotImplemented

    def get_all(self) -> Dict[str, Release]:
        stored_releases = self.storage_adapter.get_all()
        stored_reviews = self.review_store.get_all()
        releases = {}
        for release_id, stored_release in stored_releases.items():
            reviews = []

            for review_id in stored_release.get('reviews'):
                review = stored_reviews.get(review_id)
                reviews.append(review)

            release = Release(
                id=release_id,
                name=stored_release.get('name'),
                spotify_url=stored_release.get('spotify_url'),
                total_tracks=stored_release.get('total_tracks'),
                date=stored_release.get('date'),
                type=stored_release.get('type'),
                reviews=reviews
            )
            releases[release_id] = release

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
