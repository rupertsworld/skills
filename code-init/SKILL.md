---
name: code-init
description: Build codebase understanding before planning or implementation. Scoped to the task at hand by default; full orientation when there's no specific task or the codebase is new.
---

Build enough understanding of the codebase to plan or implement without guessing. Scope the effort to the task — a small change needs a small map.

## Inputs

- **Task** (optional). What's about to be planned or built. If given, scope exploration to it. If not, do a general orientation pass.

## Guidelines

- **Fan out for breadth.** Cover the ground with parallel `Explore` agents — one per area or question — rather than reading everything serially yourself.
- **Specs or docs first.** Read the routing docs — AGENTS.md / CLAUDE.md, README, any architecture notes they point to, any core guidelines. They tell you where to look and what the project thinks its own rules are. If the area has specs, read them before the code they govern — a spec is the contract the change must honor, not just orientation. Not every project has specs; the docs tell you either way.
- **Scope to the task.** Trace the code the change will actually touch: entry points into that area, the abstractions and data structures involved, the conventions in use there (naming, error handling, test patterns). Go wider only when the task is wide.
- **Read, don't assume.** Understanding comes from the actual code, not from what a project like this would typically do.
- **Stop when it stops paying.** You're done when you could explain how the change fits into what's there — not when you've seen everything.

## Play back

End with a short summary in chat: what's relevant to the task, how it shapes the approach, anything surprising or constraining. Shared understanding, not a document.
