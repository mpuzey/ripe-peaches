from typing import Dict, List

from src.collector.entities.artist import Artist
from src.collector.entities.release import Release
from src.collector.entities.review import Review
from src.collector.use_cases.music_cataloger import MusicCataloger
from src.collector.entities.publication_review import PublicationReview
from src.common.crypto import calculate_hash


class MusicReviewCataloger(MusicCataloger):

    def __init__(self):
        super().__init__()
        self.artists = {}
        self.releases = []
        self.reviews = []

    def add_review(self, data: [PublicationReview]) -> Dict[str, Artist]:
        super().add_review(data)

        return self.artists

    def get_artists(self) -> Dict[str, Artist]:
        return self.artists

    def get_releases(self) -> List[Release]:
        raise NotImplemented

    def get_reviews(self) -> List[Release]:
        raise NotImplemented
