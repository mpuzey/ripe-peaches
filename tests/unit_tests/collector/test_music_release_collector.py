import unittest

from mock import MagicMock

from src.collector.controllers.music_release_collector import MusicReleaseCollector
from src.collector.entities.artist import Artist
from src.collector.entities.external_release import ExternalRelease
from src.collector.entities.release import Release

from src.collector.use_cases.music_catalog import MusicCatalog
from src.collector.use_cases.music_cataloger import MusicCataloger


class TestMusicReleaseCollector(unittest.TestCase):

    def test__MusicReleaseCollector__collect__WillBuildUpAListOfArtistsWithReleases__WhenCalledTwice(self):
        mock_spotify = MagicMock()
        mock_spotify.get_releases.return_value = [
            ExternalRelease(
                name='Clearing The Path',
                artist='YOB',
                date='2014',
                spotify_url='https://open.spotify.com/album/7rGfoMrPEi2mXXqeiueknB?si=u3boao-mR9ev6OfJnp7kFg'),
            ExternalRelease(
                name='Atma',
                artist='YOB',
                date='2011',
                spotify_url='https://open.spotify.com/album/6WxvbvVMBUNkotw63pYcr3?si=0V88iyyGTVyCMafYoSFbXg')
        ]

        catalog = MusicCatalog()
        cataloger = MusicCataloger(catalog)
        collector = MusicReleaseCollector(cataloger)
        collector.collect(mock_spotify)

        actual_artists = collector.catalog()
        expected_artists = {
            'd92a4901abc2f02dfd347e0793ca3f1c223cbff321d30cdef2679ed13b1c58ae': Artist(
                id='d92a4901abc2f02dfd347e0793ca3f1c223cbff321d30cdef2679ed13b1c58ae',
                name='YOB',
                releases=[
                    Release(
                        id='137801a1514b811c49b2d27183e4b6fd8b7371d76cc4ff177c0a70d9700e196c',
                        name='Clearing The Path',
                        reviews=[],
                        date='2014',
                        type=None,
                        total_tracks=None,
                        spotify_url='https://open.spotify.com/album/7rGfoMrPEi2mXXqeiueknB?si=u3boao-mR9ev6OfJnp7kFg'),
                    Release(
                        id='d7c69f2ea6c8e95e8bcfe471bf9ddd57c734cc93357686b68b13e307f7c346ab',
                        name='Atma',
                        reviews=[],
                        date='2011',
                        type=None,
                        total_tracks=None,
                        spotify_url='https://open.spotify.com/album/6WxvbvVMBUNkotw63pYcr3?si=0V88iyyGTVyCMafYoSFbXg'),
                ]
            )
        }

        self.assertEqual(expected_artists, actual_artists)
