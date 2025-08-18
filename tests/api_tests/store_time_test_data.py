def get_artists():
    return {
        'e4a8ae5b53974e75ffc10d5634e4f7f66336e93bb54fcb32376e49dcaa86fb49': {
            'id': 'e4a8ae5b53974e75ffc10d5634e4f7f66336e93bb54fcb32376e49dcaa86fb49',
            'name': 'Yob',
            'releases': ['4dc37c6ac420e706a784b2c2ea7aca9f7d3be7d904add34114c9576868c375c0']
        },
        'd466bcf52eb6921b1e747e51bf2cc1441926455ba146ecc477bed1574e44f9c0': {
            'id': 'd466bcf52eb6921b1e747e51bf2cc1441926455ba146ecc477bed1574e44f9c0',
            'name': 'Sleep',
            'releases': ['9c50562e8ffce69c6d66b50ba509c4ce622a2154f45372a24646457e793db75d']
        }
    }


def get_releases():
    return {
        '4dc37c6ac420e706a784b2c2ea7aca9f7d3be7d904add34114c9576868c375c0': {
            'id': '4dc37c6ac420e706a784b2c2ea7aca9f7d3be7d904add34114c9576868c375c0',
            'name': 'Our Raw Heart',
            'reviews': ['df00a8c7810b10e3f4631b87e98be36a0e0d27dc2f2abd7e4a71222c97616e1b'],
            'date': '2019-02-15',
            'type': 'album',
            'total_tracks': 12,
            'spotify_url': 'https://spotify.com',
            'cover_url': None
        },
        '9c50562e8ffce69c6d66b50ba509c4ce622a2154f45372a24646457e793db75d': {
            'id': '9c50562e8ffce69c6d66b50ba509c4ce622a2154f45372a24646457e793db75d',
            'name': 'The Sciences',
            'reviews': ['7f5079ae824c21a92a82b85e6d212f3004f26ee1bd5556b6f76f213d884ff877'],
            'date': '2019-01-15',
            'type': 'album',
            'total_tracks': 10,
            'spotify_url': 'https://spotify.com',
            'cover_url': None
        }
    }


def get_reviews():
    return {
        'df00a8c7810b10e3f4631b87e98be36a0e0d27dc2f2abd7e4a71222c97616e1b': {
            'id': 'df00a8c7810b10e3f4631b87e98be36a0e0d27dc2f2abd7e4a71222c97616e1b',
            'publication_name': 'The Quietus',
            'date': 'Posted Jun 20, 2018',
            'link': 'http://thequietus.com/articles/24811-yob-our-raw-heart-album-review',
            'score': 80,
            'cover_url': None
        },
        '7f5079ae824c21a92a82b85e6d212f3004f26ee1bd5556b6f76f213d884ff877': {
            'id': '7f5079ae824c21a92a82b85e6d212f3004f26ee1bd5556b6f76f213d884ff877',
            'publication_name': '57-the-needle-drop',
            'date': None, 'link': 'https://www.youtube.com/watch?v=d5jWckdWqpM',
            'score': 80,
            'cover_url': None
        }
    }


def get_spotify_artists():
    return {
        '295f66f6ded4ca9e83f7785b21e4925987b5043e2c864f4df720688a8d6cd3a6':
            {
                'id': '295f66f6ded4ca9e83f7785b21e4925987b5043e2c864f4df720688a8d6cd3a6',
                'name': 'Ladytron',
                'releases': ['89e29b8440e9ad364f200b6830fe27fb87a744450e8b43b6acbdf09bc1db5019']
            },
        '0a218dc3f84d0816899ff8fc2f22e17501444398d2ca5c4b4d3a11d21f53f0c5':
            {
                'id': '0a218dc3f84d0816899ff8fc2f22e17501444398d2ca5c4b4d3a11d21f53f0c5',
                'name': 'Always Ascending',
                'releases': ['3a2fbceb5e63dab764532cb463047c7150f6f814492a20efc924c92c5fa66797']
            }
        }


def get_spotify_releases():
    return {
        '89e29b8440e9ad364f200b6830fe27fb87a744450e8b43b6acbdf09bc1db5019':
            {
                'id': '89e29b8440e9ad364f200b6830fe27fb87a744450e8b43b6acbdf09bc1db5019',
                'name': 'Ladytron',
                'date': '2019-02-15',
                'type': 'album',
                'spotify_url': 'https://spotify.com',
                'total_tracks': 12,
                'reviews': [],
                'cover_url': None
            },
        '3a2fbceb5e63dab764532cb463047c7150f6f814492a20efc924c92c5fa66797':
            {
                'id': '3a2fbceb5e63dab764532cb463047c7150f6f814492a20efc924c92c5fa66797',
                'name': 'Franz Ferdin&',
                'date': '2019-01-15',
                'type': 'album',
                'spotify_url': 'https://spotify.com',
                'total_tracks': 10,
                'reviews': [],
                'cover_url': None
            }
    }
