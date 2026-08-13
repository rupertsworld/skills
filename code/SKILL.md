---
name: code
description: Entry point and steward for code work. Indexes the code sub-skills (init, plan, implement, review, tidy), carries the shared coding guidelines, and orchestrates the phases by fanning work out to subagents. Use when starting non-trivial code work, directly ("/code <task>") or via upstream skills like /linear.
---

Depending on the task at hand, choose one or more of these workflows.

## Sub-skills

- **code-init** — build codebase understanding before working somewhere unfamiliar.
- **code-plan** — plan a change collaboratively, usually as a specification; the file fills in as decisions settle.
- **code-implement** — TDD one slice from the plan: tests first, then code until they pass. The leaf each implementation worker runs.
- **code-review** — evaluate a diff against its spec; fixes mechanical findings, raises judgment findings to the user one at a time, drives all findings to zero (shippable only when none remain open).
- **code-docs** — write, edit, or review human-facing docs, specs included: concrete, focused, self-sufficient, current.
- **code-tidy** — wind down session state: worktrees, merged branches, background processes.

The typical arc is init → plan → implement → review → PR → tidy.

## Delegation

You are the steward, not the sole worker. Fan the legwork out to subagents at every phase; work inline only when the task is too small for a subagent to be worth it.

- **Delegate the legwork, keep the judgment.** Subagents gather, verify, and execute. You keep the goal, the plan's decisions, the conversation with the user, and the go/no-go between phases — never delegate those.
- **Fan out per phase.** *init* → parallel `Explore` agents, one per area. *plan* → before handing the draft over, agents that verify every claim against the code and red-team the design. *implement* → one `code-implement` worker per independent slice (isolate parallel slices so they don't collide); babysit each, then hand the finished slice to a separate `code-review` subagent and act on its findings before moving on. *review* → for a whole change, parallel reviewers across files or dimensions.
- **Scale to the task.** One worker for a simple change; fan out only where there's genuinely independent ground to cover.
- **Digest what comes back.** Workers return high-signal findings with evidence (file:line, quoted signatures), not "looks fine." Read the returns and pull anything load-bearing into your own head — read that code yourself before it drives a decision. Stewarding on summaries alone leaves you blind.

## Guidelines

**The cardinal rule: never start implementing without a clear go-ahead.** Every change gets a stated approach first — a written plan via `code-plan`, or for impromptu work a plan proposed in chat — and implementation starts only when the user explicitly says go on it. No go-ahead, no code.
- **Suggest a branch.** Before implementation starts, suggest a feature branch name and let the user decide — they may take it, rename it, or ignore it and stay put. The plan commits to whatever branch the work lands on.
- **Init before planning or building.** Run `code-init` to build codebase understanding before `code-plan` or `code-implement`, unless it's already established this session.
- **Plan before building.** Non-trivial changes get a written plan or spec via `code-plan`; small ones at minimum a proposed approach in chat. Either way, the cardinal rule applies.
- **Test-first.** Code is written TDD — for each slice, the tests for the plan's acceptance criteria come first, then the simplest code that turns them green, then review. `code-implement` runs this loop; don't implement code-first and backfill tests at the end.
- **Review every implementation step.** Each completed piece of implementation goes to a separate `code-review` subagent before the next one starts — implement, review, adjust, continue. Not inline, not batched to the end; a step isn't done until its review findings are addressed.
- **Commit only on explicit instruction.** No commit — by you or any subagent worker — unless the user has explicitly said to commit (a general go-ahead to implement is not commit permission). Workers leave their changes uncommitted in the working tree; when the user says commit, commit. Pass this constraint into every worker prompt.
- **Docs use code-docs.** Whenever a change writes, edits, or reviews a human-facing doc, apply `code-docs` as the standard.
- **Merge via PR.** Open it with `gh`, babysit CI and feedback. After merge, archive or remove any temporary documents the work produced (plan files, scratch notes — specs stay in place), and offer `code-tidy`.
