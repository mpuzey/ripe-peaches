from typing import Dict, List

from src.collector.entities.artist import Artist
from src.collector.entities.release import Release
from src.collector.entities.review import Review
from src.collector.use_cases.music_catalog import MusicCatalog
from src.collector.entities.publication_review import PublicationReview
from src.common.crypto import calculate_hash


class MusicReviewCataloger(MusicCatalog):

    def __init__(self):
        super().__init__()
        self.artists = {}
        self.releases = []
        self.reviews = []

    def add_review(self, publication_reviews: List[PublicationReview]) -> Dict[str, Artist]:
        super().add_review(publication_reviews)

        return self.artists

    def get_artists(self) -> Dict[str, Artist]:
        return self.artists

    def get_releases(self) -> List[Release]:
        raise NotImplemented

    def get_reviews(self) -> List[Release]:
        raise NotImplemented
