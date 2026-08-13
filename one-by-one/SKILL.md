---
name: one-by-one
description: >
  Walk through a list of items one at a time. For each item, give a brief
  overview and a single suggested option, then wait for the user's decision
  before moving on. Use when the user says "/one-by-one", "go one by one",
  "walk me through these", or hands over a list to triage.
---

# One by one

Process a list sequentially — never dump the whole thing. For each item: brief overview, one suggested option, then stop and wait.

## The loop

1. **Identify the list.** If unclear, ask what list and where it lives.
2. **State the count** so the user knows the scope ("7 items, starting with the first").
3. **For each item, in order:**
   - **Overview** — 1–3 sentences: what it is, what's notable, enough context to decide without reading the source.
   - **Suggestion** — one concrete next step phrased as a recommendation ("Suggest: archive — stale 6 months."), not a menu. If torn between two, pick the stronger and name the alternative in a clause.
   - **Stop and wait.** Don't move on, don't preview what's next. Track progress ("3 of 7").
4. **Apply the decision** (accept / modify / skip), then the next item, same format.
5. **Finish** — summarize what was decided in a line or two.

If an item needs investigation before you can suggest anything, say so and suggest the investigation as the step.

## Pausing and resuming

Long walks (20+ items, multi-session) get interrupted. On "pause" / "later" / "break", **write a resume note** — wherever the setup keeps agent tasks (a task system, or a file beside the list) — with concrete state; without it, the next session re-derives everything. Capture: where you paused (entry N of M, item name); target file/destination (full path); schema/format (fields, types, enums, rules locked this session); done-so-far (completed entries + decided values); up-next (the entry awaiting confirmation + your suggestion); after-all-done step (build artifact, file summary). Enough to resume cleanly, not a full transcript.
