from typing import Dict, List

from src.app.gateways.artist_store import ArtistStore
from src.app.gateways.release_store import ReleaseStore
from src.app.gateways.review_store import ReviewStore
from src.collector.web import metacritic, aoty
from src.collector.entities.artist import Artist
from src.collector.entities.review import Review

from constants import METACRITIC_CURATED_PUBLICATIONS, METACRITIC_PUBLICATIONS_SAMPLE, AOTY_CURATED_PUBLICATIONS, AOTY_PUBLICATIONS_SAMPLE
from src.app.db.file_adapter import FileAdapter


class CollectorService:

    def __init__(self, music_cataloger, enricher):
        self.music_cataloger = music_cataloger
        self.review_store = ReviewStore(FileAdapter('reviews'))
        self.release_store = ReleaseStore(FileAdapter('releases'), self.review_store)
        self.artist_store = ArtistStore(FileAdapter('artists'), ReleaseStore(FileAdapter('releases'), self.review_store))
        self.enricher = enricher

    def collect_reviews(self):

        # TODO: the term "collect" is perhaps a bit overloaded. We describe the overall job of the service of going off
        #  to the internet and storing new reviews collecting and we call the controllers that physically fetch the data
        #  collectors as well
        self.music_cataloger.collect_reviews(metacritic, publications=METACRITIC_PUBLICATIONS_SAMPLE)
        self.music_cataloger.collect_reviews(aoty, publications=AOTY_PUBLICATIONS_SAMPLE)

        # TODO: why is music_cataloger.publication_reviews blank when we step in here ????
        recently_reviewed_artists = self.music_cataloger.catalog_reviews()

        archived_artists = self.artist_store.get_all()

        # archive_copy = archived_artists.copy()
        # known_artists = archive_copy.update(recently_reviewed_artists)
        # known_artists = {**archived_artists, **recently_reviewed_artists}
        known_artists = merge_artist_dicts(archived_artists, recently_reviewed_artists)
        print('enriching release data')

        enriched_artists = self.enricher.add_release_dates(known_artists)

        self.artist_store.put(enriched_artists)
        self.release_store.put(enriched_artists)


def merge_artist_dicts(archived_artists: Dict[str, Artist], recently_reviewed_artists: Dict[str, Artist]) -> Dict[str, Artist]:

    archived_artists = archived_artists.copy()
    for artist_id, recently_reviewed_artist in recently_reviewed_artists.items():
        if artist_id in archived_artists:
            for recently_reviewed_release in recently_reviewed_artist.releases:
                archived_releases = archived_artists.get(artist_id).releases
                if archived_releases:
                    for archived_release in archived_releases:
                        if recently_reviewed_release.id is archived_release.id:
                            combined_reviews = merge_review_lists(archived_release.reviews, recently_reviewed_release.reviews)
                            archived_release.reviews = combined_reviews
                            # actually append this back into archived artists
                    # we are always going to hit this at the moment
                    archived_releases.append(recently_reviewed_release)
                    # actually append this back into archived artists
                else:
                    archived_artists[artist_id].releases = [recently_reviewed_release]
        else:
            archived_artists[artist_id] = recently_reviewed_artist

    return archived_artists


def merge_review_lists(archived_reviews: List[Review], recent_reviews: List[Review]) -> List[Review]:
    combined_reviews = archived_reviews.copy()
    for recent_review in recent_reviews:
        for archived_review in archived_reviews:
            if recent_review.id is archived_review.id:
                break
            combined_reviews.append(recent_review)

    return combined_reviews
