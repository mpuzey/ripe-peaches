from src.collector.entities.artist import Artist


class Enricher:

    def __init__(self, source):
        self.source = source

    def add_release_dates(self, artists: [Artist]) -> [Artist]:
        enriched_artists = artists
        for artist in enriched_artists:
            enriched_releases = []
            for release in artist.releases:
                if not release.date:
                    release_details = self.source.get_release_details(artist.name, release.name)
                    release.type = release_details.type
                    release.date = release_details.date
                    release.total_tracks = release_details.total_tracks
                    release.spotify_url = release_details.spotify_url

                enriched_releases.append(release)

            enriched_artists.releases = enriched_releases

        return enriched_artists
