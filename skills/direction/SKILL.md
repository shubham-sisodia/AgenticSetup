---
name: direction
description: Pick a design direction before building, so only one design gets built. Locks the owner's taste in writing, sketches 6–8 throwaway directions at the same fidelity on one comparison page, has the owner pick or mix one, proves the riskiest part in the real stack, then hands a locked spec to the build loop. Use when starting a new page, section, hero, experiment or redesign, or when the user says "direction", "concepts", "explore options", "what should this look like" or "not jaw dropping enough".
---

# /direction: decide once, build once

Input: `$ARGUMENTS`, what is being designed (a page, section or hero) and optionally a brief path.

Why: rounds of rework come from three things: taste that was never written down, motion judged from stills,
and full builds used as sketches. Each step below removes one. Steps 1–5 take about half a day; skipping them
usually costs two or three full builds.

## 1. Taste lock (15 min, the owner answers)
Create `docs/direction/<YYYY-MM-DD>-<slug>.md` (or `briefs/` in a studio repo) from the template below and ask
the owner for the empty fields in one round:
- **3 loves and 2 hates:** real URLs or screenshots, each with one line on *exactly* what (the type, the scroll,
  the colour, the way it loads), not "the vibe".
- **The one memorable thing** this design should be remembered for.
- **The test:** what "good" means as something observable ("a visitor stops scrolling within 3 s", "reads as a
  painting at phone size", "the demo works without instructions"). This becomes the acceptance criterion.
- **Constraints:** stack, devices, budgets (size, frame time), reduced motion, content that must appear.

If the owner says "pick for me", propose each field and get a yes. Don't sketch without the loves, hates and
test; they are what makes the pick fast.

## 2. Go wide, cheap (about an hour of agent time)
Six to eight directions that differ on named axes (layout, type, colour, motion, interaction idea), not six
shades of one idea. For each: a name, one sentence, and which love it borrows from.
- One subagent per direction, in parallel, each writing only its own file:
  `docs/direction/<slug>/<n>-<name>.html`, a single self-contained HTML file (inline CSS/JS, CDN libraries only
  if the idea needs them, no project code, no build step).
- Same fidelity for all: one screen, real copy from the brief, desktop and phone width. Anything that moves gets
  a loop of 10 seconds or less, or one interaction. Light and dark only if the project ships both.
- Time box: about 15 minutes each. A sketch that needs more is a sign the idea is too complex for the brief.

## 3. Comparison page, then pick (10 min, the owner decides)
1. Screenshot every sketch at desktop and phone width and look at them yourself first; regenerate any that is
   broken or clearly below the others' fidelity.
2. Build `docs/direction/<slug>/index.html`: all directions side by side (live iframes, name, one sentence, the
   love it borrows from, and the test as a checkbox). Publish it as a private Artifact if that tool exists, else
   open it locally.
3. The owner picks one, or mixes ("A's type with C's motion"). Record the pick, why, and what was rejected and
   why in the direction doc.
4. If nothing passes the test: first fix the taste lock (a missing love or hate is the usual cause), then one more
   round changing only the axis that failed. Two rounds maximum, then talk.

## 4. Prove the riskiest part (1–2 h)
Name the one thing most likely to fail in the real build (a shader, physics, scroll choreography, phone
performance, a data dependency). Build only that, at full fidelity, in the real stack, in isolation. Check it
at phone width with 4× CPU throttle and with reduced motion. If it fails, go back to step 3 with the runner-up.

## 5. Hand off a locked spec
Write the build spec (the build loop's `docs/<PAGE>-SCRIPT.md`) with the chosen sketch's screenshots as the
visual reference, the test as acceptance criteria, and the spike's findings. From here, follow the build loop.
New ideas during the build go under `## Later` in the direction doc (a v2), not into this build.

## Rules
- Sketches are throwaway: never imported, copied into, or refactored into product code.
- Nothing in the real codebase is built before step 3's pick, except step 4's spike.
- Reply after each step with what the owner needs to do next, in one line.

## Direction doc template
```markdown
# Direction: <name>
Date · brief: <path> · status: taste lock / sketching / picked / spec written

## Taste lock
| Love | What exactly |
| --- | --- |
| <url> | <one line> |
| Hate | What exactly |
| <url> | <one line> |

Memorable thing: <one line>
Test: <observable pass criterion>
Constraints: <stack, devices, budgets, reduced motion, required content>

## Directions
| # | Name | Idea | Borrows from |
| --- | --- | --- | --- |

## Pick
Chosen: <# or mix> · why: <one line> · rejected: <# and why, one line each>

## Spike
Riskiest part: <what> · result on phone / throttled / reduced motion: <numbers>

## Later
- <ideas for v2>
```
