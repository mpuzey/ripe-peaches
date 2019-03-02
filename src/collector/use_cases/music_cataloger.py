from src.collector.entities.artist import Artist
from src.collector.entities.release import Release
from src.collector.entities.review import Review
from src.collector.use_cases.cataloger import Cataloger
from abc import abstractmethod
from typing import Dict

from src.common.crypto import calculate_hash


class MusicCataloger(Cataloger):

    def __init__(self):
        self.artists = {}

    @abstractmethod
    def add(self, data) -> Dict[str, Artist]:
        pass

    def get_artists(self) -> Dict[str, Artist]:

        return self.artists

    def create_artist(self, raw_release: Dict) -> Artist:
        artist_name = raw_release.get('artist')
        artist_id = calculate_hash(artist_name)
        artist = self.artists[artist_id] = Artist(
            id=artist_id,
            name=artist_name,
            releases=[]
        )

        if not self.artists.get(artist_id):
            self.artists[artist_id] = artist

        return artist

    @abstractmethod
    def create_release(self, artist: Artist, pulication_review: Dict) -> Release:
        pass

    @abstractmethod
    def create_review(self, publication_review: Dict, artist: Artist, release: Release) -> Review:
        pass

    def format_release_name(self, name: str) -> str:
        formatted_name = name.replace('and', '&').title()

        return formatted_name
