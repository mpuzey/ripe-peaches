import asyncio
import time
import random
from typing import Dict, List

import aiohttp

from src.collector.web.spotify import RateLimitError
from src.collector.web.spotify_album import SpotifyAlbum
from src.entities.artist import Artist
from src.entities.release import Release


class Enricher:
    # Maximum number of retry attempts for rate limit errors
    MAX_RETRIES = 15
    
    def __init__(self, source):
        self.source = source
        # Track current concurrency level
        self._current_concurrency = 10  # Start with high concurrency
        # Track if we're seeing rate limits
        self._rate_limited = False
        # Track statistics
        self.total_releases = 0
        self.releases_with_dates = 0
        self.releases_enriched = 0

    async def add_release_dates(self, artists: Dict[str, Artist]) -> Dict[str, Artist]:
        start_time = time.time()
        # Count initial statistics
        self.count_release_stats(artists)
        initial_releases_with_dates = self.releases_with_dates

        async with aiohttp.ClientSession() as session:
            enrichment_source = self.source(session)
            enriched_artists = await self.enrich_artists(artists, enrichment_source)

        # Count final statistics
        self.count_release_stats(enriched_artists)
        end_time = time.time()
        print(f"Time taken: {end_time - start_time} seconds")
        print(f"New dates added: {self.releases_with_dates - initial_releases_with_dates}")
        return enriched_artists

    def count_release_stats(self, artists: Dict[str, Artist]):
        """Count the number of releases and releases with dates"""
        self.total_releases = 0
        self.releases_with_dates = 0
        for artist_id, artist in artists.items():
            self.total_releases += len(artist.releases)
            for release in artist.releases:
                if release.date:
                    self.releases_with_dates += 1

    async def enrich_artists(self, artists, enrichment_source):
        """Enrich artists with release dates and other metadata"""
        enriched_artists = artists.copy()
        # Create a semaphore to limit concurrent requests
        semaphore = asyncio.Semaphore(self._current_concurrency)
        # Prepare tasks for enrichment
        tasks = self._create_enrichment_tasks(
            enriched_artists, semaphore, enrichment_source
        )
        # Process all artists with retries for rate limiting
        processed_responses = await asyncio.gather(*tasks)
        return self._update_artists_with_responses(enriched_artists, processed_responses)
    
    def _create_enrichment_tasks(self, artists, semaphore, enrichment_source):
        """Create tasks for artist enrichment, skipping those that don't need it"""
        tasks, skipped_count, needs_enrichment = self._prepare_enrichment_tasks(
            artists, semaphore, enrichment_source
        )
        self._log_enrichment_stats(skipped_count, needs_enrichment)
        return tasks
    
    def _log_enrichment_stats(self, skipped_count, needs_enrichment_count):
        """Log statistics about the enrichment process"""
        artists_to_enrich = needs_enrichment_count[1]
        releases_to_enrich = needs_enrichment_count[0]
        print(f"Skipping {skipped_count} artists that already have all releases enriched")
        print(f"Need to enrich {releases_to_enrich} releases from {artists_to_enrich} artists")

    def _prepare_enrichment_tasks(self, artists, semaphore, enrichment_source):
        """Create tasks for artist enrichment, skipping those that don't need it"""
        tasks = []
        skipped_count = 0
        needs_enrichment_count = [0, 0]  # [releases, artists]
        
        for artist_id, artist in artists.items():
            # Check if any release needs enrichment
            releases_needing_enrichment = [r for r in artist.releases if not r.date]
            if releases_needing_enrichment:
                needs_enrichment_count[0] += len(releases_needing_enrichment)
                needs_enrichment_count[1] += 1
                task = self.enrich_artist_with_retries(semaphore, enrichment_source, artist)
                tasks.append(task)
            else:
                skipped_count += 1
                # Just return the original artist since no enrichment is needed
                tasks.append(asyncio.create_task(asyncio.sleep(0, result=artist)))
        
        return tasks, skipped_count, needs_enrichment_count
    
    def _update_artists_with_responses(self, artists, responses):
        """Update the artists dictionary with enriched responses"""
        enriched_artists = artists.copy()
        for i, (artist_id, _) in enumerate(enriched_artists.items()):
            enriched_artists[artist_id] = responses[i]
        return enriched_artists

    async def enrich_artist_with_retries(self, semaphore, enrichment_source, artist: Artist):
        """Enriches an artist with retry logic for rate limit handling."""
        retries = 0
        # Make a copy of the artist to work with
        enriched_artist = artist.copy()
        # Get releases that need enrichment
        releases_to_enrich = [r for r in enriched_artist.releases if not r.date]
        # If no releases need enrichment, just return the artist
        if not releases_to_enrich:
            return enriched_artist
            
        # Try to enrich one release at a time until all are done
        while releases_to_enrich:
            await self._process_single_release(
                semaphore, enrichment_source, enriched_artist, 
                releases_to_enrich, retries
            )
        
        # Return the enriched artist after processing all releases
        return enriched_artist
    
    async def _process_single_release(self, semaphore, enrichment_source, 
                                    enriched_artist, releases_to_enrich, retries):
        """Process a single release with retry handling"""
        current_release = releases_to_enrich[0]
        try:
            await self._fetch_and_update_release(
                semaphore, enrichment_source, enriched_artist, current_release
            )
            # Remove this release from the list to enrich
            releases_to_enrich.pop(0)
        except RateLimitError as e:
            await self._handle_rate_limit(e, retries, enriched_artist)

    async def _fetch_and_update_release(self, semaphore, enrichment_source, 
                                       enriched_artist, current_release):
        """Fetch enrichment data for a release and update it"""
        async with semaphore:
            # Fetch the enrichment data for this specific release
            print(f"Need to enrich: {enriched_artist.name} - {current_release.name}")
            album_data = await enrichment_source.get_album(
                enriched_artist.name, current_release.name
            )
            await self._process_album_data(
                album_data, enrichment_source, enriched_artist
            )

    async def _process_album_data(self, album_data, enrichment_source, enriched_artist):
        """Process album data if available"""
        if album_data:
            release_details = await self.source.get_release_from_album(
                album_data, enriched_artist
            )
            self._update_release_with_details(enriched_artist, release_details)

    def _update_release_with_details(self, artist: Artist, release_details: Release):
        """Update a release with enrichment data"""
        for i, release in enumerate(artist.releases):
            if release.name == release_details.name:
                release.type = release_details.type
                release.date = release_details.date
                release.total_tracks = release_details.total_tracks
                release.spotify_url = release_details.spotify_url
                self.releases_enriched += 1
                break

    async def _handle_rate_limit(self, error: RateLimitError, retries: int, artist: Artist):
        """Handle rate limit errors with exponential backoff"""
        retries += 1
        self._rate_limited = True
        # Calculate backoff time
        sleep_time = self._calculate_backoff_time(error, retries)
        # Adjust concurrency if needed
        self._adjust_concurrency_if_needed(retries)
        # Handle max retries case
        if retries >= self.MAX_RETRIES:
            await self._handle_max_retries(artist)
            return self.MAX_RETRIES // 2  # Reset to half max retries
        else:
            await self._sleep_with_message(sleep_time, retries, artist)
            return retries

    def _calculate_backoff_time(self, error: RateLimitError, retries: int) -> float:
        """Calculate backoff time based on retry attempt"""
        if hasattr(error, 'retry_after') and error.retry_after:
            # Use Spotify's retry-after header if available
            base_retry = error.retry_after
        else:
            # Exponential backoff with a cap to avoid extreme values
            base_retry = min(30, 2 ** min(retries, 4))
        # Add jitter to avoid thundering herd
        jitter = random.uniform(0.1, 1.0)
        return base_retry + jitter

    def _adjust_concurrency_if_needed(self, retries: int):
        """Reduce concurrency if we're hitting too many retries"""
        if retries > 5 and self._current_concurrency > 2:
            self._current_concurrency -= 1
            print(f"Reducing concurrency to {self._current_concurrency} due to rate limits")

    async def _handle_max_retries(self, artist: Artist):
        """Handle the case when max retries is reached"""
        cool_down = 60  # 1 minute cool down
        print(f"Artist {artist.name} hit max retries. Extended cooldown for {cool_down} seconds.")
        await asyncio.sleep(cool_down)

    async def _sleep_with_message(self, sleep_time: float, retries: int, artist: Artist):
        """Sleep with an informative message"""
        print(f"Rate limit hit for artist {artist.name}. Retrying in {sleep_time:.2f}s (attempt {retries}/{self.MAX_RETRIES})")
        await asyncio.sleep(sleep_time)
