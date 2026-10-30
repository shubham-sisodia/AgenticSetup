# Upgrading <LIB>: what changed, what to check, what to refactor

The one place a consumer project (or its advisor) reads before bumping `<LIB>`. Newest release first.
Every entry answers four questions:

1. **Breaks:** does my app stop compiling or installing?
2. **Behaves differently:** defaults that changed under you. Read these even when nothing breaks.
3. **Delete your workaround:** app code written around a library gap that this release closes.
   Refactor opportunities, not requirements.
4. **Verify:** what to click after upgrading.

## How to use this doc
- Find your installed version (`npm ls <LIB>`).
- Read every entry above it, top to bottom. Each is self-contained.
- Search your code for the symbols each entry names; that is the refactor surface.

**Rule for maintainers:** every PR that bumps the version adds its entry here in the same PR. An
entry with nothing under "Behaves differently" says "none".

---

## 1.4.0: empty state and table card

**Breaks:** none.

**Behaves differently**
- `DataTable` without rows now renders `EmptyState` with the default copy instead of an empty body.
  Tests that asserted zero rows by counting `tr` elements still pass; tests that asserted the empty
  body's text need the new copy.

**Delete your workaround:** local `EmptyState` and `TableCard` wrappers. Import them from `<LIB>`.

**Verify:** open one list page with no data and one with data; check the footer pagination still sits
inside the card.
