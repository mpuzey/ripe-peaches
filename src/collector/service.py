from src.app.gateways.artist_store import ArtistStore
from src.app.gateways.release_store import ReleaseStore
from src.app.gateways.review_store import ReviewStore
from src.collector.web import metacritic, aoty
import collections
import copy

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
        recently_reviewed_artists = self.music_cataloger.catalog_reviews()
        for artist_id, artist in recently_reviewed_artists.items():
            if artist.name == "Taylor Swift":
                for release in artist.releases:
                    print(release.name)
                print('length is %s' + str(len(artist.releases)))
                print('hi')

        archived_artists = self.artist_store.get_all()
        for artist_id, artist in archived_artists.items():
            if artist.name == "Taylor Swift":
                for release in artist.releases:
                    print(release.name)
                print('length is %s' + str(len(artist.releases)))
                print('hi')

        # archive_copy = archived_artists.copy()
        # known_artists = archive_copy.update(recently_reviewed_artists)
        # known_artists = {**archived_artists, **recently_reviewed_artists}
        known_artists = deep_dict_merge(recently_reviewed_artists, archived_artists)
        for artist_id, artist in known_artists.items():
            if artist.name == "Taylor Swift":
                for release in artist.releases:
                    print(release.name)
                print('hi')
                print('length is %s' + str(len(artist.releases)))
                print('length is %s' + str(len(artist.releases)))
        print('enriching release data')

        enriched_artists = self.enricher.add_release_dates(known_artists)

        self.artist_store.put(enriched_artists)
        self.release_store.put(enriched_artists)


def deep_dict_merge(dct1, dct2, override=True) -> dict:
    """
    :param dct1: First dict to merge
    :param dct2: Second dict to merge
    :param override: if same key exists in both dictionaries, should override? otherwise ignore. (default=True)
    :return: The merge dictionary
    """
    merged = copy.deepcopy(dct1)
    for k, v2 in dct2.items():
        if k in merged:
            v1 = merged[k]
            if isinstance(v1, dict) and isinstance(v2, collections.Mapping):
                merged[k] = deep_dict_merge(v1, v2, override)
            elif isinstance(v1, list) and isinstance(v2, list):
                merged[k] = v1 + v2
            else:
                if override:
                    merged[k] = copy.deepcopy(v2)
        else:
            merged[k] = copy.deepcopy(v2)
    return merged
