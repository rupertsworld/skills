---
name: learn
description: >
  Persist new knowledge — facts, preferences, behaviors, skills, system changes.
  Use when the user wants to teach the agent something, add or modify a skill,
  update filing rules or docs, restructure the system, or remember a fact or
  preference. Trigger on "learn", "remember", "teach", "add a skill", "update
  the system", "change how you do X".
---

# Learn

Persist new knowledge into the agent system. Covers everything from "remember my email" to "create a new skill."

Refer to any provided documentation for system architecture and conventions before making structural changes.

## Decide where it goes

| What's being learned | Where to persist it |
|----------------------|---------------------|
| Short facts (identity, preferences, contacts) | `AGENTS.md` |
| Detailed rules (filing, calendars, code style) | `docs/` |
| New workflow or automation | `skills/<name>/SKILL.md` |
| Skill-specific user config (paths, IDs) | `docs/` or AGENTS.md Skills section |
| Correction to existing behavior | The skill or doc that caused the wrong behavior |
| Doesn't fit anywhere | Log it with `/log` |

## Persisting facts and preferences

1. **Read the target file first** to avoid duplicates or contradictions.
2. **Update the file** — add, update, or remove as needed. Keep AGENTS.md scannable.
3. **Confirm** what was changed and where.

Rules:
- Only persist what the user explicitly says — don't invent or assume
- If the user says to forget something, find and remove it
- Don't duplicate across files — reference instead

## Creating a new skill

1. **Gather requirements** — what should it do, when should it trigger.
2. **Choose a name** — lowercase, hyphenated, 1-64 characters.
3. **Create** `skills/<name>/SKILL.md` with YAML frontmatter and markdown body.
4. **Write the body** — one-line summary, then steps, then guidelines. Keep generic: say "refer to any provided documentation" rather than naming specific doc files or hardcoding paths.
5. **Add optional directories** if needed: `scripts/`, `references/`, `assets/`.
6. **If user-specific config is needed**, put it in docs or AGENTS.md Skills section — not in the skill.
7. **Verify** — read back SKILL.md, confirm name matches directory.

## Editing existing skills, docs, or AGENTS.md

1. **Read the file first.**
2. **Respect the layer boundaries** — skills are portable (no hardcoded paths or personal config), docs hold detail, AGENTS.md stays scannable.
3. **Make the change** — keep it minimal and scoped.
4. **Update the description** in frontmatter if the skill's purpose changed.
5. **If a new doc was created**, add a pointer from AGENTS.md Important References section.

## Guidelines

- Read any provided system architecture docs before structural changes.
- Review existing skills for tone and structure before creating a new one.
- Don't create a skill for something that's just a one-liner or a doc update.
