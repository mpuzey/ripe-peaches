import asyncio
import time
import random
from typing import Dict

import aiohttp

from src.collector.web.spotify import RateLimitError
from src.collector.web.spotify_album import SpotifyAlbum
from src.entities.artist import Artist


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
        enriched_artists = artists.copy()
        
        # Create a semaphore to limit concurrent requests
        semaphore = asyncio.Semaphore(self._current_concurrency)
        
        # Skip artists with all releases already enriched
        tasks = []
        skipped_count = 0
        needs_enrichment_count = 0
        
        for artist_id, artist in enriched_artists.items():
            # Check if any release needs enrichment
            releases_needing_enrichment = [r for r in artist.releases if not r.date]
            
            if releases_needing_enrichment:
                needs_enrichment_count += len(releases_needing_enrichment)
                task = self.enrich_artist_with_retries(semaphore, enrichment_source, artist)
                tasks.append(task)
            else:
                skipped_count += 1
                # Just return the original artist since no enrichment is needed
                tasks.append(asyncio.create_task(asyncio.sleep(0, result=artist)))
        
        print(f"Skipping {skipped_count} artists that already have all releases enriched")
        print(f"Need to enrich {needs_enrichment_count} releases from {len(tasks) - skipped_count} artists")
        
        # Process all artists with retries for rate limiting
        processed_responses = await asyncio.gather(*tasks)
        
        # Update the artists dictionary with the enriched artists
        for i, (artist_id, _) in enumerate(enriched_artists.items()):
            enriched_artists[artist_id] = processed_responses[i]

        return enriched_artists

    async def enrich_artist_with_retries(self, semaphore, enrichment_source, artist: Artist):
        """
        Enriches an artist with retry logic for rate limit handling.
        
        Args:
            semaphore: Semaphore to limit concurrent requests
            enrichment_source: The data source for enrichment
            artist: The artist to enrich
            
        Returns:
            Artist: The enriched artist after successful processing
        """
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
            current_release = releases_to_enrich[0]
            
            try:
                async with semaphore:
                    # Fetch the enrichment data for this specific release
                    print(f"Need to enrich: {enriched_artist.name} - {current_release.name}")
                    album_data = await enrichment_source.get_album(enriched_artist.name, current_release.name)
                    
                    # Process the response
                    if album_data:
                        release_details = await self.source.get_release_from_album(album_data, enriched_artist)
                        
                        # Update the release with enrichment data
                        for i, release in enumerate(enriched_artist.releases):
                            if release.name == release_details.name:
                                release.type = release_details.type
                                release.date = release_details.date
                                release.total_tracks = release_details.total_tracks
                                release.spotify_url = release_details.spotify_url
                                self.releases_enriched += 1
                                break
                    
                    # Remove this release from the list to enrich
                    releases_to_enrich.pop(0)
                    # Reset retries for the next release
                    retries = 0
                    
            except RateLimitError as e:
                retries += 1
                self._rate_limited = True
                
                # Calculate backoff time based on retry attempt and Spotify's guidance
                if hasattr(e, 'retry_after') and e.retry_after:
                    # Use Spotify's retry-after header if available
                    base_retry = e.retry_after
                else:
                    # Exponential backoff with a cap to avoid extreme values
                    base_retry = min(30, 2 ** min(retries, 4))
                
                # Add jitter to avoid thundering herd
                jitter = random.uniform(0.1, 1.0)
                sleep_time = base_retry + jitter
                
                # If we're hitting a lot of retries, reduce concurrency
                if retries > 5 and self._current_concurrency > 2:
                    self._current_concurrency -= 1
                    print(f"Reducing concurrency to {self._current_concurrency} due to rate limits")
                
                # If we've hit MAX_RETRIES, cool down significantly but don't give up
                if retries >= self.MAX_RETRIES:
                    cool_down = 60  # 1 minute cool down
                    print(f"Artist {enriched_artist.name} hit max retries. Extended cooldown for {cool_down} seconds.")
                    await asyncio.sleep(cool_down)
                    retries = self.MAX_RETRIES // 2  # Reset to half max retries to allow more attempts
                else:
                    print(f"Rate limit hit for artist {enriched_artist.name}. Retrying in {sleep_time:.2f}s (attempt {retries}/{self.MAX_RETRIES})")
                    await asyncio.sleep(sleep_time)

        # Return the enriched artist after processing all releases
        return enriched_artist
