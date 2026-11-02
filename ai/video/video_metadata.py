from dataclasses import dataclass


@dataclass(frozen=True)
class VideoMetadata:
    """
    Stores metadata about the video source.
    """

    source_id: str
    source_path: str
    fps: float
    width: int
    height: int