# The build loop: spec, parallel builders, QA

How a multi-section UI gets built by several agents at once without them stepping on each other: one
spec everyone builds from, one shared engine built first, one builder per section on disjoint files,
then reporters that check the result against the spec and a rerun table that tracks the fixes.

Template: [`templates/repo/section-spec.md`](../templates/repo/section-spec.md).

## 1. The spec is the contract

One build-from document (`docs/<PAGE>-SCRIPT.md`) that every builder reads. Per section it fixes:

| Field | Why it is in the spec |
| --- | --- |
| Beat and copy | Builders don't write copy; the copy ships as written |
| Statechart table: state, renders, events, timed transitions | Double input, mid-flight switches and timers become table rows, not `setTimeout` races |
| Edge states | Scroll away and back, hidden tab, reload: decided once, not per builder |
| Presenter plan | What an automated tour may do, and that it yields to the visitor |
| Mobile and reduced motion | Decided in the spec, so phones aren't an afterthought |
| Chunk and placeholder height | Lazy sections can't shift the layout on load |

Every section root carries `data-state` and `data-owner`. QA asserts those attributes instead of
inferring state from text, which is what makes the reports reproducible.

## 2. Build order

| Step | Who | Rule |
| --- | --- | --- |
| 1. Shared engine (the state hook, timers, ownership, registry, `data-state` bind) and its tests | One builder, sequential | Everyone builds on it, so it lands first with a unit test per contract point |
| 2. One builder per section | Parallel subagents | Each owns its section's files only; the spec names them |
| 3. Shared files (layout, header, routes, the page that mounts the sections) | The main thread, after the builders finish | No two agents ever write the same file |
| 4. Passes: phone widths, reduced motion, keyboard, axe, layout shift, then UI QA and a critique | Reporter agents | They report; they never edit |
| 5. Fix rounds | The main thread (or builders, one per finding cluster) | Then a rerun, below |

The fan-out rules are the global template's *Subagents* block ([`templates/claude/CLAUDE.md`](../templates/claude/CLAUDE.md)):
each parallel subagent gets its own files, shared files are edited by the main thread afterwards, and
rate-limited tools are called once from the main thread with results saved to disk.

## 3. Reporters

| Agent | Checks | Rubric |
| --- | --- | --- |
| [`ui-qa`](../agents/ui-qa.md) | The live page, played like an impatient user at desktop and phone sizes | The spec's own rules first: what may autoplay, run caps, budgets |
| [`design-critic`](../agents/design-critic.md) | The same page as a design | Nielsen's 10 heuristics, WCAG 2.2 AA, hierarchy, consistency with the design system |

Both follow "evidence or it didn't happen": every finding has repro steps and a screenshot or a
measured number. Reports go to `docs/qa/YYYY-MM-DD-<slug>.md` with numbered ids (`QA-01`, `F1`) so fix
rounds can cite them.

## 4. Fix rounds and the rerun table

After fixes, run the reporter again in rerun mode with the previous report. It re-verifies every id
first, then runs the full battery again for regressions:

| ID | Was | Status | Evidence (this run) |
| --- | --- | --- | --- |
| QA-01 tour scrolls the page | Major | **Fixed** | 0 page scrolls over 60 s with the tour on; `scrollY` unchanged. `$QA/noscroll.json` |
| QA-04 identical demos back to back | Major | **Still failing** (one section) | 5 identical runs in 100 s idle in section 3; cause and one-line fix |
| QA-07 hero demo | Minor | **Not applicable**: owner accepted | Verified it runs once per visit |

Then a summary count per status, and new findings with fresh ids. Statuses are only these three, so
nothing is "mostly fixed". An owner decision that accepts a finding is recorded in the spec, so the
next run judges against it.

## 5. What it produced

One page, built this way over three days: a spec with a statechart per section, one engine step, a
builder per section, and six QA and critique reports in `docs/qa/` (a first pass, a rerun, a third
pass, then a critique, a QA pass and a spacing audit of the next version).
