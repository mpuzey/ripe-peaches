from dataclasses import dataclass


@dataclass
class Review:
    id: str
    publication_name: str
    score: int
    date: str
    link: str
