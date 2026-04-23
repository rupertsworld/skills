---
name: worktree
description: Create or manage git worktrees at `~/Repos/worktrees/<repo>@<slug>/` (or `<repo>/.worktrees/<slug>/` as fallback). `/worktree <name>` creates or attaches; `/worktree rm <name>` removes; `/worktree list` lists.
---

Create and manage git worktrees so the current Claude session can switch to isolated branches without losing its sandbox or needing a new session.

## Names and slugs

Two distinct values are at play — don't conflate them:

- **`<branch>`** — the full git branch name, possibly with a convention prefix (`feat/home-screen`, `fix/login-bug`).
- **`<slug>`** — the branch name's final path segment, lowercase and hyphenated (`home-screen`, `login-bug`). This is what names the worktree directory.

When the caller passes a name containing a slash (e.g. `feat/home-screen`), treat the whole thing as `<branch>` and take everything after the last `/` as `<slug>`. When the name has no slash, `<branch>` and `<slug>` are the same string.

**The directory is always `<repo>@<slug>` — never embed the `feat/`, `fix/`, or other prefix in the directory path.** A slash in the directory name creates an unintended nested subdirectory (e.g. `television@feat/home-screen/` lives two levels deep) which breaks later lookups, removal, and most shells' autocomplete.

## Where worktrees live

Default: `~/Repos/worktrees/<repo>@<slug>/` — a flat directory of all active worktrees across every repo on the machine, named `<repo>@<slug>` so worktrees from different repos don't collide. This location is inside the session's sandbox write allowlist (`~/Repos`) and is easy to surface at the top level of the user's IDE file tree.

Fallback: `<repo>/.worktrees/<slug>/` — used only if `~/Repos/worktrees/` does not exist. The worktree is gitignored in the main checkout.

`<repo>` is the main checkout's directory basename (e.g. `television`, not `Television` or a remote slug).

## Invocation

- `/worktree <name>` — create a new worktree for branch `<name>` (the directory uses the slug portion); if the branch already exists, attach to it instead
- `/worktree` (no args) — invent a name based on the current task/conversation and existing branch conventions, then create
- `/worktree rm <name>` — remove a worktree (and optionally its branch, if safe). Accepts either the branch name or the bare slug
- `/worktree list` — show existing worktrees

## Create or attach

1. **Split the name into `<branch>` and `<slug>`.** If the input contains `/`, `<branch>` is the whole input and `<slug>` is the segment after the last `/`. Otherwise `<branch>` and `<slug>` are both the input.
2. **Pick the worktree path.**
   - If `~/Repos/worktrees/` exists: use `~/Repos/worktrees/<repo>@<slug>`.
   - Else: use `<repo>/.worktrees/<slug>`, and ensure `.worktrees/` is in the repo's root `.gitignore` (add it if not, without committing).
3. **Check the base branch.** Run `git rev-parse --abbrev-ref HEAD`. If it isn't `main`, ask the user whether to branch from the current HEAD or switch to `main` first. Don't assume.
4. **Dispatch on whether the branch exists.** `git show-ref --verify --quiet refs/heads/<branch>`:
   - **Exists → attach:** `git worktree add <path> <branch>`
   - **New → create:** `git worktree add -b <branch> <path>` from the confirmed base
5. **Install dependencies** — see below. Skip only if the repo has no package manager.
6. **Report the absolute path** of the new worktree. One line, no ceremony.
7. **Announce the session handoff** (see below).

Let git errors surface as-is — if the branch is already checked out in another worktree, if the target path exists, if the tree is dirty, the git error is clearer than anything this skill could synthesise.

## Dependency setup

A worktree that shares `node_modules/` (or any checkout-local dependency dir) with another checkout will **silently load source from the wrong branch**. In npm workspaces, package symlinks inside `node_modules/@scope/pkg` are relative (`../../packages/pkg`) and resolve against whichever `node_modules/` they live in — so a worktree whose `node_modules/` is a symlink to the main checkout's will read main's workspace-package source, not the worktree's. Tests and dev servers can pass or fail for reasons that have nothing to do with the branch under edit. **Never symlink `node_modules/` (or equivalent) from another checkout.**

After creating or attaching:

1. **Check for stale sharing.** If `<worktree>/node_modules` exists and is a symlink, delete it (`rm <worktree>/node_modules` — removes just the symlink, not the target). A real directory is fine; a symlink to another checkout is broken state.
2. **Detect and install.** From inside the worktree:
   - `package-lock.json` + `package.json` → `npm ci` (or `npm install` if the lockfile is missing)
   - `yarn.lock` → `yarn install`
   - `pnpm-lock.yaml` → `pnpm install`
   - `bun.lockb` → `bun install`
   - `uv.lock` / `poetry.lock` / `requirements.txt` → set up a worktree-local venv (`uv sync`, `poetry install`, etc.)
   - `Cargo.lock` → nothing needed; `target/` is already per-checkout
   - No recognised manifest → skip.
3. Let the install command's errors surface. Don't paper over them — with one exception below.

### Sandbox vs. package-manager caches

Package managers write to shared caches outside the repo — `~/.npm/_cacache/` for npm, `~/.bun/install/cache/` for bun, `~/Library/Caches/pnpm/` for pnpm, etc. The session sandbox usually does **not** allow writes there (it allowlists the repo and `$TMPDIR`, not arbitrary home-dir caches). When the cache path is outside the allowlist, the install fails with `EPERM` — and the error message often misattributes the cause (npm blames "root-owned files").

If `npm ci`/`npm install` fails with `EPERM` on a path under `~/.npm/_cacache/`, **don't trust the error message**. It's almost certainly the sandbox. Two fixes, in order of preference:

1. **Scratch cache in `$TMPDIR`** (preferred — keeps sandbox on): `npm ci --cache="$TMPDIR/npm-cache-<name>"`. Equivalent flags exist for other managers (`bun install --cache-dir`, `pnpm install --store-dir`, etc.).
2. **Retry with `dangerouslyDisableSandbox: true`** if the scratch-cache approach doesn't apply.

Don't ask the user to `sudo chown` their npm cache — that's treating the symptom of a misdiagnosis.

If the user is on a constrained machine and objects to the full install, ask — but make the tradeoff explicit: shared `node_modules/` will give wrong results for any cross-branch divergence in workspace packages.

## Naming

- If the user gives a name, use it verbatim as the branch name. Derive the slug from it (see "Names and slugs" above) — the slug is what names the directory.
- If not, invent a short lowercase hyphenated name based on the task at hand and the conventions of existing branches (`git branch --list` — look for prefixes like `feat/`, `fix/`, etc., and match them).
- The branch name usually carries the repo's branch prefix convention (`feat/<slug>`, `fix/<slug>`). The directory name is always `<repo>@<slug>` with no prefix.

## Session handoff — routing work to the worktree

After creating or attaching, the agent treats the worktree as the **active working location for the rest of this session**, until the user says otherwise.

This is a routing rule, not a CWD change — Claude Code's process CWD cannot change mid-session. What this means in practice:

- **File operations** (Read, Edit, Write, Glob, Grep) should target paths under the worktree root.
- **Bash commands** should run with the worktree as working directory — use `cd <worktree> && …` or `git -C <worktree> …`. Do not rely on the harness CWD.
- **Tests, builds, servers** should be started in the worktree, not the main checkout.

When announcing the new worktree, tell the user plainly: "Using `<absolute path>` as the working location for this session until you say otherwise." If they later say "switch back", "use main instead", or name another worktree, route there instead.

## Remove

`/worktree rm <name>`:

1. Derive `<slug>` from the input the same way as create (strip any prefix before the last `/`).
2. Find the worktree path via `git worktree list` (accepting either `<repo>@<slug>` in the flat dir or `<slug>` under `.worktrees/`).
3. `git worktree remove <path>` — this fails cleanly if the worktree has uncommitted work. Don't `--force` without explicit user confirmation.
4. If the branch the worktree was on still exists and is fully merged into `main` (`git branch --merged main`), ask the user whether to delete it. Never delete unmerged branches without explicit confirmation.

## List

`/worktree list`: run `git worktree list` and display the output.

## Non-goals

- Not related to the `Agent` tool's `isolation: "worktree"` flag — that's for spawning sub-agents in isolated worktrees; this skill is for the current session's working location.
- Doesn't manage sandbox config. The default flat-dir location (`~/Repos/worktrees/`) is already inside the `~/Repos` write allowlist.
