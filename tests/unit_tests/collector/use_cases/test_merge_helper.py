from typing import Dict
from src.collector.entities.artist import Artist
from src.collector.entities.release import Release
from src.collector.entities.review import Review


class ArtistDictionaryBuilder:

    def __init__(self) -> None:
        self.reset()

    def artist_dict(self):
        return self._artist_dict

    def reset(self) -> None:
        self._artist_dict = {}

    def add_artist(self, artist_id: str, artist_name: str) -> None:
        self._artist_dict[artist_id] = Artist(
            id=artist_id,
            name=artist_name,
            releases=[]
        )

    def add_release(self, artist_id: str, release_id: str, release_name: str) -> None:
        artist = self._artist_dict[artist_id]
        release = Release(
            id=release_id,
            name=release_name,
            reviews=[]
        )
        artist.releases.append(release)
        self._artist_dict[artist_id] = artist

    def add_review(self,
                   artist_id: str,
                   release_id: str,
                   review_id: str,
                   publication_name: str,
                   score: int,
                   date: str) -> None:

        artist = self._artist_dict[artist_id]

        review = Review(
            id=review_id,
            publication_name=publication_name,
            score=score,
            date=date,
            link=''
        )

        for i, release in enumerate(artist.releases):
            if release.id == release_id:
                release.reviews.append(review)
                self._artist_dict[artist.id].releases[i] = release
                break
