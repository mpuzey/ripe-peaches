from typing import Dict

from src.app.gateways.store import Store
from src.entities.review import Review


class ReviewStore(Store):

    def __init__(self, storage_adapter):
        self.storage_adapter = storage_adapter

    def get(self, id):
        raise NotImplemented

    def get_all(self) -> Dict[str, Review]:
        stored_reviews = self.storage_adapter.get_all()
        reviews = {}
        for review_id, stored_review in stored_reviews.items():
            review = Review(
                id=review_id,
                publication_name=stored_review.get('publication_name'),
                score=stored_review.get('score'),
                date=stored_review.get('date'),
                link=stored_review.get('link')
            )
            reviews[review_id] = review

        return reviews

    def put(self, reviews):
        self.storage_adapter.put(reviews)
