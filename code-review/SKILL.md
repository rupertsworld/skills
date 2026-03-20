---
name: code-review
description: Review code for plan adherence, design quality, and clean code. Use when receiving code (PRs, diffs, or changes) that needs thorough review.
---

Review code changes for plan adherence, good design, and clean code.

## Steps

1. **Read the plan** — understand what was supposed to be built. Read the acceptance criteria and any referenced docs.

2. **Review the changes** — run `git diff` or read the PR diff. Read every changed file carefully.

3. **Write a review** covering:
   - **Plan adherence** — does the code satisfy the acceptance criteria? Anything missing, extra, or deviating?
   - **Design** — are the abstractions right? Is the architecture sound? Are there simpler approaches? Is there unnecessary complexity?
   - **Code quality** — clean, well-named, well-organized? Consistent with the codebase?
   - **Tests** — are they rigorous? Do they cover the acceptance criteria? Any gaps?
   - **Enforcement** — do lints and structural tests pass? Any violations?
   - **Docs** — do any project docs need updating to reflect this change?

4. **Flag issues with severity:**
   - **Blocker** — must fix before merging. Incorrect behavior, missing acceptance criteria, security issues.
   - **Suggestion** — would improve the code but not strictly wrong. Design improvements, simplification, alternative approaches.
   - **Nit** — style, formatting, minor readability issues.

5. **Before finalization**, if the reviewed work used an ephemeral plan file, ask the user whether the plan should be removed now before any merge, push, cleanup, or other finalization step. Do not remove the plan automatically.

Write the review as a natural write-up, not a checklist. Be specific — reference files, lines, and acceptance criteria.
