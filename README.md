# Skills

Generic, reusable agent skills for Claude Code. Each skill is a self-contained workflow — a `SKILL.md` with a name, trigger description, and step-by-step instructions.

Skills are designed to be portable. They contain no personal configuration, hardcoded paths, or user-specific details. Anything personal lives in a separate private workspace alongside these skills.

## Skills in this repo

| Skill | Description |
|---|---|
| `code-implement` | TDD implementation from a plan — worktree workflow, write tests first, implement, review |
| `code-init` | Codebase orientation — read docs, map structure, summarize architecture |
| `code-plan` | Plan a code change via structured Q&A — clarify, approach, write plan |
| `code-review` | Review code for plan adherence, design, and clean code |
| `download-video` | Download a video to Desktop via yt-dlp |
| `find-skills` | Search and install skills from the skills.sh ecosystem |
| `go` | Quick launcher — jump to a file, URL, or bookmark by shortcut name |
| `learn` | Persist new knowledge — facts, prefs, behaviors, skills, system changes |
| `log` | Save a detailed session log |
| `read-later` | Save a URL as a clean readable PDF |
| `recall` | Search workspace for past context from previous sessions |
| `review` | GTD-style daily/weekly review — tasks, calendar, plans, priorities |

## Workspace setup

Skills work best as part of a broader agent workspace. Here's the setup used by this author:

```
workspace/
├── AGENTS.md          # System prompt — identity, routing, preferences
├── docs/              # Personal config (filing rules, calendar IDs, contacts, etc.)
├── logs/              # Session logs (YYYY-MM-DD Topic.md)
├── skills/            # ← this repo (symlinked or cloned here)
├── jobs/              # Background job definitions
└── user/              # Local content (notes vault, etc.) — not synced
```

**Three layers:**

- **`AGENTS.md`** — loaded every session. Identity, routing, high-level preferences. Keeps short; points to docs for detail.
- **`docs/`** — personal config read on demand. Calendar IDs, contact shortcuts, filing rules, tool-specific settings. Skills reference this with "refer to any provided documentation."
- **`skills/`** — this repo. Generic workflows that work for anyone. No personal config baked in.

This separation means skills can be public while docs and AGENTS.md stay private.

**Syncing:** The workspace (minus `user/`) syncs across machines via [Stash](https://github.com/rupertsworld/stash) — a CRDT-based file sync tool backed by GitHub. Skills live in their own repo and are symlinked into the workspace.

## Adding a skill

Each skill is a directory with a `SKILL.md`:

```
skills/
└── my-skill/
    └── SKILL.md
```

`SKILL.md` structure:

```markdown
---
name: my-skill
description: One sentence — when should this skill trigger?
---

What this skill does, in one line.

## Steps

1. Step one
2. Step two
...
```

Keep skills generic. If a skill needs user-specific config (paths, IDs, contacts), document that the skill expects it to be provided in context — don't hardcode it.
