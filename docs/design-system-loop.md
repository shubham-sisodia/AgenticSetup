# The design-system loop

How a component library stays the answer for every app built on it: an advisor that answers or logs,
two backlogs, a release contract, and a codify pass that turns the backlog into docs. Templates:
[`agents/ds-advisor.md`](../agents/ds-advisor.md) and [`templates/patterns/`](../templates/patterns).

## The pieces

| Piece | Where | Job |
| --- | --- | --- |
| `patterns/` | Inside the library repo, excluded from the package publish | Numbered docs on how to build a whole app: structure, routing, shell, data, tables, forms, dialogs, styling, anti-patterns. `starters/` holds copy-paste templates; `<platform>-addendum/` holds per-platform deltas. |
| `ds-advisor` | `~/.claude/agents/` | Answers from the hierarchy of truth, logs what it can't answer, plans designs, audits reuse, and (only when asked) codifies. |
| `GAPS.md` | `patterns/` | Every time the docs were silent (`pattern-gap`) or wrong (`doc-bug`), one entry naming the doc that should have answered. Doubles as the fallback-recipe library. |
| `PROMOTIONS.md` | `patterns/` | The same widget hand-built in 2 or more active apps: a candidate to ship in the library. |
| `UPGRADING.md` | `patterns/` | Per release: breaks, behaves differently, delete your workaround, verify. Written in the same PR as the version bump. |

Why `patterns/` lives in the library repo but outside the package: it versions with the components it
describes, but apps read it from the repo (or the advisor reads it for them), so it never bloats an
install.

## Hierarchy of truth

The advisor stops at the first source that answers completely:

1. The export barrel (`src/index.ts`): what the library actually ships.
2. `patterns/*.md`: app-level shape. Every import in a snippet is checked against the barrel first;
   docs have shipped phantom APIs before, and that is a `doc-bug`.
3. The API reference: props and usage.
4. The canonical app: the one reference project whose wiring wins when patterns conflict, and the
   source for any promoted API.
5. The consumer's own code.

## Five modes

| Mode | Trigger | Output |
| --- | --- | --- |
| lookup | One bounded question | The shape, one-line reason, citations; a GAPS entry if the docs were silent |
| review | "Review this against the patterns" | Deviations with `file:line` and the pattern that replaces each; raw colours named with their token |
| reusability audit | "What should become a library component?" | Ranked candidates, each with demand by project, proof of the export gap, and an API derived from the canonical app |
| design plan | A design handed in by the main session | Every region mapped down a three-tier ladder: exact export, known recipe, nearest primitive + flagged gap |
| codify | Explicitly invoked | Doc-bugs fixed first, proven gaps codified, entries annotated `[codified in NN-doc.md]`, one commit per doc |

**Rule: the advisor edits only the two backlogs, except in codify mode.** Everything else it returns as
text for the main thread to apply. That keeps a lookup from rewriting the docs it is meant to read.

## The loop

1. A consumer session asks the advisor something.
2. The advisor answers from the hierarchy. If `patterns/` was silent or wrong, it appends a GAPS entry
   and says so in its reply (the user is in another repo and won't see the dirty file).
3. When the same widget turns up hand-built in a second active app, a reusability audit appends a
   PROMOTIONS entry.
4. When 3 or more gaps are pending, run a codify pass: doc-bugs first (re-verified against source,
   because the entry may be stale), then gaps that a real project has implemented and kept.
5. A promotion that ships gets an `UPGRADING.md` entry whose "Delete your workaround" line names the
   local copies apps can now remove.
6. Consumers read `UPGRADING.md` before every bump; their advisor names the entries between their pin
   and the latest.

Two counting rules keep the backlog honest: demand is counted only in active code (a legacy tree being
retired is zero demand however often it repeats a widget), and a project with known anti-patterns
counts as demand but is never the API source.

## What it produced

In one library over five months: 85 gap entries, 7 promotion candidates, 5 of them shipped as
components, each with an `UPGRADING.md` entry naming the workaround to delete.

## Setting it up

1. Copy [`templates/patterns/`](../templates/patterns) into the library repo as `patterns/` and keep
   it out of the package's `files` whitelist.
2. Copy [`agents/ds-advisor.md`](../agents/ds-advisor.md) to `~/.claude/agents/`, fill in the library
   name, repo path, canonical app and reference projects.
3. Set `"uiAdvisor": "ds-advisor"` in `~/.claude/projects.json` so every registered project's session
   start tells Claude to route UI questions there ([GUIDE: Registry and session hook](GUIDE.md#registry-and-session-hook)).
4. Add the rule to the library's PR template: a version bump without an `UPGRADING.md` entry is
   incomplete.
