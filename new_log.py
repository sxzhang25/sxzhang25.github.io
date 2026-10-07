#!/usr/bin/env python3
"""Create a new log entry in _posts/.

Usage:
    python3 new_log.py "Title" ["Subtitle"]

Writes _posts/<today>-<title-as-slug>.md with the title and subtitle filled in;
add the entry text below the front matter. The date in the file name only sets
the order on /logs/ (newest first). To show a date, fill in display_date (any
text, e.g. "Aug 2025"); it appears above the title. The
entry appears at /logs/<title-as-slug>/. Put its full-size images in
_media/logs/<title-as-slug>/ and run resize_media.py; place one with
    {% include figure.html src="photo.jpg" caption="Optional caption." %}
"""

import datetime
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
POSTS = ROOT / "_posts"


def yaml_string(text):
    """Quote a value for YAML front matter."""
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def main():
    if len(sys.argv) not in (2, 3):
        sys.exit(__doc__)
    title = sys.argv[1]
    subtitle = sys.argv[2] if len(sys.argv) == 3 else ""
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    if not slug:
        sys.exit("the title needs at least one letter or number")
    if any(path.name.endswith(f"-{slug}.md") for path in POSTS.glob("*.md")):
        sys.exit(f"an entry with the URL /logs/{slug}/ already exists in _posts/")
    POSTS.mkdir(exist_ok=True)
    entry = POSTS / f"{datetime.date.today().isoformat()}-{slug}.md"
    entry.write_text(
        "---\n"
        f"title: {yaml_string(title)}\n"
        f"subtitle: {yaml_string(subtitle)}\n"
        'display_date: ""   # optional, shown above the title, e.g. "Aug 2025"\n'
        "---\n\n"
        "Write the entry here.\n"
    )
    images = ROOT / "_media" / "logs" / slug
    images.mkdir(parents=True, exist_ok=True)
    print(f"created {entry.relative_to(ROOT)}  ->  /logs/{slug}/")
    print(f"put this entry's images in {images.relative_to(ROOT)}/, then run resize_media.py")


if __name__ == "__main__":
    main()
