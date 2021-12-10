from src.app.gateways.store import Store
from typing import Dict
from src.collector.entities.artist import Artist


class ArtistStore(Store):

    def __init__(self, storage_adapter, release_store):
        self.storage_adapter = storage_adapter
        self.release_store = release_store

    def get(self, id):
        raise NotImplemented

    def get_all(self) -> Dict[str, Artist]:
        stored_artists = self.storage_adapter.get_all()
        stored_releases = self.release_store.get_all()
        artists = {}
        for artist_id, stored_artist in stored_artists.items():
            releases = []
            for release_id in stored_artist.get('releases'):
                release = stored_releases.get(release_id)
                releases.append(release)

            artist = Artist(
                id=artist_id,
                name=stored_artist.get('name'),
                releases=releases
            )
            artists[artist_id] = artist

        return artists

    def put(self, artists: Dict[str, Artist]):
        """ This method should retrieve keys using the storage method, build up a list of dupes,
        store any artists which are new and return a dict containing duplicate artist names against
        their ids. When this module is adapted to use a more robust storage method it would be ideal
        if the """

        artist_documents = {}
        for _, artist in artists.items():
            release_ids = []
            for release in artist.releases:
                release_ids.append(release.id)
            artist_document = {}
            artist_document.update(artist.__dict__)
            artist_document['releases'] = release_ids
            artist_documents[artist_document['id']] = artist_document

        self.storage_adapter.put(artist_documents)
