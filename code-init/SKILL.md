---
name: code-init
description: Comprehensive codebase review to build understanding before planning or implementation. Use at the start of a session or when working in an unfamiliar codebase.
---

Explore the codebase thoroughly to build a working understanding of it.

## Steps

### 1. Read project docs

Read any available orientation docs — AGENTS.md, README, architecture docs, design docs. Get the intended lay of the land before looking at code.

### 2. Explore structure

Map the project structure: directories, key files, entry points, config. Understand the shape before reading code.

### 3. Read code

Read the main source files. Understand:
- Core abstractions and data structures
- How the pieces connect (entry point → layers → dependencies)
- Patterns and conventions in use (error handling, naming, module structure)
- Test structure and coverage
- Build, lint, and CI setup

### 4. Summarize

Present a concise summary to the user:
- What the project does
- Key architectural decisions and patterns
- Main modules and how they relate
- Notable conventions or constraints
- Anything surprising or potentially problematic

Keep it brief. The goal is shared understanding, not a document.
