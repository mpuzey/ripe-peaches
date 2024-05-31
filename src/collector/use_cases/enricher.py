import asyncio
import time

from typing import Dict

import aiohttp

from src.collector.web.spotify_album import SpotifyAlbum
from src.entities.artist import Artist


class Enricher:

    def __init__(self, source):
        self.source = source

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

        tasks = []
        for artist_id, artist in enriched_artists.items():
            fetch_enrichment_data_task = self.fetch_enrichment_data(enrichment_source, artist)
            tasks.append((fetch_enrichment_data_task, artist))
        responses = await asyncio.gather(*(task[0] for task in tasks))

        processing_tasks = [self.process_response(response, task[1]) for response, task in zip(responses, tasks)]
        processed_responses = await asyncio.gather(*processing_tasks)

        for processed_response in processed_responses:
            if processed_response.id == artist_id:
                enriched_artists[artist_id] = processed_response

        return enriched_artists

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
