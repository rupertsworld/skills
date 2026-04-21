---
name: worktree
description: Create or manage git worktrees inside the current repo's `.worktrees/` directory. `/worktree <name>` creates or attaches; `/worktree rm <name>` removes; `/worktree list` lists. Worktrees live inside the repo so the current session's sandbox covers them without changes.
---

Create and manage git worktrees inside the current repo so the current Claude session can switch to isolated branches without losing its sandbox or needing a new session.

## Why `.worktrees/` inside the repo

The session's sandbox is scoped to the current repo. Putting worktrees under `<repo>/.worktrees/<name>/` means the new checkout is automatically inside the existing allowlist — no sandbox edits, no new session. Worktrees live alongside the repo, git sees them (via `git worktree list`), and the main checkout treats the directory as gitignored.

## Invocation

- `/worktree <name>` — create a new worktree named `<name>`; if a branch named `<name>` already exists, attach to it instead
- `/worktree` (no args) — invent a name based on the current task/conversation and existing branch conventions, then create
- `/worktree rm <name>` — remove a worktree (and optionally its branch, if safe)
- `/worktree list` — show existing worktrees

## Create or attach

1. **Ensure `.worktrees/` is gitignored.** Check the repo's root `.gitignore`. If `.worktrees/` isn't there, add it. Don't commit — let the user decide when.
2. **Check the base branch.** Run `git rev-parse --abbrev-ref HEAD`. If it isn't `main`, ask the user whether to branch from the current HEAD or switch to `main` first. Don't assume.
3. **Dispatch on whether the branch exists.** `git show-ref --verify --quiet refs/heads/<name>`:
   - **Exists → attach:** `git worktree add .worktrees/<name> <name>`
   - **New → create:** `git worktree add -b <name> .worktrees/<name>` from the confirmed base
4. **Report the absolute path** of the new worktree. One line, no ceremony.
5. **Announce the session handoff** (see below).

Let git errors surface as-is — if the branch is already checked out in another worktree, if the target path exists, if the tree is dirty, the git error is clearer than anything this skill could synthesise.

## Naming

- If the user gives a name, use it verbatim.
- If not, invent a short lowercase hyphenated name based on the task at hand and the conventions of existing branches (`git branch --list` — look for prefixes like `feat/`, `fix/`, etc., and match them). No generic prefix.

## Session handoff — routing work to the worktree

After creating or attaching, the agent treats the worktree as the **active working location for the rest of this session**, until the user says otherwise.

This is a routing rule, not a CWD change — Claude Code's process CWD cannot change mid-session. What this means in practice:

- **File operations** (Read, Edit, Write, Glob, Grep) should target paths under the worktree root.
- **Bash commands** should run with the worktree as working directory — use `cd <worktree> && …` or `git -C <worktree> …`. Do not rely on the harness CWD.
- **Tests, builds, servers** should be started in the worktree, not the main checkout.

When announcing the new worktree, tell the user plainly: "Using `<absolute path>` as the working location for this session until you say otherwise." If they later say "switch back", "use main instead", or name another worktree, route there instead.

## Remove

`/worktree rm <name>`:

1. `git worktree remove .worktrees/<name>` — this fails cleanly if the worktree has uncommitted work. Don't `--force` without explicit user confirmation.
2. If the branch `<name>` still exists and is fully merged into `main` (`git branch --merged main`), ask the user whether to delete it. Never delete unmerged branches without explicit confirmation.

## List

`/worktree list`: run `git worktree list` and display the output.

## Non-goals

- Not related to the `Agent` tool's `isolation: "worktree"` flag — that's for spawning sub-agents in isolated worktrees; this skill is for the current session's working location.
- Doesn't manage sandbox config. Worktrees live inside the repo so existing sandbox permissions already apply.
