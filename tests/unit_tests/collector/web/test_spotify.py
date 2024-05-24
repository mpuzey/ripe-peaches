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
    raise_content_type_error


class TestSpotify(asynctest.TestCase):
    def setUp(self):
        self.session = aiohttp.ClientSession()

    def tearDown(self):
        self.loop.run_until_complete(self.session.close())

    # @patch('src.collector.web.spotify.aiohttp.ClientSession.get')
    # @patch('src.collector.web.spotify.requests.post')
    # async def test__spotify__Spotify__get_spotify_album__ReturnsSpotifyAlbum__WhenUnexpectedMimeTypeErrorIsStatusReceivedFromSessionGet(
    #         self, mock_post, mock_get):
    #
    #     authorization_response = MagicMock()
    #     authorization_response.text = '{"access_token": "mock_access_token"}'
    #     mock_post.return_value = authorization_response
    #
    #     search_by_artist_response = MagicMock()
    #     search_by_artist_response.json = CoroutineMock()
    #     search_by_artist_response.json.side_effect = ContentTypeError(MagicMock(), (MagicMock()))
    #
    #     # Set the return value of mock_get to an instance of MockClientResponse
    #     mock_get.return_value = MockClientResponse(search_by_artist_response)
    #
    #     expected_album = {'name': 'Now & Then [Single]', 'artist': 'The Beatles'}
    #
    #     spotify = Spotify(self.session)
    #
    #     album = await spotify.get_spotify_album('The Beatles', 'Now & Then [Single]')
    #
    #     assert album == expected_album


    # @asynctest.patch('src.collector.web.spotify.aiohttp.ClientSession.get', new_callable=asynctest.CoroutineMock)
    # @asynctest.patch('src.collector.web.spotify.requests.post')
    # async def test__spotify__Spotify__get_spotify_album__ReturnsSpotifyAlbum__WhenUnexpectedMimeTypeErrorIsStatusReceivedFromSessionGet(
    #         self, mock_post, mock_get):
    #
    #     authorization_response = MagicMock()
    #     authorization_response.text = '{"access_token": "mock_access_token"}'
    #     mock_post.return_value = authorization_response
    #
    #     search_by_artist_response = MagicMock()
    #     search_by_artist_response.json = CoroutineMock()
    #     search_by_artist_response.json.side_effect = ContentTypeError(MagicMock(), (MagicMock()))
    #
    #     # Mock the __aenter__ and __aexit__ methods
    #     mock_get.return_value.__aenter__.return_value = search_by_artist_response
    #     mock_get.return_value.__aexit__ = CoroutineMock()
    #
    #     expected_album = {'name': 'Now & Then [Single]', 'artist': 'The Beatles'}
    #
    #     spotify = Spotify(self.session)
    #
    #     album = await spotify.get_spotify_album('The Beatles', 'Now & Then [Single]')
    #
    #     assert album == expected_album



    @asynctest.patch('src.collector.web.spotify.aiohttp.ClientSession.get', new_callable=AsyncContextManagerMock)
    @asynctest.patch('src.collector.web.spotify.requests.post')
    async def test__spotify__Spotify__get_spotify_album__ReturnsSpotifyAlbum__WhenUnexpectedMimeTypeErrorIsStatusReceivedFromSessionGet(
            self, mock_post, mock_get):

        authorization_response = MagicMock()
        authorization_response.text = '{"access_token": "mock_access_token"}'
        mock_post.return_value = authorization_response

        search_by_artist_response = MagicMock()
        search_by_artist_response.json = CoroutineMock()
        # content_type_error = ContentTypeError(MagicMock(), MagicMock())
        # search_by_artist_response.json.side_effect = raise_content_type_error

        # Create an instance of MockClientResponse with the JSON data you want response.json() to return
        search_by_artist_response = MockClientResponse(json_data={"albums": {"items": []}})

        # Mock the __aenter__ and __aexit__ methods
        mock_get.return_value.__aenter__.return_value = search_by_artist_response
        mock_get.return_value.__aexit__ = CoroutineMock()

        expected_album = {'name': 'Now & Then [Single]', 'artist': 'The Beatles'}

        spotify = Spotify(self.session)

        album = await spotify.get_spotify_album('The Beatles', 'Now & Then [Single]')

        assert album == expected_album
