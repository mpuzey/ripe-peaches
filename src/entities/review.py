from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Review:
    id: str
    publication_name: str
    score: int
    date: str
    link: str
    cover_url: str = None
