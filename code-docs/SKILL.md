---
name: code-docs
description: Sets the standard for documents (e.g. those in the `docs/` folder) — the human-readable explanation of what the code does and why, and other related project information, specs included. Use whenever writing, editing, or reviewing a doc. Enforces best practices.
---

Docs must adhere to the following principles. When you write a doc, double check it against these principles and revise continuously & iteratively until it satisfies all of them.

- **Clear purpose.** Each document exists for one nameable reason — an architectural decision, a workflow, a tricky implementation. State it in the opening, in plain prose, so you can hold it and check the rest against it. If you can't state that reason in a few sentences, don't write the document.
- **Serves the purpose.** Every sentence advances that purpose; cut anything off-purpose, even when it's true and well-written. The common failure is pulling in surrounding context and over-cooking it into the doc. Relevance is the test, not length.
- **Be concrete.** Say plainly what you mean. If a phrase sounds meaningful but a reader can't tell exactly what it denotes, replace it with the specific thing. Don't let a metaphor do the work a precise sentence should.
- **Sober register.** Keep the voice plain and matter-of-fact — unemotive, no enthusiasm or chattiness. Closer to a government notice than a message to a friend.
- **Tight and focused.** Explain the why and the how; don't restate what the code already shows. Cut every word that isn't doing work.
- **Don't over-produce.** Write only what the subject needs. Don't pull in surrounding context and inflate it into something longer than warranted — a common failure mode. A doc is as long as it needs to be and no longer.
- **Snippets earn their place.** Include a code snippet only when it shows what prose can't — a hard-to-describe pattern, a concrete type or signature, pseudo-code for a non-obvious flow. Keep it to the one concept being taught; snippets rot faster than prose.
- **No assumed context.** Don't rely on knowledge the reader is presumed to have. Link to that context or define it inline. Don't over-index on negatives either: say what should happen, and state what doesn't happen only when a cold reader would otherwise assume it does.
- **Don't repeat yourself.** Each fact lives in one place. If something is said twice, move it to a single home and link to it.
- **Clean information architecture.** Order headings and content so a reader can scan and grasp the shape of the information. The format is free; the structure is never muddy. If it isn't clean, reorganize.
- **Consistent.** Match conventions — terminology, structure, formatting — within the document and across the `docs/` folder. Where an existing document follows these principles, follow it. Where it breaks them, follow the skill instead and flag the conflict rather than copying the flaw.
- **Stays current.** Outdated docs mislead worse than missing ones. Update the doc when the code it describes changes.
