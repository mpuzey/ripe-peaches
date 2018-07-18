def get_artist_sample():
    return {
        '6d36d7e180b92eacd41f75ec53c4c4681f965c36db1dc7770e64e0f4e3166ab4': {
            'id': '6d36d7e180b92eacd41f75ec53c4c4681f965c36db1dc7770e64e0f4e3166ab4',
            'name': 'Rp Boo',
            'releases': [
                '0227438fc7af5cd3e37464870b4fce85fae7a4f3ddebe80594b0181db2c31a4f'
            ]
        },
        '7fd24a70ad382f7019780298658cc417995ee63c2b1e0a73c09ce2864e81da16': {
            'id': '7fd24a70ad382f7019780298658cc417995ee63c2b1e0a73c09ce2864e81da16',
            'name': 'Okzharp',
            'releases': [
                '0c0f12aab588d760168fc6a42fd2ec424c531bc9fe3bb9516559bcb55599b304'
            ]
        }
    }


def get_release_sample():
    return {
        '0227438fc7af5cd3e37464870b4fce85fae7a4f3ddebe80594b0181db2c31a4f': {
            'id': '0227438fc7af5cd3e37464870b4fce85fae7a4f3ddebe80594b0181db2c31a4f',
            'name': 'I\'ll Tell You What!',
            'reviews': [
                'b2daf7b6cd3733dd28bca48311d68a7bcc476bc0a628a128b4aa25be6095e3f1',
                'c2daf7b6cd3733dd28bca48311d68a7bcc476bc0a628a128b4aa25be6095e3f1'
            ]
        },
        '0c0f12aab588d760168fc6a42fd2ec424c531bc9fe3bb9516559bcb55599b304': {
            'id': '0c0f12aab588d760168fc6a42fd2ec424c531bc9fe3bb9516559bcb55599b304',
            'name': 'Closer Apart',
            'reviews': [
                'c0f9f586742633de7ada3b7766e512c67e322f6579c02d42045a79a42028f2be',
                'd0f9f586742633de7ada3b7766e512c67e322f6579c02d42045a79a42028f2be'
            ]
        }
    }


def get_review_sample():
    return {
        'b2daf7b6cd3733dd28bca48311d68a7bcc476bc0a628a128b4aa25be6095e3f1': {
            'score': '80',
            'publication_name': 'The Quietus',
            'date': 'Posted Jul 16, 2018',
            'link': 'http://thequietus.com/articles/24982-rp-boo-i-ll-tell-you-what-album-review',
            'id': 'b2daf7b6cd3733dd28bca48311d68a7bcc476bc0a628a128b4aa25be6095e3f1'
        },
        'c2daf7b6cd3733dd28bca48311d68a7bcc476bc0a628a128b4aa25be6095e3f1': {
            'score': '60',
            'publication_name': 'Pitchfork',
            'date': 'Posted Jul 17, 2018',
            'link': 'http://some-pitchwork-review-link',
            'id': 'c2daf7b6cd3733dd28bca48311d68a7bcc476bc0a628a128b4aa25be6095e3f1'
        },
        'c0f9f586742633de7ada3b7766e512c67e322f6579c02d42045a79a42028f2be': {
            'score': '80',
            'publication_name': 'The Quietus',
            'date': 'Posted Jul 16, 2018',
            'link': 'http://thequietus.com/articles/24925-okzharp-manthe-ribane-closer-apart-lead-album-review',
            'id': 'c0f9f586742633de7ada3b7766e512c67e322f6579c02d42045a79a42028f2be'
        },
        'd0f9f586742633de7ada3b7766e512c67e322f6579c02d42045a79a42028f2be': {
            'score': '100',
            'publication_name': 'Pitchfork',
            'date': 'Posted Jul 17, 2018',
            'link': 'http://some-pitchwork-review-link',
            'id': 'd0f9f586742633de7ada3b7766e512c67e322f6579c02d42045a79a42028f2be'
        }
    }
