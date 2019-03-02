from src.collector.entities.artist import Artist
from src.collector.entities.release import Release
from src.collector.entities.review import Review
from src.collector.entities.collector import Collector
from src.common.crypto import calculate_hash


class MusicReviewScraper(Collector):

    def __init__(self):
        self.raw_reviews = []
        self.artists = {}

    def collect(self, source, **kwargs):

        publications = kwargs.get('publications')
        for publication in publications:
            print('scraping ' + publication)
            publication_reviews = source.get_reviews(publication)

            if not publication_reviews:
                print('No reviews available for the following publication: %s' % repr(publication))

            self.raw_reviews.extend(publication_reviews)

        print('finished scraping!')

    def parse(self):

        for raw_review in self.raw_reviews:
            artist = self._build_artist(raw_review)
            release = self._build_release(artist, raw_review)
            self._build_review(raw_review, artist, release)

        return self.artists

    def _build_artist(self, raw_review) -> Artist:

        artist_name = raw_review.get('artist')
        artist_id = calculate_hash(artist_name)
        artist = self.artists[artist_id] = Artist(
            id=artist_id,
            name=artist_name,
            releases=[]
        )

        if not self.artists.get(artist_id):
            self.artists[artist_id] = artist

        return artist

    def _build_release(self, artist, raw_review) -> Release:

        artist_name = artist.name
        release_name = _format_release_name(raw_review.get('release_name'))
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

    def _build_review(self, raw_review, artist, release) -> Review:

        # TODO: Check for pre-existing review?
        artist_name = artist.name
        release_id = release.id

        release_name = _format_release_name(raw_review.get('release_name'))
        publication_name = raw_review.get('publication_name')

        review_id = calculate_hash(artist_name + release_name + publication_name)
        review = Review(
            id=review_id,
            publication_name=publication_name,
            score=raw_review.get('score'),
            date=raw_review.get('date'),
            link=raw_review.get('link')
        )

        for i, release in enumerate(self.artists[artist.id].releases):
            if release.id == release_id:
                release.reviews.append(review)
                self.artists[artist.id].releases[i] = release
                break

        return review


def _format_release_name(name):
    formatted_name = name.replace('and', '&').title()

    return formatted_name

