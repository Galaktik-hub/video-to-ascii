import cv2
import numpy as np

# Characters ordered from lightest to darkest density.
ASCII_CHARS = " .,-~:;=!*#$@"


def frame_to_grayscale(frame: np.ndarray) -> np.ndarray:
    """
    Convert an RGB color frame to a grayscale image.

    :param frame: RGB image as a numpy array (H×W×3).
    :return: Grayscale image as a numpy array (H×W).
    """
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


def resize_frame(frame: np.ndarray, width: int, height: int) -> np.ndarray:
    """
    Resize a frame to the given dimensions.

    :param frame: Input image (any number of channels).
    :param width: Target width in pixels / columns.
    :param height: Target height in pixels / rows.
    :return: Resized image.
    """
    return cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)


def map_pixels_to_ascii(grayscale_frame: np.ndarray, invert: bool) -> str:
    """
    Map every pixel intensity (0-255) in a grayscale frame to an ASCII
    character, producing a multi-line string.

    :param grayscale_frame: 2D numpy array of uint8 values.
    :param invert: Invert the pixels' intensity.
    :return: A string with newlines separating each row.
    """
    global ASCII_CHARS

    # Normalize pixel values into the index range of ASCII_CHARS
    num_chars = len(ASCII_CHARS)
    indices = (grayscale_frame / 255 * (num_chars - 1)).astype(int)

    # Invert the ASCII_CHARS if we want to invert the pixels intensity
    if invert:
        ASCII_CHARS = ASCII_CHARS[::-1]

    # Build each row by looking up the character for every pixel
    rows: list[str] = []
    for row in indices:
        rows.append("".join(ASCII_CHARS[pixel] for pixel in row))

    return "\n".join(rows)


def convert_frame(frame: np.ndarray, width: int, height: int, invert: bool) -> str:
    """
    Take a raw RGB frame and return a ready-to-display ASCII string.

    :param frame: RGB image from OpenCV.
    :param width: Target width (terminal columns).
    :param height: Target height (terminal rows).
    :param invert: Invert the pixels' intensity.
    :return: Multi-line ASCII art string.
    """
    grayscale = frame_to_grayscale(frame)
    resized = resize_frame(grayscale, width, height)
    return map_pixels_to_ascii(resized, invert)
