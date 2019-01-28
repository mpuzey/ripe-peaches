import os
import json
import base64
import requests
import constants


def get_releases():

    details = load_credentials()
    authorization_response = requests.post('https://accounts.spotify.com/api/token',
                                           data={'grant_type': 'client_credentials'},
                                           headers={'Authorization': details})

    access_token = json.loads(authorization_response.text).get('access_token')
    next_page = constants.SPOTIFY_NEW_RELEASE_SEARCH
    raw_releases = []

    while next_page:
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
        return None

    return albums.get('items'), albums.get('next')


def parse_releases(raw_releases):

    releases = []
    for release in raw_releases:
        releases.append({
            'release_name': release.get('name'),
            'release_artist': release.get('artists')[0].get('name'),
            'release_date': release.get('release_date'),
            'release_type': release.get('type'),
            'spotify_url': release.get('external_urls').get('spotify'),
            'total_tracks': release.get('total_tracks')
        })

    return releases


if __name__ == "__main__":
    get_releases()
