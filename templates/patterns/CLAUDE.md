# CLAUDE.md: `patterns/` folder

Rules for any session working inside `patterns/`.

## Scope
**Do cover:** folder layout, providers, routing shapes, app shell, navigation, auth flows, data layer,
page templates, tables, forms, drawers, dialogs, notifications, styling, icons, anti-patterns.

**Don't cover:** component props (→ the API reference), install steps, per-component snippets (link
to them), any project's business logic (→ that project's own docs).

If you are writing a props table or a component demo, stop: it belongs in the root docs. Link out.

## Writing style
- Terse. Pattern first: the shape, then the example, then a one-line reason.
- Real file paths (`src/pages/invoices/InvoicesPage.tsx`, not `path/to/page.tsx`).
- No hedging, no preambles, no emojis, no comments that narrate the code.

## When a project diverges
1. The project is wrong: fix the project.
2. The pattern is wrong: update the pattern doc first, then apply it in the project.
Never let a project ship against a stale pattern doc.

## File naming
`NN-topic-name.md`, two-digit ordinal in reading order. Insert with a decimal suffix (`07.5-wizards.md`)
rather than renumbering, so inbound links stay stable.

## PR workflow
Branch `feature/patterns-<topic>` off trunk. Commit prefix `patterns: <doc>: <change>`. No package
version bump for `patterns/`-only PRs.

## Do not
- Recommend a dependency that isn't already used in 2 or more apps.
- Reference an internal URL or a secret.
