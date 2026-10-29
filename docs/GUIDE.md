# Guide

The full reasoning behind each layer. Templates referenced here live in [`templates/`](../templates), [`skills/`](../skills) and [`prompts/`](../prompts).

## Core principles

A rule typed in chat dies with the session; a rule that was already skipped needs a hook, not more text. Put each rule in the most durable place that fits.

| If the rule is… | Put it in | Why |
| --- | --- | --- |
| A project fact (port, active folder, env prefix, design-system package) | `.claude/guardrails.json` in the repo | Stated at every session start and enforced by hooks; teammates get it too |
| Something Claude already ignored once | A hook | Runs whether or not the model remembers |
| A multi-step job you typed more than twice | A skill | One command, same steps every time |
| About code shape (no native buttons, router links only) | A lint rule | Catches people and old code, not just Claude |
| What the UI should look like | `DESIGN.md` at the repo root | Read by every agent like CLAUDE.md; lintable |
| A habit that holds in every repo | `~/.claude/CLAUDE.md` | Global, cheap, but advisory only |
| Machine behavior (retention, default model) | `~/.claude/settings.json` | Set once |

Three more rules of thumb:

- **Done means verified.** A UI change is done only when a screenshot or a passing spec shows it.
- **One session per branch or task.** Long-lived sessions get compacted, and early instructions are the first thing lost. Checkpoint, then start fresh.
- **Hooks fail open.** A bug in a hook should mean "guard didn't fire", never a blocked session.

## Global CLAUDE.md

[`templates/claude/CLAUDE.md`](../templates/claude/CLAUDE.md) → `~/.claude/CLAUDE.md`. Habits for every repo: verify first, use what exists, know the API shape, sweeps, shell, dev servers, git and releases, secrets, subagents, sessions. Project facts go in each repo's guardrails.json instead.

## settings.json

[`templates/claude/settings.json`](../templates/claude/settings.json) → merge into `~/.claude/settings.json`.

- `cleanupPeriodDays: 365` matters most: the default deletes transcripts after about 30 days, and retros lose their detail.
- `model`: a default stops you running `/model` every session.
- `GH_HOST`: change it only if you use a GitHub Enterprise host.
- `permissions.deny`: keeps env and registry files out of context.

## Per-repo `.claude/guardrails.json`

[`templates/repo/guardrails.json`](../templates/repo/guardrails.json). One small file per repo; every value replaces a correction you'd otherwise type again. Keep only the keys that apply, and commit it.

| Key | Stops |
| --- | --- |
| `devPort` | A second dev server, or the wrong port |
| `activePaths`, `pathRules`, `frozenPaths` | Edits in the wrong folder for the current branch |
| `envPrefixes` | `VITE_` vs `REACT_APP_` mix-ups, `process.env` in a Vite tree |
| `designSystem` | Hand-rolled native elements where a component exists |
| `setup.copyFromMain` | Worktrees that won't start because `.env` is missing |
| `verifyCommand`, `uiGlobs` | "Done" on unverified UI changes |
| `release` | PRs to a published package without a version bump |
| `notes` | One-line project facts you keep repeating |

Every rule can be switched off under a `rules` key (for example `"rules": { "designSystem": false }`). Only published packages need `release`.

## Hooks

Wiring: [`templates/repo/hooks.json`](../templates/repo/hooks.json). Each denial tells Claude the fix, so it corrects itself in the same turn.

| Hook | Event | What it does |
| --- | --- | --- |
| `session_start.py` | SessionStart | States branch and trunk, active folder, off-limits paths, env convention, design system, dev port, setup files, commands and `notes`. Loads the branch's latest checkpoint. Flags stale or very large resumed sessions. Runs on start, resume, clear and compaction. |
| `prompt_guard.py` | UserPromptSubmit | Blocks a prompt containing a token, key, password or one-time code, and explains how to pass it instead. `!allow-secret` sends a harmless test value. |
| `bash_guard.py` | PreToolUse (Bash) | Denies `sleep N; poll`, `git add -A` / `.` / `commit -a`, a second dev server or wrong port, reusing an existing tag (suggests the next free one), `gh pr create` without a version bump, and zsh quoting traps. Asks before deleting or force-pushing remote tags. |
| `edit_guard.py` | PreToolUse (Write, Edit, MultiEdit) | Denies edits to off-limits or frozen paths, new env vars with the wrong prefix, and newly added native elements where the design system has a component. Checks only added text. A `guardrails-allow-native` comment opts out one line. |
| `stop_verify.py` | Stop | If this turn edited UI files and nothing verified them, blocks the stop once and asks for verification or an explicit "not verified". Never loops. |

## Skills

| Skill | Use when | Steps |
| --- | --- | --- |
| `init` | Setting up a new repo | Detect package manager, dev port, trunk, folders, env prefixes, design system, setup files, commands, release setup → confirm in one table → write `.claude/guardrails.json` |
| `ship [dev\|prod\|release]` | "Ship it", "cut a tag" | Verify the fix → stage explicit paths → lint, test, verify → version bump if releasing → conventional commit → build → next free tag in the repo's scheme → push → `gh run watch` in background |
| `verify-ui [route]` | After any visual change; "I don't see it" | Reuse the dev server and open tab → confirm a dependency fix actually loaded → check the real API response → headless Playwright at the target viewport → read the screenshot → report evidence or "not verified" |
| `checkpoint [note]` | Before a restart, break or compaction | Update `.claude/checkpoints/<branch>.md` ([template](../templates/repo/checkpoint.md)). Under 60 lines, no secrets. Next session loads it |
| `sweep <change>` | "Everywhere", "you missed one" | Define old vs new → inventory with several search patterns → confirm → apply in batches → re-search to prove zero left → test and spot-check |
| `devup` | New worktree or clone; app won't start | Copy `.env`/`.npmrc` from the main checkout → install → reuse or start the server on `devPort` → `wait-on` (not sleep) → confirm it answers |
| [`design-system-from-brief`](../skills/design-system-from-brief/SKILL.md) | New project's visual design | Brief → `DESIGN.md` → lint → one sample screen → export tokens |

## Agents

A skill is a recipe you run; an agent is a specialist you hand a job to. Add one when a reviewer keeps
catching the same class of problem by hand.

| Agent | Use when | What it does |
| --- | --- | --- |
| [`ui-qa`](../agents/ui-qa.md) | Before showing any visual or interactive change; "QA this page" | Drives the live page in Chrome at 1440×900 and 390×844, light/dark and reduced motion. Checks fit, overflow, tap targets, contrast, tabs that land off-screen, autoplay, and helpers (tours, carousels) that fight the user. Plays every control like an impatient user (rapid clicks, mid-flight switches, scroll away and back). Reports findings with repro steps and screenshots; never edits code. |

Why it exists: screenshots and heuristic critiques miss interaction-level bugs (a demo cursor acting
while the user's own click is still running, a loop that returns to the state the user just left, a
comparison that phones can no longer compare). Those only show up when something actually plays the UI.

## Session retros

Claude Code keeps your prompts (`~/.claude/history.jsonl`) and transcripts (`~/.claude/projects`) on disk; a retro reads them and tells you which rules to add. Run it monthly. No-plugin version: [`prompts/session-retro.md`](../prompts/session-retro.md).

If secrets turn up: rotate first, then scrub local copies, then delete any backups the scrubber made.

## Design

Don't lock into one design system: generate one per project from a short brief, validate it on one screen, then sync it to code. Keep the installed skill stack small, because overlapping design skills fight each other.

### Workflow

1. **Write a brief** ([template](../templates/design/brief.md)). Same shape every time.
2. **Generate `DESIGN.md`** with the [design-system-from-brief](../skills/design-system-from-brief/SKILL.md) skill (or in Claude Design, then save as DESIGN.md).
3. **Lint it:** `npx -y @google/design.md lint DESIGN.md` (structure + WCAG contrast).
4. **Validate with one real screen** (a dense one, if the product is dense). Tweak, then use it for the full project.
5. **Sync to code:** export Tailwind or DTCG tokens with the same CLI, or `/design-sync` in Claude Code.
6. **Day to day:** small steps, name components in prompts, ask for a review pass (accessibility, contrast, hierarchy, usability).

### The one repo to adopt: DESIGN.md

[google-labs-code/design.md](https://github.com/google-labs-code/design.md) is Google's open spec (Apache-2.0): YAML tokens plus prose rationale in one root file that Claude Code, Cursor and Codex read like CLAUDE.md. The CLI lints, diffs (`diff DESIGN.md DESIGN-v2.md`) and exports (`--format tailwind`, `--format dtcg`). It turns the brief-to-design-system step into a file you can check, which is the same "rules live in files, not chat" idea as the guardrails. [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) supplies ready DESIGN.md seeds.

### Recommended skills (October 2026; star counts move daily)

| Skill | Category | What it does | Pick it if |
| --- | --- | --- | --- |
| frontend-design (Anthropic) | UI baseline | Steers UI away from generic AI defaults | Always; built in |
| ui-ux-pro-max | UI/UX | Design rules, palettes, fonts, UX checks; the most popular community design skill | You want one broad all-rounder |
| Impeccable (Paul Bakaus) | UI taste | Opinionated, consistent polish pass | Product UI; the default taste pick |
| taste-skill | UI taste | Style variants: minimalist, brutalist, soft, redesign, image-to-code | You want to choose a direction explicitly |
| [Hallmark](https://github.com/Nutlope/hallmark) | UI taste | Anti-AI-slop rule set; `audit`, `redesign`, `study <screenshot or URL>`; avoids repeating layouts | Marketing pages where variety matters |
| web-design-guidelines (Vercel) | UX review | Audits code against Vercel's interface guidelines | Final review pass |
| interface-design | Design memory | Persists design decisions across sessions | You generate per-project systems |
| [ux-ui-agent-skills](https://github.com/plugin87/ux-ui-agent-skills) | Design systems | DTCG tokens, 52 components, WCAG 2.2, quality gates | You want rigorous, enforceable systems |
| Emil Kowalski's skills | UI motion | Refined interaction motion (creator of Sonner, Vaul) | Micro-interaction feel |
| motion-dev-animations-skill | UI motion | Motion.dev (Framer Motion's successor) animations | React + Motion apps |
| [gsap-skills](https://github.com/greensock/gsap-skills) | UI motion | Official GSAP skills: core, timeline, ScrollTrigger, React, performance | Projects using GSAP |
| [web-animation-skills](https://github.com/iart-ai/web-animation-skills) | UI motion | GSAP, SVG, Lottie, transitions; graceful reduced motion | Broad web animation coverage |
| [motion-graphics-skills](https://github.com/charlie947/motion-graphics-skills) | Video | Animation as code, renders MP4, keeps a MOTION.md | Short animated videos |
| claude-remotion-skill | Video | Springs, choreography, captions, sound with Remotion | Rendering video with Remotion |

**Suggested stack (five, no overlaps):**

1. frontend-design (built in)
2. interface-design, so per-project systems persist
3. One taste skill: **Impeccable** (or taste-skill / Hallmark, not more than one)
4. One UI motion skill: Emil Kowalski's or motion-dev; gsap-skills if the project uses GSAP
5. web-design-guidelines as the final review pass

Add a video skill only for video work. Third-party skills can run commands: read each SKILL.md before installing.

### Component registries via the shadcn MCP server

Skills teach Claude how to design; a registry gives it finished components. Set up per project, not globally:

1. Add the shadcn MCP server: `pnpm dlx shadcn@latest mcp init --client claude`, or copy [`templates/design/mcp.json`](../templates/design/mcp.json) to `.mcp.json`.
2. Add registries to `components.json` ([example](../templates/design/components.registries.json)).
3. Restart Claude Code, run `/mcp`; `shadcn` should show Connected.
4. Prompt by registry: "Add a background effect from @react-bits to the hero".

| Registry | What | Notes |
| --- | --- | --- |
| [React Bits](https://reactbits.dev/get-started/mcp) | Free animated React components | Start here for marketing pages |
| [Canvas UI](https://github.com/DavidHDev/canvas-ui) | WebGL effects over your live DOM | MIT + Commons Clause (check before commercial use); full effect needs a Chrome flag, others get a fallback |
| Magic UI | Animated components | Check its docs for current registry setup |

Use registries for landing pages, portfolios and demos; skip them for dense product UI and repos with their own design system (that wins). Installed components land as source: review them, check `prefers-reduced-motion`, and verify visually. Private registry tokens go in `.env.local` as `${REGISTRY_TOKEN}`, never pasted.

### Shader effects (Shaders MCP, paid)

[Shaders MCP](https://shaders.com/docs/guide/mcp) installs and customizes WebGPU shader effects and needs a Shaders Pro account. Add with OAuth (avoid API keys typed into commands):

```bash
claude mcp add --transport http shaders https://shaders.com/mcp
```

Before shipping a shader: check a static fallback without WebGPU, watch GPU/battery cost and pause off-screen effects, respect `prefers-reduced-motion`, and look at a screenshot. Start with React Bits; reach for Shaders when you need true GPU effects and the project justifies the subscription.

### Looked at, not adopted

- [nexu-io/open-design](https://github.com/nexu-io/open-design): a whole local-first alternative to Claude Design; replaces rather than joins this stack.
- [oso95/scroll-world](https://github.com/oso95/scroll-world): scroll-driven video "fly-through" landing pages; needs a paid rendering backend; keep for a one-off showcase.

## Lint enforcement

The edit hook only stops Claude; a lint rule in CI stops everyone. [`templates/repo/eslint.config.js`](../templates/repo/eslint.config.js) uses `react/forbid-elements` with the same mapping as `designSystem.forbidElements`. For a real exception: `// eslint-disable-next-line react/forbid-elements -- reason` plus a `guardrails-allow-native` comment.

## Security checklist

- [ ] Never paste tokens, passwords or one-time codes into prompts; they land in plain text in `~/.claude/history.jsonl` and the transcript.
- [ ] Keep secrets in env vars or an untracked `.env`, and tell Claude the variable name.
- [ ] Keep the prompt guard on.
- [ ] Deny reads of `.env` and `.npmrc` in settings.json.
- [ ] Test-account logins go in `.env.local`; checkpoints and notes name the account only.
- [ ] If a secret leaks: rotate first, then scrub local copies, then delete backups.
- [ ] Review any third-party skill's SKILL.md and scripts before installing.

## Maintenance cadence

| When | Do | Signal it's working |
| --- | --- | --- |
| Every session | Start fresh per branch; checkpoint before stopping | No "where were we?" prompts |
| Every new repo | Write guardrails.json, commit it, add the lint rule | Session start lists the repo's facts |
| Every new project's UI | Brief → DESIGN.md → lint → one test screen → export | Components named in prompts exist in code |
| Monthly | Run a retro; turn each repeated correction into config, a hook, a skill or a lint rule | The same correction doesn't appear twice |
| Quarterly | Re-check the skill stack; remove overlaps | Five or fewer design skills installed |

If a theme doesn't drop after a month, its guard isn't firing: check that repo's guardrails.json first.
