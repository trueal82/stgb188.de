from pathlib import Path

BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
CONTENT_DIR = BASE_DIR / "content"
OUTPUT_DIR = BASE_DIR / "static"

def parse_content_file(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    title = path.stem.capitalize()
    heading = title
    filename = path.name
    content = raw
    order = 0

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
                        filename = value
                    elif key == "order":
                        try:
                            order = int(value)
                        except ValueError:
                            pass
    # Ensure Startseite (index.html) is ordered first regardless of filename sorting
    if filename == "index.html":
        order = -100

    return {
        "filename": filename,
        "title": title,
        "heading": heading,
        "content": content.strip(),
        "order": order,
    }


def load_pages() -> list[dict]:
    if not CONTENT_DIR.exists():
        raise FileNotFoundError(f"Content directory not found: {CONTENT_DIR}")
    pages = []
    for path in CONTENT_DIR.glob("*.html"):
        pages.append(parse_content_file(path))
    pages.sort(key=lambda page: (page.get("order", 0), page["filename"]))
    return pages


def load_template(name: str) -> str:
    path = TEMPLATES_DIR / name
    return path.read_text(encoding="utf-8")


def render_menu(pages: list[dict], active_href: str) -> str:
    template = load_template("menu.html")
    menu = []
    for item in pages:
        active = "active" if item["filename"] == active_href else ""
        menu.append(
            template.replace("{{href}}", item["filename"]).replace("{{label}}", item["title"]).replace("{{active}}", active)
        )
    return "\n".join(menu)


def build_page(page: dict, pages: list[dict]):
    base = load_template("base.html")
    footer = load_template("footer.html")
    from datetime import datetime
    html = (
        base.replace("{{title}}", page["title"])
        .replace("{{heading}}", page["heading"])
        .replace("{{menu}}", render_menu(pages, page["filename"]))
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


def copy_assets():
    assets_src = TEMPLATES_DIR / 'assets'
    js_src = TEMPLATES_DIR / 'js'
    assets_dst = OUTPUT_DIR / 'assets'
    js_dst = OUTPUT_DIR / 'js'
    # copy asset files (SVGs, images)
    if assets_src.exists():
        assets_dst.mkdir(parents=True, exist_ok=True)
        for p in assets_src.iterdir():
            if p.is_file():
                (assets_dst / p.name).write_bytes(p.read_bytes())
                print(f"Copied asset: {assets_dst / p.name}")
    # copy JS files
    if js_src.exists():
        js_dst.mkdir(parents=True, exist_ok=True)
        for p in js_src.iterdir():
            if p.is_file() and not p.name.endswith('.bak') and not p.name.startswith('.'):
                (js_dst / p.name).write_text(p.read_text(encoding='utf-8'), encoding='utf-8')
                print(f"Copied script: {js_dst / p.name}")


def build():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    copy_style()
    copy_assets()
    pages = load_pages()
    for page in pages:
        build_page(page, pages)


if __name__ == "__main__":
    build()
