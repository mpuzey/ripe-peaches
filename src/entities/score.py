from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Score:
    id: str
    release_id: str
    release_name: str
    artist_id: str
    artist_name: str
    score: int
    reviews_counted: int
