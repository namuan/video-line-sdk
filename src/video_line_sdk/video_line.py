import logging
from pathlib import Path
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import numpy as np
from moviepy.editor import ColorClip
from moviepy.editor import CompositeVideoClip
from moviepy.editor import VideoFileClip
from moviepy.video.VideoClip import VideoClip

from .color import Color
from .coordinates import Coordinates
from .exceptions import InvalidVideoError
from .exceptions import VideoLineError
from .exceptions import VideoNotFoundError


class VideoLine:
    def __init__(self, video_path: str, verbose: bool = False):
        self.video_path = Path(video_path)
        self._setup_logging(verbose)
        self._load_video()
        self._pending_lines: List[dict] = []

    def _setup_logging(self, verbose: bool):
        self.logger = logging.getLogger(__name__)
        level = logging.INFO if verbose else logging.WARNING
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=level
        )

    def _load_video(self):
        if not self.video_path.exists():
            raise VideoNotFoundError(f"Video file not found: {self.video_path}")

        try:
            self._clip = VideoFileClip(str(self.video_path))
        except Exception as e:
            raise InvalidVideoError(f"Failed to load video: {e}")

    def _convert_coordinates(self, coords: Coordinates) -> Tuple[int, int]:
        return int(coords.x), int(coords.y)

    def _make_mask_creator(
        self,
        start: Coordinates,
        end: Coordinates,
        thickness: int,
        draw_duration: float,
        start_time: float,
    ) -> callable:
        start_x, start_y = self._convert_coordinates(start)
        end_x, end_y = self._convert_coordinates(end)

        def create_mask(t):
            mask = np.zeros((self.height, self.width), dtype="float32")

            if t < start_time:
                return mask

            adjusted_t = t - start_time

            if adjusted_t < draw_duration:
                progress = adjusted_t / draw_duration
                current_x = int(start_x + (end_x - start_x) * progress)
                current_y = int(start_y + (end_y - start_y) * progress)

                x_coords = np.linspace(start_x, current_x, num=1000)
                y_coords = np.linspace(start_y, current_y, num=1000)
            else:
                x_coords = np.linspace(start_x, end_x, num=1000)
                y_coords = np.linspace(start_y, end_y, num=1000)

            for x, y in zip(x_coords, y_coords):
                x, y = int(x), int(y)
                if 0 <= x < self.width and 0 <= y < self.height:
                    mask[
                        max(0, y - thickness // 2) : min(
                            self.height, y + thickness // 2
                        ),
                        max(0, x - thickness // 2) : min(
                            self.width, x + thickness // 2
                        ),
                    ] = 1.0

            return mask

        return create_mask

    def draw_line(
        self,
        start: Coordinates,
        end: Coordinates,
        color: Union[Color, str] = Color.RED,
        thickness: int = 5,
        draw_duration: float = 2.0,
        start_time: Optional[float] = None,
    ) -> "VideoLine":
        if isinstance(color, str):
            color = Color(color)

        self._pending_lines.append(
            {
                "start": start,
                "end": end,
                "color": color,
                "thickness": thickness,
                "draw_duration": draw_duration,
                "start_time": start_time if start_time is not None else 0.0,
            }
        )

        return self

    def save(self, output_path: str, fps: Optional[int] = None) -> str:
        if not self._pending_lines:
            raise VideoLineError("No lines to draw")

        clips = [self._clip]

        for line in self._pending_lines:
            color_clip = ColorClip(
                size=(self.width, self.height), color=Color(line["color"]).rgb
            )
            color_clip = color_clip.set_duration(self._clip.duration)

            mask_clip = VideoClip(
                make_frame=self._make_mask_creator(
                    line["start"],
                    line["end"],
                    line["thickness"],
                    line["draw_duration"],
                    line["start_time"],
                ),
                duration=self._clip.duration,
                ismask=True,
            )

            color_clip = color_clip.set_mask(mask_clip)
            clips.append(color_clip)

        final_clip = CompositeVideoClip(clips)
        final_clip.write_videofile(
            output_path, fps=fps or self._clip.fps, codec="libx264"
        )

        return output_path

    @property
    def width(self) -> int:
        return int(self._clip.w)

    @property
    def height(self) -> int:
        return int(self._clip.h)

    @property
    def duration(self) -> float:
        return float(self._clip.duration)

    @property
    def fps(self) -> float:
        return float(self._clip.fps)

    def __enter__(self) -> "VideoLine":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self, "_clip"):
            self._clip.close()
