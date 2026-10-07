#!/usr/bin/env python3
"""Keep the visuals galleries in sync with the images in assets/artwork/.

Usage:
    python3 new_artwork.py            # add new entries/galleries, remove orphaned entries
    python3 new_artwork.py --dry-run  # only report what would change

Each gallery is a folder (folders can be nested, e.g. highlights/2024):
    assets/artwork/<gallery>/      the images
    _artworks/<gallery>/           one entry (.md) per piece
    visuals/<gallery>/index.html   the gallery page, also listed in the visuals menu

For each new image (e.g. assets/artwork/highlights/blue-hour.jpg) this writes a
stub _artworks/highlights/blue-hour.md with the image path filled in and the
title guessed from the file name, keeping its capitalization (dashes and
underscores become spaces). Fill in the medium and size (and fix the title) by
hand. Existing entries are never modified.

If an image folder has no gallery page yet, one is created (titled after the
folder, e.g. portraits-of-home -> "portraits of home") at the end of its menu.

Entries whose image points into assets/artwork/ but whose file no longer exists
are deleted. Entries that point anywhere else (e.g. an image hosted elsewhere)
are left alone. Gallery pages are never deleted.
"""

import argparse
import datetime
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent
IMAGE_DIR = ROOT / "assets" / "artwork"
ENTRY_DIR = ROOT / "_artworks"
PAGE_DIR = ROOT / "visuals"
IMAGE_URL_PREFIX = "/assets/artwork/"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


def entry_image(entry):
    """The `image:` value of an entry (the whole line, so spaces are kept), or None."""
    match = re.search(r"^image:[ \t]*(.*?)[ \t]*$", entry.read_text(), re.MULTILINE)
    return match.group(1).strip("'\"") if match else None


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def remove_orphans(dry_run):
    """Delete entries for local images that have been deleted."""
    removed = []
    for entry in sorted(ENTRY_DIR.rglob("*.md")):
        image = entry_image(entry)
        if not image or not image.startswith(IMAGE_URL_PREFIX):
            continue
        if not (ROOT / image.lstrip("/")).exists():
            if not dry_run:
                entry.unlink()
            removed.append((entry.relative_to(ROOT), image))
    return removed


def add_entries(dry_run):
    """Create stub entries for images that no entry uses yet."""
    used = {entry_image(entry) for entry in ENTRY_DIR.rglob("*.md")}
    created, loose = [], []
    for image in sorted(IMAGE_DIR.rglob("*")):
        if not image.is_file() or image.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        gallery = image.parent.relative_to(IMAGE_DIR)
        if gallery == pathlib.Path("."):
            loose.append(image.relative_to(ROOT))
            continue
        url = "/" + image.relative_to(ROOT).as_posix()
        if url in used:
            continue
        entry = ENTRY_DIR / gallery / f"{slugify(image.stem)}.md"
        if entry.exists():
            print(f"skipped {image.relative_to(ROOT)}: {entry.relative_to(ROOT)} already exists")
            continue
        # Keep the file name's own capitalization; only dashes/underscores become spaces.
        title = re.sub(r"[-_]+", " ", image.stem).strip()
        date = datetime.date.fromtimestamp(image.stat().st_mtime).isoformat()
        if not dry_run:
            entry.parent.mkdir(parents=True, exist_ok=True)
            entry.write_text(
                "---\n"
                f"image: {url}\n"
                f"title: {title}\n"
                "medium: \n"
                "size: \n"
                f"date: {date}\n"
                "---\n"
            )
        created.append(entry.relative_to(ROOT))
    return created, loose


def next_nav_order(parent_dir):
    """One more than the largest nav_order among the gallery pages in parent_dir."""
    orders = [0]
    for page in parent_dir.glob("*/index.html"):
        match = re.search(r"^nav_order:\s*(\d+)", page.read_text(), re.MULTILINE)
        if match:
            orders.append(int(match.group(1)))
    return max(orders) + 1


def add_gallery_pages(dry_run):
    """Create a gallery page for every image folder (and its parents) that lacks one."""
    created = []
    folders = {d.relative_to(IMAGE_DIR) for d in IMAGE_DIR.rglob("*") if d.is_dir()}
    for folder in sorted(folders, key=lambda f: len(f.parts)):  # parents first
        page = PAGE_DIR / folder / "index.html"
        if page.exists():
            continue
        title = re.sub(r"[-_]+", " ", folder.name).strip()
        order = next_nav_order(page.parent.parent)
        if not dry_run:
            page.parent.mkdir(parents=True, exist_ok=True)
            page.write_text(
                "---\n"
                "layout: default\n"
                f"title: {title}\n"
                f"gallery: {folder.as_posix()}   # folder name in _artworks/ and assets/artwork/\n"
                f"nav_order: {order}   # position in the visuals submenu\n"
                "wide: true\n"
                "intro:   # optional text above the artwork (Markdown); leave empty for none\n"
                "---\n"
                '<section class="page-content">\n'
                "\t{% include gallery.html folder=page.gallery %}\n"
                "</section>\n"
            )
        created.append(page.relative_to(ROOT))
    return created


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dry-run", action="store_true", help="report changes without making them")
    args = parser.parse_args()

    ENTRY_DIR.mkdir(exist_ok=True)
    removed = remove_orphans(args.dry_run)
    created, loose = add_entries(args.dry_run)
    pages = add_gallery_pages(args.dry_run)

    prefix = "would " if args.dry_run else ""
    if removed:
        print(f"{prefix}remove (image file is gone):")
        for path, image in removed:
            print(f"  {path}  ({image})")
    if pages:
        print(f"{prefix}create gallery pages:")
        for path in pages:
            print(f"  {path}")
    if created:
        print(f"{prefix}create entries:")
        for path in created:
            print(f"  {path}")
        if not args.dry_run:
            print("fill in the medium and size for each, then rebuild.")
    if loose:
        print("skipped (move these into a gallery folder such as assets/artwork/highlights/):")
        for path in loose:
            print(f"  {path}")
    if not (removed or created or pages or loose):
        print("galleries are already in sync with assets/artwork/")


if __name__ == "__main__":
    main()
