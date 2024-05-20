import asyncio

from typing import Dict

import aiohttp

from src.entities.artist import Artist


class Enricher:

    def __init__(self, source):
        self.source = source

    async def add_release_dates(self, artists: Dict[str, Artist]) -> Dict[str, Artist]:
        enriched_artists = artists.copy()

        async with aiohttp.ClientSession() as session:
            tasks = []
            for artist_id, artist in enriched_artists.items():
                enrich_artist_task = self.enrich_artist(session, artist)
                tasks.append(enrich_artist_task)
                # enriched_artist = await enrich_artist_task
                # enriched_artists[artist_id] = enriched_artist
            enriched_artists = await asyncio.gather(*tasks)

        return enriched_artists

    async def enrich_artist(self, session: aiohttp.ClientSession, artist: Artist) -> Artist:

        enriched_releases = []
        for release in artist.releases:
            if not release.date:
                enrichment_source = self.source(session)

                release_details = enrichment_source.get_release_details(artist.name, release.name)
                release.type = release_details.type
                release.date = release_details.date
                release.total_tracks = release_details.total_tracks
                release.spotify_url = release_details.spotify_url

            enriched_releases.append(release)

        artist.releases = enriched_releases
        yield artist
