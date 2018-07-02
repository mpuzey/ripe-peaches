from app.use_cases.store import Store


class ArtistStore(Store):

    def __init__(self, adapter):
        self.adapter = adapter

    def get(self):
        artists = self.adapter.get('artists')
        return artists

    def put(self, artists):
        json_blob = {'artists': artists}
        self.adapter.put(json_blob)
