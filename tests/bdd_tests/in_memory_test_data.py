
def get_reviews():
    return [
        {
            'artist': 'Yob',
            'date': 'Posted Jun 20, 2018',
            'publication_name': 'The Quietus',
            'release_name': 'Our Raw Heart',
            'score': '80',
            'link': 'http://thequietus.com/articles/24811-yob-our-raw-heart-album-review'
        },
        {
            'artist': 'Sleep',
            'publication_name': '57-the-needle-drop',
            'release_name': 'The Sciences',
            'score': '80',
            'link': 'https://www.youtube.com/watch?v=d5jWckdWqpM'
        }
    ]


def get_artists():
    return {
        'e4a8ae5b53974e75ffc10d5634e4f7f66336e93bb54fcb32376e49dcaa86fb49': {
                'id': 'e4a8ae5b53974e75ffc10d5634e4f7f66336e93bb54fcb32376e49dcaa86fb49',
                'name': 'Yob',
                'releases': {
                    '4dc37c6ac420e706a784b2c2ea7aca9f7d3be7d904add34114c9576868c375c0': {
                        'id': '4dc37c6ac420e706a784b2c2ea7aca9f7d3be7d904add34114c9576868c375c0',
                        'name': 'Our Raw Heart',
                        'reviews': {
                            'df00a8c7810b10e3f4631b87e98be36a0e0d27dc2f2abd7e4a71222c97616e1b': {
                                'score': '80',
                                    'publication_name': 'The Quietus',
                                    'date': 'Posted Jun 20, 2018',
                                    'link': 'http://thequietus.com/articles/24811-yob-our-raw-heart-album-review',
                                    'id': 'df00a8c7810b10e3f4631b87e98be36a0e0d27dc2f2abd7e4a71222c97616e1b'
                            }
                        }
                    }
                }
            },
        'd466bcf52eb6921b1e747e51bf2cc1441926455ba146ecc477bed1574e44f9c0': {
            'id': 'd466bcf52eb6921b1e747e51bf2cc1441926455ba146ecc477bed1574e44f9c0',
            'name': 'Sleep',
            'releases': {
                '9c50562e8ffce69c6d66b50ba509c4ce622a2154f45372a24646457e793db75d': {
                    'id': '9c50562e8ffce69c6d66b50ba509c4ce622a2154f45372a24646457e793db75d',
                    'name': 'The Sciences',
                    'reviews': {
                        '7f5079ae824c21a92a82b85e6d212f3004f26ee1bd5556b6f76f213d884ff877': {
                            'score': '80',
                            'publication_name': '57-the-needle-drop',
                            'date': None,
                            'link': 'https://www.youtube.com/watch?v=d5jWckdWqpM',
                            'id': '7f5079ae824c21a92a82b85e6d212f3004f26ee1bd5556b6f76f213d884ff877'
                        }
                    }
                }
            }
        }
    }
