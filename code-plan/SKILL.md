---
name: code-plan
description: Plan a code change collaboratively and log the decisions to a plan file as they settle. Plans a whole feature or a single section depending on what the caller asks for. Used standalone or as a sub-skill inside /code.
---

The plan is made in conversation. The desired effect is a magical document that fills in and revises its contents based on what the caller confirms. Things go into the doc only once clearly confirmed — never ahead of the conversation — and its structure may change as required when new information comes to light.

## Workflow

1. **Understand the goal.** What the change is for and what success looks like. Read the relevant code first. If the goal is fuzzy, ask.
2. **Discuss in chat.** Propose approaches, candidates, trade-offs — in the conversation, never in the file. The file gets none of your speculation.
3. **Write what settled.** When a decision lands — the caller engaged and confirmed — fold it into the file, in the shape they confirmed, revising and restructuring earlier content as new decisions reshape it. Before the first write, read `code-docs`: the plan must abide by it. Loop 2 and 3 regularly — write in small increments as decisions settle, not in one batch at the end — until the plan covers the change.
4. **Harden.** When the drafting loop winds down — decisions have stopped landing and the plan covers the change — suggest this phase to the caller. On their go: fan out subagents to verify every claim against the code and red-team the design. Tighten wording, fix facts, surface anything contested — add no new decisions. The plan is final only on the caller's explicit sign-off.

## Guidelines

- **Planning is usually specification.** The heart of most plans is the behavioral contract — what the change does, observed at its interfaces. When the project keeps specs, the plan can take the form of a new or updated spec; when it doesn't, the plan file carries that weight itself. Either way the rest of this skill applies unchanged.
- **Behavior before technical.** Formalize the behavior for the user and the contracts at interfaces first; discuss technical implementation details after, and only if required.
- **Structure emerges.** No fixed set of headings — cluster related decisions under appropriate headings as they accumulate, typically under behavior and implementation where relevant, splitting or merging sections as the shape of the change becomes clear. A heading exists only once it has agreed content under it; no empty scaffolding, no TBD placeholders.
- **The file contains only agreed content.** No invented candidates, no placeholder sections, no template scaffolding. An open question appears only if it was actually raised and left open.
- **Don't make stuff up.** Every claim about current code comes from reading it. Quote current signatures when changing an interface.
- **Reuse what exists.** Check for existing patterns, names, and conventions before proposing new ones.
- **Pin what was decided, skip what wasn't.** Genuinely open choices are marked as the implementer's call, not filled with invented decisions.
- **Plans use code-docs.** Concrete language, economy, self-sufficiency.
- **Output target.** Suggest a target — the caller's supplied path, the area's existing spec(s) mutated in place with no separate plan doc, or a new plan or spec file at the codebase's logical spot — but the caller always confirms it before the first write.
