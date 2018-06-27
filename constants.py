""" This module holds reusable strings and integers for the application. It consolidates changes to
these values. """
import os
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
PUBLIC_ROOT = os.path.join(ROOT_PATH, 'static')


# Metacritic
METACRITIC_CURATED_PUBLICATIONS = ['pitchfork', 'consequence-of-sound', 'rolling-stone',
                                   'the-guardian', 'downed-in-sound', 'the-quietus',
                                   'sputnikmusic', 'spin',
                                   'beats-per-minute-formerly-one-thirty-bpm']
METACRITIC_PUBLICATIONS_SAMPLE = ['the-quietus', 'sputnikmusic', 'consequence-of-sound']
METACRITIC_PUBLICATION_URL = 'http://www.metacritic.com/publication/{publication_name}?' \
      'filter=music&num_items={release_count}'
METACRITIC_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}
METACRITIC_SCRAPE_BATCH_SIZE = 100

# AOTY
AOTY_CURATED_PUBLICATIONS = ['57-the-needle-drop', '/32-exclaim', '18-the-four-oh-five',
                             '7-popmatters', '31-the-skinny', '8-all-music', '2-av-club']
AOTY_PUBLICATIONS_SAMPLE = ['57-the-needle-drop','7-popmatters']
AOTY_PUBLICATION_URL = 'https://www.albumoftheyear.org/publication/{publication_name}/reviews/'
AOTY_REQUEST_HEADERS = METACRITIC_REQUEST_HEADERS

# Regex
ARTIST_PARTS_REGEX = '(?:.*?\/){3}([^\/?#]+)'
