---
name: log
description: >
  Save a detailed session log. Use when the user wants to save, archive,
  or log the current session. Trigger on "log", "save session", "log this".
---

Write a comprehensive session log to `logs/`.

## Steps

1. **Choose a topic name** from the conversation's main subject. Short, sentence case (e.g. "Skill cleanup", "Stash sync debugging").

2. **Create the file** at `logs/YYYY-MM-DD <topic>.md`.

3. **Write a detailed debrief** of the session. Not a transcript — a rich, readable account of what happened. Include:
   - What was the goal
   - What was explored, tried, and discovered
   - Key findings, examples, data points, error messages — anything useful
   - Decisions made and why
   - What changed (files, config, architecture)
   - Important facts, context, or things to remember
   - Open questions or next steps

   Write it as natural prose and bullet points — no rigid template. The goal is: someone reading this next week should be able to fully understand what happened and pick up where things left off.

4. **Confirm** the file path when done.

## Rules

- If multiple saves happen on the same day with the same topic, append a number: `2026-02-24 Skills setup 2.md`
- Be thorough — err on the side of too much detail over too little
- Include specific examples, code snippets, or findings when relevant
- No raw message transcripts — synthesize and organize the information
