---
name: handoff
description: Produce a dev-ready handoff spec from a design-tool frame (region-by-region component mapping, states, edge cases) and optionally file the implementation ticket in <TRACKER>. Use when the user says "handoff", "spec this", or "make this buildable".
---

# /handoff: design-to-dev handoff

Input: `$ARGUMENTS`, a design-tool URL, optionally a <TRACKER> project key to file the ticket in.

1. Pull the frame through the design tool's MCP server: a screenshot and the design context (load the
   tools with ToolSearch if deferred), plus the variables and tokens it uses.
2. Delegate component mapping to `ds-advisor`: give it the design context and ask it to map every
   region to a library component or a library-native fallback, and to flag real gaps for
   `patterns/GAPS.md`. Never guess a mapping yourself.
3. Write `handoffs/YYYY-MM-DD-<slug>.md`:
   - Region table: region → component → props and variants → data source
   - **States**: loading, empty, error, partial: what each region shows
   - **Edge cases**: longest realistic strings, zero / one / many, permissions
   - **Tokens**: colours, spacing and type by token name, not hex
   - **Open gaps**: anything with no library answer, as questions for the design-system owner
4. If a <TRACKER> project key was given, create the implementation ticket with the spec summary and a
   link to the frame. If no key was given, confirm with the user before creating one.
5. Reply with the region table summary, the gaps, and file and ticket links.
