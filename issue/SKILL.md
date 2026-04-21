---
name: issue
description: Start work on a Linear issue. Fetches the issue, creates a worktree on a conventionally-named branch (e.g. `feat/do-this-thing`), reads the project's must-read docs (following AGENTS.md / CLAUDE.md routing), then invokes the code-plan skill to produce a plan. Use when the user says "/issue <key-or-name>" or asks to start, begin, pick up, or plan work on a Linear issue.
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

### 2. Derive a branch name

Produce a short conventional branch name of the form `<prefix>/<slug>`.

- **Prefix** — infer from the issue:
  - `fix/` if labelled `bug` or the title clearly describes a defect ("Fix …", "… broken", "… regression").
  - `chore/` if labelled `chore`, `infra`, `tooling`, `refactor`, or the work is clearly non-user-facing.
  - `feat/` otherwise (default).
  - If the repo's existing branches (`git branch --list` / `git branch -r`) use different conventions, match them instead.
- **Slug** — kebab-case a short form of the issue title. Lowercase, alphanumerics and hyphens only, collapse repeats, strip leading/trailing hyphens. Drop filler words (`the`, `a`, `for`, etc.) if needed to keep it under ~40 chars. Don't include the Linear key in the slug — the key lives in commits/PRs, not the branch name.
- Show the proposed name to the user in one line before proceeding so they can override. If the user supplied a name in the invocation, use it verbatim.

### 3. Create a worktree on that branch

- Invoke the `worktree` skill with the derived name (e.g. `feat/do-this-thing`). This creates `.worktrees/<name>/` on a branch of the same name, or attaches if the branch already exists.
- Treat the worktree as the active working location for the rest of the session — read docs, run the planning dialogue, and write the plan there.

### 4. Read the project's must-read docs

- Look for `AGENTS.md` and `CLAUDE.md` in the repo root. These route to the docs that must be read before making changes.
- Follow the links in those files — architecture, guidelines, and any area-specific docs that match the issue's topic.
- Read area-relevant docs carefully; skim the rest.
- If the issue touches an area not covered by the routing, grep the codebase to find the relevant module and skim its code and tests.
- If the repo has no AGENTS.md / CLAUDE.md, fall back to the README and the top-level `docs/` directory.

### 5. Hand off to code-plan

- Summarize in one or two sentences what the issue wants and what was read.
- Invoke the `code-plan` skill to run the structured planning dialogue.
- Carry the Linear issue key into the plan so it can be referenced during implementation (e.g. in the plan's overview or in commit messages).

## Notes

- Stop at a written plan. Do not start implementation.
- If the issue already contains a detailed plan, surface that and ask whether to still run the full code-plan dialogue or use the issue's plan as the basis.
- If a Linear tool call fails (auth, missing workspace, etc.), tell the user rather than guessing at the issue's contents.
