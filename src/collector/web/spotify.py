import os
import json
import base64
import requests


def get_releases(access_token, url='https://api.spotify.com/v1/browse/new-releases?limit=10'):

    response = requests.get(url, headers={'Authorization': 'Bearer %s' % access_token}).json()

    albums = response.get('albums')
    items = albums.get('items')
    next_url = albums.get('next')

    if not next_url:
        return items, None

    return items, next_url


def get_recent_releases():

    client_id = os.environ.get('SPOTIFY_CLIENT_ID')
    client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')
    client_details = '%s:%s' % (client_id, client_secret)
    encoded_client_details = base64.b64encode(client_details.encode('utf-8')).decode('utf-8')
    deets = 'Basic %s' % encoded_client_details

    authorization_response = requests.post('https://accounts.spotify.com/api/token',
                                           data={'grant_type': 'client_credentials'},
                                           headers={'Authorization': deets})

    access_token = json.loads(authorization_response.text).get('access_token')
    # //2910 1970
    # 9950 returns 50 releases for 2018

    url = 'https://api.spotify.com/v1/browse/new-releases?limit=10'
    raw_releases = []
    while True:
        items, url = get_releases(access_token, url)
        raw_releases.extend(items)

        if not url:
            break

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

    with open('dump.txt', 'w+') as outfile:
        json.dump({'releases': releases}, outfile)


if __name__ == "__main__":
    get_recent_releases()
