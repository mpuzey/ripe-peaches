from typing import Dict
from dataclasses import dataclass
from src.collector.entities.review import Review


@dataclass
class Release:
    id: str
    name: str
    reviews: Dict[str, Review]
    date: str = None
    type: str = None
    total_tracks: int = None
    spotify_url: str = None
