from src.collector.entities.artist import Artist
from src.collector.entities.release import Release
from src.collector.use_cases.music_catalogue import MusicCatalogue

from src.common.crypto import calculate_hash


class MusicReleaseCataloger(MusicCatalogue):

    def __init__(self):

        super().__init__()
        self.artists = {}

    def add_release(self, raw_releases):
        for raw_release in raw_releases:

            artist = self.create_artist(raw_release)

            self.create_release(artist, raw_release)

        return self.artists

    def create_artist(self, raw_release) -> Artist:

        artist_name = raw_release.get('artist')
        artist_id = calculate_hash(artist_name)
        artist = self.artists[artist_id] = Artist(
            id=artist_id,
            name=artist_name,
            releases=[]
        )

        if not self.artists.get(artist_id):
            self.artists[artist_id] = artist

        return artist

    def create_release(self, artist: Artist, raw_release) -> Release:

        artist_name = artist.name
        release_name = super().format_release_name(raw_release.get('name'))
        release_id = calculate_hash(artist_name + release_name)

        existing_release = next((x for x in artist.releases if x.id == release_id), None)
        release = Release(
                id=calculate_hash(artist_name + release_name),
                name=release_name,
                reviews=[],
                date=raw_release.get('date'),
                type=raw_release.get('type'),
                spotify_url=raw_release.get('spotify_url'),
                total_tracks=raw_release.get('total_tracks'),
            )

        if not existing_release:
            artist.releases.append(release)
            self.artists[artist.id] = artist

        return release
