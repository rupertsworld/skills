---
name: issue-start
description: Start work on a Linear issue. Fetches the issue, reads the project's must-read docs (following AGENTS.md / CLAUDE.md routing), then invokes the code-plan skill to produce a plan. Use when the user says "/issue-start <key-or-name>" or asks to start, begin, pick up, or plan work on a Linear issue.
---

Ground in a Linear issue and the project's routing docs, then hand off to `code-plan` for a structured planning dialogue.

## Input

The user provides either:
- A Linear issue identifier like `TEL-123`
- A fragment of the issue title or description to search for

If the input is missing or ambiguous, ask the user which issue before proceeding.

## Steps

### 1. Fetch the issue

- If the input matches `[A-Z]+-\d+`, call `mcp__linear__get_issue` with that key.
- Otherwise, call `mcp__linear__list_issues` with the input as a query. If more than one plausibly matches, show the top few and ask the user which one.
- Read the description, parent/sub-issues, labels, and the latest comments via `mcp__linear__list_comments`. Note the problem, the motivation, and any constraints or acceptance criteria already captured.

### 2. Create a worktree for the issue

- Invoke the `worktree` skill with the issue key lowercased (e.g. `TEL-123` → `tel-123`) as the name. This creates `.worktrees/<key>/` on a branch of the same name, or attaches if the branch already exists.
- If the issue key can't be determined (e.g. the user searched by title and didn't confirm a key), ask before inventing a name.
- Treat the worktree as the active working location for the rest of the session — read docs, run the planning dialogue, and write the plan there.

### 3. Read the project's must-read docs

- Look for `AGENTS.md` and `CLAUDE.md` in the repo root. These route to the docs that must be read before making changes.
- Follow the links in those files — architecture, guidelines, and any area-specific docs that match the issue's topic.
- Read area-relevant docs carefully; skim the rest.
- If the issue touches an area not covered by the routing, grep the codebase to find the relevant module and skim its code and tests.
- If the repo has no AGENTS.md / CLAUDE.md, fall back to the README and the top-level `docs/` directory.

### 4. Hand off to code-plan

- Summarize in one or two sentences what the issue wants and what was read.
- Invoke the `code-plan` skill to run the structured planning dialogue.
- Carry the issue key into the plan so it can be referenced during implementation (e.g. in the plan's overview or in commit messages).

## Notes

- Stop at a written plan. Do not start implementation.
- If the issue already contains a detailed plan, surface that and ask whether to still run the full code-plan dialogue or use the issue's plan as the basis.
- If a Linear tool call fails (auth, missing workspace, etc.), tell the user rather than guessing at the issue's contents.
