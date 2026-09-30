# Personal site

<a href="https://sxzhang25.github.io/">sxzhang25.github.io</a>

Built using Jekyll and Github Pages.

I try and keep things as simple as possible. There are many commits because I like to change every little thing.

## Editing content

Most content lives in `_data/`:

- `publications.yml` — publications list (authors link via `people.yml`)
- `people.yml` — collaborator homepages
- `projects.yml` — projects page
- `news.yml` — home page news (enable with `show_news: true` in `index.html`)
- `nav.yml` — header links

## Structure

- `_layouts/base.html` — HTML shell; `default.html` (main site) and `publication.html` (paper project pages) extend it
- `_includes/` — shared head, header, publication entry, analytics, MathJax
- `_sass/` — styles: `_tokens.scss` (colors, fonts, breakpoints), `_base.scss` (shared element defaults), `_site.scss`, `_post.scss`, `_project-page.scss`
- `css/main.scss`, `css/publication.scss` — stylesheet entry points

Pages that use LaTeX should set `math: true` in their front matter. Set `google_analytics` in `_config.yml` to enable GA4.

## Local preview

```sh
bundle install
bundle exec jekyll serve
```
