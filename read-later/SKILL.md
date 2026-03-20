---
name: read-later
description: Save a web URL as a simplified, readable PDF for later reading. Use when the user wants to save a webpage, article, or link for later reading, or says "read later", "save this page", "save article".
---

Save a web URL as a clean, readable PDF. Refer to any skill-specific documentation provided in context for the output directory. If none is configured, default to `<workspace_dir>/read-later/`.

## Steps

1. The user provides a URL (or you extract one from context).
2. Run the save script:
   ```bash
   python3 scripts/save-url.py "<URL>" --output "<output-dir>"
   ```
3. Report the saved filename and path to the user.

## Notes

- The script auto-installs `readability-lxml`, `requests`, and `lxml` if missing.
- Uses Mozilla's Readability algorithm to extract article content, strips ads/nav/clutter.
- Renders to PDF via Chrome headless (`--print-to-pdf`).
- Filenames are derived from the article title + date: `YYYY.MM.DD Slug Name.pdf`
- If the title can't be extracted, falls back to the domain name.
