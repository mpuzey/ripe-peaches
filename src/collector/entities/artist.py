from typing import Dict
from dataclasses import dataclass
from src.collector.entities.release import Release


@dataclass
class Artist:
    id: str
    name: str
    releases: Dict[str, Release]
