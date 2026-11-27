"""Entrypoint for the news-image-20261127 poster.

Renders THE WORLD front page for Friday 27 November 2026 to
``entry.png`` (1024x1024) next to this file, using only the Python
standard library plus Pillow for drawing.

Run:  python3 main.py
"""

import os

from draw_poster import draw_poster

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    poster = draw_poster()
    if poster.size != (1024, 1024):
        raise SystemExit("unexpected poster size: {}".format(poster.size))
    out_path = os.path.join(HERE, "entry.png")
    poster.save(out_path, "PNG")
    print("saved {} ({}x{})".format(out_path, poster.width, poster.height))


if __name__ == "__main__":
    main()
