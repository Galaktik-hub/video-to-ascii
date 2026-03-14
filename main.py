import argparse

from src.converter import convert_frame
from src.player import Player
from src.terminal import compute_display_size
from src.video import FrameExtractor, Video


def parse_arguments() -> argparse.Namespace:
    """
    Parse and return command-line arguments.

    :return: Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        prog="Video to ASCII",
        description="Play videos in your terminal with ASCII characters.",
    )
    parser.add_argument("-v", "--video", help="Path to the video file", required=True)
    parser.add_argument(
        "-W",
        "--width",
        type=int,
        default=None,
        help="Override display width (columns)",
    )
    parser.add_argument(
        "-H",
        "--height",
        type=int,
        default=None,
        help="Override display height (rows)",
    )
    parser.add_argument(
        "-i",
        "--invert",
        type=bool,
        default=False,
        help="Invert the intensity of each pixel",
    )
    return parser.parse_args()


def main() -> None:
    """Application entry point."""
    args = parse_arguments()

    video = Video(args.video)

    invert = args.invert

    try:
        # Compute the display size
        display_cols, display_rows = compute_display_size(
            frame_width=video.width,
            frame_height=video.height,
            term_cols=args.width,
            term_rows=args.height,
        )

        frame_extractor = FrameExtractor(video)

        def converter(frame):
            return convert_frame(frame, display_cols, display_rows, invert)

        player = Player(
            frame_extractor=frame_extractor,
            converter=converter,
            fps=video.fps,
        )

        player.play()
    finally:
        video.release()


if __name__ == "__main__":
    main()
