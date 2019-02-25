from src.collector.use_cases.parser import Parser
from abc import abstractmethod

from src.common.crypto import calculate_hash


class MusicParser(Parser):

    def __init__(self):
        self.artists = {}

    @abstractmethod
    def parse(self, data):
        pass

    def build_artist(self, raw_review):

        artist_name = raw_review.get('artist')
        artist_id = calculate_hash(artist_name)

        if not self.artists.get(artist_id):
            self.artists[artist_id] = {
                'id': artist_id,
                'name': artist_name,
                'releases': {}
            }

        return artist_id
