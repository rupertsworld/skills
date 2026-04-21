---
name: push
description: Send a coding task to a cloud Claude Code session via `claude --remote`. Cloud VM clones the repo from GitHub at the current branch and runs the work there. Registers as a background task so it's monitorable via `TaskOutput` or the local `/tasks` command. Use when the user wants to offload implementation to the cloud instead of running it locally, or says "push this to cloud / Claude Code for web / run this remotely / offload".
---

Ship a coding task to a cloud Claude Code session and track it as a background task.

## Input

Either:
- A path to a file that exists on disk (e.g. `docs/plans/foo.md`) — wrap as: `Implement the plan at <path> on the current branch. Commit and push when done. Open a PR linking the plan.`
- Anything else — pass through as the prompt verbatim.

## Steps

### 1. Sync state to origin

The cloud VM clones from GitHub at the current branch's pushed tip. Anything local-only (uncommitted changes, unpushed commits) won't be visible. This stage makes sure the branch on origin reflects what the user expects the cloud to see.

Gather state first (parallel):
- `git rev-parse --abbrev-ref HEAD` — current branch.
- `git status --porcelain` — uncommitted/untracked.
- `git ls-remote --exit-code --heads origin <branch>` — branch exists on origin (exit 2 = missing).
- `git log --oneline origin/<branch>..HEAD 2>/dev/null` — unpushed commits (empty if origin missing).

Refuse outright:
- Branch is `main` / `master` or detached HEAD. Cloud clones the current branch; `main` is almost never what the user means.

Otherwise act:

- **If the input arg is an existing file path and is untracked or modified**, stage just that file and commit it: `git add <path> && git commit -m "Add <path>"` (or "Update <path>"). Targeted so we don't sweep in unrelated dirty state.
- **If other uncommitted or untracked files remain** after the targeted commit, summarize them and ask the user whether to stage them (with what grouping/message), ignore them, or abort. Never bulk-stage silently.
- **If branch is not on origin**, `git push -u origin <branch>`. First-time publish; low-risk, proceed without further prompt.
- **If branch is on origin but has unpushed commits**, `git push`. Same low-risk.

After this stage, the branch tip on origin equals the local tip, so the cloud VM will see what we intend.

### 2. Dispatch

Run `claude --remote "<prompt>"` via `Bash` with `run_in_background: true`. Capture the returned task_id from the Bash result.

If the repo isn't available to the Claude GitHub App (user says "no GitHub" or first attempt errors with a repo-access message), retry with `CCR_FORCE_BUNDLE=1 claude --remote "<prompt>"` — same run_in_background — which uploads the local repo directly instead of cloning from GitHub.

### 3. Report

Tell the user:
- The task_id.
- That they can watch progress from their terminal with `/tasks`, or ask this agent to poll with `TaskOutput`.
- The claude.ai/code URL if they want to steer the session in the browser (`claude sessions` or `/tasks` lists URLs).

If the user asks to monitor from the conversation, use `TaskOutput(task_id, block: false)` for a snapshot or `block: true` to wait for completion. For continuous polling, `/loop` with a reasonable interval (e.g. `/loop 5m` checking TaskOutput) — not a tight poll.

## Notes

- `claude --remote` runs on a sandboxed cloud VM, authed via the Claude GitHub App. First-time users need `/web-setup` to link their gh token.
- One-way: the cloud session can be pulled back to the local terminal later with `claude --teleport <session>`. This skill is just the outbound dispatch.
- Docs: https://code.claude.com/docs/en/claude-code-on-the-web.md , https://code.claude.com/docs/en/web-quickstart.md
