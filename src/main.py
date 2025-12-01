import argparse
import mimetypes


def convert_to_ascii():
    pass


def play():
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Video to ASCII",
        description="A simple program to play your videos in your terminal with ASCII characters",
    )
    parser.add_argument('-v', '--video', help='Path to video file', required=True)
    args = parser.parse_args()

    video = args.video

    try:
        mime, _ = mimetypes.guess_type(video)

        # Validate the given file
        if not mime.startswith("video/"):
            raise ValueError("The given file does not correspond to an .mp4 file.")

    except FileNotFoundError:
        print("The given path does not point to any file.")

    video_ascii = convert_to_ascii()

    play(video_ascii)
