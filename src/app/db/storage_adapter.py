from abc import ABC, abstractmethod


class StorageAdapter(ABC):

    @abstractmethod
    def get(self, id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def put(self, data):
        pass
