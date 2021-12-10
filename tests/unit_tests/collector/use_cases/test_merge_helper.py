import copy
from typing import Dict
from src.collector.entities.artist import Artist
from src.collector.entities.release import Release
from src.collector.entities.review import Review


class ArtistDictionaryBuilder:

    def __init__(self):
        self.current_release_id = None
        self.current_artist_id = None
        self._artist_dict = {}

    def artist_dict(self) -> Dict[str, Artist]:
        return self._artist_dict.copy()

    def reset(self):
        self.__init__()
        return self

    def select_artist(self, artist_id: str):
        self.current_artist_id = artist_id
        return copy.copy(self)

    def select_release(self, release_id: str):
        self.current_release_id = release_id
        return copy.copy(self)

    def add_artist(self, artist_id: str, artist_name: str):
        self.current_artist_id = artist_id
        self._artist_dict[artist_id] = Artist(
            id=artist_id,
            name=artist_name,
            releases=[]
        )
        return copy.copy(self)

    def add_release(self, release_id: str, release_name: str):
        self.current_release_id = release_id
        artist = self._artist_dict[self.current_artist_id]
        release = Release(
            id=release_id,
            name=release_name,
            reviews=[]
        )
        artist.releases.append(release)
        self._artist_dict[self.current_artist_id] = artist
        return copy.copy(self)

    def add_review(self, review_id: str, publication_name: str, score: int, date: str):
        artist = self._artist_dict[self.current_artist_id]

        review = Review(
            id=review_id,
            publication_name=publication_name,
            score=score,
            date=date,
            link=''
        )

        for i, release in enumerate(artist.releases):
            if release.id == self.current_release_id:
                release.reviews.append(review)
                self._artist_dict[artist.id].releases[i] = release
                break

        return copy.copy(self)
