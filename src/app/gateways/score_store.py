from src.app.gateways.store import Store
from constants import MINIMUM_REVIEWS_COUNTED


class ScoreStore(Store):

    def __init__(self, storage_adapter, release_adapter):
        self.storage_adapter = storage_adapter
        self.release_adapter = release_adapter

    def get(self, id):
        raise NotImplemented

    def get_all(self):
        scores = self.storage_adapter.get_all()
        releases = self.release_adapter.get_all()

        for _, score in scores.items():

            release_id = score.get('release_id')
            release = releases.get(release_id)
            release_date = release.get('date')
            if release_date:
                scores[release_id]['date'] = release_date

        return {_: value for _, value in scores.items() if value.get('reviews_counted') > MINIMUM_REVIEWS_COUNTED}

    def put(self, scores):
        self.storage_adapter.put(scores)
