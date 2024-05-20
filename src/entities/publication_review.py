from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class PublicationReview:
    artist: str
    release_name: str
    score: int
    publication_name: str
    link: str
    date: str = None

    # def artist(self) -> Artist:
    #     id = calculate_hash(self.artist)
    #     artist = Artist(id=id, name=self.artist, releases=[])
    #     return artist
    #
    # def review(self) -> Review:
    #     raise NotImplemented
    #
    # def release(self) -> Release:
    #     raise NotImplemented
