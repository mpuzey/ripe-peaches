from dataclasses import dataclass
from dataclasses_json import dataclass_json
from src.collector.entities.artist import Artist
from src.collector.entities.release import Release
from src.collector.entities.review import Review
from src.common.crypto import calculate_hash


@dataclass_json
@dataclass
class PublicationRelease:
    artist: str
    name: str
