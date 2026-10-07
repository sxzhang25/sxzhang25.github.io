#!/usr/bin/env python3
"""Create a new log entry in _posts/.

Usage:
    python3 new_log.py "Title" ["Subtitle"]

Writes _posts/<today>-<title-as-slug>.md with the title and subtitle filled in;
add the entry text below the front matter. The date in the file name only sets
the order on /logs/ (newest first) and is never shown. The entry appears at
/logs/<title-as-slug>/.
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
        "---\n\n"
        "Write the entry here.\n"
    )
    print(f"created {entry.relative_to(ROOT)}  ->  /logs/{slug}/")


if __name__ == "__main__":
    main()
