---
name: tidy
description: Wind down transient state from a development session — stop background processes, remove worktrees for merged branches, repoint linked CLIs back at the main checkout, and delete merged branches locally and on the remote. Use when the user says "tidy up", "clean up", "/tidy", or just finished a ship-it flow (merge + push) and wants the machine back to a clean baseline.
---

Return the machine to a clean baseline after a feature lands. `/tidy` walks a cleanup list — background processes, worktrees, linked binaries, merged branches — and acts only with confirmation for anything destructive or shared.

## Scope: only touch what this session created

**Never remove worktrees or delete branches this session didn't work on, even if they look merged.** A merged branch you've never touched may still be load-bearing for the user — open in an editor, holding a deliberate checkpoint, left around on purpose. You don't know.

The relevant question isn't "is this branch merged into main?" — it's "did I create this branch or worktree in this session, or was it explicitly handed to me to clean up?"

- In scope: worktrees the agent created in this session, branches the agent created, binaries the agent linked, processes the agent started.
- Out of scope: anything that existed before the session started. Mention it in the report if it looks like it could be cleaned up, but don't act without explicit instruction.

If in doubt, ask.

## Invocation

- `/tidy` — survey the current session + repo and propose a cleanup list. Act only after the user confirms (or opts individual items out).

## The cleanup list

Walk these in order. For each, first report what was found; only act after the user agrees (or if the action is clearly safe and local).

### 1. Background processes

Stop any long-running processes started during the session.

- Agent-managed background tasks (dev servers, test watchers, file watchers) — stop via the runtime's stop mechanism for each known task id.
- Detached processes (nohup, `&`, daemons intentionally left running) — identify the PIDs first and confirm before killing. Prefer `SIGTERM`; only escalate to `SIGKILL` if the process refuses to exit.
- Don't stop processes the user didn't start in this session.

### 2. Worktrees

List worktrees: `git worktree list`. For each worktree under `.worktrees/<name>/` **that this session created or explicitly worked on**:

- If its branch is fully merged into `main` (see §4 for the check), it's a cleanup candidate.
- Remove via the `worktree` skill's remove path: `git worktree remove .worktrees/<name>`. No `--force` unless the user explicitly asks — a dirty worktree is a signal, not an obstacle.
- Leave worktrees whose branches still have unmerged work alone. Mention them so the user can decide.

**Pre-existing worktrees are out of scope.** If they happen to be merged, list them in the report as "other merged worktrees you may want to clean up later", but do not propose removing them without explicit instruction.

### 3. Linked CLIs and symlinks

If earlier in this session a global binary was linked from a worktree or feature branch (`npm link`, `pip install -e`, `cargo install --path`, symlink into `~/.local/bin`, etc.), repoint it back at the main checkout so the user's shell doesn't keep resolving to a path that's about to be deleted.

- The agent knows what was linked because it ran the command. Re-run the equivalent linking command from the main checkout to overwrite the symlink.
- After repointing, `which <command>` should resolve to a path inside the main checkout, not a worktree.
- If nothing was linked this session, skip this step silently.

### 4. Merged local branches

- Fetch first: `git fetch --all --prune` so "merged into main" reflects the remote's current state.
- Identify candidates: `git branch --merged main` — exclude `main`, `master`, and the currently checked-out branch.
- Delete each with `git branch -d <name>`. Never `-D` (force) unless the user explicitly authorizes it for a specific branch.
- If `git branch -d` refuses because a branch isn't merged to `main` per git's check, surface the refusal — do not escalate.

### 5. Merged remote branches

For each local branch being deleted that also exists on `origin`:

- Check whether the remote branch is merged (`git branch -r --merged origin/main | grep origin/<name>`).
- **Ask the user before pushing any deletion** — `git push origin --delete <name>` affects shared state. Batch the list of candidates into one confirmation prompt rather than asking per-branch.
- Only delete remotes the user pushed themselves. If a remote branch belongs to someone else, don't touch it.

## Safety rules

- Never delete `main`, `master`, or the branch currently checked out in any worktree.
- Never `--force`, `-D`, or `--no-verify` anything without explicit per-item authorization.
- Walk the cleanup list out loud before acting so the user can opt items out.
- For non-git directory deletions, prefer `trash` over `rm` when available.
- Treat remote-destructive actions (remote branch delete, force push) as always requiring confirmation, even if the user already said "tidy up everything" — restate exactly which remote refs will disappear.

## Reporting

At the end, print a short summary: what was stopped, what was removed, what was repointed, and anything left behind with the reason (unmerged branch, dirty worktree, user opted out).

## Non-goals

- Does not run tests, builds, or lints — that's a verification step, separate from cleanup.
- Does not commit, merge, or push feature work — that belongs to the shipping flow, before `/tidy` runs.
- Does not manage long-lived environment state (global npm packages, installed daemons, system services) — only transient things created during the session.
