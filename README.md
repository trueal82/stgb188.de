# StGB 188 Static Website

This repository contains a small privacy-friendly static website with a shared layout and content pages. No external fonts, scripts, or trackers are used.

## Structure

- `build.py` — generates HTML pages in `static/` from page content and shared templates.
- `templates/base.html` — page shell with header, navigation, content container, and footer.
- `templates/menu.html` — shared navigation item template.
- `templates/footer.html` — shared footer block.
- `templates/style.css` — local stylesheet used by all pages.
- `content/` — source page fragments and frontmatter metadata.
- `static/` — generated website output ready for publishing.

## Pages

- `static/index.html` — Startseite
- `static/impressum.html` — Impressum
- `static/datenschutzerklaerung.html` — Datenschutzerklärung
- `static/paragraph188.html` — Was ist StGB 188

## Build

Run the generator to create or refresh the static files:

```bash
/usr/local/bin/python3 build.py
```

Open `static/index.html` in a browser to preview the site.

## Publish to GitHub

The generated site lives in `static/`. For GitHub Pages, you can either:

1. copy the contents of `static/` into a `docs/` directory and publish from the `docs/` folder in repository settings, or
2. commit `static/` and use a custom GitHub Pages deployment workflow that serves from that folder.

## Maintenance

- Add or update content pages in `content/`.
- Change layout and shared markup in `templates/`.
- Adjust look-and-feel in `templates/style.css`.

## Privacy and compliance

- No external resources are loaded.
- No JavaScript or analytics are included.
- The website is fully self-contained and does not share user data with third parties.
