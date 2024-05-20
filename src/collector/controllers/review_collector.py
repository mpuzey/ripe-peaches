from abc import ABC, abstractmethod
from src.entities.publication_review import PublicationReview


class ReviewCollector(ABC):

    @abstractmethod
    def collect_reviews(self, source, **kwargs) -> [PublicationReview]:
        pass
