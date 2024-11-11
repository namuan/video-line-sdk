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

# Chain multiple lines with different timings
video.draw_line(
    start=Coordinates(0, 50),
    end=Coordinates(100, 50),
    color=Color.BLUE,
    start_time=0.0,
    draw_duration=1.0,
).draw_line(
    start=Coordinates(50, 0, absolute=True),
    end=Coordinates(50, 100, absolute=True),
    color=Color("#00FF00"),
    start_time=1.0,
    draw_duration=1.0,
).save(".my_cache/multi_line.mp4")
