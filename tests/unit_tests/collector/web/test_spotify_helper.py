from unittest.mock import MagicMock, patch

import aiohttp
from aiohttp import ContentTypeError


class CustomClientSession(aiohttp.ClientSession):
    async def get(self, *args, **kwargs):
        raise ContentTypeError(MagicMock(), MagicMock())


def raise_content_type_error():
    print("raise_content_type_error is called")
    content_type_error = ContentTypeError(MagicMock(), MagicMock())
    raise content_type_error


class MockClientResponse:

    def __init__(self, json_data):
        self._json_data = json_data

    async def __aenter__(self):

        # return self.json()

        content_type_error = ContentTypeError(MagicMock(), MagicMock())
        raise content_type_error

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def json(self):
        return self._json_data


class AsyncContextManagerMock(MagicMock):
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
