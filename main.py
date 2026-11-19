"""Copy the finished entry image to the submission output directory.

The entry image (entry.png, produced by build/render.py) is copied byte
for byte to <output>/entry.png. The copy is deterministic: the same input
bytes always produce the same output bytes, and no metadata, timestamps
or recompression are involved.

Usage:
    python3 main.py              # copies to /output/entry.png
    python3 main.py /some/dir    # copies to /some/dir/entry.png

Standard library only, no network access.
"""

import hashlib
import sys
from pathlib import Path

SOURCE_NAME = "entry.png"
DEFAULT_OUTPUT_DIR = Path("/output")


def source_path():
    """The entry image sitting next to this script."""
    return Path(__file__).resolve().parent / SOURCE_NAME


def digest(data):
    """Short helper: hex SHA-256 of a bytes object."""
    return hashlib.sha256(data).hexdigest()


def copy_entry(destination_dir):
    """Write an exact copy of entry.png into destination_dir.

    Returns the (destination path, sha256 hex) of the file written.
    """
    origin = source_path()
    if not origin.is_file():
        raise SystemExit(f"missing source image: {origin}")
    payload = origin.read_bytes()
    target_dir = Path(destination_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / SOURCE_NAME
    target.write_bytes(payload)
    # Confirm the copy on disk is byte-identical to the source.
    written = target.read_bytes()
    if digest(written) != digest(payload):
        raise SystemExit(f"copy verification failed: {target}")
    return target, digest(payload)


def main(argv):
    """Entry point: pick the output directory and report what was copied."""
    out_dir = Path(argv[1]) if len(argv) > 1 else DEFAULT_OUTPUT_DIR
    target, checksum = copy_entry(out_dir)
    print(f"copied {source_path().name} -> {target}")
    print(f"sha256: {checksum}")


if __name__ == "__main__":
    main(sys.argv)
