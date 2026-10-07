---
# Create entries with `python3 new_log.py "Title" "Subtitle"`, or copy this file
# to _posts/YYYY-MM-DD-some-title.md. The date in the file name only sets the
# order on /logs/ (newest first) and is never shown; the rest of the file name
# becomes the URL (/logs/some-title/).
title: Some title
subtitle: A short line shown under the title
display_date: Aug 12-15, 2025   # optional; shown above the title (leave "" to hide)
---

The entry text goes here, in Markdown.

To add a figure, put the full-size image in _media/logs/some-title/, run resize_media.py, and add a line like
this where it should appear (it shows to the right of the text that follows):

{% include figure.html src="photo.jpg" caption="An optional caption." %}
