""" This module holds reusable strings and integers for the application. It consolidates changes to
these values. """
import os
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
# PUBLIC_ROOT = os.path.join(ROOT, 'static')


# Metacritic
CURATED_METACRITIC_PUBLICATIONS = ['pitchfork', 'consequence-of-sound', 'rolling-stone',
                                   'the-guardian', 'downed-in-sound']
METACRITIC_PUBLICATION_URL = 'http://www.metacritic.com/publication/{publication_name}?' \
      'filter=music&num_items={release_count}'
METACRITIC_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}
METACRITIC_SCRAPE_BATCH_SIZE = 100


# Regex
ARTIST_PARTS_REGEX = '(?:.*?\/){3}([^\/?#]+)'
