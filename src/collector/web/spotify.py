import aiohttp
from urllib import parse
import json
import base64
import requests
from aiohttp import ContentTypeError

import constants
import string

from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_RESULTS_LIMIT
from src.collector.web.spotify_album import SpotifyAlbum
from src.entities.artist import Artist
from src.entities.external_release import ExternalRelease


class RateLimitError(Exception):
    """
    Exception raised when Spotify API rate limit is reached.
    """
    def __init__(self, message="Spotify API rate limit exceeded", retry_after=None):
        self.message = message
        self.retry_after = retry_after
        super().__init__(self.message)


class Spotify:

    def __init__(self, session):
        print(f"Initializing Spotify with Client ID length: {len(SPOTIFY_CLIENT_ID) if SPOTIFY_CLIENT_ID else 'None'}, Secret length: {len(SPOTIFY_CLIENT_SECRET) if SPOTIFY_CLIENT_SECRET else 'None'}")
        self.access_token = self._get_access_token()
        self.session = session

    @staticmethod
    def _get_access_token():
        client_id = SPOTIFY_CLIENT_ID
        client_secret = SPOTIFY_CLIENT_SECRET
        
        if not client_id or not client_secret:
            print("WARNING: Missing Spotify credentials!")
            print(f"Client ID: {'Present' if client_id else 'Missing'}")
            print(f"Client Secret: {'Present' if client_secret else 'Missing'}")
            return None
        
        encoded = Spotify._encode_client_credentials(client_id, client_secret)
        return Spotify._request_access_token(encoded)

    @staticmethod
    def _encode_client_credentials(client_id, client_secret):
        creds = f'{client_id}:{client_secret}'
        encoded = base64.b64encode(creds.encode('utf-8')).decode('utf-8')
        return f'Basic {encoded}'

    @staticmethod
    def _request_access_token(encoded):
        try:
            resp = requests.post(
                'https://accounts.spotify.com/api/token',
                data={'grant_type': 'client_credentials'},
                headers={'Authorization': encoded}
            )
            
            if resp.status_code != 200:
                print(f"Spotify authentication failed with status code: {resp.status_code}")
                print(f"Response: {resp.text}")
                return None
            
            access_token = json.loads(resp.text).get('access_token')
            print(f"Successfully obtained Spotify access token: {access_token[:5]}...")
            return access_token
        except Exception as e:
            print(f"Error getting Spotify access token: {e}")
            return None

    async def get_album(self, artist_name, album_name):
        print('enriching ' + artist_name + ' release: ' + album_name + ' from Spotify')
        if not self.access_token:
            print("No access token available - authentication failed")
            return {}
        try:
            search_result = await self.search_by_album_and_artist(artist_name, album_name)
            if not search_result['albums']['items']:
                search_result = await self.search_by_album(artist_name, album_name)
            album_id = self._find_best_album_id(search_result, artist_name, album_name)
            if album_id:
                return await self.get_album_details(album_id)
            print("No matching album found.")
            return {}
        except RateLimitError as e:
            raise

    def _find_best_album_id(self, search_result, artist_name, album_name):
        items = search_result.get('albums', {}).get('items', []) if search_result else []
        for album in items:
            if (
                album.get('name', '').lower() == album_name.lower() and
                any(a['name'].lower() == artist_name.lower() for a in album.get('artists', [])) and
                album.get('album_type') == 'album'
            ):
                return album['id']
        return None

    async def get_album_details(self, album_id):
        url = f'https://api.spotify.com/v1/albums/{album_id}'
        async with self.session.get(
            url,
            headers={'Authorization': f'Bearer {self.access_token}'}
        ) as response:
            if response.status != 200:
                print(f'Error fetching album details: {response.status} - {response.reason}')
                return None
            try:
                return await response.json()
            except ContentTypeError as e:
                print(f'Error parsing album details: {e}')
                return None

    @staticmethod
    async def get_release_from_album(spotify_album, artist: Artist) -> ExternalRelease:
        release_date = spotify_album.get('release_date')
        album_type = spotify_album.get('album_type')
        total_tracks = spotify_album.get('total_tracks')
        spotify_url = Spotify._get_spotify_url(spotify_album)
        images = spotify_album.get('images', [])
        cover_url = images[0]['url'] if images else None
        return ExternalRelease(
            name=spotify_album.get('name'),
            artist=artist.name,
            date=release_date,
            type=album_type,
            total_tracks=total_tracks,
            spotify_url=spotify_url,
            cover_url=cover_url
        )

    @staticmethod
    def _get_spotify_url(spotify_album):
        external_urls = spotify_album.get('external_urls')
        if external_urls:
            return external_urls.get('spotify')
        return None

    async def search_by_album_and_artist(self, artist_name, album_name):
        search = 'https://api.spotify.com/v1/search'
        query = f'album:"{album_name}" artist:{artist_name}'
        
        async with self.session.get(
            search,
            headers={'Authorization': f'Bearer {self.access_token}'},
            params=[('type', 'album'), ('q', query), ('limit', SPOTIFY_RESULTS_LIMIT)]
        ) as response:
            return await self._parse_search_response(response, artist_name, album_name)

    async def search_by_album(self, artist_name, album_name):
        search = 'https://api.spotify.com/v1/search'
        query = f'album:"{album_name}"'
        
        async with self.session.get(
            search,
            headers={'Authorization': f'Bearer {self.access_token}'},
            params=[('type', 'album'), ('q', query), ('limit', SPOTIFY_RESULTS_LIMIT)]
        ) as response:
            return await self._parse_search_response(response, artist_name, album_name, by_artist=False)
            
    async def _parse_search_response(self, response, artist_name, album_name, by_artist=True):
        result = {'albums': {'items': []}}
        if response.status == 429:
                retry_after = int(response.headers.get('Retry-After', 30))
                raise RateLimitError(
                    f'Spotify rate limit hit for artist: {artist_name}, album: {album_name}',
                    retry_after=retry_after
                )
        if response.status != 200:
            print(f'Error: {response.status} - {response.reason}')
            return result
            try:
                response_json = await response.json()
            items = response_json.get('albums', {}).get('items', [])
            if by_artist:
                filtered = [a for a in items if a['name'].lower() == album_name.lower()]
                result['albums']['items'] = filtered
            else:
                filtered = [a for a in items if any(artist_name.lower() in artist['name'].lower() for artist in a['artists']) and a['name'].lower() == album_name.lower()]
                result['albums']['items'] = filtered
            except ContentTypeError as e:
                print(f'Error parsing response: {e}')
        return result

    @staticmethod
    async def build_external_release(spotify_album, artist) -> ExternalRelease:
        release_date = spotify_album.get('release_date')
        album_type = spotify_album.get('album_type')
        total_tracks = spotify_album.get('total_tracks')
        spotify_url = Spotify._get_spotify_url(spotify_album)

        return ExternalRelease(
            name=spotify_album.get('name'),
            artist=artist.name,
            date=release_date,
            type=album_type,
            total_tracks=total_tracks,
            spotify_url=spotify_url
        )

    def get_releases(self) -> [ExternalRelease]:
        print('Fetching recent releases from Spotify...')
        external_releases = []
        for char in string.ascii_lowercase:
            external_releases.extend(self._fetch_releases_for_char(char))
        
        return self._parse_releases(external_releases)

    def _fetch_releases_for_char(self, char):
        char_releases = []
        next_page = constants.SPOTIFY_NEW_RELEASE_SEARCH.format(char=char)
        
        while next_page:
            offset = dict(parse.parse_qsl(parse.urlsplit(next_page).query)).get('offset', 0)
            if int(offset) >= 10000:
                break
                
            response = requests.get(
                next_page, 
                headers={'Authorization': f'Bearer {self.access_token}'}
            ).json()
            
            new_items, next_page = self._parse_response(response)
            if new_items:
                char_releases.extend(new_items)
                
        return char_releases

    @staticmethod
    def _parse_response(response):
        albums = response.get('albums')
        if not albums:
            return None, None

        items = albums.get('items')
        valid_items = [item for item in items if item]
        return valid_items, albums.get('next')

    @staticmethod
    def _parse_releases(external_releases) -> [ExternalRelease]:
        releases = []
        for external_release in external_releases:
            release = Spotify._create_release_from_external(external_release)
            releases.append(release)

        print('Finished fetching recent releases from Spotify')
        return releases

    @staticmethod
    def _create_release_from_external(external_release) -> ExternalRelease:
        images = external_release.get('images', [])
        cover_url = images[0]['url'] if images else None
        return ExternalRelease(
            name=external_release.get('name'),
            artist=external_release.get('artists')[0].get('name'),
            date=external_release.get('release_date'),
            type=external_release.get('type'),
            spotify_url=external_release.get('external_urls').get('spotify'),
            total_tracks=external_release.get('total_tracks'),
            cover_url=cover_url
        )
