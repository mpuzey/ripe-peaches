from typing import List
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from src.collector.entities.release import Release

# TODO: artist is specific to music, do we prefer a Creator/ Author rename or generic parent?

@dataclass_json
@dataclass
class Artist:
    id: str
    name: str
    releases: List[Release]
