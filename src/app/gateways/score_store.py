from src.app.use_cases.store import Store
from constants import MINIMUM_REVIEWS_COUNTED


class ScoreStore(Store):

    def __init__(self, storage_adapter):
        self.storage_adapter = storage_adapter

    def get(self):
        scores = self.storage_adapter.get()
        return {_: value for _, value in scores.items() if value.get('reviews_counted') > MINIMUM_REVIEWS_COUNTED}

    def put(self, scores):
        self.storage_adapter.put(scores)
