from src.collector.use_cases.collector import Collector

from src.common.crypto import calculate_hash


class MusicReleaseScraper(Collector):

    def __init__(self):
        self.raw_releases = []
        self.artists = {}

    def collect(self, source, **kwargs):

        releases = source.get_releases()

        if not releases:
            print('No releases available for the following publication: %s' % repr(source))

        self.raw_releases.extend(releases)

    def parse(self):
        for raw_release in self.raw_releases:

            artist_id = self._build_artist(raw_release)

            self._build_release(artist_id, raw_release)

        return self.artists

    def _build_artist(self, raw_release):

        artist_name = raw_release.get('artist')
        artist_id = calculate_hash(artist_name)

        self.artists[artist_id] = {
            'id': artist_id,
            'name': artist_name,
            'releases': {}
        }

        return artist_id

    def _build_release(self, artist_id, raw_release):

        artist_name = raw_release.get('artist')
        release_name = _format_release_name(raw_release.get('name'))

        release_id = calculate_hash(artist_name + release_name)

        self.artists[artist_id]['releases'][release_id] = {
            'id': calculate_hash(artist_name + release_name),
            'name': release_name,
            'date': raw_release.get('date'),
            'type': raw_release.get('type'),
            'spotify_url': raw_release.get('spotify_url'),
            'total_tracks': raw_release.get('total_tracks'),
            'reviews': {}
        }

        return release_id


def _format_release_name(name):

    formatted_name = name.replace('and', '&').title()

    return formatted_name
