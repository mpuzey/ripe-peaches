import unittest
from typing import Any, Tuple

import aiohttp
import asynctest
from aiohttp import ContentTypeError
from asynctest import MagicMock, CoroutineMock

from src.collector.web.spotify import Spotify

from unittest.mock import patch, MagicMock
from asynctest import TestCase

from tests.unit_tests.collector.web.test_spotify_helper import MockClientResponse, AsyncContextManagerMock, \
    raise_content_type_error, CustomClientSession


class TestSpotify(asynctest.TestCase):
    def setUp(self):
        self.session = aiohttp.ClientSession()

    def tearDown(self):
        self.loop.run_until_complete(self.session.close())


    @asynctest.patch('src.collector.web.spotify.aiohttp.ClientSession.get', new_callable=AsyncContextManagerMock)
    @asynctest.patch('src.collector.web.spotify.requests.post')
    async def test__spotify__Spotify__get_spotify_album__ReturnsSpotifyAlbum__WhenSessionGetIsSuccessful(
            self, mock_post, mock_get):
        authorization_response = MagicMock()
        authorization_response.text = '{"access_token": "mock_access_token"}'
        mock_post.return_value = authorization_response

        search_by_artist_response = MagicMock()
        search_by_artist_response.json = CoroutineMock()

        search_by_artist_response = MockClientResponse(json_data={"albums": {"items": []}})

        mock_get.return_value.__aenter__.return_value = search_by_artist_response
        mock_get.return_value.__aexit__ = CoroutineMock()

        expected_album = {'name': 'Now & Then [Single]', 'artist': 'The Beatles'}

        spotify = Spotify(self.session)

        album = await spotify.get_spotify_album('The Beatles', 'Now & Then [Single]')

        assert album == expected_album

    # @asynctest.patch('src.collector.web.spotify.aiohttp.ClientSession', new=CustomClientSession)
    # @asynctest.patch('src.collector.web.spotify.requests.post')
    # async def test__spotify__Spotify__get_spotify_album__ReturnsSpotifyAlbum__WhenUnexpectedMimeTypeErrorIsStatusReceivedFromSessionGet(
    #         self, mock_post):
    #
    #     authorization_response = MagicMock()
    #     authorization_response.text = '{"access_token": "mock_access_token"}'
    #     mock_post.return_value = authorization_response
    #
    #     # Set the get method of self.session to a CoroutineMock that raises a ContentTypeError
    #     self.session.get = CoroutineMock(side_effect=ContentTypeError(MagicMock(), MagicMock()))
    #
    #     expected_album = {'name': 'Now & Then [Single]', 'artist': 'The Beatles'}
    #
    #     spotify = Spotify(self.session)
    #
    #     album = await spotify.get_spotify_album('The Beatles', 'Now & Then [Single]')
    #
    #     assert album == expected_album

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
    @asynctest.patch('src.collector.web.spotify.aiohttp.ClientSession.get', new_callable=AsyncContextManagerMock)
    @asynctest.patch('src.collector.web.spotify.requests.post')
    async def test__spotify__Spotify__get_spotify_album__ReturnsSpotifyAlbum__WhenUnexpectedMimeTypeErrorIsStatusReceivedFromSessionGet(
            self, mock_post, mock_get):
        authorization_response = MagicMock()
        authorization_response.text = '{"access_token": "mock_access_token"}'
        mock_post.return_value = authorization_response

        search_by_artist_response = MagicMock()
        search_by_artist_response.json = CoroutineMock()
        # search_by_artist_response.json.side_effect = raise_content_type_error

        # TODO: does response.json() raise the exception or does session.get()?

        # Create an instance of MockClientResponse with the JSON data you want response.json() to return
        # TODO: note that this is probably the wrong approach because if we are getting into the .json() call in the try
        #       then that show that we have not raised the ContentTypeError exception on the session.get with statement
        search_by_artist_response = MockClientResponse(json_data={"albums": {"items": []}})

        # Mock the __aenter__ and __aexit__ methods
        mock_get.return_value.__aenter__.return_value = search_by_artist_response
        mock_get.return_value.__aexit__ = CoroutineMock()

        expected_album = {'name': 'Now & Then [Single]', 'artist': 'The Beatles'}

        spotify = Spotify(self.session)

        album = await spotify.get_spotify_album('The Beatles', 'Now & Then [Single]')

        assert album == expected_album