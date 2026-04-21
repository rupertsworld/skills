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

### 3. Write the plan

With both stages approved, write the plan. Follow the structure below.

**Where to save:**
- If the user specifies a path, use that
- Otherwise, save to `plan.md` in the project root

Plans are ephemeral. They're work orders, not permanent documentation. After implementation, they can be discarded.

## Plan structure

### Overview (top of document)

Start with **why** this change exists and a brief description of what it does. Include the reasoning and motivation — not just "what" but "why this way." If there are distinct deployment modes or usage contexts, describe them here.

Keep it to a short paragraph or two. The reader should understand the purpose and shape of the change before reading any details.

### Core sections (body)

Organize the body around the **core pieces** of the change — not generic headings like "scope" or "acceptance criteria", but named after the actual things being built or changed. For example: "CLI", "TelevisionClient", "Source reorganization", "Skill".

Each core section should flow from high-level to specific:

1. **Behavior / API first.** What does this piece do from the outside? Commands, endpoints, methods, inputs/outputs. Lead with the interface the user or consumer sees.
2. **Decisions.** Key choices made during discussion — trade-offs, conventions, defaults, constraints specific to this piece. Only include decisions that matter to the implementer; skip anything obvious.
3. **Tests.** What tests should exist for this piece. Brief descriptions, not full test code. Group them with the piece they test, not in a separate section.

If specific types, APIs, or signatures were agreed on during planning, include them in the relevant section. Don't exhaustively specify implementation details — but do pin down anything that was explicitly decided.

Not every section needs all three sub-parts. A small change might just need behavior + tests. A reorganization might just need the key moves and a note that existing tests must pass. Match the weight to the piece.

### Constraints (bottom)

Invariants that apply across the whole change. Things the implementation must never violate. "Server is always the source of truth", "all operations go through X", "never do Y."

### API / behavior changes (bottom, if any)

If the plan modifies any existing API, event shape, storage format, CLI flag, return value, error type, or observable behavior, list each change here with:
- **Before:** the current signature/shape/behavior (quoted from code)
- **After:** the new signature/shape/behavior
- **Affected callers:** every consumer touched by the change
- **Migration / compatibility note:** breaking or not, and what downstream work is implied

If there are no such changes, omit this section.

### Out of scope (bottom)

What's explicitly excluded. Prevents scope creep and sets expectations.

### Docs to update (bottom)

Which documentation files need updating as part of this change.

## Guidance

- **Prefer clarity and completeness over expediency.** Plans should be explicit enough that implementers do not need to infer critical behavior, interfaces, or constraints from context.
- **Keep it short.** A page or two max. If it's longer, the scope is too big; split it.
- **Don't prescribe file names or directory trees in detail.** Specify the structure and key moves, but let the implementer decide exact file names unless one was explicitly agreed on.
- **Pin what was decided, skip what wasn't.** If something was discussed and a choice was made, capture it. If it wasn't discussed, don't invent a decision — leave it to the implementer.
- **Group tests with their piece.** Don't collect all tests at the bottom — put them next to the thing they verify.

## Re-thinking the plan

If a path is getting messy or may cause future issues, bring it to the user's attention — the plan may need revision before continuing.
