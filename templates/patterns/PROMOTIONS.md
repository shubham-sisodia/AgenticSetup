# <LIB>: promotion candidates

Append-only backlog of widgets re-implemented in **2 or more active apps** that the library does not
ship yet. Distinct from `GAPS.md`: GAPS = "the docs are silent on an app-level shape"; PROMOTIONS =
"the same widget is hand-built in several apps and should live in the library".

When a candidate ships, annotate its heading `[shipped in vX.Y.Z]`.

## Promotion bar
- **Demand:** re-implemented in 2 or more active apps. Legacy trees being retired don't count.
- **Export gap:** confirmed absent from the export barrel.
- **API source:** derived from the canonical app's variant, unioning props others genuinely need.
  Anti-pattern variants are the thing being replaced, never the API base.
- **Shape:** a reusable widget becomes a component; an app-level composition becomes a pattern doc.

## Entry format

```
## YYYY-MM-DD: <proposed component name>

**Demand:** <project:count, project:count>
**Export gap:** confirmed absent, `src/index.ts:LL`
**Canonical implementer (API base):** `<canonical app path>:LL-LL`
**Other variants:** `<project:path>`, `<project:path>` (flag the anti-pattern variant being replaced)
**Proposed API:** <props; note token usage>
**Recommendation:** promote-as-component | codify-as-pattern (`NN-doc.md`)
```

---

<!-- Entries below, newest at the bottom -->
