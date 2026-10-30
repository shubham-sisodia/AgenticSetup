# AgenticSetup

A reusable setup for AI-assisted development with Claude Code: where each rule should live, copy-ready templates, a project registry with a commit gate that actually runs, and a curated UI/UX/motion skill stack.

One setup, one ladder. Each rule goes on the most durable rung that fits, in this fix order:

1. **Per-repo fact** in `docs/PROJECT_CONTEXT.md` (and optionally `.claude/guardrails.json`)
2. **Hook** for anything Claude already ignored once: the registry hook and the commit gate in [`hooks/projects.py`](hooks/projects.py)
3. **Skill** for a multi-step job you'd otherwise retype
4. **Lint rule** for code shape, so it catches people too
5. **Global habit** in `~/.claude/CLAUDE.md`
6. **Setting** in `~/.claude/settings.json`

Agents and gates sit beside the ladder: an **agent** when a check needs judgement (an advisor per project, a test agent, UI QA, a design critic), a **gate** when skipping the check must be impossible. Plus a `DESIGN.md` per project for how the UI should look, and a monthly retro that tells you which rung to tighten next.

What runs today: the registry hook (session start) and the commit gate. The guardrails hooks and six workflow skills described in the guide are **proposed, not built yet**, and are labelled that way.

## Setup (about an hour, once)

- [ ] 1. Merge [`templates/claude/settings.json`](templates/claude/settings.json) into `~/.claude/settings.json` (keeps transcripts for a year, denies `.env` reads, wires the two hooks; thinking, effort and plugin lines are taste).
- [ ] 2. Copy [`templates/claude/CLAUDE.md`](templates/claude/CLAUDE.md) to `~/.claude/CLAUDE.md`. Trim what you don't need; if you already have one, merge both ways.
- [ ] 3. Copy [`hooks/projects.py`](hooks/projects.py) to `~/.claude/hooks/` and [`templates/claude/projects.json`](templates/claude/projects.json) to `~/.claude/projects.json`; replace the example entries with your projects.
- [ ] 4. Copy the agents you want from [`agents/`](agents) to `~/.claude/agents/`: at least `test-engineer` and `ui-qa`. Agents and skills are personal: never put them under a project's `.claude/`.
- [ ] 5. For each repo: add it to `projects.json`, write `docs/PROJECT_CONTEXT.md` from [the template](templates/repo/PROJECT_CONTEXT.md), copy [`agents/project-advisor.md`](agents/project-advisor.md) (or the closest sibling) to `~/.claude/agents/<alias>-advisor.md`, and add `~/.claude/agent-context/test-engineer/<folder>.md` from [the example](templates/claude/agent-context/test-engineer/example.md). `.claude/guardrails.json` is optional, a facts file until its hooks ship.
- [ ] 6. If the repo has a design system, add the matching lint rule ([`templates/repo/eslint.config.js`](templates/repo/eslint.config.js)).
- [ ] 7. Copy the skills from [`skills/`](skills) to `~/.claude/skills/`; fill the `<TRACKER>` placeholders in the four studio skills.
- [ ] 8. For each new project's UI: fill [`templates/design/brief.md`](templates/design/brief.md), generate and lint a `DESIGN.md`.
- [ ] 9. Install a small design skill stack (max five; see the guide).
- [ ] 10. Check it runs: start a session in a registered repo (the alias line and the advisor rule appear), stage a change and ask for a commit (the gate denies it until the checklist is ticked).
- [ ] 11. Run a session retro now as a baseline ([`prompts/session-retro.md`](prompts/session-retro.md)), then monthly.

## Where rules go

| If the rule is… | Put it in |
| --- | --- |
| A project fact (port, active folder, env prefix, design-system package) | `docs/PROJECT_CONTEXT.md`, or `.claude/guardrails.json` |
| A business rule, or "where does this change go" | The project's advisor, which owns `docs/PROJECT_CONTEXT.md` |
| Something Claude already ignored once | A hook |
| Something that must be true before a commit | The commit gate: `projects.py gate` + `test-engineer` |
| A multi-step job you typed more than twice | A skill |
| About code shape (no native buttons, router links only) | A lint rule |
| How to build with the component library | The library's `patterns/` docs, answered by `ds-advisor` |
| What the UI should look like | `DESIGN.md` |
| A habit for every repo | `~/.claude/CLAUDE.md` |
| A check a reviewer keeps catching by hand (timing, autoplay, mobile dead ends) | An agent, e.g. `agents/ui-qa.md` |
| Machine behavior | `~/.claude/settings.json` |

## Layout

```
README.md                                         this file
docs/GUIDE.md                                     full guide: ladder, registry, gate, hooks, skills, agents, output modes, retros, design, cadence
docs/design-system-loop.md                        library patterns, advisor modes, GAPS / PROMOTIONS / UPGRADING, codify pass
docs/build-loop.md                                spec -> parallel builders -> QA -> rerun table
docs/figma-authoring.md                           authoring Figma files so an agent rebuilds a screen in one pass
hooks/projects.py                                 registry hook: session, gate, checklist  -> ~/.claude/hooks/
agents/test-engineer.md                           generic test agent that fills the commit checklist -> ~/.claude/agents/
agents/project-advisor.md                         advisor template, <PROJECT> placeholders  -> ~/.claude/agents/<alias>-advisor.md
agents/ds-advisor.md                              design-system advisor template, five modes -> ~/.claude/agents/
agents/ui-qa.md                                   browser QA that plays the UI like an impatient user; rerun mode
agents/design-critic.md                           Nielsen + WCAG 2.2 AA critique with evidence; rerun mode
agents/ux-researcher.md                           cited discovery research
agents/competitor-scout.md                        browser teardowns of competitor flows
skills/design-system-from-brief/SKILL.md          brief -> DESIGN.md -> lint -> export
skills/brief/SKILL.md                             issue or idea -> design brief
skills/teardown/SKILL.md                          parallel competitor teardowns
skills/critique/SKILL.md                          rubric critique per screen, systemic issues first
skills/handoff/SKILL.md                           frame -> component mapping, states, edge cases, ticket
templates/claude/CLAUDE.md                        global rules        -> ~/.claude/CLAUDE.md
templates/claude/settings.json                    machine settings + hook wiring -> ~/.claude/settings.json
templates/claude/projects.json                    project registry    -> ~/.claude/projects.json
templates/claude/agent-context/test-engineer/example.md  per-repo test instructions -> ~/.claude/agent-context/test-engineer/<folder>.md
templates/repo/PROJECT_CONTEXT.md                 the advisor's record -> <repo>/docs/PROJECT_CONTEXT.md
templates/repo/test-checklist.md                  a filled commit checklist (lives in .git/test-checklists/)
templates/repo/section-spec.md                    build-from spec with a statechart table per section
templates/repo/guardrails.json                    optional per-repo facts -> <repo>/.claude/guardrails.json
templates/repo/hooks.json                         hook wiring for the guardrails plugin (proposed, not built yet)
templates/repo/checkpoint.md                      per-branch checkpoint shape
templates/repo/eslint.config.js                   react/forbid-elements matching designSystem
templates/patterns/                               README, CLAUDE, GAPS, PROMOTIONS, UPGRADING -> <library repo>/patterns/
templates/studio/CLAUDE.md                        design-studio workspace: five stages
templates/design/brief.md                         design brief
templates/design/mcp.json                         shadcn MCP server   -> <repo>/.mcp.json
templates/design/components.registries.json       registries block   -> <repo>/components.json
prompts/session-retro.md                          retro prompt: transcripts + prompt history, calibration, report sections
```

## Design stack at a glance

- **Adopt:** [google-labs-code/design.md](https://github.com/google-labs-code/design.md) — a root `DESIGN.md` every agent reads, lintable for WCAG contrast, exportable to Tailwind or DTCG tokens.
- **Skills:** frontend-design · interface-design · Impeccable · one motion skill (Emil Kowalski's, motion-dev, or gsap-skills for GSAP projects) · web-design-guidelines.
- **Registries (marketing pages):** React Bits, Canvas UI via the shadcn MCP server. **Shaders MCP** for paid GPU effects.

Details and trade-offs: [docs/GUIDE.md](docs/GUIDE.md).
