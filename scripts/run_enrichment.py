#!/usr/bin/env python3
"""
Run only the enrichment process (Spotify enrichment) on existing artist/release data in the file store.
This script does NOT scrape or collect new data from Metacritic or AOTY.
"""
import os
import asyncio
from src.collector.use_cases.enricher import Enricher
from src.collector.web.spotify import Spotify
from src.app.gateways.artist_store import ArtistStore
from src.app.gateways.release_store import ReleaseStore
from src.app.gateways.review_store import ReviewStore
from src.app.db.file_adapter import FileAdapter

# Print Spotify credentials
print(f"Using SPOTIFY_CLIENT_ID: {os.environ.get('SPOTIFY_CLIENT_ID', 'Not set')[:5]}...")
print(f"Using SPOTIFY_CLIENT_SECRET: {os.environ.get('SPOTIFY_CLIENT_SECRET', 'Not set')[:5]}...")

# Set up stores
review_store = ReviewStore(FileAdapter('reviews'))
release_store = ReleaseStore(FileAdapter('releases'), review_store)
artist_store = ArtistStore(FileAdapter('artists'), release_store)

# Load existing artists
artists_before = artist_store.get_all()
print(f"Number of artists before enrichment: {len(artists_before)}")
print(f"Number of releases before enrichment: {sum(len(artist.releases) for artist in artists_before.values()) if artists_before else 0}")

# Count releases with dates and cover_urls before enrichment
releases_with_dates_before = 0
releases_with_cover_before = 0
for artist in artists_before.values():
    for release in artist.releases:
        if release.date:
            releases_with_dates_before += 1
        if release.cover_url:
            releases_with_cover_before += 1
print(f"Number of releases with dates before: {releases_with_dates_before}")
print(f"Number of releases with cover_url before: {releases_with_cover_before}")

# Run enrichment
print("\nRunning enrichment process (Spotify only)...")
enricher = Enricher(Spotify)
async def enrich():
    return await enricher.add_release_dates(artists_before)
artists_after = asyncio.run(enrich())

# Save enriched artists
artist_store.put(artists_after)

# Print stats after enrichment
artists_after = artist_store.get_all()
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