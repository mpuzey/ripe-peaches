import os
from urllib import parse
import json
import base64
import requests
import constants


def get_releases():

    print('Fetching recent releases from Spotify...')
    details = load_credentials()
    authorization_response = requests.post('https://accounts.spotify.com/api/token',
                                           data={'grant_type': 'client_credentials'},
                                           headers={'Authorization': details})

    access_token = json.loads(authorization_response.text).get('access_token')
    next_page = constants.SPOTIFY_NEW_RELEASE_SEARCH
    raw_releases = []

    while next_page:
        offset = dict(parse.parse_qsl(parse.urlsplit(next_page).query)).get('offset', 0)
        if int(offset) >= 10000:
            break
        response = requests.get(next_page, headers={'Authorization': 'Bearer %s' % access_token}).json()
        new_items, next_page = parse_response(response)
        raw_releases.extend(new_items)

    return parse_releases(raw_releases)


def load_credentials():

    client_id = os.environ.get('SPOTIFY_CLIENT_ID')
    client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')
    client_details = '%s:%s' % (client_id, client_secret)
    encoded_client_details = base64.b64encode(client_details.encode('utf-8')).decode('utf-8')
    details = 'Basic %s' % encoded_client_details

    return details


def parse_response(response):

    albums = response.get('albums')

    if not albums:
        return None, None

    items = albums.get('items')
    valid_items = [item for item in items if item]

    return valid_items, albums.get('next')


def parse_releases(raw_releases):

    releases = []
    for release in raw_releases:
        releases.append({
            'name': release.get('name'),
            'artist': release.get('artists')[0].get('name'),
            'date': release.get('release_date'),
            'type': release.get('type'),
            'spotify_url': release.get('external_urls').get('spotify'),
            'total_tracks': release.get('total_tracks')
        })

    print('Finished fetching recent releases from Spotify')
    return releases
