from typing import Dict
from src.collector.entities.artist import Artist


class Enricher:

    def __init__(self, source):
        self.source = source

    def add_release_dates(self, artists: Dict[str, Artist]) -> Dict[str, Artist]:
        enriched_artists = artists
        for artist_id, artist in enriched_artists.items():
            enriched_releases = []
            for release in artist.releases:
                if not release:
                    # TODO: This needs looking into - how have we got a data integrity issue?
                    print(f'A release for {artist.name} could not be located')
                    continue
                if not release.date:
                    release_details = self.source.get_release_details(artist.name, release.name)
                    release.type = release_details.type
                    release.date = release_details.date
                    release.total_tracks = release_details.total_tracks
                    release.spotify_url = release_details.spotify_url

                enriched_releases.append(release)

            artist.releases = enriched_releases
            enriched_artists[artist_id] = artist

        return enriched_artists
