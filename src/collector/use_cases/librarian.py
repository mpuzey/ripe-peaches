from typing import List, Dict
from src.collector.entities.release import Release
from src.collector.entities.review import Review
from src.collector.entities.artist import Artist
from src.collector.entities.publication_review import PublicationReview
from src.collector.entities.external_release import ExternalRelease
from abc import ABC, abstractmethod


class Librarian(ABC):

    @abstractmethod
    def add_reviews(self, publication_reviews: List[PublicationReview]) -> Dict[str, Artist]:
        pass

    @abstractmethod
    def add_releases(self, publication_releases: List[ExternalRelease]) -> Dict[str, Artist]:
        pass

    @abstractmethod
    def format_release_name(self, name: str) -> str:
        pass
