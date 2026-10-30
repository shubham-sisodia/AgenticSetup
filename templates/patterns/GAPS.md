# <LIB> patterns: gaps log

Append-only log of questions the pattern docs could not answer, or answered wrongly, when the
design-system advisor was consulted. It is also the fallback-recipe library: an entry that says how to
build a missing component from primitives is the tier-2 answer the advisor reuses in design plans.

When a gap is codified, annotate its heading `[codified in NN-doc.md, YYYY-MM-DD]` so this file stays a
live backlog, not a graveyard. Entries with `Source consulted: none, unsolved` are the most valuable:
the docs are silent and no project has solved it either.

## Entry format

```
## YYYY-MM-DD: <short topic, 3-6 words>

**Type:** doc-bug | pattern-gap
**Project:** <project> (`<LIB>` <pinned version>)
**Question:** <one line>
**Patterns doc that should cover this:** `NN-doc.md` §section, or `missing entirely`
**Source consulted:** `<path>:LL`, or `none, unsolved`
**Suggested codified pattern:** <one line of what the doc should add>
**Contradicts consumer docs:** `<project>/CLAUDE.md:LL` "<quoted claim>", or `none`
```

`doc-bug` = a numbered doc states something false (a phantom export, a wrong prop); these jump the
codify queue. `pattern-gap` = the docs are silent.

---

<!-- Entries below, newest at the bottom -->

## 2026-01-14: Segmented view toggle [codified in 13-components-reference.md, 2026-02-02]

**Type:** pattern-gap
**Project:** acme-web (`<LIB>` 1.6.4)
**Question:** Is there a segmented control for a two-way view switch (board vs table)?
**Patterns doc that should cover this:** `13-components-reference.md`, missing entirely
**Source consulted:** `acme-web/src/pages/board/ViewToggle.tsx:1-30` (icon-only Tabs bound to `?view=`)
**Suggested codified pattern:** icon-only tab triggers bound to a `?view=` URL param; no native toggle group exists in 1.6.x.
**Contradicts consumer docs:** none
