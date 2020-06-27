from src.collector.entities.artist import Artist
from src.collector.entities.release import Release
from src.collector.entities.review import Review
from src.collector.use_cases.cataloger import Cataloger
from abc import abstractmethod
from typing import Dict, List

from src.common.crypto import calculate_hash


class MusicCataloger(Cataloger):

    def __init__(self):
        self.artists = {}
        self.releases = []
        self.reviews = []

    @abstractmethod
    def add(self, data) -> Dict[str, Artist]:
        pass

    def get_artists(self) -> Dict[str, Artist]:

        return self.artists

    def get_releases(self) -> List[Release]:

        return self.releases

    def get_reviews(self) -> List[Review]:

        return self.reviews

    def create_artist(self, publication_review: Dict) -> Artist:
        artist_name = publication_review.get('artist')
        artist_id = calculate_hash(artist_name)
        artist = self.artists[artist_id] = Artist(
            id=artist_id,
            name=artist_name,
            releases=[]
        )

        if not self.artists.get(artist_id):
            self.artists[artist_id] = artist

        return artist

    def format_release_name(self, name: str) -> str:
        formatted_name = name.replace('and', '&').title()

        return formatted_name
