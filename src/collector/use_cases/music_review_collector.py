from src.collector.use_cases.collector import Collector

from abc import abstractmethod


class MusicReviewCollector(Collector):

    @abstractmethod
    def collect(self, source, **kwargs):
        pass

    @abstractmethod
    def parse(self):
        pass
