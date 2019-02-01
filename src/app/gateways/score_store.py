from src.app.use_cases.store import Store
from constants import MINIMUM_REVIEWS_COUNTED


class ScoreStore(Store):

    def __init__(self, storage_adapter, release_adapter):
        self.storage_adapter = storage_adapter
        self.release_adapter = release_adapter

    def get(self):
        scores = self.storage_adapter.get()
        releases = self.release_adapter.get()
        for release_id, release in releases.items():
            score = scores.get(release_id)
            if not score or score.get('date'):
                continue
            release_date = release.get('date')
            if release_date:
                scores[release_id]['date'] = release_date

        return {_: value for _, value in scores.items() if value.get('reviews_counted') > MINIMUM_REVIEWS_COUNTED}

    def put(self, scores):
        self.storage_adapter.put(scores)
