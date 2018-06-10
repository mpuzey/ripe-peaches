from abc import ABC, abstractmethod


class Store(ABC):

    # @abstractmethod
    # def get_recent_releases(self):
    #     pass
    #
    # @abstractmethod
    # def store_releases(self, releases):
    #     pass
    #
    # @abstractmethod
    # def get_reviews_by_year(self, year):
    #     pass

    @abstractmethod
    def get_recent_reviews(self):
        pass

    @abstractmethod
    def store_reviews(self, reviews):
        pass

    # @abstractmethod
    # def store_publications(self, publications):
    #     pass
