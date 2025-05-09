""" This module constitutes as the single point of configuration for the application and pulls
# the necessary environment variables required to run the application. Such as secrets. """
import os

SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
SPOTIFY_RESULTS_LIMIT = 50


# Aggregation
THUMBS_UP_THRESHOLD = 80

# Scores
MINIMUM_REVIEWS_COUNTED = 5

# Metacritic - scraping from metacritic is slow but we pull 100 releases at a time
METACRITIC_PUBLICATIONS = ['pitchfork', 'consequence-of-sound', 'rolling-stone',
                                   'the-guardian', 'drowned-in-sound', 'the-quietus',
                                   'sputnikmusic', 'spin', 'beats-per-minute-formerly-one-thirty-bpm',
                                   'the-observer-uk', 'tiny-mix-tapes', 'mojo', 'musicomhcom', 'under-the-radar',
                                   'exclaim', 'paste-magazine', 'american-songwriter', 'now-magazine', 'clash-music',
                                   'the-wire', 'no-ripcord', 'delusions-of-adequacy', 'new-musical-express-nme',
                                   'the-independent-uk', 'record-collector', 'uncut', 'diy-magazine',
                                   'alternative-press', 'the-new-york-times', 'the-405', 'dusted-magazine',
                                   'the-av-club', 'the-skinny']
METACRITIC_PUBLICATIONS_SAMPLE = ['the-quietus', 'sputnikmusic', 'consequence-of-sound', 'uncut', 'record-collector']

METACRITIC_SCRAPE_BATCH_SIZE = 100

# AOTY - scraping from AOTY is quicker but we pull only 30 releases at once
AOTY_PUBLICATIONS_SAMPLE = ['57-the-needle-drop', '7-popmatters', '8-all-music', '2-av-club']
AOTY_PUBLICATIONS = ['57-the-needle-drop', '7-popmatters', '8-all-music', '23-pretty-much-amazing',
                             '28-the-line-of-best-fit', '17-under-the-radar', '62-metal-sucks', #'61-metal-injection',
                             '52-gigsoup', '59-spectrum-culture', '63-flood-magazine', '46-entertainment-weekly',
                             '33-xxl', '55-the-telegraph']