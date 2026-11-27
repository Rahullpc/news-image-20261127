"""Salin poster yang sudah di-render ke direktori output grader.

Program ini TIDAK me-render apa pun. Poster (entry.png) sudah dibuat
sebelumnya dan terletak di folder yang sama dengan file ini; tugas
satu-satunya adalah menyalinnya ke $MAKEFUN_OUTPUT_DIR (atau /output
kalau variabel itu tidak ada) agar grader bisa mengambilnya.
Hanya memakai pustaka standar Python.
"""

import hashlib
import os
import shutil
import sys

MAX_BYTES = 1_048_576  # 1 MiB


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")

    if not os.path.isfile(source):
        print("error: entry.png tidak ditemukan di %s" % here, file=sys.stderr)
        return 1

    source_size = os.path.getsize(source)
    if source_size > MAX_BYTES:
        print("error: entry.png sumber %d byte melebihi batas %d byte"
              % (source_size, MAX_BYTES), file=sys.stderr)
        return 1
    source_sha = sha256_of(source)

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        os.makedirs(output_dir, exist_ok=True)
    except OSError as exc:
        print("error: tidak bisa membuat direktori output %s: %s"
              % (output_dir, exc), file=sys.stderr)
        return 1

    dest = os.path.join(output_dir, "entry.png")
    if os.path.abspath(dest) == os.path.abspath(source):
        print("error: direktori output sama dengan folder sumber; "
              "tidak ada yang perlu disalin", file=sys.stderr)
        return 1
    try:
        shutil.copyfile(source, dest)
    except OSError as exc:
        print("error: gagal menyalin %s ke %s: %s"
              % (source, dest, exc), file=sys.stderr)
        return 1

    size = os.path.getsize(dest)
    if size > MAX_BYTES:
        print("error: hasil salinan %d byte melebihi batas %d byte"
              % (size, MAX_BYTES), file=sys.stderr)
        return 1
    if size != source_size:
        print("error: ukuran hasil salinan (%d byte) berbeda dari sumber "
              "(%d byte)" % (size, source_size), file=sys.stderr)
        return 1

    dest_sha = sha256_of(dest)
    if dest_sha != source_sha:
        print("error: sha256 hasil salinan berbeda dari sumber; "
              "salinan rusak", file=sys.stderr)
        return 1

    print("source: %s" % source)
    print("dest:   %s" % dest)
    print("size:   %d bytes" % size)
    print("sha256: %s" % dest_sha)
    return 0


if __name__ == "__main__":
    sys.exit(main())
