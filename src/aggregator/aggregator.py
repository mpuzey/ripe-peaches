from abc import ABC, abstractmethod


class Aggregator(ABC):

    @abstractmethod
    def aggregate(self, data):
        pass
