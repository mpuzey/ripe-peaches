
def get_raw_reviews():
    return [
        {
            'artist': 'Yob',
            'date': 'Posted Jun 20, 2018',
            'publication_name': 'The Quietus',
            'release_name': 'Our Raw Heart',
            'score': 80,
            'link': 'http://thequietus.com/articles/24811-yob-our-raw-heart-album-review'
        },
        {
            'artist': 'Sleep',
            'publication_name': '57-the-needle-drop',
            'release_name': 'The Sciences',
            'score': 80,
            'link': 'https://www.youtube.com/watch?v=d5jWckdWqpM'
        }
    ]


def get_raw_releases():
    return [
        {

        }
    ]

    'name': release.get('name'),
    'artist': release.get('artists')[0].get('name'),
    'date': release.get('release_date'),
    'type': release.get('type'),
    'spotify_url': release.get('external_urls').get('spotify'),
    'total_tracks': release.get('total_tracks')