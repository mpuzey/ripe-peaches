from abc import ABC, abstractmethod


class Store(ABC):

    # @abstractmethod
    # def __init__(self, adapter):
    #     pass

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def put(self, data):
        pass
