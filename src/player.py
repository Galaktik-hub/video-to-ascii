"""
Player module.

Handles the real-time playback loop: iterates over frames, converts
each to ASCII, and renders them to the terminal at the correct FPS.
"""

import sys
import time
from typing import Callable

from src.video import FrameExtractor


class Player:
    """
    Real-time ASCII video player.

    Reads frames from a FrameExtractor, converts them using the
    provided converter function, and displays them in the terminal
    at the original video frame rate.
    """

    # ANSI escape: move cursor to the top-left corner without clearing
    _CURSOR_HOME = "\033[H"
    # ANSI escape: hide / show cursor to avoid flicker
    _CURSOR_HIDE = "\033[?25l"
    _CURSOR_SHOW = "\033[?25h"

    def __init__(
        self,
        frame_extractor: FrameExtractor,
        converter: Callable,
        fps: float,
    ):
        """
        :param frame_extractor: An iterable that yields raw RGB frames.
        :param converter: A callable(frame) -> str that produces ASCII art.
        :param fps: Target frames per second for playback.
        """
        self._frame_extractor = frame_extractor
        self._converter = converter
        self._fps = fps
        self._frame_duration = 1.0 / fps

    def play(self) -> None:
        """
        Start playback.  Blocks until the video ends or the user
        interrupts with Ctrl-C.
        """
        try:
            self._hide_cursor()
            self._clear_screen()

            for frame in self._frame_extractor:
                start = time.perf_counter()

                ascii_art = self._converter(frame)
                self._render(ascii_art)

                self._wait(start)

        except KeyboardInterrupt:
            pass
        finally:
            self._show_cursor()

    # ── rendering helpers ────────────────────────────────────────────

    def _render(self, ascii_art: str) -> None:
        """Move cursor home and overwrite the terminal with new content."""
        sys.stdout.write(self._CURSOR_HOME + ascii_art)
        sys.stdout.flush()

    def _wait(self, frame_start: float) -> None:
        """Sleep for the remaining frame duration to maintain target FPS."""
        elapsed = time.perf_counter() - frame_start
        remaining = self._frame_duration - elapsed
        if remaining > 0:
            time.sleep(remaining)

    # ── cursor helpers ───────────────────────────────────────────────

    def _hide_cursor(self) -> None:
        sys.stdout.write(self._CURSOR_HIDE)
        sys.stdout.flush()

    def _show_cursor(self) -> None:
        sys.stdout.write(self._CURSOR_SHOW)
        sys.stdout.flush()

    @staticmethod
    def _clear_screen() -> None:
        """Clear the entire terminal once at the start of playback."""
        sys.stdout.write("\033[2J")
        sys.stdout.flush()
