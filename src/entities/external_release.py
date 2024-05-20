from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class ExternalRelease:
    name: str
    artist: str
    # TODO: stop date from being nullable
    date: str = None
    type: str = None
    total_tracks: int = None
    spotify_url: str = None
