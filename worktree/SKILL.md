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
4. **Install dependencies** — see below. Skip only if the repo has no package manager.
5. **Add a flat-dir symlink** — see below. Skip silently if the user doesn't use the convention.
6. **Report the absolute path** of the new worktree. One line, no ceremony.
7. **Announce the session handoff** (see below).

Let git errors surface as-is — if the branch is already checked out in another worktree, if the target path exists, if the tree is dirty, the git error is clearer than anything this skill could synthesise.

## Dependency setup

A worktree that shares `node_modules/` (or any checkout-local dependency dir) with another checkout will **silently load source from the wrong branch**. In npm workspaces, package symlinks inside `node_modules/@scope/pkg` are relative (`../../packages/pkg`) and resolve against whichever `node_modules/` they live in — so a worktree whose `node_modules/` is a symlink to the main checkout's will read main's workspace-package source, not the worktree's. Tests and dev servers can pass or fail for reasons that have nothing to do with the branch under edit. **Never symlink `node_modules/` (or equivalent) from another checkout.**

After creating or attaching:

1. **Check for stale sharing.** If `.worktrees/<name>/node_modules` exists and is a symlink, delete it (`rm .worktrees/<name>/node_modules` — removes just the symlink, not the target). A real directory is fine; a symlink to another checkout is broken state.
2. **Detect and install.** From inside the worktree:
   - `package-lock.json` + `package.json` → `npm ci` (or `npm install` if the lockfile is missing)
   - `yarn.lock` → `yarn install`
   - `pnpm-lock.yaml` → `pnpm install`
   - `bun.lockb` → `bun install`
   - `uv.lock` / `poetry.lock` / `requirements.txt` → set up a worktree-local venv (`uv sync`, `poetry install`, etc.)
   - `Cargo.lock` → nothing needed; `target/` is already per-checkout
   - No recognised manifest → skip.
3. Let the install command's errors surface. Don't paper over them.

If the user is on a constrained machine and objects to the full install, ask — but make the tradeoff explicit: shared `node_modules/` will give wrong results for any cross-branch divergence in workspace packages.

## Flat-dir symlink

If the user keeps a flat index of active worktrees at `~/Repos/worktrees/` (the directory exists), add a symlink there pointing at the new worktree:

```bash
ln -s <worktree-absolute-path> ~/Repos/worktrees/<name>
```

This gives one place to see every active worktree across all repos without navigating into each repo's `.worktrees/`. If `~/Repos/worktrees/` doesn't exist, skip silently — it's a user convention, not required for the worktree to work.

If `~/Repos/worktrees/<name>` already exists, let the error surface rather than clobbering — the user may have a separate worktree of the same name from another repo.

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
2. If `~/Repos/worktrees/<name>` is a symlink (from the flat-dir convention), remove it: `rm ~/Repos/worktrees/<name>` (removes the symlink only, not the target). Only touch it if it's a symlink — never a real directory.
3. If the branch `<name>` still exists and is fully merged into `main` (`git branch --merged main`), ask the user whether to delete it. Never delete unmerged branches without explicit confirmation.

## List

`/worktree list`: run `git worktree list` and display the output.

## Non-goals

- Not related to the `Agent` tool's `isolation: "worktree"` flag — that's for spawning sub-agents in isolated worktrees; this skill is for the current session's working location.
- Doesn't manage sandbox config. Worktrees live inside the repo so existing sandbox permissions already apply.
