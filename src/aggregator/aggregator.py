from abc import ABC, abstractmethod


class MusicAggregator(ABC):

    @abstractmethod
    def aggregate_artists(self, artist):
        pass
