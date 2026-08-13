---
name: code-review
description: "Evaluate a code change — diff, PR, or branch — against what it was meant to do: spec adherence, design, correctness, security, tests. Fixes what needs no human call (bugs, defects, mechanical issues) and raises design and architecture findings to the user, driving all findings to zero — a change is shippable only when none remain open. Use when receiving code that needs thorough review."
---

Judge a change: does it do what it was meant to, correctly and well? This skill is evaluation — it owns the judgment and the findings, and delivers its judgment in conversation.

## Inputs

- **The change** — a diff, PR, or branch.
- **The specification** — what the change was meant to do: a plan or a collection of specs, with acceptance criteria and referenced docs, when one exists. Without one, review against the stated intent.

## Review

Read the specification first, then every changed file in the diff — carefully, not skimmed. Cover, where relevant:

- **Spec adherence** — acceptance criteria satisfied? Anything missing, extra, or deviating?
- **Design** — right abstractions, sound architecture, no needless complexity, a simpler approach available?
- **Correctness** — does it actually work? Edge cases, error paths, race conditions, unintended consequences.
- **Security** — input handling, authz, secrets, injection, anything that widens the attack surface.
- **Tests** — rigorous, covering the criteria, no gaps.
- **Enforcement** — lints and structural checks pass.
- **Specs and docs** — specs and project docs consistent with the implementation: nothing left stale by the change, no spec or doc claiming behavior the code doesn't have (or the reverse); any changed human-facing docs satisfy `code-docs`.

For a large diff, fan out: parallel reviewers across files or the dimensions above, each returning findings with file:line evidence. You synthesize, reading any hunk a finding hinges on yourself.

## Findings

Every finding gets one of two tags — chosen by **who must resolve it**, never by severity or by how confident you feel:

- **mechanical** — there is an objectively right resolution and no human call to make: bugs, broken edge cases, security defects, missing or weak tests, lint violations, stale docs. A correctness or security problem lands here *even when you are only half-sure* — verify and fix; uncertainty never waves it through.
- **judgment** — resolution needs the user: design and architecture calls, interface shape, trade-offs, scope questions — anything where their feedback changes what the right fix is. Never resolved silently.

Each finding carries a short title naming the issue, file:line evidence, and a recommended action.

## Resolution — drive findings to zero

A change is **shippable only when no findings remain open**. There is no "ship with caveats" and no "shippable anyway".

1. **Close mechanical findings first.** Fix them (or hand them to the implementer to fix), re-verify, and record them in the report as closed.
2. **Raise judgment findings to the user.** Walk them one at a time — evidence and a recommendation per finding, the user's call on each. What to fix, dismiss, or defer is decided there, not declared by this skill.
3. **Final run.** Apply the user's decisions, re-review the ground they touch, and close out every finding.

## Output

A short judgment in chat:

- **Assessment** — a rough call on the current state: acceptable or not, what holds up, what's weak. A few sentences.
- **Judgment findings** — how many, as a summary list ordered by weight (one line each: the finding's title and the gist).
- Then prompt the user to go through them one by one, per Resolution step 2.

For mechanical fixes, note briefly what ground was covered and how it was verified.

For example:

> **Assessment:** The change does what the spec asks and holds up well — architecture is sound, tests cover the criteria. I fixed and verified 4 mechanical findings (an unhandled `null` in the parser, two missing edge-case tests, a stale README paragraph); the suite is green. Three judgment findings remain, one of them substantial, so it's not shippable yet.
>
> **Judgment findings (3):**
> 1. **Retry logic placement** — retry lives in the transport layer; may belong at the call site.
> 2. **Unspecified eviction policy** — the cache assumes LRU; the spec is silent on it.
> 3. **Flag naming divergence** — the new flag doesn't match its sibling commands.
>
> Want to go through them one by one?
