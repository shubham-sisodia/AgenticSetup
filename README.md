# AgenticSetup

A reusable setup for AI-assisted development with Claude Code: where each rule should live, copy-ready templates, and a curated UI/UX/motion skill stack.

One setup, four layers:

1. **Global habits** in `~/.claude/CLAUDE.md`
2. **Machine settings** in `~/.claude/settings.json`
3. **Per-repo facts** in `.claude/guardrails.json`, enforced by hooks
4. **Skills** for the multi-step jobs you'd otherwise retype

Plus a `DESIGN.md` per project for how the UI should look, and a monthly retro that tells you which layer to tighten next.

## Setup (about 45 minutes, once)

- [ ] 1. Merge [`templates/claude/settings.json`](templates/claude/settings.json) into `~/.claude/settings.json` (keeps transcripts for a year, sets a default model).
- [ ] 2. Copy [`templates/claude/CLAUDE.md`](templates/claude/CLAUDE.md) to `~/.claude/CLAUDE.md`. Trim what you don't need.
- [ ] 3. Copy [`skills/design-system-from-brief`](skills/design-system-from-brief) to `~/.claude/skills/`.
- [ ] 4. In each repo, add `.claude/guardrails.json` from [`templates/repo/guardrails.json`](templates/repo/guardrails.json), keep the keys that apply, and commit it.
- [ ] 5. If the repo has a design system, add the matching lint rule ([`templates/repo/eslint.config.js`](templates/repo/eslint.config.js)).
- [ ] 6. For each new project's UI: fill [`templates/design/brief.md`](templates/design/brief.md), generate and lint a `DESIGN.md`.
- [ ] 7. Install a small design skill stack (max five; see the guide).
- [ ] 8. Run a session retro now as a baseline ([`prompts/session-retro.md`](prompts/session-retro.md)), then monthly.

## Where rules go

| If the rule is… | Put it in |
| --- | --- |
| A project fact (port, active folder, env prefix, design-system package) | `.claude/guardrails.json` |
| Something Claude already ignored once | A hook |
| A multi-step job you typed more than twice | A skill |
| About code shape (no native buttons, router links only) | A lint rule |
| What the UI should look like | `DESIGN.md` |
| A habit for every repo | `~/.claude/CLAUDE.md` |
| Machine behavior | `~/.claude/settings.json` |

## Layout

```
README.md                                   this file
docs/GUIDE.md                               full guide: principles, hooks, skills, retros, design, security, cadence
templates/claude/CLAUDE.md                  global rules        -> ~/.claude/CLAUDE.md
templates/claude/settings.json              machine settings    -> ~/.claude/settings.json
templates/repo/guardrails.json              per-repo facts      -> <repo>/.claude/guardrails.json
templates/repo/hooks.json                   hook wiring reference (guardrails plugin)
templates/repo/checkpoint.md                per-branch checkpoint shape
templates/repo/eslint.config.js             react/forbid-elements matching designSystem
templates/design/brief.md                   design brief
templates/design/mcp.json                   shadcn MCP server   -> <repo>/.mcp.json
templates/design/components.registries.json registries block   -> <repo>/components.json
skills/design-system-from-brief/SKILL.md    brief -> DESIGN.md -> lint -> export
prompts/session-retro.md                    retro prompt that works without any plugin
```

## Design stack at a glance

- **Adopt:** [google-labs-code/design.md](https://github.com/google-labs-code/design.md) — a root `DESIGN.md` every agent reads, lintable for WCAG contrast, exportable to Tailwind or DTCG tokens.
- **Skills:** frontend-design · interface-design · Impeccable · one motion skill (Emil Kowalski's, motion-dev, or gsap-skills for GSAP projects) · web-design-guidelines.
- **Registries (marketing pages):** React Bits, Canvas UI via the shadcn MCP server. **Shaders MCP** for paid GPU effects.

Details and trade-offs: [docs/GUIDE.md](docs/GUIDE.md).
