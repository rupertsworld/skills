---
name: code-plan
description: Create a plan for a code change through structured Q&A. Clarifies behavior, captures decisions and acceptance criteria. Use when starting a new feature or change that needs a clear plan before implementation.
---

Create a plan for a code change through a structured dialogue.

## Stages

Work through these stages in order. Get explicit approval before moving to the next.

### 1. Clarify

Ask clarifying questions **one-by-one** to understand:
- What the feature/change does from the user's perspective
- Expected behavior and edge cases
- Inputs, outputs, error cases
- What's in scope and what's not

### 2. Approach

Once behavior is clear, discuss how it should be built:
- Architecture and key abstractions
- Where it fits in the existing codebase
- Trade-offs between approaches
- What the acceptance criteria are

When proposing names, types, states, or conventions, check the existing codebase first. Reuse existing patterns, constants, and naming conventions rather than inventing new ones. If a concept already exists in code (e.g. a state enum, a status shape, a naming pattern), align with it.

Don't specify types, interfaces, or implementation details — those are the agent's job during implementation. Focus on decisions and constraints.

#### API or behavior changes

**Critical:** Any time the plan touches an interface — a new API, a changed API, a new or modified CLI flag, a new event, a modified return shape, a new or modified observable behavior — pin the interface down fully and confirm it with the user before writing the plan.

The point is **clarity on the whole interface**, not compatibility. The user and the implementer should both be able to see the full shape of every interface the plan introduces or changes, without having to infer it.

For each interface involved:

1. **Verify what's there now.** If modifying something that exists, read the code (don't guess). Quote the current signature or shape so it's clear what's changing.
2. **Lay out the full interface.** Name, inputs, outputs, error cases, side effects. For events/messages, the full payload shape. For a CLI, every flag and its semantics. For a function, the signature and what it returns in each case. No hand-waving — if a field's shape isn't nailed down, nail it down now.
3. **Walk through each interface explicitly.** Don't fold this into a general "does the approach look good?" sign-off. Present each interface on its own and confirm it — "the `X` event will carry `{a, b, c}` — confirm?" If something is ambiguous or under-specified, resolve it now, not during implementation.

When in doubt, err toward more explicit. Pinning an interface down in the plan is cheap; discovering mid-implementation that the user had a different shape in mind is not.

### 3. Summary report

Before writing the plan, produce a **Summary report** for the user to approve. This is a compact lay-of-the-land view of the post-change system — a reference map, not prose or a todo list. It exists so the user can confirm the whole shape of the change at once rather than inferring it from bullet lists.

The report is a separate artifact from the plan. It can feed the plan later, but the plan uses domain-based sections that integrate these pieces under its own headings.

Format: normal markdown. Render the report with an H1 title and normal H2 sub-sections — not inside a fenced code block, not a fixed-width text box. The outline below is a menu of candidate sections in canonical order; use only the ones that apply to this change, and pick whichever structure inside each section (bullets, prose, code blocks for literal output) reads most clearly.

Candidate sections, in order:

- `# Summary — <short title>`
- One- or two-sentence narrative: what the change is, why it exists, what it replaces. Enough context that the rest of the doc reads cleanly.
- `## Behavior change` — "was X; now Y" facts about observable app behavior. Lead with the semantic delta. Include implementation detail when the how is load-bearing for understanding the shape of the change (e.g. "reads root package.json at CJS-require time because the bundle sits next to it post-install") — skip it when the how is incidental.
- `## UI change` — end-user surface changes (CLI, web UI, prompts). Render concrete before/after output when practical: CLI output, log lines, prompt strings. Don't try to ASCII-art a whole web UI — describe it in prose when literal rendering isn't feasible.
- `## Interface delta` — programmatic interfaces the plan touches. Cluster by kind: HTTP, client methods, CLI signatures, types, events, errors. Before/after form for anything with a "before." Events belong here too — fan-out rules, ordering, payloads.
- `## Ownership` — one line per package/module that gains or changes responsibility. Not what it does in general, just what's new/changed.
- `## Data flow` — include only when the call chain is non-obvious (e.g. mid-layer indirection, event-driven coordination across services). Skip for straightforward changes.

Not every section applies to every change. Skip any that would be empty, trivial, or redundant with another section in this specific change. A tiny change might only have Behavior change + Interface delta; a UI-only change might skip Interface delta entirely. Don't pad.

Tone: present-tense descriptions of the post-change state. No imperatives ("we will…"), no todo-list framing.

Walk the user through the report and get explicit approval before writing the plan.

### 4. Write the plan

With all prior stages approved, write the plan. Follow the structure below.

**Where to save:**
- If the user specifies a path, use that
- Otherwise, save to `plan.md` in the project root

Plans are ephemeral. They're work orders, not permanent documentation. After implementation, they can be discarded.

## Plan structure

### Overview (top of document)

A short narrative paragraph or two — the big-picture "why." What's the problem, what does this change replace, why this shape. Written for a reader who hasn't followed the dialogue.

Optionally follow the paragraph with a "Major changes" dot-list — a handful of bullets calling out the biggest observable deltas (behavioral, interface-level, or UX). Useful for medium-sized changes where one paragraph can't name every headline. Keep it short; a reader who wants detail goes to the domain sections.

The Summary report from Stage 3 does **not** reappear as a section in the plan. Its contents get distributed into the Overview bullets and the domain sections where each piece naturally belongs — behavior changes inline with the code that changes them, interface deltas next to the route/method they modify, UI renders inside the CLI/UI section, ownership notes mentioned where relevant. The Summary report is a pre-plan approval artifact, not a plan section.

### Domain sections (body)

Group the body around **functional/domain areas of the change**, named after the concept (not the package). For TV-78: "Artifact removal" and "Workspace removal" rather than "ServerStore" and "Routes." Multiple layers of a single concept (store + route + client + types) belong in the same section.

Each domain section weaves everything relevant together:

- **What changes and how it behaves.** The core mechanic.
- **Rationale inline.** Why nested URL instead of flat? Why 404 instead of no-op? The "why this way" lives next to the "what," so the reader doesn't have to cross-reference a separate Decisions list.
- **Interfaces touched.** Signatures, payloads, events, errors belonging to this domain. Give the reader enough context to find and understand the interface without grepping:
  - **Where it lives.** Package + file path (e.g. "`ArtifactClient` in `packages/shared/src/client.ts`"), or class/module for typescript-level interfaces, or the route path for HTTP.
  - **What it is today.** If modifying an existing interface, quote or summarize the current shape alongside the new shape so the delta is visible. Don't force the reader to infer "this is a change" from the fact that the section exists.
  - **Full new shape.** Inputs, outputs, fields, errors. No hand-waving — if a field's shape isn't nailed down, nail it down now.
- **Tests.** The scenarios that prove this piece works. Short descriptions.

Domains vary — sometimes a single concept deserves its own section (CLI, Web UI, a cross-cutting helper like "reference membership"), sometimes two concepts share one. Pick what makes the reader's job easiest.

No separate **Decisions** section — the plan is all decisions. Rationale lives inline where it applies.

No separate **Constraints** section unless a genuinely cross-cutting invariant has no natural home in a domain section (rare). If it has a home, put it there.

### Out of scope

What's explicitly excluded. Prevents scope creep and sets expectations.

### Docs to update

Which documentation files need updating as part of this change.

## Guidance

- **Prefer clarity and completeness over expediency.** Plans should be explicit enough that implementers do not need to infer critical behavior, interfaces, or constraints from context.
- **Keep it short.** A page or two max. If it's longer, the scope is too big; split it.
- **Don't prescribe file names or directory trees in detail.** Specify the structure and key moves, but let the implementer decide exact file names unless one was explicitly agreed on.
- **Pin what was decided, skip what wasn't.** If something was discussed and a choice was made, capture it. If it wasn't discussed, don't invent a decision — leave it to the implementer.
- **Domain sections over mechanical groupings.** "Artifact removal" beats "ServerStore + Routes + Client" as a grouping — it follows how a reader thinks about the change, not how the code is filed.

## Re-thinking the plan

If a path is getting messy or may cause future issues, bring it to the user's attention — the plan may need revision before continuing.
