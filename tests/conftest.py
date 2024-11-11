from pathlib import Path

import pytest


@pytest.fixture
def sample_video_path():
    # Use the actual video file from tests/data directory
    base_dir = Path(__file__).parent
    video_path = base_dir / "data" / "sample.mp4"

    if not video_path.exists():
        raise FileNotFoundError(f"Test video file not found at {video_path}")

    return str(video_path)
