import unittest
from typing import Any, Tuple

import aiohttp
import asyncio
import asynctest
from asynctest import MagicMock, CoroutineMock, patch
from unittest.mock import MagicMock

from src.collector.web.spotify import Spotify
from tests.unit_tests.collector.web.test_spotify_helper import AsyncContextManagerMock, \
    raise_content_type_error, MockClientResponse, search_by_artist_and_album_success_response


class TestSpotify(asynctest.TestCase):
    async def setUp(self):
        # Create session in the context of an event loop provided by asynctest
        self.session = aiohttp.ClientSession()

    async def tearDown(self):
        # Close the session properly
        await self.session.close()

    @patch('src.collector.web.spotify.Spotify._get_access_token')
    @asynctest.patch('src.collector.web.spotify.aiohttp.ClientSession.get', new_callable=AsyncContextManagerMock)
    async def test__spotify__Spotify__get_album__ReturnsSpotifyAlbum__WhenSessionGetIsSuccessful(
            self, mock_get, mock_get_access_token):
        # Mock the access token
        mock_get_access_token.return_value = "mock_access_token"
        
        # Create mock response with our test data
        json_data = search_by_artist_and_album_success_response()
        search_by_artist_response = MockClientResponse(json_data=json_data)

        # Mock the aiohttp client session get method
        mock_get.return_value.__aenter__.return_value = search_by_artist_response
        mock_get.return_value.__aexit__ = CoroutineMock()

        expected_album = json_data.get('albums').get('items')[0]
        
        # Initialize Spotify with our mock session
        spotify = Spotify(self.session)
        
        # Call the method under test
        album = await spotify.get_album('The Beatles', 'Now & Then [Single]')
        
        # Debug outputs
        print("Expected:", expected_album)
        print("Actual:", album)

        # Compare exact values to verify
        self.assertEqual(album, expected_album)
        

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
    @asynctest.patch('src.collector.web.spotify.aiohttp.ClientSession.get', new_callable=AsyncContextManagerMock)
    async def test__spotify__Spotify__get_album__ReturnsSpotifyAlbum__WhenUnexpectedMimeTypeErrorIsStatusReceivedFromSessionGet(
            self, mock_get, mock_get_access_token):
        # Mock the access token
        mock_get_access_token.return_value = "mock_access_token"

        search_by_artist_response = MagicMock()
        search_by_artist_response.json.side_effect = raise_content_type_error

        mock_get.return_value.__aenter__.return_value = search_by_artist_response

        spotify = Spotify(self.session)

        album = await spotify.get_album('The Beatles', 'Now & Then [Single]')

        assert album == {}
