import asyncio

from src.app.gateways.artist_store import ArtistStore
from src.app.gateways.release_store import ReleaseStore
from src.app.gateways.review_store import ReviewStore
from src.collector.web import metacritic, aoty
from src.collector.use_cases.merge import merge_artist_dicts

from config import METACRITIC_PUBLICATIONS, METACRITIC_PUBLICATIONS_SAMPLE, AOTY_PUBLICATIONS, AOTY_PUBLICATIONS_SAMPLE
from src.app.db.file_adapter import FileAdapter


class CollectorService:

    def __init__(self, music_cataloger, enricher):
        self.music_cataloger = music_cataloger
        self.review_store = ReviewStore(FileAdapter('reviews'))
        self.release_store = ReleaseStore(FileAdapter('releases'), self.review_store)
        self.artist_store = ArtistStore(FileAdapter('artists'), ReleaseStore(FileAdapter('releases'), self.review_store))
        self.enricher = enricher

    def collect_reviews(self):
        self.music_cataloger.collect_reviews(metacritic, publications=METACRITIC_PUBLICATIONS)
        self.music_cataloger.collect_reviews(aoty, publications=AOTY_PUBLICATIONS)

        recently_reviewed_artists = self.music_cataloger.catalog_reviews()

        archived_artists = self.artist_store.get_all()

        known_artists = merge_artist_dicts(archived_artists, recently_reviewed_artists)
        print('enriching release data')

        enriched_artists = asyncio.run(self.enricher.add_release_dates(artists=known_artists))
        enriched_artists2 = enriched_artists.copy()

        self.artist_store.put(enriched_artists)
        self.release_store.put(enriched_artists2)


class EnricherService:
    def __init__(self, enricher):
        self.review_store = ReviewStore(FileAdapter('reviews'))
        self.release_store = ReleaseStore(FileAdapter('releases'), self.review_store)
        self.artist_store = ArtistStore(FileAdapter('artists'), self.release_store)
        self.enricher = enricher

    def enrich_stored_releases(self):
        """Enrich all releases in the store with metadata from Spotify."""
        # Load existing artists
        artists = self.artist_store.get_all()
        print(f"Number of artists before enrichment: {len(artists)}")
        print(f"Number of releases before enrichment: {sum(len(artist.releases) for artist in artists.values()) if artists else 0}")

        # Count releases with dates and cover_urls before enrichment
        releases_with_dates_before = 0
        releases_with_cover_before = 0
        for artist in artists.values():
            for release in artist.releases:
                if release.date:
                    releases_with_dates_before += 1
                if release.cover_url:
                    releases_with_cover_before += 1
        print(f"Number of releases with dates before: {releases_with_dates_before}")
        print(f"Number of releases with cover_url before: {releases_with_cover_before}")

        # Run enrichment
        print("\nRunning enrichment process (Spotify only)...")
        enriched_artists = asyncio.run(self.enricher.enrich(artists=artists))

        # Save enriched artists
        self.artist_store.put(enriched_artists)

        # Print stats after enrichment
        artists_after = self.artist_store.get_all()
        print(f"Number of artists after enrichment: {len(artists_after)}")
        print(f"Number of releases after enrichment: {sum(len(artist.releases) for artist in artists_after.values())}")

        releases_with_dates_after = 0
        releases_with_cover_after = 0
        for artist in artists_after.values():
            for release in artist.releases:
                if release.date:
                    releases_with_dates_after += 1
                if release.cover_url:
                    releases_with_cover_after += 1
        print(f"Number of releases with dates after: {releases_with_dates_after}")
        print(f"Number of releases with cover_url after: {releases_with_cover_after}")
        print(f"New dates added: {releases_with_dates_after - releases_with_dates_before}")
        print(f"New cover_urls added: {releases_with_cover_after - releases_with_cover_before}")
