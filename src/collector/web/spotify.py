import os
from ssl import SSLEOFError
from urllib import parse
import json
import base64
import requests
from aiohttp import ContentTypeError

import constants
import string
import aiohttp
from typing import Coroutine

from src.collector.web.spotify_album import SpotifyAlbum
from src.entities.artist import Artist
from src.entities.external_release import ExternalRelease


class Spotify:

    def __init__(self, session):
        self.access_token = self._get_access_token()
        self.session = session

    @staticmethod
    def _get_access_token():
        client_id = os.environ.get('SPOTIFY_CLIENT_ID')
        client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')
        client_details = '%s:%s' % (client_id, client_secret)
        encoded_client_details = base64.b64encode(client_details.encode('utf-8')).decode('utf-8')
        details = 'Basic %s' % encoded_client_details

        authorization_response = requests.post('https://accounts.spotify.com/api/token',
                                               data={'grant_type': 'client_credentials'},
                                               headers={'Authorization': details})
        print(authorization_response.text)
        access_token = json.loads(authorization_response.text).get('access_token')

        return access_token

    async def get_spotify_album(self, artist_name, album_name):  # -> Coroutine[None, None, SpotifyAlbum]:

        print('enriching ' + artist_name + ' release: ' + album_name + 'from Spotify')
        spotify_album = await self.search_by_album_and_artist(artist_name, album_name)

        if not spotify_album:
            spotify_album = await self.search_by_album(artist_name, album_name)

        return spotify_album

    async def get_release_from_album(self, spotify_album, artist: Artist):  # -> Coroutine[None, None, ExternalRelease]:
        return await self.build_external_release(spotify_album, artist)

    async def search_by_album_and_artist(self, artist_name, album_name):
        search = 'https://api.spotify.com/v1/search'
        query = f'album:"{album_name}"+artist:"{artist_name}"'

        spotify_album = {}

        try:
            async with (self.session.get(search,
                                         headers={'Authorization': 'Bearer %s' % self.access_token},
                                         params=[('type', 'album'), ('q', query)])
                        as response):
                response_json = await response.json()
                # response_status_code = response.status
                # response_reason = response.reason
                # if response_status_code != 200:
                #     print(f'Error: {response_status_code} - {response_reason}')
                #     return spotify_album

            for album in response_json['albums']['items']:
                if album['name'].lower() == album_name.lower():
                    return album

        except ContentTypeError as e:
            print(e)

        return spotify_album

    async def search_by_album(self, artist_name, album_name):
        search = 'https://api.spotify.com/v1/search'
        query = f'album:"{album_name}"'

        async with self.session.get(search,
                                    headers={'Authorization': 'Bearer %s' % self.access_token},
                                    params=[('type', 'album'), ('q', query)]) as response:
            response_json = await response.json()
        spotify_album = {}
        for album in response_json['albums']['items']:
            for artist in album['artists']:
                if artist['name'] in artist_name and album['name'].lower() == album_name.lower():
                    spotify_album = album
                    break

        return spotify_album

    @staticmethod
    async def build_external_release(spotify_album, artist) -> ExternalRelease:
        release_date = spotify_album.get('release_date')
        album_type = spotify_album.get('album_type')
        total_tracks = spotify_album.get('total_tracks')
        external_urls = spotify_album.get('external_urls')
        spotify_url = None
        if external_urls:
            spotify_url = external_urls.get('spotify')

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
        wildcard_chars = list(string.ascii_lowercase)
        for char in wildcard_chars:
            next_page = constants.SPOTIFY_NEW_RELEASE_SEARCH.format(char=char)
            while next_page:
                offset = dict(parse.parse_qsl(parse.urlsplit(next_page).query)).get('offset', 0)
                if int(offset) >= 10000:
                    break
                response = requests.get(next_page, headers={'Authorization': 'Bearer %s' % self.access_token}).json()
                new_items, next_page = self._parse_response(response)
                if new_items:
                    external_releases.extend(new_items)

        return self._parse_releases(external_releases)

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
            release = ExternalRelease(
                name=external_release.get('name'),
                artist=external_release.get('artists')[0].get('name'),
                date=external_release.get('release_date'),
                type=external_release.get('type'),
                spotify_url=external_release.get('external_urls').get('spotify'),
                total_tracks=external_release.get('total_tracks')
            )
            releases.append(release)

        print('Finished fetching recent releases from Spotify')
        return releases
