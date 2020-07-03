from src.collector.entities.artist import Artist
from src.collector.entities.release import Release
from src.collector.entities.review import Review
from src.collector.use_cases.cataloger import Cataloger
from abc import abstractmethod
from typing import Dict, List
from src.collector.entities.publication_review import PublicationReview

from src.common.crypto import calculate_hash


class MusicCataloger(Cataloger):

    def __init__(self):
        self.artists = {}
        self.releases = []
        self.reviews = []

    def add_review(self, publication_reviews: List[PublicationReview]) -> Dict[str, Artist]:
        print(publication_reviews)
        for publication_review in publication_reviews:
            artist = self._create_artist(publication_review)

            release_id = self._create_release(artist, publication_review)

            self._create_review(publication_review, artist, release_id)

        return self.artists

    def add_release(self, data) -> Dict[str, Artist]:
        raise NotImplemented

    def get_artists(self) -> Dict[str, Artist]:

        return self.artists

    def get_releases(self) -> List[Release]:

        raise NotImplemented

    def get_reviews(self) -> List[Review]:

        raise NotImplemented

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

        if not self.artists.get(artist_id):
            self.artists[artist_id] = artist

        return self.artists[artist_id]

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
            self.artists[artist.id] = artist

        return release

    def _create_review(self, publication_review: PublicationReview, artist: Artist, release: Release) -> Review:

        # TODO: Check for pre-existing review?
        artist_name = artist.name
        release_id = release.id

        release_name = self.format_release_name(publication_review.release_name)
        publication_name = publication_review.get('publication_name')

        review_id = calculate_hash(artist_name + release_name + publication_name)
        review = Review(
            id=review_id,
            publication_name=publication_name,
            score=publication_review.get('score'),
            date=publication_review.get('date'),
            link=publication_review.get('link')
        )

        for i, release in enumerate(self.artists[artist.id].releases):
            if release.id == release_id:
                release.reviews.append(review)
                self.artists[artist.id].releases[i] = release
                break

        return review
