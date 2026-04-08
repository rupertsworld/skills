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
mode. Codex persists every session to disk, so resuming by id (or `--last`)
continues the same conversation with no host process required.

## Two modes

### Mode A — Foreground (small, self-contained)

Fire once, block until Codex replies, read the answer, move on. Use for:

- Second opinions on a small decision
- A specific code question Codex might answer better
- A self-contained sub-task that can be stated in one prompt

Run as a **regular (blocking) Bash call**. Write the final message to a file
with `-o` so the output is clean and easy to read back:

```bash
codex exec \
  -s read-only \
  --skip-git-repo-check \
  -o /tmp/codex-out.md \
  "Here is the problem: … Answer with a plan, not code."
```

Then read `/tmp/codex-out.md`. Without `-o`, Codex prints a mix of progress
and the final message to stdout — readable but noisier.

Pick the sandbox to match the task:

- `-s read-only` — analysis, review, advice (default choice)
- `-s workspace-write` — Codex may edit files in the current workspace
- `--full-auto` — shorthand for `-s workspace-write` with on-request approvals
- Avoid `--dangerously-bypass-approvals-and-sandbox` unless the user explicitly asks

Pass `-C <dir>` to scope Codex to a specific working directory, and
`--add-dir <dir>` for extra writable paths. Use `--skip-git-repo-check` when
running outside a git repo.

### Mode B — Background (long-running, iterative)

Kick off Codex on a larger task, let it work, check on it, feed it more
prompts in the same session as needed. Use for:

- Multi-file refactors or implementations Codex will tackle from a plan
- Research tasks where Codex will explore and summarize
- Anything where you want to be able to interrupt, ask clarifying questions,
  or redirect mid-flight

**Start the session (background):** run `codex exec` as a Bash task with
`run_in_background: true`. Capture its task id — that's what Claude Code uses
to monitor, poll output, and kill:

```bash
codex exec \
  -s workspace-write \
  -C /path/to/workspace \
  --json \
  -o /tmp/codex-session-1-last.md \
  "<kickoff prompt with plan, constraints, success criteria>"
```

`--json` makes Codex emit JSONL events to stdout, which surfaces a
`session_meta` event at the start containing the session id (`payload.id`,
a UUID). Grep the captured output for it and hold onto it for follow-ups.
If only one Codex session is ever in flight at a time, `--last` is an
acceptable substitute and no id capture is needed.

**Check on it:** use `BashOutput`/`TaskOutput` against the background task
id at any time. Completion arrives automatically as a system message on the
next turn.

**Interrupt / adjust / follow up (same session):** once the current turn has
finished (or after killing the background task), run Codex again with
`exec resume`:

```bash
# By captured session id (preferred when multiple sessions in flight)
codex exec resume <SESSION_ID> \
  -s workspace-write \
  "Reconsider the approach — constraint X has changed. Here's what to do instead: …"

# Or the most recent session
codex exec resume --last "Keep going, but add tests for the parser."
```

Each `resume` is itself a fresh process that can again be run foreground or
background depending on how long the follow-up will take. Session state
lives on disk in `~/.codex/sessions/` — no daemon keeps it alive between
turns.

**Kill it:** if Codex goes off the rails, kill the background Bash task by
id. The session file is still on disk, and the state at time of kill is
resumable via `exec resume`.

## Capturing the session id

Two reliable ways, in order of simplicity:

1. **`--last`** — for the common case of "continue the session you just
   ran." No id needed. Only safe when a single Codex session is in flight.
2. **`--json` + grep** — run Codex with `--json` and parse the first
   `session_meta` line from stdout. The UUID is at `payload.id`. This is
   the robust approach when multiple Codex sessions may coexist.

The `~/.codex/sessions/YYYY/MM/DD/rollout-…-<uuid>.jsonl` path also embeds
the id in the filename, as a last-resort fallback.

## Prompting Codex

Codex does **not** share the current session's context. Every call is cold
unless it's a `resume`. For kickoffs, include:

- The specific task or question, stated plainly
- The exact context needed — file paths (Codex can read them), constraints,
  success criteria, what "done" looks like
- The desired answer shape (plan, diff, critique, code, pros/cons)
- Anything the current session has already tried and ruled out

Do not paste whole files unless essential — Codex can read the filesystem.
Point at paths and tell it what to look at.

For follow-up prompts in the same session, keep them tight and
conversational — Codex already has the prior turns.

## Context discipline

- Do not dump `BashOutput` or `/tmp/codex-*.md` contents into the current
  session wholesale. Read selectively, summarize, cite.
- When relaying Codex's conclusions to the user, attribute explicitly
  ("Codex suggests…", "Per Codex…") and summarize — point at the output
  file if the user wants the full text.
- Note where Codex agrees or disagrees with the current session's prior
  reasoning, and which view is being adopted.

## Guidelines

- Pick the mode to match the task size, not the importance. Small = Mode A,
  large/iterative = Mode B.
- One Codex session per topic. Don't multiplex unrelated asks through a
  single resumed session.
- Prefer waiting for a foreground consult over racing ahead if its answer
  directly blocks the next step.
- Treat Codex as a peer, not an oracle — evaluate its answer critically
  before acting on it.
- Never chain resumes without reading the prior response first.
- Default to the most restrictive sandbox (`read-only`) unless the task
  clearly requires writes.
