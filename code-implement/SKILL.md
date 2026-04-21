---
name: code-implement
description: TDD implementation from a plan. Writes all tests first, then implements until they pass, then reviews against acceptance criteria.
---

You are implementing functionality in an existing codebase through test-driven development, based on a plan that has been meticulously prepared for you. You must approach this as an exemplary experienced developer, with attention to detail, adherence to best-practices and architectural excellence, and be thorough in your execution.

Below are the steps.

---

### 1. Review codebase

Run the `/code-review` skill to gain a general understanding of the codebase.

### 2. Review the plan

Read the plan being implemented. Understand the full scope — decisions, acceptance criteria, constraints — before writing any code. Read any referenced documentation (architecture docs, behavioral specs) for orientation, if you haven't already.

### 3. Set up worktree (optional, if prompted)

Create a git worktree in `.worktrees/` on a temporary implementation branch. All work happens in the worktree, keeping the main working directory clean and the original branch free.

```bash
git worktree add .worktrees/<branch-name> -b impl/<branch-name> <branch-name>
```

If a worktree for the branch already exists, reuse it.

---

**Note:** Depending on the scale of the change, you might want to tackle steps 4–7 in one go, or in smaller targeted batches.

---

### 4. Write tests

Write tests that cover the plan's acceptance criteria before writing any implementation code.

- Test names should map to acceptance criteria so failures are traceable
- Layer tests by type (unit, integration, e2e) where appropriate for the project
- Tests must rigorously exercise real code paths — no shortcuts
- Reasonable mocks only where necessary (external services, I/O)
- Test observable outcomes, not internal mechanics

### 5. Implement

Write code in full completeness, and with thoroughness and adherence to best practices, to pass the tests. Iterate until all tests pass.

- Refer to any code style documentation and enforcement rules (lints, structural tests)
- Adhere to the style and organization of existing code
- Re-use existing techniques, functions, types where practical
- Keep it simple — the simplest implementation that satisfies the acceptance criteria
- If the plan specifies types, interfaces, or other implementation details, follow them
- 
### 6. Run enforcement

Run all lints, structural tests, and CI checks. Fix any violations. The enforcement layer catches architectural mistakes that the plan doesn't specify — import boundaries, complexity limits, naming conventions.

### 7. Review against plan

Once all tests pass, review the implementation in-depth:

- Walk through every acceptance criterion — is it met?
- Are edge cases handled?
- Is anything missing or extra?
- Review project docs — do any need updating to reflect this change?

For any issues/inconsistencies found, go back to 4.

---

### 8. Commit, merge, and clean up worktree

Commit all changes on the `impl/<branch-name>` branch from within the worktree. Then fast-forward the original branch and clean up.

**Important:** The fast-forward and cleanup commands run from the **original working directory** (the workspace root, NOT the worktree). Do NOT checkout the original branch — `git fetch .` updates the branch ref without requiring a checkout. The original working directory stays on whatever branch it's currently on.

```bash
# from the worktree: commit
cd .worktrees/<branch-name>
git add -A && git commit -m "..."

# from the original working directory (NOT the worktree): fast-forward the original branch
cd /path/to/workspace/root
git fetch . impl/<branch-name>:<branch-name>

# clean up (also from the original working directory)
git worktree remove .worktrees/<branch-name>
git branch -d impl/<branch-name>
```

Never checkout or switch branches in the original working directory. The whole point of this workflow is that the original checkout is untouched.

---

## When the plan is wrong

If implementation reveals a plan issue — stop and flag it. Do not work around it. The plan needs to be revised first.
