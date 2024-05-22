import unittest
from typing import Any, Tuple

import aiohttp
import asynctest
from aiohttp import ContentTypeError
from asynctest import MagicMock

from src.collector.web.spotify import Spotify


class CoroutineMagicMock:
    pass


class TestSpotify(asynctest.TestCase):

    # def setUp(self):
    #     client_session = MagicMock()
    #     self.spotify = Spotify(client_session)

    @asynctest.patch('src.collector.web.spotify.aiohttp.ClientSession')
    @asynctest.patch('src.collector.web.spotify.requests.post')
    async def test__spotify__Spotify__get_spotify_album__CompletesEnrichment__WhenUnexpectedMimeTypeReceivedWith429ToTooManyRequestsStatus(self, mock_post, mock_session):

        authorization_response = MagicMock()
        authorization_response.text = '{"access_token": "mock_access_token"}'
        mock_post.return_value = authorization_response

        search_by_artist_response = MagicMock()
        search_by_artist_response.json.side_effect = ContentTypeError(MagicMock(), (MagicMock()))
        mock_session.get.return_value = search_by_artist_response

        async with aiohttp.ClientSession() as client_session:

            spotify = Spotify(client_session)

            try:
                album = await spotify.get_spotify_album('The Beatles', 'Now & Then [Single]')
            except ContentTypeError as e:
                assert str(e) == 'Attempt to decode JSON with unexpected mimetype: '

        assert album is not None # TODO: diff album to expected album