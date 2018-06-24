from abc import ABC, abstractmethod


class Collector(ABC):

    @staticmethod
    @abstractmethod
    def collect(data, source):
        pass
