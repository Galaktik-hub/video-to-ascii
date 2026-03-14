import shutil


def get_terminal_size() -> tuple[int, int]:
    """
    Return the current terminal size.

    :return: A tuple (columns, rows).
    """
    size = shutil.get_terminal_size()
    return size.columns, size.lines


def compute_display_size(
    frame_width: int,
    frame_height: int,
    term_cols: int | None = None,
    term_rows: int | None = None,
) -> tuple[int, int]:
    """
    Compute the best (cols, rows) to display a frame in the terminal
    while preserving the video's aspect ratio.

    Terminal characters are roughly twice as tall as they are wide, so
    we account for that with a 0.5 correction factor on the height.

    :param frame_width: Original video frame width in pixels.
    :param frame_height: Original video frame height in pixels.
    :param term_cols: Override for terminal columns (auto-detected if None).
    :param term_rows: Override for terminal rows (auto-detected if None).
    :return: (display_columns, display_rows) that fit the terminal.
    """
    if term_cols is None or term_rows is None:
        term_cols, term_rows = get_terminal_size()

    aspect_ratio = frame_width / frame_height

    char_aspect_correction = 0.5

    # Fit by width first, then check if height overflows
    display_cols = term_cols
    display_rows = int(display_cols / aspect_ratio * char_aspect_correction)

    if display_rows > term_rows:
        display_rows = term_rows
        display_cols = int(display_rows * aspect_ratio / char_aspect_correction)

    return max(display_cols, 1), max(display_rows, 1)
