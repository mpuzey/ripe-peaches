from typing import List, Dict
from src.collector.entities.release import Release
from src.collector.entities.review import Review
from src.collector.entities.artist import Artist
from abc import ABC, abstractmethod


class Catalog(ABC):

    @abstractmethod
    def add_artists(self, artists: Dict[str, Artist]) -> Dict[str, Artist]:
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
