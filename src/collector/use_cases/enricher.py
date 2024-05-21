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
            tasks = []
            for artist_id, artist in enriched_artists.items():
                enrich_artist_task = self.enrich_artist(session, artist)
                tasks.append((enrich_artist_task, artist))
            responses = await asyncio.gather(*(task[0] for task in tasks))

            processing_tasks = [self.process_response(response, task[1]) for response, task in zip(responses, tasks)]
            processed_responses = await asyncio.gather(*processing_tasks)

            for processed_response in processed_responses:
                if processed_response.id == artist_id:
                    enriched_artists[artist_id] = processed_response

        end_time = time.time()

        print(f"Time taken: {end_time - start_time} seconds")

        return enriched_artists

    async def enrich_artist(self, session: aiohttp.ClientSession, artist: Artist) -> Artist:

        enriched_releases = []
        for release in artist.releases:
            if not release.date:
                enrichment_source = self.source(session)

                release_details = await enrichment_source.get_spotify_album(artist.name, release.name)
                release.type = release_details.type
                release.date = release_details.date
                release.total_tracks = release_details.total_tracks
                release.spotify_url = release_details.spotify_url

            enriched_releases.append(release)

        artist.releases = enriched_releases
        return artist

    def process_response(self, album, artist: Artist):
        self.source.get_release_from_album(album, artist)
