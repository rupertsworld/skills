---
name: codex
description: >
  Consult the Codex CLI from within the current session via bladerun. Use when
  a second opinion is wanted, when Codex is a better fit for the task (deep
  reasoning, alternative architecture exploration, tricky bugs), or when
  offloading a self-contained sub-problem without losing the current context.
  Trigger on "ask codex", "consult codex", "what does codex think", "get codex
  to look at this".
---

# Codex

Fire-and-wait consultation of the Codex CLI via bladerun. Codex runs as a
background process; the current session keeps working or waits, then reads
the response when it completes. No daemon, no persistent server — each
consult is a cold spawn that can optionally resume a prior Codex session by id.

## When to use

- A second opinion on architecture, a plan, or a tricky bug before committing
- Codex is known to be stronger at the specific task at hand (deep
  step-by-step reasoning, math-heavy work, alternative framings)
- Exploring an alternative approach in parallel without derailing the main
  session's context
- Self-contained sub-problems that can be stated in one prompt

## When NOT to use

- Tasks the current session can handle directly — don't outsource reflexively
- Long supervised runs that need iteration and feedback — use a dedicated
  bladerun run instead
- Anything requiring the main session's full working context — the consult
  starts cold

## How it works

1. **Kick off the consult** with bladerun as a background Bash task
   (`run_in_background: true`):

   ```
   bladerun consult codex -p "<prompt>"
   ```

   To continue a previous thread, pass `--session <id>`.

2. **Capture the run id** from bladerun's output. Hold onto it if follow-ups
   are likely.

3. **Keep working** on the main task. The background task will auto-notify
   on completion — no polling needed.

4. **Read the response** once notified, using `bladerun tail <id>` or the log
   path bladerun prints.

5. **Integrate the answer** into the session's reasoning. Attribute explicitly
   when surfacing conclusions to the user ("Codex suggests…").

## Threads

For multi-turn consultations, capture the session id from the first consult
and reuse it with `--session <id>` on subsequent calls. Codex resumes from its
native session store; bladerun just forwards the resume flag. No state lives
in bladerun itself, so threads survive across Claude Code sessions — a thread
id from yesterday can be resumed today.

Keep threads scoped: one consult session per topic. If a topic shifts, start
a new thread rather than piling context onto an existing one.

## Prompting Codex

Codex has no shared context with the current session. Every consult is a cold
start. Include in the prompt:

- The specific question or task, stated plainly
- Only the context needed to answer — summarize, don't paste whole files
- The desired answer shape (plan, diff, critique, pros/cons, code)
- Any constraints (language, style, "don't write tests", etc.)

Frame prompts as standalone requests a stranger could answer.

## Reporting back to the user

When relaying Codex's response:

- Attribute it clearly ("Codex suggests…", "Per Codex…")
- Summarize — never dump the full transcript inline
- Note where Codex agrees or disagrees with the current session's prior
  reasoning, and which view is being adopted and why
- If the user wants the full response, point at the log path

## Guidelines

- One consult per discrete question. Don't bundle unrelated asks.
- Prefer waiting for the consult rather than racing ahead if its answer
  directly blocks the next step.
- Treat Codex as a peer, not an oracle — evaluate its answer critically before
  acting on it.
- Don't chain consults without reading the prior response first.
