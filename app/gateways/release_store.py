from app.use_cases.store import Store


class ReleaseStore(Store):

    def __init__(self, storage_adapter):
        self.storage_adapter = storage_adapter

    def get(self):
        releases = self.storage_adapter.get('releases')
        return releases

    def put(self, releases):
        self.storage_adapter.put(releases)
