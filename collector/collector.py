from abc import ABC, abstractmethod


class Collector(ABC):
    def get_data(self):
        pass
