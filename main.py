"""Entry program for news-image-20261119 (Python 3.13, standard library only).

The finished image lives beside this file as entry.png; the program simply
copies it to /output/entry.png. No network, no clock, no randomness, so two
runs always write identical bytes. Outside the grader, MAKEFUN_OUTPUT_DIR
stands in for /output.
"""
import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
