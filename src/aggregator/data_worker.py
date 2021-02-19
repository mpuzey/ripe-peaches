from abc import ABC, abstractmethod


class DataWorker(ABC):

    @abstractmethod
    def work(self, data):
        pass
