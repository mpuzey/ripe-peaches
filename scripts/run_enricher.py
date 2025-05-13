#!/usr/bin/env python3
"""
Run the enrichment process on existing artist/release data in the file store.
This script does NOT scrape or collect new data from Metacritic or AOTY.
"""
import os
from src.collector.service import EnricherService
from src.collector.use_cases.enricher import Enricher
from src.collector.web.spotify import Spotify

# Print Spotify credentials
print(f"Using SPOTIFY_CLIENT_ID: {os.environ.get('SPOTIFY_CLIENT_ID', 'Not set')[:5]}...")
print(f"Using SPOTIFY_CLIENT_SECRET: {os.environ.get('SPOTIFY_CLIENT_SECRET', 'Not set')[:5]}...")

# Create enricher with Spotify
enricher = Enricher(Spotify)

# Create the service
service = EnricherService(enricher)

# Run enrichment
service.enrich_stored_releases() 