from typing import Dict
from src.collector.entities.artist import Artist
from src.collector.entities.release import Release
from src.collector.entities.review import Review
from src.collector.use_cases.music_cataloger import MusicCataloger

from src.common.crypto import calculate_hash


class MusicReviewCataloger(MusicCataloger):

    def __init__(self):
        super().__init__()
        self.artists = {}

    def add(self, data: Dict) -> Dict[str, Artist]:
        for publication_review in data:

            artist = self.create_artist(publication_review)

            release_id = self.create_release(artist, publication_review)

            self.create_review(publication_review, artist, release_id)

        return self.artists

    def get_releases(self):
        raise NotImplemented

    def get_reviews(self):
        raise NotImplemented

    def create_artist(self, publication_review: Dict) -> Artist:

        return super().create_artist(publication_review)

    def create_release(self, artist: Artist, raw_review) -> Release:

        artist_name = artist.name
        release_name = super().format_release_name(raw_review.get('release_name'))
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

    def create_review(self, publication_review, artist: Artist, release: Release) -> Review:

        # TODO: Check for pre-existing review?
        artist_name = artist.name
        release_id = release.id

        release_name = super().format_release_name(publication_review.get('release_name'))
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
