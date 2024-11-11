# Video Line SDK

A Python SDK for drawing animated lines on videos.

![](docs/sample.gif)

## Features

- Draw animated lines on videos
- Customizable line colors, thickness, and animation duration

## Installation

```shell
python3 -m pip install git+https://github.com/namuan/video-line-sdk
```

## Quick Start

### Basic Usage

```python
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
```

### Advanced Usage

```python
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
    start=Coordinates(50, 0),
    end=Coordinates(50, 100),
    color=Color("#00FF00"),
    start_time=1.0,
    draw_duration=1.0,
).save(".my_cache/multi_line.mp4")
```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

### Fork the repository
Create your feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request

## Development Setup

```shell
# Clone the repository
git clone https://github.com/namuan/video-line-sdk.git
cd video-line-sdk

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements/requirements-dev.txt
```

## Testing

### Run all tests
```shell
./venv/bin/pytest
```

### Run specific test file
```shell
./venv/bin/pytest tests/test_core.py
```

### Run with verbose output
```shell
./venv/bin/pytest -v
```

# Run with coverage report
```shell
./venv/bin/pytest --cov=video-line-sdk --cov-report=html
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Support
If you encounter any problems or have suggestions, please open an issue.
