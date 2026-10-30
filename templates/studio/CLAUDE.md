# Design studio workspace

This folder is a product-design workspace run through Claude Code. Every design effort moves through
five stages, each backed by a skill or an agent:

| Stage | Command / agent | Powered by |
| --- | --- | --- |
| 1. Discover | `/research <question>` + `ux-researcher` agent | Web search and fetch |
| 2. Teardown | `/teardown <product or URL>` + `competitor-scout` agent | Browser automation |
| 3. Define | `/brief <issue key or one-liner>` | The issue tracker's MCP server |
| 4. Design | The design tool's MCP server, per `frameworks/figma-authoring.md` (copied from AgenticSetup `docs/figma-authoring.md`) | The design tool, the component library |
| 5. Critique and handoff | `/critique <url>` and `/handoff <url>` + `design-critic` and `ds-advisor` | The design tool, the tracker |

## Folder layout
- `frameworks/`: durable specs and contracts (e.g. the design-tool authoring framework)
- `research/`: synthesised research reports
- `teardowns/`: competitor teardown notes and screenshots
- `briefs/`: design briefs (problem, users, constraints, success metrics)
- `critiques/`: heuristic and accessibility critiques
- `handoffs/`: dev handoff specs (component mapping, states, edge cases)

Name artifacts `YYYY-MM-DD-<slug>.md`. Every artifact links back to the brief it serves.

## Conventions
- **A brief is the contract**: no production design work starts without one in `briefs/`.
- Critiques use Nielsen's 10 heuristics and WCAG 2.2 AA as the rubric, scored per screen.
- Handoffs map every region of a frame to a library component, or flag a gap. Delegate that mapping
  to `ds-advisor`; never guess.
- When motion, interaction or feel can't be judged from static frames, build a live HTML or React
  prototype (the `frontend-design` skill) instead.
- For wide work (tear down five competitors, critique twelve screens), use a workflow to fan agents
  out in parallel.
