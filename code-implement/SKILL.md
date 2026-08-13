---
name: code-implement
description: TDD one slice from a plan. Tests first, then code until they pass, then review against the plan. A leaf skill, run directly or as a delegated implementation worker.
---

Implement a planned change test-first.

## Inputs

- **Plan** — (optional) the path of the plan or spec we are implementing.

## Flow

1. **Ground.** If `code-init` hasn't been run in this context, run it now, scoped to the task. Read the plan fully — decisions, acceptance criteria, constraints — before writing any code.
2. **Architecture.** If the plan leaves the architecture unspecified or underspecified, work it out now, before any tests or code: spend real cycles sketching the pieces — modules, boundaries, data flow, how it composes with what exists — and optimize for the cleanest, most modular, extensible shape. Don't let the architecture emerge incidentally from the order code gets written.
3. **Tests first.** Write tests covering the plan's acceptance criteria before any implementation (levels below). For larger changes, work in test → implement batches rather than one pass.
4. **Implement.** The simplest code that passes the tests. Match the existing style and organization, reuse existing functions and types, follow whatever the plan pins. Iterate until green.
5. **Enforce.** Run lints, structural tests, and CI checks; fix violations — they catch what the plan doesn't specify.
6. **Review against the plan.** Every acceptance criterion met? Edge cases handled? Anything missing or extra? Project docs needing updates? If updating human-facing docs, apply `code-docs`. Issues found → back to step 3.
7. **Review the code itself.** A separate pass from plan adherence: is it beautiful — succinct, clear, readable? Does it abide the style guide? Refine and re-run until the answer is yes with tests still green.
8. **Leave the work uncommitted.** Committing happens only on explicit instruction — the user's, relayed by the caller in the task prompt. Without it, finish with the changes in the working tree; never commit on your own initiative. When instructed, commit on the current branch with the repo's commit convention. Pushing, the PR, and cleanup are always the caller's job — stop there.

## Style guide

All code must abide the style guide. The project's own (routed from AGENTS.md / CLAUDE.md) takes precedence; absent one, use the default in [resources/style-guide.md](resources/style-guide.md).

## Test levels

**North star:** the user should never have to run the app to verify the change. If the suite passes, the feature works — beyond reasonable doubt. Tests that can't give that confidence are at the wrong level.

Pick the level by user-observable surface, not by how big the change is:

- **e2e — default for anything a user can touch.** CLI commands, UI flows, HTTP endpoints. Drive the real entry point the way a user would. If the user could verify it by clicking or typing, the test must do exactly that.
- **integration — for internal seams with no user surface.** A service talking to the DB, a pipeline stage, cross-module wiring.
- **unit — only when the logic itself is what's tricky.** Parsers, reducers, algorithms with real branching. Not for "the change is small".
- **none — for truly trivial changes.** Renames, typos, refactors with no behavior change. Existing tests still pass; don't invent a test to feel productive.

If e2e infrastructure doesn't exist for the surface you're touching, stop and flag it — build it in a separate plan -> implement step (preferred) or explicitly call out dropping to integration and why. Never silently default down.

Test names map to acceptance criteria. Exercise real code paths; mock only true externals — never the thing under test or the layer beneath it. Test observable outcomes, not internal mechanics. Tests must exhaustively test real behavior and implementation requirements, not just be written to trivially pass.

## Bug fixes

Before writing any code, reproduce the reported symptom — run the failing scenario, or load the actual affected surface in its real environment. Finding the "obvious fix" already in the codebase is a signal you've misread the issue, not that it's fixed. If you genuinely can't reproduce after honest effort, say so plainly rather than shipping a no-op fix behind a passing test.

## When the plan is wrong

If implementation reveals a plan issue, or the code is getting messy and the architecture is problematic, stop and flag it. Don't work around it — the plan gets revised first.
