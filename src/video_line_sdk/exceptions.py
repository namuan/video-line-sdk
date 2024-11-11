# video_line_sdk/exceptions.py
class VideoLineError(Exception):
    """Base exception for VideoLine SDK"""


class VideoNotFoundError(VideoLineError):
    """Raised when video file is not found"""


class InvalidVideoError(VideoLineError):
    """Raised when video file is invalid"""
