from app.use_cases.store import Store


class ReleaseStore(Store):

    def __init__(self, adapter):
        self.adapter = adapter

    def get(self):
        releases = self.adapter.get('releases')
        return releases

    def put(self, releases):
        json_blob = {'releases': releases}
        self.adapter.put(json_blob)
