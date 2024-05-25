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
        enriched_artists = artists.copy()

        start_time = time.time()

        async with aiohttp.ClientSession() as session:
            enrichment_source = self.source(session)

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

        end_time = time.time()

        print(f"Time taken: {end_time - start_time} seconds")

        return enriched_artists

    @staticmethod
    async def fetch_enrichment_data(enrichment_source, artist: Artist):
        for release in artist.releases:
            if not release.date:
                return await enrichment_source.get_spotify_album(artist.name, release.name)
        return {}

    """
    Process the response from the source and update the artist's releases with the enriched release details.

    Args:
        album (str): The album name.
        artist (Artist): The artist object.

    Returns:
        Artist: The updated artist object with enriched release details.

    TODO:
        - Handle multiple releases being enriched without duplicating or removing other releases which have already
          been enriched. process_response is called for each response back from Spotify (each release) so is not unique
          per artist.
    """
    def process_response(self, album, artist: Artist) -> Artist:
        if not album:
            return artist

        release_details = self.source.get_release_from_album(album, artist)

        enriched_releases = []
        # TODO: need to be able to handle multiple releases being enriched without duplicating or removing other
        #  releases which have already been enriched. process_response is called for each response back from Spotify
        #  (each release) so is not unique per artist.
        for release in artist.releases:
            if release.name == release_details.name:
                release.type = release_details.type
                release.date = release_details.date
                release.total_tracks = release_details.total_tracks
                release.spotify_url = release_details.spotify_url

            enriched_releases.append(release)

        artist.releases = enriched_releases
        return artist
