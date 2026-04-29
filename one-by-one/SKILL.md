---
name: one-by-one
description: >
  Walk through a list of items one at a time. For each item, give a brief
  overview and a single suggested option, then wait for the user's decision
  before moving on. Use when the user says "/one-by-one", "go one by one",
  "walk me through these", or hands over a list to triage.
---

# One by one

Process a list of items sequentially. Don't dump the whole list at once. For each item: brief overview, one suggested option, then wait.

## Steps

1. **Identify the list** — the items the user wants to walk through. If unclear, ask what list and where it lives.

2. **Confirm count** — state how many items there are so the user knows the scope (e.g. "There are 7 items. Starting with the first.").

3. **For each item, in order:**
   - **Overview** — 1–3 sentences. What it is, what's notable, what state it's in. Include enough context for the user to make a call without reading the source.
   - **Suggested option** — one concrete next step, not a menu. Phrase it as a recommendation ("Suggest: archive this — it's been stale for 6 months.").
   - **Stop and wait** — do not move to the next item. Do not preview what's coming. Wait for the user's response.

4. **Apply the decision** — accept, modify, or skip. Then move to the next item with the same format.

5. **Finish** — when the list is exhausted, summarize what was decided in one or two lines.

## Guidelines

- One item per turn. Never batch.
- One suggestion per item. If torn between two, pick the stronger one and mention the alternative in a single clause.
- Keep overviews tight — the user is making a decision, not reading a report.
- If an item needs more investigation before a suggestion is possible, say so and suggest the investigation as the next step.
- Track progress (e.g. "3 of 7") so the user knows where they are.
