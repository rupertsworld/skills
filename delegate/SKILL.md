---
name: delegate
description: Delegate a task to a background coding agent via acpx. Use when the user wants a second opinion, a long-running background task, or to offload work to another agent.
---

Delegate a task to a background coding agent (default: Codex) using acpx sessions. The delegated agent runs independently — you can check on it, steer it, or cancel it at any time.

## When to use

- **Second opinion**: Get a different perspective on a problem or approach
- **Background work**: Offload a long-running task (refactoring, test writing, migration) while continuing other work
- **Parallel exploration**: Try an alternative approach without interrupting the current session

## Three modes: short, long-unattended, long-steered

Pick a mode before delegating — they have different command shapes and follow-up behavior.

- **Short (foreground)**: quick second opinions, one-shot questions, small reviews. Omit `--no-wait` so the result comes back in the same turn. Return the answer to the user and move on.
- **Long unattended (background task)**: "just go do this, ping me when done." Run acpx synchronously (no `--no-wait`) but wrap it in `Bash` with `run_in_background: true`. The whole turn runs inside a Claude Code background task — output streams through `TaskOutput`, and a `<task-notification>` fires automatically when the acpx turn ends. No polling. Best for fire-and-forget work where you don't need to steer mid-turn.
- **Long steered (`--no-wait` + `/loop`)**: iterative work where you want to read progress and send follow-ups. Use `--no-wait` so the session detaches, then invoke `/loop` to poll, steer, or cancel. Best when the user explicitly wants tight steering.

If unsure which of the two long modes fits, ask. Defaults: "make a PR / write the tests / refactor X" → **long unattended** is usually right. "Explore / investigate / iterate on this" → **long steered**.

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
- **Agent** (optional): Which agent to use — default is `codex`, but `claude`, `pi`, `gemini`, etc. are available
- **Working directory** (optional): Defaults to current project directory
- **Permissions** (optional): `--approve-all` for full autonomy, `--approve-reads` for read-only autonomy (default), or `--deny-all` for no tool access

### 2. Create the session and send the first prompt in one shell command

Generate a descriptive session name from the task (e.g., `refactor-auth`, `test-coverage`, `review-api`). Chain `sessions ensure` and the first `prompt` call with `&&` so they go out as a single `Bash` tool call — avoids a round-trip and the permission prompt that comes with it.

**Short** — omit `--no-wait`, result returns in this turn:

```bash
acpx <agent> sessions ensure --name <session-name> && \
acpx --approve-reads <agent> -s <session-name> "<prompt>"
```

**Long unattended** — same command as short, but wrap the whole thing in `Bash` with `run_in_background: true`. The acpx turn runs inside a Claude Code background task. Output streams through `TaskOutput`, and `<task-notification>` fires on completion. Capture the returned task_id.

```bash
acpx <agent> sessions ensure --name <session-name> && \
acpx --approve-reads <agent> -s <session-name> "<prompt>"
# invoked via Bash with run_in_background: true
```

**Long steered** — `--no-wait`, detach, then `/loop` to poll:

```bash
acpx <agent> sessions ensure --name <session-name> && \
acpx --approve-reads <agent> -s <session-name> --no-wait "<prompt>"
```

Include relevant context in the prompt — file paths, constraints, what has already been tried. A good delegation prompt is self-contained.

(Only split into two calls if you need to inspect the `ensure` output — rare.)

### 3. Report back

Tell the user:
- The session name
- How to check on it (see commands below)
- Whether it's running async or waiting for a result

### 4. For long mode: loop to check in

After kicking off a `--no-wait` session, invoke the `/loop` skill to poll and steer it. Let the model self-pace:

```
/loop check on <session-name>: read recent output, decide whether to steer, send a follow-up prompt, or cancel. Stop looping when the session is idle and the task is done.
```

**Cadence**: default to **~3 minutes (180s)** between check-ins. Rupert wants tight steering on delegated work, not a set-and-forget. 3 min also stays inside the 5-min prompt-cache window, so each tick is cheap. Only stretch further if the agent explicitly said it's off doing something that will take much longer.

On each tick:
1. `acpx <agent> status -s <session-name>` — is it still running?
2. `acpx <agent> sessions read <session-name> --tail 50` — what did it just do?
3. Decide: let it keep going, send a steering prompt, or cancel. Surface anything notable to the user.
4. If the task is complete, summarize and end the loop (omit `ScheduleWakeup`).

Do not block the user's turn waiting on the agent — the loop exists precisely so the main session stays responsive.

---

## Ongoing management

After delegation, the user may ask to check in, steer, or stop the agent. Use these commands:

### Check status

```bash
acpx <agent> status -s <session-name>
```

### Read recent output

```bash
acpx <agent> sessions read <session-name> --tail 50
```

For a summary of turns:

```bash
acpx <agent> sessions history <session-name> --limit 10
```

### Steer the agent

Send a follow-up prompt to redirect or refine its work:

```bash
acpx --approve-reads <agent> -s <session-name> --no-wait "Actually, focus on X instead of Y"
```

### Cancel in-flight work

```bash
acpx <agent> cancel -s <session-name>
```

This cooperatively cancels the current prompt. The session stays alive — you can send new prompts after cancelling.

### Close the session

When the task is done:

```bash
acpx <agent> sessions close <session-name>
```

Note: `sessions read`, `sessions history`, `sessions show`, and `sessions close` all take the session name as a **positional argument**, not `-s`. The `-s` flag is only for `prompt`/`cancel`/`status`/`set`/`set-mode`.

---

## Tips

- **Session names persist.** You can come back to a session in a future conversation if it's still alive.
- **List all sessions** with `acpx <agent> sessions list` to see what's running.
- **Max turns**: Use `--max-turns <n>` to limit how much work the agent does autonomously.
- **Timeout**: Use `--timeout <seconds>` to cap how long a single response can take.
- **One-shot mode**: For tasks that don't need a session, use `acpx <agent> exec "<prompt>"` instead.
