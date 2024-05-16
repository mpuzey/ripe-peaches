from typing import List
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from src.entities.review import Review


@dataclass_json
@dataclass
class Release:
    id: str
    name: str
    reviews: List[Review]
    date: str = None
    type: str = None
    total_tracks: int = None
    spotify_url: str = None
