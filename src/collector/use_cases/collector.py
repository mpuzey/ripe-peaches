from abc import ABC, abstractmethod


class Collector(ABC):

    @abstractmethod
    def collect(self, source, **kwargs):
        pass

    @abstractmethod
    def catalog(self):
        pass
