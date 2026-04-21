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

#### Changes to existing API or behavior

**Critical:** If the plan proposes modifying an existing API, event shape, storage format, CLI flag, return value, error type, or any observable behavior — flag it explicitly and confirm before proceeding.

For each proposed change:

1. **Verify the current state.** Read the relevant code (don't guess). Quote the current signature, shape, or behavior so the user can see exactly what's changing.
2. **State the change clearly.** "Currently X does Y; this plan changes it to do Z." Name every call site, consumer, or caller that is affected.
3. **Call out compatibility impact.** Is this a breaking change? Does it require a migration? Does it affect persisted data, stored artifacts, or on-wire formats? Does it change something another workspace or package depends on?
4. **Get explicit confirmation.** Do not fold API/behavior changes into the broader approach sign-off — ask about each one specifically. "This changes the shape of the `X` event — confirm?" A general "yes, the approach looks good" is not sufficient confirmation for a breaking change.

Default to preserving existing behavior. If a change looks convenient but isn't strictly required by the task, propose it separately rather than bundling it in.

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
