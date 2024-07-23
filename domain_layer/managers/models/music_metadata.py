from dataclasses import dataclass


@dataclass(frozen=True)
class MusicMetadata:
    title: str
    artist: str
    album: str
    year: int
    track: int
    genre: str
    duration: int
    filename: str
