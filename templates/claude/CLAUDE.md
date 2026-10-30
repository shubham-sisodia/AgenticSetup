# Global working rules

## Verify first
- Before any build, lint, commit or tag for a fix, confirm it works where the user will see it: the running app, the tab already open (check DOM and network), or a headless Playwright check. Never open a new tab or a second dev server when one exists.
- Never say "done" for a UI change without evidence (a screenshot you looked at, or a passing spec). If you can't verify here, say "not verified" and what to check.
- Don't commit or tag a fix the user hasn't seen working unless asked to ship it.
- When a fix lives in a dependency, confirm the consuming app loads the new version first.

## Use what exists
- Build UI from the project's design system (DESIGN.md and its component library). Before writing a native <button>, <input>, <select>, <table> or a hand-rolled widget, check the design system's exports and docs. If nothing fits, say so and ask.
- Follow existing patterns (routing links, forms, dialogs, data fetching) over inventing new ones.

## Know the shape before you render it
- Before writing UI that renders API data, fetch a real response (or read the typed client) and cite the keys you'll use.
- Don't fire a query until its required params exist.

## Sweeps
- For "do it everywhere": list every call site first (several search patterns), confirm, apply, then re-search and show zero left.

## Shell
- Quote args containing * ? [ ] (e.g. --include='*.tsx'). In zsh write "${var}:path", never "$var:path".
- Use absolute paths. cd to the main checkout before removing a worktree.
- A grep/ls that finds nothing exits 1; that's an answer, not a failure. Append || true when chaining.
- Never `sleep N; check`. Run long commands in the background or use a blocking wait (gh run watch, gh pr checks --watch, npx wait-on tcp:PORT).

## Dev servers
- Use the project's dev port with --strictPort. If it's already listening, reuse it.
- A new worktree needs .env / .npmrc copied from the main checkout before it runs.
- Ask before killing a process you didn't start.

## Git and releases
- Stage explicit paths in a separate command; never git add -A, git add . or git commit -a. Review git diff --cached --stat first.
- Before tagging: git fetch --tags, pick the next unused tag in the repo's scheme, build, then push. Never move or delete a pushed tag.
- A change to a published package bumps version, lockfile and changelog in the same PR.

## Secrets
- Never ask for, echo, or write secrets into files, commits, checkpoints or messages. Refer to env-var names. If one is pasted, say it should be rotated.

## Subagents
- Give each parallel subagent its own files. Shared files are edited by the main thread after they finish.
- Rate-limited tools (design APIs, paid APIs) are called once from the main thread; save results to disk and pass paths.
- Agents and skills are personal: they live in `~/.claude/agents/` and `~/.claude/skills/`, never under a project's `.claude/`. Project-level copies fail with "agent type not found" in other checkouts and worktrees, drift from the personal copy, and the registry below names agents that must resolve from every repo.

## Projects, advisors, commit gate
- Refer to projects by alias. `~/.claude/projects.json` maps folder → alias, kind, advisor, test agent; the session hook (`~/.claude/hooks/projects.py session`) injects the alias list and the current project's rules. Worktrees resolve to their main repo.
- Session start: invoke the project's advisor (`<project>-advisor`) with the first task and the current branch. UI and component questions go to the design-system advisor (`ds-advisor`).
- Before every commit: stage in a separate command, then have the test agent (`test-engineer`) verify the staged diff and tick the per-hunk checklist (`python3 ~/.claude/hooks/projects.py checklist`). The gate hook denies the commit until every hunk is ticked. Waive only when the user explicitly does: `CLAUDE_SKIP_TEST_GATE=1 git commit ...`.
- New project: add it to `projects.json`, copy the closest sibling advisor (by kind) to `~/.claude/agents/<alias>-advisor.md`, add `~/.claude/agent-context/test-engineer/<folder>.md`, and seed `docs/PROJECT_CONTEXT.md` in the repo.

## Sessions
- One session per branch or task. Before a restart, a long break or a large context, write a checkpoint: done, in progress, next, open issues, decisions.
