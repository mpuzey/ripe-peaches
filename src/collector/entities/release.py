from typing import Dict
from dataclasses import dataclass
from src.collector.entities.review import Review

@dataclass
class Release:
    id: str
    name: str
    releases: Dict[Review]
