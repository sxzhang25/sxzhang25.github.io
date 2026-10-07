#!/usr/bin/env python3
"""Make web-sized copies of the full-size images in _media/.

Usage:
    python3 resize_media.py            # resize new or changed images, remove stale copies
    python3 resize_media.py --dry-run  # only report what would change

Keep the full-size originals in _media/ (never committed; back them up
elsewhere) using the same folders as the site:
    _media/logs/<post-slug>/photo.jpg    ->  assets/logs/<post-slug>/photo.jpg
    _media/artwork/<gallery>/piece.png   ->  assets/artwork/<gallery>/piece.jpg

Each copy is at most MAX_EDGE pixels on its long edge (smaller for logs, whose
figures are shown narrower than artwork), rotated upright, and
stripped of metadata (including camera location). Photos stay JPEGs with their
original file name; PNGs become JPEGs too (piece.png -> piece.jpg) unless they
have transparency. Only images whose original is new or newer than its copy are
redone (delete a copy to force it, e.g. after changing MAX_EDGE). Copies in assets/logs/ and assets/artwork/ whose original is gone are
deleted. Other files (e.g. .mp4, .gif) are copied as they are.

After adding artwork, run new_artwork.py to create entries for the new copies.
"""

import argparse
import pathlib
import shutil

from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).resolve().parent
SOURCE = ROOT / "_media"
OUTPUT = ROOT / "assets"
MANAGED = ("logs", "artwork")   # folders of assets/ that mirror _media/
MAX_EDGE = {"logs": 1600, "artwork": 2400}   # long edge in pixels, per folder
JPEG_QUALITY = 82
RESIZABLE = {".jpg", ".jpeg", ".png", ".webp"}
SKIP = {".DS_Store", ".gitkeep"}


def has_transparency(image):
    if image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info):
        return image.convert("RGBA").getchannel("A").getextrema()[0] < 255
    return False


def output_path(source):
    """Where the web copy of an original goes."""
    target = OUTPUT / source.relative_to(SOURCE)
    if source.suffix.lower() == ".png":
        with Image.open(source) as image:
            if not has_transparency(image):
                return target.with_suffix(".jpg")
    return target


def make_copy(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    if source.suffix.lower() not in RESIZABLE:
        shutil.copy2(source, target)
        return
    with Image.open(source) as image:
        image = ImageOps.exif_transpose(image)
        max_edge = MAX_EDGE[source.relative_to(SOURCE).parts[0]]
        image.thumbnail((max_edge, max_edge), Image.LANCZOS)
        if target.suffix.lower() == ".png":
            image.save(target, optimize=True)
        else:
            image.convert("RGB").save(target, quality=JPEG_QUALITY, optimize=True, progressive=True)
    # A small image can come out larger than the original; keep the original then.
    if target.suffix.lower() == source.suffix.lower() and target.stat().st_size > source.stat().st_size:
        shutil.copy2(source, target)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dry-run", action="store_true", help="report changes without making them")
    args = parser.parse_args()

    sources = [p for folder in MANAGED for p in sorted((SOURCE / folder).rglob("*"))
               if p.is_file() and p.name not in SKIP]
    wanted = set()
    made = []
    for source in sources:
        target = output_path(source)
        wanted.add(target)
        if target.exists() and target.stat().st_mtime >= source.stat().st_mtime:
            continue
        if not args.dry_run:
            make_copy(source, target)
        made.append((source, target))

    stale = [p for folder in MANAGED for p in sorted((OUTPUT / folder).rglob("*"))
             if p.is_file() and p.name not in SKIP and p not in wanted]
    if not args.dry_run:
        for path in stale:
            path.unlink()

    prefix = "would " if args.dry_run else ""
    if made:
        print(f"{prefix}write:")
        for source, target in made:
            size = "" if args.dry_run else f"  ({source.stat().st_size / 1e6:.1f} MB -> {target.stat().st_size / 1e6:.1f} MB)"
            print(f"  {target.relative_to(ROOT)}{size}")
    if stale:
        print(f"{prefix}remove (original is gone from _media/):")
        for path in stale:
            print(f"  {path.relative_to(ROOT)}")
    if not (made or stale):
        print("assets/ is already in sync with _media/")


if __name__ == "__main__":
    main()
