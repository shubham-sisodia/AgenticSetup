# Session retro prompt (no plugin needed)

Paste into `claude` started from your home folder. Read-only on your transcripts.

```text
Analyze my past Claude Code sessions and write a report. Read-only: write nothing except the report.
1. Transcripts are in ~/.claude/projects/<project>/*.jsonl. List each project's session count, date range and size. Cover the last 90 days.
2. Write a Python script that streams each .jsonl and outputs one summary per session: project, timestamps, first prompt (300 chars), user turns, tool-call counts, files edited, Bash commands (flag git/test/build), tool errors, and prompts that correct you ("no", "wrong", "undo", "still"). Redact anything that looks like a secret.
3. If there are more than ~5 projects, use one subagent per project. Produce: per-project themes and status, a weekly timeline, effort, friction, and recommendations (CLAUDE.md, hooks, skills) with evidence.
4. Write ~/claude-session-report.md with a TL;DR of at most 5 bullets, tables for stats, and "(inferred)" on anything not directly observed.
```

To reuse: save as `~/.claude/commands/session-report.md` and run `/session-report`.

## Reading the report

- **Rules you stated in chat** (always / never / remember). If one recurs, it never reached config.
- **Rules that exist but weren't followed.** A skipped CLAUDE.md rule needs a hook.
- **Recurring themes across projects.** Many projects → global rule or hook; one project → that repo's config.
- **Repeated errors**, ignoring grep/ls probes that simply found nothing.
- **Long-lived sessions.** Wall-clock far above active hours means corrections cluster late.
- **Security and retention.** Secrets on disk come first; transcripts being deleted means raise `cleanupPeriodDays`.

Fix order: guardrails.json value → hook → skill → lint rule → CLAUDE.md line → settings.
