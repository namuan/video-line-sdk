# video_line_sdk/coordinates.py
from dataclasses import dataclass


@dataclass
class Coordinates:
    x: float
    y: float
    absolute: bool = False

    def __post_init__(self):
        if not self.absolute:
            if not 0 <= self.x <= 100 or not 0 <= self.y <= 100:
                raise ValueError("Percentage coordinates must be between 0 and 100")
