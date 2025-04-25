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

    async def add_release_dates(self, artists: Dict[str, Artist]) -> Dict[str, Artist]:
        start_time = time.time()

        async with aiohttp.ClientSession() as session:
            enrichment_source = self.source(session)
            enriched_artists = await self.enrich_artists(artists, enrichment_source)

        end_time = time.time()

        print(f"Time taken: {end_time - start_time} seconds")

        return enriched_artists

    async def enrich_artists(self, artists, enrichment_source):
        enriched_artists = artists.copy()
        
        # Create a semaphore to limit concurrent requests
        semaphore = asyncio.Semaphore(self._current_concurrency)
        
        # Create tasks to process each artist
        tasks = []
        for artist_id, artist in enriched_artists.items():
            task = self.enrich_artist_with_retries(semaphore, enrichment_source, artist)
            tasks.append(task)
        
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
        
        while True:  # Keep trying until we succeed or explicitly decide to skip
            try:
                async with semaphore:
                    # Fetch the enrichment data for this artist
                    album_data = await self.fetch_enrichment_data(enrichment_source, artist)
                    
                    # Process the response and return the enriched artist
                    return await self.process_response(album_data, artist)
                    
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
                    print(f"Artist {artist.name} hit max retries. Extended cooldown for {cool_down} seconds.")
                    await asyncio.sleep(cool_down)
                    retries = self.MAX_RETRIES // 2  # Reset to half max retries to allow more attempts
                else:
                    print(f"Rate limit hit for artist {artist.name}. Retrying in {sleep_time:.2f}s (attempt {retries}/{self.MAX_RETRIES})")
                    await asyncio.sleep(sleep_time)

    @staticmethod
    async def fetch_enrichment_data(enrichment_source, artist: Artist):
        for release in artist.releases:
            if not release.date:
                return await enrichment_source.get_album(artist.name, release.name)
        return {}

    """
    Processes the response from the source (e.g. Spotify) and updates the artist's releases with the enriched release 
    details for the single release. Handles a single release being enriched without duplicating the release or removing
    other releases which may or may not have already been enriched. process_response is called for each response back 
    from Spotify (each release) so a call to it is not unique per artist.

    Args:
        album (str): The album name.
        artist (Artist): The artist object.

    Returns:
        Artist: The updated artist object with enriched release details.
    """
    async def process_response(self, album_from_source, artist: Artist) -> Artist:
        if not album_from_source:
            return artist

        release_details = await self.source.get_release_from_album(album_from_source, artist)

        enriched_releases = []
        for release in artist.releases:
            if release.name == release_details.name:
                release.type = release_details.type
                release.date = release_details.date
                release.total_tracks = release_details.total_tracks
                release.spotify_url = release_details.spotify_url

            enriched_releases.append(release)

        artist.releases = enriched_releases
        return artist
