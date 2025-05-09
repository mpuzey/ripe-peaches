import unittest
from typing import Any, Tuple

import aiohttp
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock

from src.collector.web.spotify import Spotify
from tests.unit_tests.collector.web.test_spotify_helper import AsyncContextManagerMock, \
    raise_content_type_error, MockClientResponse, search_by_artist_and_album_success_response
from src.entities.artist import Artist
from src.entities.release import Release
from src.collector.use_cases.enricher import Enricher


class TestSpotify(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.session = aiohttp.ClientSession()

    async def asyncTearDown(self):
        await self.session.close()

    @patch('src.collector.web.spotify.Spotify._get_access_token')
    @patch('src.collector.web.spotify.Spotify.get_album_details', new_callable=AsyncMock)
    @patch('src.collector.web.spotify.aiohttp.ClientSession.get', new_callable=lambda: AsyncContextManagerMock())
    async def test__spotify__Spotify__get_album__ReturnsSpotifyAlbum__WhenSessionGetIsSuccessful(
            self, mock_get, mock_get_album_details, mock_get_access_token):
        mock_get_access_token.return_value = "mock_access_token"
        json_data = search_by_artist_and_album_success_response()
        search_by_artist_response = MockClientResponse(json_data=json_data)
        mock_get.return_value.__aenter__.return_value = search_by_artist_response
        expected_album_details = {"name": "Now & Then [Single]", "id": "dummy_id", "images": [{"url": "https://mock.cover/nowandthen.jpg"}]}
        mock_get_album_details.return_value = expected_album_details
        spotify = Spotify(self.session)
        album = await spotify.get_album('The Beatles', 'Now & Then [Single]')
        self.assertEqual(album, expected_album_details)
        # Check cover_url propagation if present
        if 'images' in album and album['images']:
            self.assertEqual(album['images'][0]['url'], 'https://mock.cover/nowandthen.jpg')

    """
    Test case for the `get_spotify_album` method of the `Spotify` class.

    This test case verifies that the `get_spotify_album` method returns a `SpotifyAlbum` object when an
    `UnexpectedMimeTypeError` is raised during the `Session.get` call.

    Parameters:
        - mock_post (MagicMock): A mock object for the `requests.post` function.
        - mock_get (MagicMock): A mock object for the `aiohttp.ClientSession.get` method.

    Returns:
        - None

    Raises:
        - AssertionError: If the returned `album` does not match the expected `expected_album`.
    """
    @patch('src.collector.web.spotify.Spotify._get_access_token')
    @patch('src.collector.web.spotify.aiohttp.ClientSession.get', new_callable=lambda: AsyncContextManagerMock())
    async def test__spotify__Spotify__get_album__ReturnsSpotifyAlbum__WhenUnexpectedMimeTypeErrorIsStatusReceivedFromSessionGet(
            self, mock_get, mock_get_access_token):
        mock_get_access_token.return_value = "mock_access_token"
        search_by_artist_response = MagicMock()
        search_by_artist_response.json.side_effect = raise_content_type_error
        mock_get.return_value.__aenter__.return_value = search_by_artist_response
        spotify = Spotify(self.session)
        album = await spotify.get_album('The Beatles', 'Now & Then [Single]')
        assert album == {}

    def test__spotify__create_release_from_external__sets_cover_url(self):
        mock_album = {
            'name': 'Now & Then [Single]',
            'artists': [{'name': 'The Beatles'}],
            'release_date': '2023-11-02',
            'type': 'album',
            'external_urls': {'spotify': 'https://open.spotify.com/album/2qQP2NgOoH6HqknnbpJmIk?si=GEiQbz98T5CwWiU9DqPlNQ'},
            'total_tracks': 2,
            'images': [
                {'height': 640, 'url': 'https://mock.cover/nowandthen.jpg', 'width': 640}
            ]
        }
        release = Spotify._create_release_from_external(mock_album)
        self.assertEqual(release.cover_url, 'https://mock.cover/nowandthen.jpg')

    def test_enricher_propagates_cover_url(self):
        # Simulate a Spotify enrichment returning a Release with cover_url
        artist = Artist('1', 'Test Artist', [Release('Test Release', 'Test Release', [], None, None, None, None, None)])
        mock_release = Release('Test Release', 'Test Release', [], '2022-01-01', 'album', 10, 'https://spotify.com', 'https://mock.cover/nowandthen.jpg')
        mock_source = MagicMock()
        mock_source.get_release_from_album = AsyncMock(return_value=mock_release)
        enricher = Enricher(mock_source)
        enricher._update_release_with_details(artist, mock_release)
        self.assertEqual(artist.releases[0].cover_url, 'https://mock.cover/nowandthen.jpg')
