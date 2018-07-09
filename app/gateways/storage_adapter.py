from abc import ABC, abstractmethod


class StorageAdapter(ABC):

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def put(self, data):
        pass

    @abstractmethod
    def post(self, data):
        pass
