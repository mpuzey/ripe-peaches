import os
import json
import base64
import requests


def get_releases(access_token, offset):

    response = requests.get('https://api.spotify.com/v1/search?type=album&q=year:1970&offset=%s&limit=50' % str(offset),
                        headers={'Authorization': 'Bearer %s' % access_token})

    return json.loads(response.text).get('albums').get('items')


def get_recent_releases():

    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')
    client_details = '%s:%s' % (client_id, client_secret)
    encoded_client_details = base64.b64encode(client_details.encode('utf-8')).decode('utf-8')
    deets = 'Basic %s' % encoded_client_details

    authorization_response = requests.post('https://accounts.spotify.com/api/token',
                                           data={'grant_type': 'client_credentials'},
                                           headers={'Authorization': deets})

    access_token = json.loads(authorization_response.text).get('access_token')
    # //2910 1970
    # 9950 returns 50 releases for 2018

    raw_releases = []
    offset = 0
    while True:
        buffer = get_releases(access_token, offset)
        raw_releases.extend(buffer)
        offset += 50

        if len(buffer) < 50:
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
