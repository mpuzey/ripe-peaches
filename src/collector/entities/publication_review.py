from dataclasses import dataclass
from src.collector.entities.artist import Artist
from src.common.crypto import calculate_hash


@dataclass
class PublicationReview:
    artist: str
    release_name: str
    score: int
    publication_name: str
    date: str
    link: str

    def artist(self) -> Artist:
        # id = calculate_hash(self.artist)
        # artist = Artist(id=id, name=self.artist, releases=[])
        # return artist
        pass

    def review(self):
        pass

    def release(self):
        pass
