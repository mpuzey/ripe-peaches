from dataclasses import dataclass


@dataclass
class Score:
    id: str
    release_id: str
    release_name: str
    artist_id: str
    artist_name: str
    score: int
    reviews_counted: int
