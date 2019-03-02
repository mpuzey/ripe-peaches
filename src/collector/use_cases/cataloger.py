from typing import List, Dict
from src.collector.entities.release import Release
from src.collector.entities.review import Review
from abc import ABC, abstractmethod


class Cataloger(ABC):

    @abstractmethod
    def add(self, data: List) -> Dict:
        pass

    @abstractmethod
    def get_reviews(self):
        pass

    @abstractmethod
    def get_releases(self):
        pass

    @abstractmethod
    def create_release(self, publication_review: Dict) -> Release:
        pass

    @abstractmethod
    def create_review(self, publication_review: Dict) -> Review:
        pass

    @abstractmethod
    def format_release_name(self, name: str) -> str:
        pass
