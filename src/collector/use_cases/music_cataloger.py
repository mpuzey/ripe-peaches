from src.collector.entities.artist import Artist
from src.collector.entities.release import Release
from src.collector.entities.review import Review
from src.collector.use_cases.librarian import Librarian

from abc import abstractmethod
from typing import Dict, List
from src.collector.entities.publication_review import PublicationReview
from src.collector.entities.publication_release import PublicationRelease


from src.common.crypto import calculate_hash


class MusicCataloger(Librarian):

    def __init__(self, catalog):
        self.catalog = catalog
        self.new_artists = {}

    def add_reviews(self, publication_reviews: List[PublicationReview]) -> Dict[str, Artist]:

        for publication_review in publication_reviews:
            artist = self._create_artist(publication_review)

            release_id = self._create_release(artist, publication_review)

            self._create_review(publication_review, artist, release_id)

        self.catalog.add_artists(self.new_artists)
        return self.catalog.get_artists()

    def add_releases(self, publication_releases) -> Dict[str, Artist]:  #: List[PublicationRelease]) -> Dict[str, Artist]:
        for raw_release in publication_releases:

            artist = self._create_artist(raw_release)

            self._create_release(artist, raw_release)

        return self.artists

    def format_release_name(self, name: str) -> str:
        formatted_name = name.replace('and', '&').title()

        return formatted_name

    def _create_artist(self, publication_review: PublicationReview) -> Artist:

        artist_name = publication_review.artist
        artist_id = calculate_hash(artist_name)
        artist = Artist(
            id=artist_id,
            name=artist_name,
            releases=[]
        )

        if not self.new_artists.get(artist_id):
            self.new_artists[artist_id] = artist

        return self.new_artists[artist_id]

    def _create_release(self, artist: Artist, publication_review: PublicationReview) -> Release:

        artist_name = artist.name
        release_name = self.format_release_name(publication_review.release_name)
        release_id = calculate_hash(artist_name + release_name)

        existing_release = next((x for x in artist.releases if x.id == release_id), None)
        release = Release(
            id=calculate_hash(artist_name + release_name),
            name=release_name,
            reviews=[]
        )

        if not existing_release:
            artist.releases.append(release)
            self.new_artists[artist.id] = artist

        return release

    def _create_review(self, publication_review: PublicationReview, artist: Artist, release: Release) -> Review:

        # TODO: Check for pre-existing review?
        artist_name = artist.name
        release_id = release.id

        release_name = self.format_release_name(publication_review.release_name)
        publication_name = publication_review.publication_name

        review_id = calculate_hash(artist_name + release_name + publication_name)
        review = Review(
            id=review_id,
            publication_name=publication_name,
            score=publication_review.score,
            date=publication_review.date,
            link=publication_review.link
        )

        for i, release in enumerate(self.new_artists[artist.id].releases):
            if release.id == release_id:
                release.reviews.append(review)
                self.new_artists[artist.id].releases[i] = release
                break

        return review
