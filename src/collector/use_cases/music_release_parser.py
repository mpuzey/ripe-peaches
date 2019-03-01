from src.collector.use_cases.music_parser import MusicParser


class MusicReleaseParser(MusicParser):

    def __init__(self):
        self.artists = {}

    def parse(self, data):
        pass
