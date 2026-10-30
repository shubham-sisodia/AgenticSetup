---
name: critique
description: Run a rubric-based usability and accessibility critique of a design-tool frame, a screenshot, or a live URL. Use when the user says "critique", "review this design", "what's wrong with this screen", or pastes a design link asking for feedback.
---

# /critique: design critique

Input: `$ARGUMENTS`, a design-tool URL, an image path or a live URL. Several targets allowed. Add
`rerun <previous report path>` to re-verify an earlier critique after fixes.

1. Delegate each target to the `design-critic` agent with today's date and the absolute path of
   `critiques/`. Run the targets in parallel.
2. If the design belongs to a project built on the shared component library, also ask `ds-advisor`
   whether the screen deviates from the library's patterns, and merge its findings under a
   "Design-system consistency" section.
3. Synthesise: merge findings that appear on several screens into systemic issues (those matter more
   than per-screen nits).
4. Reply with Blockers first, then Majors, then a one-line verdict per screen, then file paths. If the
   user asks for fixes in the design tool, load that tool's authoring skill first.
