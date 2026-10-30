# <LIB> app patterns

App-level composition patterns for apps built on `<LIB>`. Versioned with the library, excluded from
the package publish (not in the `files` whitelist in `package.json`), so it ships only through the
repo.

| Doc | Purpose | Location |
| --- | --- | --- |
| `<API_REFERENCE>.md` | Component API and props | Library root (published) |
| `patterns/` (this folder) | How to build a whole app with the library | Library repo only |

Patterns never duplicate component API docs; they link out.

## Reading order

- **New project:** 00 → 01 → 02 → 03 → 05 → 06 → 07, then copy from `starters/`.
- **Adding a feature:** jump to the doc for the task (new route → `02-routing.md`, list page →
  `07-page-templates.md` + `08-tables.md`, form → `09-forms.md`, destructive action → `11-dialogs.md`).
- **Upgrading the library:** read `UPGRADING.md` first.
- **Another platform:** the web docs first, then `<platform>-addendum/` for the deltas.

## Index

| # | Doc | Topic |
| --- | --- | --- |
| 00 | `00-stack-and-install.md` | Stack versions, install, build config |
| 01 | `01-project-structure.md` | Folder layout, providers stack |
| 02 | `02-routing.md` | Routes, `?tab=` pattern, protected routes |
| … | … | … |
| 16 | `16-anti-patterns.md` | What not to do, with the reason |

## Backlogs

| File | Holds | Written by |
| --- | --- | --- |
| `GAPS.md` | Questions the docs could not answer, and docs that were wrong | The advisor, every time it is silent |
| `PROMOTIONS.md` | Widgets hand-built in 2 or more active apps | The advisor, in reusability audits |
| `UPGRADING.md` | Per release: breaks, behaves differently, delete your workaround, verify | Whoever bumps the version, in the same PR |
