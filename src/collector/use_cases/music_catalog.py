from src.collector.entities.artist import Artist
from src.collector.entities.release import Release
from src.collector.entities.review import Review
from src.collector.use_cases.catalog import Catalog
from typing import Dict, List


class MusicCatalog(Catalog):

    def __init__(self):
        self.artists = {}
        self.releases = []
        self.reviews = []

    def add_artists(self, artists: Dict[str, Artist]) -> Dict[str, Artist]:
        self.artists.update(artists)
        return self.artists

    def get_artists(self) -> Dict[str, Artist]:

        return self.artists

    def get_releases(self) -> List[Release]:

        raise NotImplemented

    def get_reviews(self) -> List[Review]:

        raise NotImplemented
