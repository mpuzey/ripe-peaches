""" This module holds reusable strings and integers for the application. It consolidates changes to
these values. """
import os
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
PUBLIC_ROOT = os.path.join(ROOT_PATH, 'static')


# Metacritic - scraping from metacritic is slow but we pull 100 releases at at time
METACRITIC_CURATED_PUBLICATIONS = ['pitchfork', 'consequence-of-sound', 'rolling-stone',
                                   'the-guardian', 'drowned-in-sound', 'the-quietus',
                                   'sputnikmusic', 'spin',
                                   'beats-per-minute-formerly-one-thirty-bpm']
METACRITIC_PUBLICATIONS_SAMPLE = ['the-quietus', 'sputnikmusic', 'consequence-of-sound']
METACRITIC_PUBLICATION_URL = 'https://www.metacritic.com/publication/{publication_name}?' \
      'filter=music&num_items={release_count}'
METACRITIC_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}
METACRITIC_SCRAPE_BATCH_SIZE = 100

# AOTY - scraping from AOTY is quicker but we pull only 30 releases at once
AOTY_CURATED_PUBLICATIONS = ['57-the-needle-drop', '/32-exclaim', '18-the-four-oh-five',
                             '7-popmatters', '31-the-skinny', '8-all-music', '2-av-club']
AOTY_PUBLICATIONS = ['57-the-needle-drop', '/32-exclaim', '18-the-four-oh-five', '7-popmatters',
                     '31-the-skinny', '8-all-music', '2-av-club', '25-diy', '5-musicomh', '9-nme',
                     '13-no-ripcord', '11-paste', '23-pretty-much-amazing','18-the-four-oh-five',
                     '28-the-line-of-best-fit', '4-tiny-mix-tapes', '17-under-the-radar',
                     '62-metal-sucks', '61-metal-injection', '52-gigsoup', '59-spectrum-culture',
                     '53-the-independent', '63-flood-magazine', '46-entertainment-weekly', '33-xxl',
                     '55-the-telegraph', '58-the-observer', '43-clash']
AOTY_PUBLICATION_URL = 'https://www.albumoftheyear.org/publication/{publication_name}/reviews/'
AOTY_REQUEST_HEADERS = METACRITIC_REQUEST_HEADERS

# Spotify
SPOTIFY_YEAR_SEARCH = 'https://api.spotify.com/v1/search?type=album&q=year:1970&offset=%s&limit=50'
SPOTIFY_NEW_RELEASE_SEARCH = 'https://api.spotify.com/v1/search?type=album&q=tag:new&limit=50'

# Regex
ARTIST_PARTS_REGEX = '(?:.*?\/){3}([^\/?#]+)'

# Aggregation
THUMBS_UP_THRESHOLD = 80

# Scores
MINIMUM_REVIEWS_COUNTED = 10
