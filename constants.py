""" This module holds reusable strings and integers for the application. It consolidates changes to
these values. """
import os
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
PUBLIC_ROOT = os.path.join(ROOT_PATH, 'static')


METACRITIC_PUBLICATION_URL = 'https://www.metacritic.com/publication/{publication_name}?' \
      'filter=albums&num_items={release_count}'
METACRITIC_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

AOTY_PUBLICATION_URL = 'https://www.albumoftheyear.org/publication/{publication_name}/reviews/'
AOTY_REQUEST_HEADERS = METACRITIC_REQUEST_HEADERS

# Spotify
SPOTIFY_NEW_RELEASE_SEARCH = 'https://api.spotify.com/v1/search?type=album&q={char}*+tag:new&limit=50'

# Regex
ARTIST_PARTS_REGEX = '(?:.*?\/){3}([^\/?#]+)'

