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
x = 500
y = 500
start_time = 1.0
video.draw_line(
    start=Coordinates(x, y),
    end=Coordinates(x, y + 10),
    color=Color.WHITE,
    start_time=start_time,
    draw_duration=1.0,
    thickness=5,
).draw_line(
    start=Coordinates(x, y + 5),
    end=Coordinates(x + 1000, y + 5),
    color=Color.WHITE,
    start_time=start_time + 2,
    draw_duration=1.0,
    thickness=5,
).draw_line(
    start=Coordinates(x + 1000, y),
    end=Coordinates(x + 1000, y + 10),
    color=Color.WHITE,
    start_time=start_time + 2 + 1,
    draw_duration=1.0,
    thickness=5,
).save(".my_cache/multi_line.mp4")
