# from src.collector.entities.artist import Artist
# from src.collector.entities.release import Release
# from src.collector.use_cases.librarian import Librarian
# from src.collector.entities.external_release import ExternalRelease
#
# from src.common.crypto import calculate_hash
#
#
# class MusicReleaseCataloger(Librarian):
#
#     def __init__(self, catalog):
#         self.catalog = catalog
#         self.artists = {}
#
#     def add_reviews(self, raw_releases):
#         raise NotImplemented
#
#     def add_releases(self, raw_releases):
#         for raw_release in raw_releases:
#
#             artist = self._create_artist(raw_release)
#
#             self._create_release(artist, raw_release)
#
#         return self.artists
#
#     def format_release_name(self, name: str) -> str:
#         formatted_name = name.replace('and', '&').title()
#         return formatted_name
#
#     def _create_artist(self, external_release: ExternalRelease) -> Artist:
#
#         artist_name = external_release.get('artist')
#         artist_id = calculate_hash(artist_name)
#         artist = self.artists[artist_id] = Artist(
#             id=artist_id,
#             name=artist_name,
#             releases=[]
#         )
#
#         if not self.artists.get(artist_id):
#             self.artists[artist_id] = artist
#
#         return artist
#
#     def _create_release(self, artist: Artist, raw_release) -> Release:
#
#         artist_name = artist.name
#         release_name = super().format_release_name(raw_release.get('name'))
#         release_id = calculate_hash(artist_name + release_name)
#
#         existing_release = next((x for x in artist.releases if x.id == release_id), None)
#         release = Release(
#                 id=calculate_hash(artist_name + release_name),
#                 name=release_name,
#                 reviews=[],
#                 date=raw_release.get('date'),
#                 type=raw_release.get('type'),
#                 spotify_url=raw_release.get('spotify_url'),
#                 total_tracks=raw_release.get('total_tracks'),
#             )
#
#         if not existing_release:
#             artist.releases.append(release)
#             self.artists[artist.id] = artist
#
#         return release
