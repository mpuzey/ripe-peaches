from typing import List
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from src.entities.release import Release
import copy


@dataclass_json
@dataclass
class Artist:
    id: str
    name: str
    releases: List[Release]

    def copy(self):
        """Creates a deep copy of the artist including all releases"""
        return copy.deepcopy(self)
