---
name: delegate
description: Delegate a task to a background coding agent via acpx. Use when the user wants a second opinion, a long-running background task, or to offload work to another agent.
---

Delegate a task to a background coding agent (default: Codex) using acpx sessions. The delegated agent runs independently — you can watch it live, steer it, or cancel it at any time.

## When to use

- **Second opinion**: Different perspective on a problem or approach
- **Background work**: Long-running refactor, test writing, migration, etc. while you keep working
- **Parallel exploration**: Try an alternative approach without interrupting the current session

## Two modes: short and long-steered

- **Short (foreground)**: quick second opinions, one-shot questions, small reviews. Omit `--no-wait`; the result returns in this turn. Hand the answer back to the user and move on.
- **Long steered**: the default for real work. Wrap foreground acpx in Claude's `Bash run_in_background: true` and pass `--format json` — the live JSON event stream flows to the `.output` file (tool calls, agent text deltas, usage updates), so you can read it at any time. Interject by chaining `cancel` + a fresh prompt in one Bash call.

`--no-wait` is an acpx CLI flag that lets you queue a prompt and return immediately instead of blocking on the current turn — useful if you need to fire a prompt without waiting. The **default recommended pattern below uses foreground acpx + Claude bg-task**, not `--no-wait`, because the bg-task wrapper gives the same non-blocking behavior on the Claude side *and* captures the live stream. Reach for `--no-wait` only when you want the acpx process itself to detach (e.g. long cron-like fires), at the cost of no local stream capture.

## Important: sandbox

All `acpx` commands **must** run outside the sandbox (`dangerouslyDisableSandbox: true`). acpx spawns agent processes via npm/npx, which need write access to `~/.npm` — the Claude Code sandbox blocks this.

## Command syntax

Permission flags (`--approve-all`, `--approve-reads`, `--deny-all`) and other global options go **before** the agent name:

```bash
acpx --approve-reads codex -s <session> "prompt"
#     ↑ global flag    ↑ agent
```

Agent-level options (`-s`, `--no-wait`, `-f`) go **after** the agent name.

## Steps

### 1. Gather context

Ask the user:
- **What to delegate**: The task or question for the background agent
- **Agent** (optional): default is `codex`, but `claude`, `pi`, `gemini`, etc. work
- **Permissions** (optional): `--approve-all`, `--approve-reads` (default), or `--deny-all`

### 2. Kick off the session

Generate a descriptive session name (`refactor-auth`, `test-coverage`, `review-api`). Every acpx interaction below is **one Bash tool call** — chain with `&&` so `sessions ensure` and the first prompt go out together, avoiding a second permission prompt. acpx itself has no single-command ensure-and-prompt; the chain is the tightest it allows.

**Short** — foreground, result in this turn:

```bash
acpx <agent> sessions ensure --name <name> && \
  acpx --approve-reads <agent> -s <name> "<prompt>"
```

**Long steered** — foreground acpx + `--format json` + Claude bg-task (`run_in_background: true`):

```bash
acpx <agent> sessions ensure --name <name> && \
  acpx --format json --approve-reads <agent> -s <name> "<prompt>"
```

The bg-task doesn't block your turn. The `.output` file fills with live JSON events (`sessionUpdate: agent_message_chunk | tool_call | tool_call_update | usage_update`) — read it any time to see what the agent is thinking or doing right now. A `<task-notification>` fires when the acpx turn completes.

Include relevant context in the prompt — file paths, constraints, what has been tried. A good delegation prompt is self-contained.

### 3. Report back

Tell the user:
- The session name
- That the live stream is in the task `.output` file (and offer to peek)
- Whether the turn is still running or already returned

### 4. Watching and steering a long session

Don't block the user's turn. The main session stays responsive while the delegated turn runs.

**Peek at the stream** — grep the `.output` file for counts, recent tool titles, or agent text:

```bash
grep -c '"sessionUpdate"' <output-file>
grep -o '"title":"[^"]*"' <output-file> | tail -10
grep -o '"agent_message_chunk"[^}]*"text":"[^"]*"' <output-file> | tail -5
```

**Session status / transcript** (works even after the turn has ended):

```bash
acpx <agent> status -s <name>
acpx <agent> sessions read <name> --tail 50
acpx <agent> sessions history <name> --limit 10
```

**Interject (cancel current turn + send new prompt) — one Bash call**:

```bash
acpx <agent> cancel -s <name> && \
  acpx --format json --approve-reads <agent> -s <name> "<new prompt>"
```

Cancel is cooperative and returns immediately (`cancel requested`). Session context persists across the cancel — the new prompt sees everything the agent learned in prior turns.

**Queue instead of cancel** — if you want to let the current turn finish but line up a follow-up, use `--no-wait`:

```bash
acpx --approve-reads <agent> -s <name> --no-wait "<follow-up>"
```

**Pacing when self-driving a /loop**: default to **~3 minutes (180s)** between check-ins. Rupert wants tight steering on delegated work, not set-and-forget. 3 min also stays inside the 5-min prompt-cache window. Stretch further only if the agent has explicitly said it's off doing something long.

### 5. Close when done

```bash
acpx <agent> sessions close <name>
```

Note: `sessions read`, `history`, `show`, and `close` take the session name as a **positional argument**. The `-s` flag is only for `prompt` / `cancel` / `status` / `set` / `set-mode`.

---

## Tips

- **Session names persist.** You can come back to a session in a future conversation if it's still alive.
- **List sessions** with `acpx <agent> sessions list`.
- **Max turns**: `--max-turns <n>` to limit autonomous work.
- **Timeout**: `--timeout <seconds>` to cap how long a single response can take.
- **One-shot**: `acpx <agent> exec "<prompt>"` for tasks that don't need a saved session.
