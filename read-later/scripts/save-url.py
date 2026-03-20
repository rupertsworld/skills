#!/usr/bin/env python3
"""Save a URL as a simplified, readable PDF."""

import subprocess
import sys
import os
import re
import tempfile
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

VENV_DIR = Path(__file__).parent / ".venv"
PACKAGES = ["requests", "lxml", "readability-lxml"]


def ensure_venv():
    """Create a venv and install deps if needed."""
    if VENV_DIR.exists():
        return
    subprocess.check_call([sys.executable, "-m", "venv", str(VENV_DIR)])
    pip = VENV_DIR / "bin" / "pip"
    subprocess.check_call([str(pip), "install", "-q"] + PACKAGES)


def reexec_in_venv():
    """Re-execute this script inside the venv if we're not already in it."""
    venv_python = VENV_DIR / "bin" / "python3"
    if Path(sys.executable).resolve() == venv_python.resolve():
        return
    ensure_venv()
    os.execv(str(venv_python), [str(venv_python), __file__] + sys.argv[1:])


reexec_in_venv()

import requests  # noqa: E402
from readability import Document  # noqa: E402

DEFAULT_OUTPUT_DIR = Path.home() / "Workspace" / "read-later"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

CSS = """
body {
    font-family: Georgia, 'Times New Roman', serif;
    max-width: 700px;
    margin: 40px auto;
    padding: 0 20px;
    line-height: 1.7;
    color: #222;
    font-size: 16px;
}
h1 { font-size: 1.8em; margin-bottom: 0.3em; line-height: 1.3; }
h2, h3 { margin-top: 1.5em; }
img { max-width: 100%; height: auto; }
pre, code { font-size: 0.9em; background: #f5f5f5; padding: 2px 6px; border-radius: 3px; }
pre { padding: 12px; overflow-x: auto; }
blockquote { border-left: 3px solid #ccc; margin-left: 0; padding-left: 16px; color: #555; }
a { color: #222; text-decoration: underline; }
.source-url { font-size: 0.85em; color: #888; word-break: break-all; margin-bottom: 2em; }
"""


def title_case_slug(text: str, max_len: int = 60) -> str:
    text = re.sub(r"[^\w\s]", "", text).strip()
    words = text.split()
    result = " ".join(w.capitalize() for w in words)
    return result[:max_len].rstrip()


def save_url(url: str, output_dir: Path = DEFAULT_OUTPUT_DIR) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/120.0.0.0 Safari/537.36"
    }
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()

    doc = Document(resp.text)
    title = doc.short_title() or urlparse(url).netloc
    content_html = doc.summary()

    # Resolve relative URLs using the original page URL
    base_url = url.rstrip("/")
    html = f"""<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<base href="{base_url}">
<style>{CSS}</style>
</head><body>
<h1>{title}</h1>
<div class="source-url">{url}</div>
{content_html}
</body></html>"""

    # Build filename as "Title (Author, Year).pdf"
    year = str(date.today().year)
    # Split on common title/author separators: | — – -
    parts = re.split(r"\s*[|—–]\s*|\s+-\s+", title)
    if len(parts) >= 2:
        title_part = title_case_slug(parts[0].strip())
        author_part = title_case_slug(parts[-1].strip())
        filename = f"{title_part} ({author_part}, {year}).pdf"
    else:
        slug = title_case_slug(title)
        filename = f"{slug} ({year}).pdf"
    output_path = output_dir / filename

    with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w", encoding="utf-8") as f:
        f.write(html)
        tmp_html = f.name

    try:
        subprocess.run(
            [
                CHROME,
                "--headless",
                "--disable-gpu",
                "--no-sandbox",
                "--print-to-pdf=" + str(output_path),
                "--print-to-pdf-no-header",
                "--virtual-time-budget=5000",
                tmp_html,
            ],
            capture_output=True,
            timeout=30,
        )
    finally:
        os.unlink(tmp_html)

    if not output_path.exists():
        print(f"ERROR: PDF was not created at {output_path}", file=sys.stderr)
        sys.exit(1)

    size_kb = output_path.stat().st_size / 1024
    print(f"Saved: {output_path}")
    print(f"Title: {title}")
    print(f"Size:  {size_kb:.0f} KB")
    return output_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Save a URL as a readable PDF.")
    parser.add_argument("url", help="The URL to save")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_DIR, help="Output directory")
    args = parser.parse_args()
    save_url(args.url, args.output)
