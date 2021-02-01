from typing import List, Dict
from src.collector.entities.release import Release
from src.collector.entities.review import Review
from src.collector.entities.artist import Artist
from src.collector.entities.publication_review import PublicationReview
from abc import ABC, abstractmethod


class Cataloger(ABC):

    @abstractmethod
    def add_review(self, publication_reviews: List[PublicationReview]) -> Dict[str, Artist]:
        pass

    @abstractmethod
    def add_release(self, data: Dict) -> Dict[str, Artist]:
        pass

    @abstractmethod
    def get_artists(self) -> Dict[str, Artist]:
        pass

    @abstractmethod
    def get_releases(self) -> List[Release]:
        pass

    @abstractmethod
    def get_reviews(self) -> List[Review]:
        pass

    @abstractmethod
    def format_release_name(self, name: str) -> str:
        pass
