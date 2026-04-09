---
name: codex
description: >
  Delegate work to the Codex CLI from within the current session. Two modes:
  (1) foreground fire-and-wait for small, self-contained asks; (2) background
  long-running sessions for larger tasks that need check-ins, interrupts, and
  follow-up prompts. Both use `codex exec` directly — no server, no daemon,
  no wrappers. Trigger on "ask codex", "consult codex", "get codex to…",
  "delegate this to codex", "have codex work on this".
---

# Codex

Use the Codex CLI as a sub-agent via its native `codex exec` non-interactive
mode. Codex persists every session to disk (`~/.codex/sessions/…`), so
resuming by id (or `--last`) continues the same conversation with no host
process required.

## Two modes

### Mode A — Foreground (small, self-contained)

Fire once, block until Codex replies, read the answer, move on. Use for:

- Second opinions on a small decision
- A specific code question Codex might answer better
- A self-contained sub-task that can be stated in one prompt

Run as a **regular (blocking) Bash call**. Write the final message to a file
with `-o` so the output is clean:

```bash
codex exec \
  -s read-only \
  --skip-git-repo-check \
  -C <working-dir> \
  -o /tmp/codex-out.md \
  "Here is the problem: … Answer with a plan, not code." < /dev/null
```

Then read `/tmp/codex-out.md`. Without `-o`, Codex prints a mix of progress
and the final message to stdout — readable but noisier.

Pick the sandbox to match the task:

- `-s read-only` — analysis, review, advice (default choice)
- `-s workspace-write` — Codex may edit files in the current workspace
- `--full-auto` — shorthand for `-s workspace-write` with on-request approvals
- Avoid `--dangerously-bypass-approvals-and-sandbox` unless the user explicitly asks

Always pass `-C <dir>` to pin Codex's working directory. If omitted, Codex
inherits the parent process cwd — which may not be where you meant to work.

### Mode B — Background (long-running, iterative)

Kick off Codex on a larger task, let it work, check on it, feed it more
prompts in the same session as needed. Use for:

- Multi-file refactors or implementations Codex will tackle from a plan
- Research tasks where Codex will explore and summarize
- Anything where you want to interrupt, ask clarifying questions, or
  redirect mid-flight

**Start the session (background):** run `codex exec` as a Bash task with
`run_in_background: true`. Capture the returned task id for monitoring
and kill control:

```bash
codex exec \
  --full-auto \
  --skip-git-repo-check \
  -C <working-dir> \
  --json \
  -o <working-dir>/last.md \
  "<kickoff prompt with plan, constraints, success criteria>" < /dev/null
```

`--json` emits JSONL events to stdout. The first relevant event is
`{"type":"thread.started","thread_id":"<UUID>"}` — that UUID is the session
id for `exec resume`. Capture it from the output stream.

**The within-session loop is event-driven, not polled.** While the
background task runs, do other useful work (or respond to the user). When
the task completes, the host auto-injects a task-completion notification
as a system reminder — that's the wake-up. Do **not** call
`TaskOutput`/`BashOutput` with `block:true` just to wait; that blocks the
current turn and defeats backgrounding.

**Do not peek for status updates.** The task's status until completion
is, by definition, "still running." If the user asks "how's it going?"
and no completion notification has arrived, answer from that knowledge
alone — do **not** call `TaskOutput`/`BashOutput` to check. Peeks dump
a wall of intermediate output into the conversation and make the flow
feel blocking even when it isn't.

Peek **only** when there is a concrete reason to make a **steering
decision** — e.g. suspicion it's off course, need to verify it's past
a specific milestone before proceeding, or the user has given new
information that may invalidate the kickoff. Use `block:false` for
those peeks. If the peek confirms a problem, kill the background task
and resume with new instructions.

**Interrupt / adjust / follow up (same session):** kill the background
task, then re-invoke with `exec resume`. The session file on disk preserves
all prior turns, so Codex picks up where it left off:

```bash
# By captured session id (preferred when multiple sessions may be in flight)
codex exec resume <SESSION_ID> \
  --full-auto \
  -C <working-dir> \
  --json \
  -o <working-dir>/last.md \
  "Reconsider — constraint X has changed. Do Y instead." < /dev/null

# Or the most recent session
codex exec resume --last \
  -C <working-dir> \
  "Keep going, but add tests for the parser." < /dev/null
```

Each `resume` is a fresh process, so **every flag must be re-passed**,
including `-C`, `-s` / `--full-auto`, `--skip-git-repo-check`, `-o`, and
`--json`. Nothing is inherited from the original `exec` except the
conversation state on disk. Forgetting `-C` on resume is the most common
footgun — Codex will silently run in the parent process cwd.

**Kill it:** kill the background Bash task by id with the host's task
stop mechanism. The session file is still on disk and remains resumable.

## Capturing the session id

In order of simplicity:

1. **`--last`** — "continue the session you just ran." No id needed. Safe
   only when a single Codex session is in flight at a time.
2. **Plain stdout** — without `--json`, Codex prints a `session id: <UUID>`
   line near the top of its output. A simple grep pulls it out. Good for
   foreground calls.
3. **`--json` + `thread.started`** — with `--json`, the first few JSONL
   events include `{"type":"thread.started","thread_id":"<UUID>"}`. Most
   robust across multiple concurrent sessions.

The `~/.codex/sessions/YYYY/MM/DD/rollout-…-<uuid>.jsonl` filename also
embeds the id as a last-resort fallback.

## Gotchas (Claude Code host environment)

These are specific to running Codex from within Claude Code's Bash tool:

- **Close stdin with `< /dev/null`.** When the prompt is a CLI argument,
  Codex still tries to read stdin to append as a `<stdin>` block. In
  backgrounded Bash, stdin stays open forever and Codex hangs. Explicitly
  redirect `< /dev/null` on every invocation, foreground or background.

- **Claude Code's seatbelt sandbox breaks Codex.** Codex's underlying
  `system-configuration` crate reads macOS SystemConfiguration framework,
  which Claude Code's seatbelt blocks, causing a Rust panic on startup.
  Launch Codex with the host's sandbox bypass flag (for Claude Code's Bash
  tool: `dangerouslyDisableSandbox: true`). Codex's own `-s` sandbox is
  unaffected and still enforces its sandbox policy inside Codex — set it
  appropriately per task.

- **`-C` does not persist across `exec resume`.** Re-pass it every time.

- **Auto-notification on completion is the loop.** The host injects a
  `<task-notification>` system message when the background Bash task
  exits. No manual polling needed. Use intermediate `block:false` peeks
  only for steering decisions, not for waiting.

## Prompting Codex

Codex does **not** share the current session's context. Every call is cold
unless it's a `resume`. For kickoffs, include:

- The specific task or question, stated plainly
- The exact context needed — file paths (Codex can read them), constraints,
  success criteria, what "done" looks like
- The desired answer shape (plan, diff, critique, code, pros/cons)
- Anything the current session has already tried and ruled out
- Any environment constraints that will bite Codex (e.g., "no network,
  stdlib only") if they're known up front

Do not paste whole files unless essential — Codex can read the filesystem.
Point at paths and tell it what to look at.

For follow-up prompts in the same session, keep them tight and
conversational — Codex already has the prior turns.

## Context discipline

- Do not dump raw output files or `BashOutput` contents into the current
  session wholesale. Read selectively, summarize, cite paths.
- When relaying Codex's conclusions, attribute explicitly ("Codex suggests…",
  "Per Codex…") and summarize. Point at the output file if the user wants
  the full text.
- Note where Codex agrees or disagrees with the current session's prior
  reasoning, and which view is being adopted.

## Guidelines

- Pick the mode to match the task shape: small/self-contained = Mode A,
  large/iterative = Mode B.
- One Codex session per topic. Don't multiplex unrelated asks through a
  single resumed session.
- Treat Codex as a peer, not an oracle — evaluate its answers critically
  before acting.
- Never chain resumes without reading the prior response first.
- Default to the most restrictive sandbox (`-s read-only`) unless the task
  clearly requires writes.
- Cross-session supervision (checking on a Codex run while the main Claude
  Code session is idle or closed) is **out of scope** for this skill. It
  requires a scheduler like `CronCreate` or a `SessionStart` hook.
