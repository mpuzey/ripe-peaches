from typing import List

from src.entities.publication_review import PublicationReview
from src.entities.external_release import ExternalRelease


def get_publication_reviews() -> List[PublicationReview]:
    return [
        PublicationReview(
            artist='Yob',
            date='Posted Jun 20, 2018',
            publication_name='The Quietus',
            release_name='Our Raw Heart',
            score=80,
            link='http://thequietus.com/articles/24811-yob-our-raw-heart-album-review'
        ),
        PublicationReview(
            artist='Sleep',
            publication_name='57-the-needle-drop',
            release_name='The Sciences',
            score=80,
            link='https://www.youtube.com/watch?v=d5jWckdWqpM'
        )
    ]


def get_enriched_releases() -> List[ExternalRelease]:
    return [
        ExternalRelease(
            name='Our Raw Heart',
            artist='Yob',
            date='2019-02-15',
            type='album',
            spotify_url='https://spotify.com',
            total_tracks=12
        ),
        ExternalRelease(
            name='The Sciences',
            artist='Sleep',
            date='2019-01-15',
            type='album',
            spotify_url='https://spotify.com',
            total_tracks=10
        )
    ]


def get_external_releases() -> List[ExternalRelease]:
    return [
        ExternalRelease(
            name='Ladytron',
            artist='Ladytron',
            date='2019-02-15',
            type='album',
            spotify_url='https://spotify.com',
            total_tracks=12
        ),
        ExternalRelease(
            name='Franz Ferdinand',
            artist='Always Ascending',
            date='2019-01-15',
            type='album',
            spotify_url='https://spotify.com',
            total_tracks=10
        )
    ]
