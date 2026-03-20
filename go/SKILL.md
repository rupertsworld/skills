---
name: go
description: >
  Quick launcher for frequent files, URLs, and bookmarks. Use when the user
  says "go to", "open", or uses "/go <name>" to jump to a saved shortcut.
---

# Go

Jump to a frequently used file, URL, or bookmark by shortcut name.

## Steps

1. **Parse the argument** — the user provides a shortcut name (e.g., `/go todo`, `/go calendar`).

2. **Look up the shortcut** — refer to any provided documentation for saved shortcuts. Match the argument against shortcut names.

3. **Execute the shortcut:**
   - **File:** Read the file.
   - **URL:** Open it in the browser (`open <url>` on macOS).
   - **`.webloc` file:** Extract the URL with `plutil -extract URL raw` then open it.
   - **No match:** List available shortcuts so the user can pick one, or offer to save a new one.

4. **Persist shortcuts** — after resolving a target, save it to a documentation file so it's available next time. Don't wait to be asked.

## Guidelines

- Keep shortcut names short and memorable (1-2 words)
- If no argument is given, list all available shortcuts
- Proactively save any resolved shortcut that isn't already stored
