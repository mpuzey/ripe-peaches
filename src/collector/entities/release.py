from typing import Dict
from dataclasses import dataclass


@dataclass
class Release:
    id: str
    name: str
    reviews: Dict
    date: str = None
    type: str = None
    total_tracks: int = None
    spotify_url: str = None
