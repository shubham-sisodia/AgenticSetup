# Guide

The full reasoning behind each layer. Templates referenced here live in [`templates/`](../templates), [`hooks/`](../hooks), [`agents/`](../agents), [`skills/`](../skills) and [`prompts/`](../prompts). Longer loops have their own docs: [design-system loop](design-system-loop.md), [build loop](build-loop.md), [Figma authoring](figma-authoring.md).

## Core principles

A rule typed in chat dies with the session; a rule that was already skipped needs a hook, not more text. Put each rule in the most durable place that fits.

| If the rule is… | Put it in | Why |
| --- | --- | --- |
| A project fact (port, active folder, env prefix, design-system package) | The repo: `docs/PROJECT_CONTEXT.md`, or `.claude/guardrails.json` | Read by the project's advisor on every call; teammates get it too |
| Something Claude already ignored once | A hook | Runs whether or not the model remembers |
| A multi-step job you typed more than twice | A skill | One command, same steps every time |
| About code shape (no native buttons, router links only) | A lint rule | Catches people and old code, not just Claude |
| A habit that holds in every repo | `~/.claude/CLAUDE.md` | Global, cheap, but advisory only |
| A check a reviewer keeps catching by hand | An agent | A specialist with a fixed checklist and an evidence rule |
| Something that must be true before a commit | The commit gate (hook + test agent) | The commit is refused until it is |
| How to build with the component library | The library's `patterns/` docs | One answer for every app, kept current by a loop |
| What the UI should look like | `DESIGN.md` at the repo root | Read by every agent like CLAUDE.md; lintable |
| Machine behavior (retention, default model, hooks, plugins) | `~/.claude/settings.json` | Set once |

The ladder, in fix order: **per-repo fact → hook → skill → lint rule → global habit → setting**. Agents and the gate are rungs too: an agent when the check needs judgement, the gate when skipping it must be impossible.

Three more rules of thumb:

- **Done means verified.** A UI change is done only when a screenshot or a passing spec shows it.
- **One session per branch or task.** Long-lived sessions get compacted, and early instructions are the first thing lost. Checkpoint, then start fresh.
- **Hooks fail open.** A bug in a hook should mean "guard didn't fire", never a blocked session.

## Global CLAUDE.md

[`templates/claude/CLAUDE.md`](../templates/claude/CLAUDE.md) → `~/.claude/CLAUDE.md`. Habits for every repo: verify first, use what exists, know the API shape, sweeps, shell, dev servers, git and releases, secrets, subagents, sessions, and the projects / advisors / commit gate block. Project facts go in each repo instead.

If you already have a global file, merge in both directions: an existing file tends to carry the project and gate rules but not the habits, and a retro can only test a rule that is actually installed.

## settings.json

[`templates/claude/settings.json`](../templates/claude/settings.json) → merge into `~/.claude/settings.json`.

| Key | Why | Taste or needed |
| --- | --- | --- |
| `cleanupPeriodDays: 365` | The default deletes transcripts after about 30 days, and retros lose their detail | Needed |
| `model` | A default stops you running `/model` every session. Use whatever string `/model` currently accepts | Taste |
| `permissions.deny` | Keeps env and registry files out of context | Needed |
| `hooks` | Wires the registry hook (`session`) and the commit gate (`gate`) | Needed for the registry and gate |
| `alwaysThinkingEnabled`, `effortLevel`, `modelSettings` | Thinking on by default, medium effort, high for the largest model | Taste |
| `enabledPlugins`, `extraKnownMarketplaces` | The two output-mode plugins ([Output modes](#output-modes)) | Taste |

## Registry and session hook

One JSON file, [`templates/claude/projects.json`](../templates/claude/projects.json) → `~/.claude/projects.json`, maps each project folder to an alias, a kind (`new`, `migration`, `library`, `workspace`), an advisor and a test agent. One script, [`hooks/projects.py`](../hooks/projects.py) → `~/.claude/hooks/projects.py`, reads it.

On `startup`, `resume`, `clear` and `compact`, `projects.py session` injects:

1. The alias list, so "fix the filter in acme" resolves without a path.
2. For the current project: invoke its advisor with the first task and the branch (and send UI questions to `uiAdvisor`, if set).
3. If it has a tester: stage separately, have the tester verify the staged diff, then commit.

How a folder is matched, in order:

1. The main repo's folder name, via `git rev-parse --git-common-dir`. Every worktree of `acme-web` resolves to `acme-web`.
2. Any ancestor folder name, for projects that are not git repos (a design workspace).

`tester: null` means no commit gate for that project. `advisor: null` means no advisor rule. Agents named here must live in `~/.claude/agents/` so they resolve from every checkout.

## Commit gate

The `gate` mode of the same script runs on every Bash call and only acts on `git commit` in a registered project with a tester.

| Situation | Result |
| --- | --- |
| `git add` or `commit -a` / `--all` inside the commit command | Denied: stage in a separate command first |
| No checklist for this exact staged diff | Denied, with the checklist path and the command that creates it |
| Any `- [ ]` left, or a file with fewer ticks than hunks | Denied: `app.ts: 0/1 hunks checked` |
| Every hunk ticked | Allowed |
| `CLAUDE_SKIP_TEST_GATE=1` in the command | Allowed: only when the user explicitly waived testing |
| Only lockfiles, snapshots or non-code files staged | Allowed |
| The hook crashes | Allowed: it exits 1 with a traceback, which Claude Code shows but does not block on |

The checklist lives at `.git/test-checklists/<sha256 of the staged diff>.md`, so it is never committed and any re-stage needs a new one. `projects.py checklist` writes the skeleton: one `- [ ]` line per hunk, grouped by file. The test agent ([`agents/test-engineer.md`](../agents/test-engineer.md)) picks the cheapest layer that proves each hunk (unit, component, Playwright, or typecheck only, said explicitly), runs it, and ticks only what passed. Example: [`templates/repo/test-checklist.md`](../templates/repo/test-checklist.md).

The agent is generic. It resolves the repo name the same way the hook does and loads `~/.claude/agent-context/test-engineer/<repo>.md` for the stack, commands, layer table and spec-first mode ([example](../templates/claude/agent-context/test-engineer/example.md)). With no file it works from the repo's own test config and says so.

## Per-repo facts

Two files in the repo, both committed:

- **`docs/PROJECT_CONTEXT.md`** ([template](../templates/repo/PROJECT_CONTEXT.md)): product, business rules, flows, architecture, data, auth, deployment, numbered open questions. Owned by the project's advisor, which reads it first on every call.
- **`.claude/guardrails.json`** ([template](../templates/repo/guardrails.json)), optional: machine-readable facts. The hooks meant to read and enforce it are proposed, not built yet (see [Hooks](#hooks)), so today it only works as text the model may or may not honour. Keep it if you want the facts in one place; don't count it as enforcement.

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

## Hooks

What runs today:

| Hook | Event | What it does |
| --- | --- | --- |
| `projects.py session` | SessionStart (`startup\|resume\|clear\|compact`) | Alias list, the project's advisor rule and test rule ([Registry](#registry-and-session-hook)) |
| `projects.py gate` | PreToolUse (Bash) | Denies `git commit` until the staged diff's checklist is complete ([Commit gate](#commit-gate)) |

Each denial tells Claude the fix, so it corrects itself in the same turn.

### Guardrails layer (proposed, not built yet)

A plugin of five scripts that would read `guardrails.json`. None of them exists yet; the wiring reference is [`templates/repo/hooks.json`](../templates/repo/hooks.json). Until they ship, the rules below live in the global CLAUDE.md as habits.

| Hook | Event | What it would do |
| --- | --- | --- |
| `session_start.py` | SessionStart | States branch and trunk, active folder, off-limits paths, env convention, design system, dev port, setup files, commands and `notes`. Loads the branch's latest checkpoint. Flags stale or very large resumed sessions. |
| `prompt_guard.py` | UserPromptSubmit | Blocks a prompt containing a token, key, password or one-time code, and explains how to pass it instead. `!allow-secret` sends a harmless test value. |
| `bash_guard.py` | PreToolUse (Bash) | Denies `sleep N; poll`, `git add -A` / `.` / `commit -a`, a second dev server or wrong port, reusing an existing tag (suggests the next free one), `gh pr create` without a version bump, and zsh quoting traps. Asks before deleting or force-pushing remote tags. |
| `edit_guard.py` | PreToolUse (Write, Edit, MultiEdit) | Denies edits to off-limits or frozen paths, new env vars with the wrong prefix, and newly added native elements where the design system has a component. Checks only added text. A `guardrails-allow-native` comment opts out one line. |
| `stop_verify.py` | Stop | If this turn edited UI files and nothing verified them, blocks the stop once and asks for verification or an explicit "not verified". Never loops. |

## Skills

What ships in [`skills/`](../skills) → `~/.claude/skills/`:

| Skill | Use when | Steps |
| --- | --- | --- |
| [`design-system-from-brief`](../skills/design-system-from-brief/SKILL.md) | New project's visual design | Brief → `DESIGN.md` → lint → one sample screen → export tokens |
| [`brief`](../skills/brief/SKILL.md) | Starting a design effort | Issue or idea → related research → `briefs/YYYY-MM-DD-slug.md` |
| [`teardown`](../skills/teardown/SKILL.md) | "How does X do Y" | One `competitor-scout` per product, in parallel → steal / avoid synthesis |
| [`critique`](../skills/critique/SKILL.md) | "Review this design" | `design-critic` per screen + `ds-advisor` consistency → systemic issues first |
| [`handoff`](../skills/handoff/SKILL.md) | "Make this buildable" | Frame → `ds-advisor` maps every region → states, edge cases, tokens, gaps → optional ticket |

The four studio skills name the issue tracker and wiki as placeholders (`<TRACKER>`, `<WIKI>`): replace them with the MCP servers you use. More skills worth writing are listed under [Maintenance cadence](#maintenance-cadence).

## Agents

A skill is a recipe you run; an agent is a specialist you hand a job to. Add one when a reviewer keeps catching the same class of problem by hand.

**Agents and skills are personal: they live in `~/.claude/agents/` and `~/.claude/skills/`, never under a project's `.claude/`.** A project-level agent failed three times with "agent type not found" from another checkout; personal copies resolve from every repo and worktree, and the registry depends on that.

| Agent | Use when | What it does |
| --- | --- | --- |
| [`ui-qa`](../agents/ui-qa.md) | Before showing any visual or interactive change; "QA this page" | Drives the live page at 1440×900 and 390×844, light/dark and reduced motion. Checks fit, overflow, tap targets, contrast, autoplay, helpers that fight the user; plays every control like an impatient user. Reports with repro steps and evidence; never edits code. Rerun mode re-verifies a previous report's ids. |
| [`design-critic`](../agents/design-critic.md) | "Critique this screen" | Nielsen's 10 heuristics + WCAG 2.2 AA, scored per screen; every finding carries evidence. Rerun mode, same table as ui-qa. |
| [`test-engineer`](../agents/test-engineer.md) | Before every commit; any test work | Fills the per-hunk checklist the gate requires ([Commit gate](#commit-gate)). |
| [`project-advisor`](../agents/project-advisor.md) | Template: one per project | Business rules, architecture, data, auth; owns `docs/PROJECT_CONTEXT.md` ([below](#one-advisor-per-project)). |
| [`ds-advisor`](../agents/ds-advisor.md) | Any question about building with the component library | Five modes; edits only its two backlogs except in codify mode ([design-system loop](design-system-loop.md)). |
| [`ux-researcher`](../agents/ux-researcher.md) | Discovery, "how do others solve X" | Primary sources, every claim cited, disagreements surfaced. |
| [`competitor-scout`](../agents/competitor-scout.md) | Teardowns | Walks a real product in a new browser tab; steal / avoid tied to screenshots. |

Why ui-qa exists: screenshots and heuristic critiques miss interaction-level bugs (a demo cursor acting while the user's own click is still running, a loop that returns to the state the user just left, a comparison that phones can no longer compare). Those only show up when something actually plays the UI.

### One advisor per project

Each registered project gets `~/.claude/agents/<alias>-advisor.md` and a `docs/PROJECT_CONTEXT.md` in the repo. The operating contract is the same in every advisor ([template](../agents/project-advisor.md)):

- **No memory.** It reads `docs/PROJECT_CONTEXT.md` first on every call, then the code.
- **Cites `file:line`.** Code wins when the docs disagree.
- **Owns the doc.** It updates PROJECT_CONTEXT.md when a rule becomes known and keeps open questions numbered.
- **Holds the boundary.** It never decides UI or component choice (that is `ds-advisor`), and `ds-advisor` never decides business rules.

A new project copies the closest sibling by kind, not a blank template:

| New project is… | Copy the advisor from | Copy the test file from |
| --- | --- | --- |
| A migration (legacy tree → new tree on the shared library) | Your most recent migration advisor | Its `agent-context/test-engineer/<folder>.md` |
| A new app on the shared library | A scaffold-stage new-app advisor, or a backend-heavy one if the backend is the hard part | A new-app test file |
| An app with a hard device or display constraint (an embedded small-display app) | The device-constrained advisor | Its own test agent, modelled on the device one, with layout as an asserted gate |
| The first project of its kind | [`agents/project-advisor.md`](../agents/project-advisor.md) | [`example.md`](../templates/claude/agent-context/test-engineer/example.md) |

Then: add the entry to `projects.json`, rewrite the copied advisor's name, description, domain and paths (keep the contract, scope and "Where things live"), and seed `docs/PROJECT_CONTEXT.md` and `docs/TESTING.md` in the repo.

## Output modes

Two machine-level plugins change the shape of every answer. They are per machine (`enabledPlugins` in `~/.claude/settings.json`), not per repo, so turn them on for how you work, not for a project.

| Plugin | What it changes | Turn it on when |
| --- | --- | --- |
| `i-have-adhd` | Answer first, numbered steps, one next action at the end | Long answers lose you; you want to act on the first line |
| `ponytail` | Laziest correct solution: question whether the task needs to exist, standard library before dependencies, one line before fifty. Adds review, audit and debt commands for over-engineering | You keep trimming generated code back down |

Both install from their GitHub marketplaces (the `extraKnownMarketplaces` block in the settings template). Read each plugin's files before enabling it, like any third-party skill.

## Session retros

Claude Code keeps your prompts (`~/.claude/history.jsonl`, prompts only but older) and transcripts (`~/.claude/projects`, full sessions) on disk; a retro reads both and tells you which rules to add. Run it monthly with [`prompts/session-retro.md`](../prompts/session-retro.md).

Where only the prompt history covers a period, active hours are estimated from prompt gaps and calibrated against days that have transcripts (in one run, prompt-gap hours had to be multiplied by 1.66). The report marks estimates "(inferred)" and adds three sections: rules that exist but were not followed, dormant projects, and security.

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


## Design studio

For design work outside a code repo, a workspace with its own [`CLAUDE.md`](../templates/studio/CLAUDE.md) runs five stages, each backed by a skill or agent: discover (`ux-researcher`), teardown (`/teardown`, `competitor-scout`), define (`/brief`), design (the design tool's MCP server, authored per [Figma authoring](figma-authoring.md)), critique and handoff (`/critique`, `/handoff`, `design-critic`, `ds-advisor`). Artifacts go to `research/ teardowns/ briefs/ critiques/ handoffs/` as `YYYY-MM-DD-slug.md`.

Three rules hold it together: a brief is the contract (no production design work without one), critiques are scored on Nielsen's heuristics and WCAG 2.2 AA, and handoffs map every region to a library component or flag a gap, delegated to `ds-advisor`, never guessed. Register the workspace in `projects.json` with `kind: workspace` and `tester: null`: it gets the alias list but no commit gate.

## Building a page with several agents

The spec → parallel builders → QA loop is in [build-loop.md](build-loop.md): a statechart table per section, the shared engine first, one builder per section on disjoint files, shared files by the main thread after, then `ui-qa` and `design-critic` against `data-state`, with a rerun table per fix round.

## Lint enforcement

A hook only stops Claude; a lint rule in CI stops everyone. [`templates/repo/eslint.config.js`](../templates/repo/eslint.config.js) uses `react/forbid-elements` with the same mapping as `designSystem.forbidElements`. For a real exception: `// eslint-disable-next-line react/forbid-elements -- reason`.

## Security checklist

- [ ] Never paste tokens, passwords or one-time codes into prompts; they land in plain text in `~/.claude/history.jsonl` and the transcript.
- [ ] Keep secrets in env vars or an untracked `.env`, and tell Claude the variable name.
- [ ] Deny reads of `.env` and `.npmrc` in settings.json.
- [ ] Test-account logins go in `.env.local`; checkpoints and notes name the account only.
- [ ] If a secret leaks: rotate first, then scrub local copies, then delete backups.
- [ ] Review any third-party skill's or plugin's files before installing.
- [ ] No prompt guard runs yet (proposed above), so the first item is on you.

## Maintenance cadence

| When | Do | Signal it's working |
| --- | --- | --- |
| Every session | Start fresh per branch; checkpoint before stopping | No "where were we?" prompts |
| Every new repo | Add it to `projects.json`, copy the sibling advisor, seed `docs/PROJECT_CONTEXT.md`, add the test-agent context file and the lint rule | Session start names the project and its advisor; a commit without a checklist is denied |
| Every new project's UI | Brief → DESIGN.md → lint → one test screen → export | Components named in prompts exist in code |
| Every library release | `UPGRADING.md` entry in the same PR; codify pass when 3 or more gaps are pending | Consumers bump without surprises |
| Monthly | Run a retro; turn each repeated correction into config, a hook, a skill or a lint rule | The same correction doesn't appear twice |
| Quarterly | Re-check the skill stack; remove overlaps | Five or fewer design skills installed |

A retro can only test a rule that is actually installed: before blaming a rule for not working, check that the template line reached `~/.claude/CLAUDE.md` (or the hook reached settings). If a theme doesn't drop after a month, its guard isn't firing.

### Skills worth writing next (proposed, not built yet)

None of these exists as a `SKILL.md` yet; the steps are written, so each is a short file away.

| Skill | Use when | Steps |
| --- | --- | --- |
| `init` | Setting up a new repo | Detect package manager, dev port, trunk, folders, env prefixes, design system, setup files, commands, release setup → confirm in one table → write `.claude/guardrails.json` |
| `ship [dev\|prod\|release]` | "Ship it", "cut a tag" | Verify the fix → stage explicit paths → lint, test, verify → version bump if releasing → conventional commit → build → next free tag in the repo's scheme → push → `gh run watch` in background |
| `verify-ui [route]` | After any visual change; "I don't see it" | Reuse the dev server and open tab → confirm a dependency fix actually loaded → check the real API response → headless Playwright at the target viewport → read the screenshot → report evidence or "not verified" |
| `checkpoint [note]` | Before a restart, break or compaction | Update `.claude/checkpoints/<branch>.md` ([template](../templates/repo/checkpoint.md)). Under 60 lines, no secrets |
| `sweep <change>` | "Everywhere", "you missed one" | Define old vs new → inventory with several search patterns → confirm → apply in batches → re-search to prove zero left → test and spot-check |
| `devup` | New worktree or clone; app won't start | Copy `.env`/`.npmrc` from the main checkout → install → reuse or start the server on `devPort` → `wait-on` (not sleep) → confirm it answers |
