from unittest.mock import MagicMock

import aiohttp
from aiohttp import ContentTypeError


def search_by_artist_and_album_success_response():
    return {
        'albums': {
            'items': [
                {
                    'name': 'Now & Then [Single]',
                    'artists': ['The Beatles'],
                    'type': 'single',
                    'external_urls': 'https://open.spotify.com/album/2qQP2NgOoH6HqknnbpJmIk?si=GEiQbz98T5CwWiU9DqPlNQ',
                    'total_tracks': '2'
                }
            ]
        }
    }


class CustomClientSession(aiohttp.ClientSession):
    async def get(self, *args, **kwargs):
        raise ContentTypeError(MagicMock(), MagicMock())


def raise_content_type_error():
    content_type_error = ContentTypeError(MagicMock(), MagicMock())
    raise content_type_error


class MockClientResponse:

    def __init__(self, json_data):
        self._json_data = json_data
        self.status = 200
        self.reason = 'OK'

    async def json(self):
        return self._json_data


class AsyncContextManagerMock(MagicMock):
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
