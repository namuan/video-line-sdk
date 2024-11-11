import pytest
from video_line_sdk import VideoLine
from video_line_sdk import VideoNotFoundError


def test_video_line_initialization(sample_video_path):
    video = VideoLine(sample_video_path)
    assert video.video_path.name == "sample.mp4"


def test_invalid_video_path():
    with pytest.raises(VideoNotFoundError):
        VideoLine("nonexistent_video.mp4")
