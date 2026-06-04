from pathlib import Path

BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
CONTENT_DIR = BASE_DIR / "content"
OUTPUT_DIR = BASE_DIR / "static"

NAV_ITEMS = [
    {"href": "index.html", "label": "Startseite"},
    {"href": "impressum.html", "label": "Impressum"},
    {"href": "datenschutzerklaerung.html", "label": "Datenschutzerklärung"},
    {"href": "paragraph188.html", "label": "Was ist der Paragraph 188"},
]


def parse_content_file(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    title = path.stem.capitalize()
    heading = title
    content = raw

    if raw.startswith("---"):
        parts = raw.split("---", 2)
        if len(parts) >= 3:
            _, meta_block, content = parts
            for line in meta_block.strip().splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    key = key.strip().lower()
                    value = value.strip()
                    if key == "title":
                        title = value
                    elif key == "heading":
                        heading = value
                    elif key == "filename":
                        path = path.with_name(value)
    return {
        "filename": path.name,
        "title": title,
        "heading": heading,
        "content": content.strip(),
    }


def load_pages() -> list[dict]:
    if not CONTENT_DIR.exists():
        raise FileNotFoundError(f"Content directory not found: {CONTENT_DIR}")
    pages = []
    for path in sorted(CONTENT_DIR.glob("*.html")):
        pages.append(parse_content_file(path))
    return pages


def load_template(name: str) -> str:
    path = TEMPLATES_DIR / name
    return path.read_text(encoding="utf-8")


def render_menu(active_href: str) -> str:
    template = load_template("menu.html")
    menu = []
    for item in NAV_ITEMS:
        active = "active" if item["href"] == active_href else ""
        menu.append(
            template.replace("{{href}}", item["href"]).replace("{{label}}", item["label"]).replace("{{active}}", active)
        )
    return "\n".join(menu)


def build_page(page: dict):
    base = load_template("base.html")
    footer = load_template("footer.html")
    from datetime import datetime
    html = (
        base.replace("{{title}}", page["title"])
        .replace("{{heading}}", page["heading"])
        .replace("{{menu}}", render_menu(page["filename"]))
        .replace("{{content}}", page["content"])
        .replace("{{footer}}", footer)
        .replace("{{year}}", str(datetime.now().year))
    )
    output_path = OUTPUT_DIR / page["filename"]
    output_path.write_text(html, encoding="utf-8")
    print(f"Written: {output_path}")


def copy_style():
    style = load_template("style.css")
    css_dir = OUTPUT_DIR / "css"
    css_dir.mkdir(parents=True, exist_ok=True)
    (css_dir / "style.css").write_text(style, encoding="utf-8")
    print(f"Written: {css_dir / 'style.css'}")


def build():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    copy_style()
    for page in load_pages():
        build_page(page)


if __name__ == "__main__":
    build()
