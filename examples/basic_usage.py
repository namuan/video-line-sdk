import os
from pathlib import Path

from video_line_sdk import Color
from video_line_sdk import Coordinates
from video_line_sdk import VideoLine

script_dir = os.path.dirname(__file__)
output_dir = Path(".my_cache")
output_dir.mkdir(exist_ok=True)
video_path = Path(script_dir).joinpath("sample.mp4")
video = VideoLine(video_path.as_posix())
# Basic usage with percentages
(
    video.draw_line(
        start=Coordinates(50, 100),
        end=Coordinates(50, 0),
        color=Color.RED,
        thickness=5,
        draw_duration=2.0,
    ).save(".my_cache/output.mp4")
)
