from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class SpotifyAlbum:
    artist_name: str = None
    album_name: str = None
    release_date: str = None
    album_type: str = None
    total_tracks: int = None
    url: str = None
