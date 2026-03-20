---
name: recall
description: >
  Search and retrieve past context — session logs, docs, decisions, anything
  discussed before. Use when the user says "recall", "what did we discuss",
  "find that thing", "when did we", or wants to look up something from a
  previous session.
---

# Recall

Search the workspace for past context and present what's found. This includes session logs, docs, configuration, and anything else in the workspace.

## Steps

1. **Search broadly** — cast a wide net across all workspace directories. Use Grep across multiple directories, Glob by date pattern, or both.

2. **Present results** with date and relevant excerpts, not just filenames. If one clear match, show it directly.

3. **Drill down** if asked.

## Guidelines

- Start with excerpts and context — let the user ask for more
- Session logs are dated (`YYYY-MM-DD <topic>.md`) — use date patterns to narrow searches
- If no matches, suggest alternative search terms
