from typing import List
from dataclasses import dataclass

@dataclass
class DBArtist:
    id: str
    name: str
    releases: List[str]
