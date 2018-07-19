from src.app.use_cases.store import Store


class ScoreStore(Store):

    def __init__(self, storage_adapter):
        self.storage_adapter = storage_adapter

    def get(self):
        scores = self.storage_adapter.get()
        return scores

    def put(self, scores):
        self.storage_adapter.put(scores)
