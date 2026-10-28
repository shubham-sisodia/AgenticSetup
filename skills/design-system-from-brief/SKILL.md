---
name: design-system-from-brief
description: Generate a project design system from a written brief as a root DESIGN.md (Google's open spec) - tokens, type scale, spacing, components and one sample screen - then lint it for structure and WCAG contrast. Use when starting a new project's visual design.
---

Turn the user's design brief into a `DESIGN.md` at the project root that any coding agent can read.

1. **Read the brief** (template: `templates/design/brief.md`). If product type, mood, density or constraints are missing, ask once.
2. **Optionally seed** from a DESIGN.md in VoltAgent/awesome-design-md whose style matches the mood; adapt it, don't copy it.
3. **Write `DESIGN.md`** in the google-labs-code/design.md format:
   - YAML front matter with the tokens: colors (light, and dark if required), typography scale (sizes, weights, line heights, fonts), spacing scale, radius and shadow tokens matched to the density.
   - Markdown body with the rationale: overview and mood, how each token group is meant to be used, core components (button, input, select, table, card, dialog, nav) with their states, and do's and don'ts.
4. **Lint it** and fix every error before presenting:
   ```bash
   npx -y @google/design.md lint DESIGN.md
   ```
   Contrast failures are errors, not warnings.
5. **Build one sample screen** for the main use case using only the tokens, and look at it (screenshot) before calling the system usable.
6. **Export when syncing to code:**
   ```bash
   npx -y @google/design.md export --format tailwind DESIGN.md > tailwind.theme.json
   npx -y @google/design.md export --format dtcg DESIGN.md > tokens.json
   ```
7. End with three open questions about choices you weren't sure of.

Later changes: edit `DESIGN.md`, re-run lint, and use `npx -y @google/design.md diff DESIGN.md DESIGN-v2.md` to review what changed.
