from typing import List
from dataclasses import dataclass

@dataclass
class DBRelease:
    id: str
    name: str
    reviews: List[str]
