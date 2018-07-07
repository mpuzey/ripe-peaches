from app.use_cases.store import Store


class ArtistStore(Store):

    def __init__(self, storage_adapter):
        self.storage_adapter = storage_adapter

    def get(self):
        artists = self.storage_adapter.get()
        return artists

    def put(self, artists):
        """ This method should retrieve keys using the storage method, build up a list of dupes,
        store any artists which are new and return a dict containing duplicate artist names against
        their ids. When this module is adapted to use a more robust storage method it would be ideal
        if the """

        # should it be this module that adds the ids?
        existing_artists = self.storage_adapter.put(artists, 'name')

        return existing_artists
