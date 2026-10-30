# <Page> script

Build-from document. Builders read only this file, the engine contract (§4) and their own section.
Brief: `docs/brief.md`. QA reports land in `docs/qa/`.

## 1. The concept
One paragraph: what the page is, and the one idea every section serves.

## 2. Section order
| # | Section | Kept / merged / new / cut | Why |
| --- | --- | --- | --- |
| 1 | <name> | new | <one line> |

## 3. Sections

Conventions for every table: `after N` is a timed transition that starts on entering the state and is
cancelled on leaving it. Events are tagged `by: visitor | presenter | system`. "Ignored" means the
event is listed with no transition, so a double press is a no-op by construction. Every section root
carries `data-state` and `data-owner` for QA.

### 3.1 <Section name>

**Beat.** One line: what the visitor should feel or learn.

**Copy.** Headline, lede, muted line, exactly as shipped.

**Quirk.** What the visitor can do, in plain words.

**Machine `<id>`.** Context `{ <fields and initial values> }`.

| State | Renders | Events | Timed |
| --- | --- | --- | --- |
| `idle` | <what is on screen> | `PRESS` → `working` (action: <context change>) | |
| `working` | <...> | `PRESS` ignored | `after 600` → `done` |
| `done` | <...> | `RESET` → `idle` | |

**Edge states.** Double input, scroll away and back (`OUT_OF_VIEW`), hidden tab (`HIDDEN`), reload.

**Presenter plan.** Which events the tour may send, in which states, how many runs per visit, and that
it stops the moment the visitor acts.

**Mobile (390).** What changes: layout, sizes, what moves where.

**Reduced motion.** What still happens (semantic waits stay) and what is dropped (tweens).

**Chunk.** Initial or lazy, its size budget, and its fixed placeholder height per breakpoint.

## 4. Engine contract
The shared code every section builds on: the hook's signature, timer semantics, ownership, the
registry, the `data-state` bind. Number each guarantee so builders and tests can cite it.

## 5. Budget
| Piece | Chunk | ~KB gz | Adds | What it buys |
| --- | --- | --- | --- | --- |

## 6. Build order
| Step | Work | Depends on | Parallel? |
| --- | --- | --- | --- |
| 1 | Engine, state chip, a Playwright helper that reads `data-state` | none | no: everyone builds on it |
| 2a | Section 1 | 1 | yes |
| 2b | Section 2 | 1 | yes |
| 3 | Shared files (layout, header, routes), by the main thread | 2 | no |
| 4 | Passes: phone widths, reduced motion, keyboard, axe, UI QA against `data-state` | everything | last |

## 7. Open questions for the owner
Numbered. Record answers below with the date, and fold them into the sections above.
