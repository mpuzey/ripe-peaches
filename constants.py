""" This module holds reusable strings and integers for the application. It consolidates changes to
these values. """
import os
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
# PUBLIC_ROOT = os.path.join(ROOT, 'static')

# Regex
ARTIST_PARTS_REGEX = '(?:.*?\/){3}([^\/?#]+)'
