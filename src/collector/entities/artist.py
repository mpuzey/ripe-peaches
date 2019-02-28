from typing import Dict
from dataclasses import dataclass


@dataclass
class Artist:
    id: str
    name: str
    releases: Dict
