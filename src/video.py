import mimetypes
from pathlib import Path

import cv2
import numpy as np


def is_media_file(file: Path) -> bool:
    """
    Determine whether the provided file is a video based on its MIME type.

    :param file: Path to the file.
    :return: True if the file is a video, False otherwise.
    """
    mime = mimetypes.guess_type(file)[0]

    if mime is not None:
        return mime.split("/")[0] == "video"

    return False


def _validate_provided_path(path: str) -> Path:
    """
    Validate that the path points to an existing video file.

    :param path: Raw path string from the user.
    :return: A validated Path object.
    :raises FileNotFoundError: If the file does not exist.
    :raises ValueError: If the file is not a video.
    """
    resolved = Path(path)

    if not resolved.is_file():
        raise FileNotFoundError(f"File '{resolved}' was not found.")

    if not is_media_file(resolved):
        raise ValueError("File does not seem to be a video.")

    return resolved


class Video:
    """
    Represents a loaded video file.

    Wraps an OpenCV VideoCapture and exposes metadata properties.
    """

    def __init__(self, path: str):
        self.path: Path = _validate_provided_path(path)
        self._capture = cv2.VideoCapture(str(self.path))

        if not self._capture.isOpened():
            raise RuntimeError(f"OpenCV could not open '{self.path}'.")

    @property
    def fps(self) -> float:
        """Frames per second of the video."""
        return self._capture.get(cv2.CAP_PROP_FPS)

    @property
    def total_frames(self) -> int:
        """Total number of frames in the video."""
        return int(self._capture.get(cv2.CAP_PROP_FRAME_COUNT))

    @property
    def width(self) -> int:
        """Frame width in pixels."""
        return int(self._capture.get(cv2.CAP_PROP_FRAME_WIDTH))

    @property
    def height(self) -> int:
        """Frame height in pixels."""
        return int(self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    @property
    def capture(self) -> cv2.VideoCapture:
        """The underlying OpenCV VideoCapture object."""
        return self._capture

    def release(self) -> None:
        """Release the OpenCV VideoCapture resources."""
        self._capture.release()


class FrameExtractor:
    """
    Iterable that yields frames from a Video one at a time.

    Usage::

        extractor = FrameExtractor(video)
        for frame in extractor:
            process(frame)
    """

    def __init__(self, video: Video):
        self._video = video

    def __iter__(self):
        """Return self as the iterator."""
        return self

    def __next__(self) -> np.ndarray:
        """
        Read and return the next frame.

        :return: A RGB numpy array of the frame.
        :raises StopIteration: When there are no more frames.
        """
        success, frame = self._video.capture.read()

        if not success:
            raise StopIteration

        return frame
