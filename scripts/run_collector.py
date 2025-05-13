#!/usr/bin/env python3
"""
Manually run the collection process
"""
import os
import sys
import asyncio
import json
from src.collector.service import CollectorService
from src.collector.use_cases.enricher import Enricher
from src.collector.web.spotify import Spotify
from src.collector.use_cases.music_catalog import MusicCatalog
from src.collector.use_cases.music_cataloger import MusicCataloger
from src.collector.controllers.music_release_collector import MusicReleaseCollector
from src.collector.controllers.music_review_collector import MusicReviewCollector
from src.app.gateways.artist_store import ArtistStore
from src.app.gateways.release_store import ReleaseStore
from src.app.gateways.review_store import ReviewStore
from src.app.db.file_adapter import FileAdapter

# Print Spotify credentials
print(f"Using SPOTIFY_CLIENT_ID: {os.environ.get('SPOTIFY_CLIENT_ID', 'Not set')[:5]}...")
print(f"Using SPOTIFY_CLIENT_SECRET: {os.environ.get('SPOTIFY_CLIENT_SECRET', 'Not set')[:5]}...")

# Set up components
music_catalog = MusicCatalog()
review_collector = MusicReviewCollector()
release_collector = MusicReleaseCollector()
music_cataloger = MusicCataloger(music_catalog, review_collector, release_collector)

# Create enricher with Spotify
enricher = Enricher(Spotify)

# Create the service with debug enabled
service = CollectorService(music_cataloger, enricher)

# Print the state before collection
review_store = ReviewStore(FileAdapter('reviews'))
release_store = ReleaseStore(FileAdapter('releases'), review_store)
artist_store = ArtistStore(FileAdapter('artists'), release_store)

artists_before = artist_store.get_all()
print(f"Number of artists before collection: {len(artists_before)}")
print(f"Number of releases before collection: {sum(len(artist.releases) for artist in artists_before.values()) if artists_before else 0}")

# Count releases with dates already set
releases_with_dates_before = 0
releases_without_dates_before = 0
for artist in artists_before.values():
    for release in artist.releases:
        if release.date:
            releases_with_dates_before += 1
        else:
            releases_without_dates_before += 1
            
print(f"Number of releases with dates already set: {releases_with_dates_before}")
print(f"Number of releases without dates: {releases_without_dates_before}")

# Run the collection process
print("\nRunning collection process...")
service.collect_reviews()

# Print the state after collection
artists_after = artist_store.get_all()
print(f"Number of artists after collection: {len(artists_after)}")
print(f"Number of releases after collection: {sum(len(artist.releases) for artist in artists_after.values())}")

# Count releases with dates after
releases_with_dates_after = 0
releases_without_dates_after = 0
for artist in artists_after.values():
    for release in artist.releases:
        if release.date:
            releases_with_dates_after += 1
        else:
            releases_without_dates_after += 1
            
print(f"Number of releases with dates after collection: {releases_with_dates_after}")
print(f"Number of releases without dates after collection: {releases_without_dates_after}")
print(f"New dates added: {releases_with_dates_after - releases_with_dates_before}") 