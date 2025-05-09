""" This module holds reusable strings and integers for the application. It consolidates changes to
these values. """
import os
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
PUBLIC_ROOT = os.path.join(ROOT_PATH, 'static')


METACRITIC_PUBLICATION_URL = 'https://www.metacritic.com/publication/{publication_name}?' \
      'filter=albums&num_items={release_count}'
METACRITIC_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/135.0.7049.116 Safari/537.36'
}

AOTY_PUBLICATION_URL = 'https://www.albumoftheyear.org/publication/{publication_name}/reviews/'
AOTY_REQUEST_HEADERS = METACRITIC_REQUEST_HEADERS

# Spotify
SPOTIFY_NEW_RELEASE_SEARCH = 'https://api.spotify.com/v1/search?type=album&q={char}*+tag:new&limit=50'

# Regex
ARTIST_PARTS_REGEX = '(?:.*?\/){3}([^\/?#]+)'

ENHANCED_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.7049.116 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.metacritic.com/",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Connection": "keep-alive",
    # "Cookie": "...",  # Only if needed, try without first
}

