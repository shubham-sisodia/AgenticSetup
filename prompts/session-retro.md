# Session retro prompt

Paste into `claude` started from your home folder. Read-only on your transcripts and prompt history.

```text
Analyze my past Claude Code sessions and write a report. Read-only: write nothing except the report and scripts in a scratch folder.
1. Two sources. Transcripts are in ~/.claude/projects/<project>/*.jsonl (full sessions, deleted after cleanupPeriodDays). ~/.claude/history.jsonl keeps only my prompts, but goes back further. List each project's session count, date range and size from both. Cover the last 90 days.
2. Write two Python scripts in a scratch folder. (a) Stream each transcript and output one summary per session: project, timestamps, first prompt (300 chars), user turns, tool-call counts, files edited, Bash commands (flag git/test/build), tool errors, hook denials, and prompts that correct you ("no", "wrong", "undo", "still", "again"). (b) Stream history.jsonl and output prompts per project per day. Redact with regexes before anything is printed: API keys and tokens (sk-, ghp_, xox, AKIA, long base64/hex), passwords after "password", one-time codes, emails, bearer headers.
3. Active hours: from transcripts, sum gaps between consecutive events under 30 min. For history-only days, estimate from prompt gaps the same way, then calibrate: compute the ratio transcript-hours / prompt-gap-hours on days that have both and multiply history-only estimates by it. State the ratio. Mark every estimate "(inferred)".
4. If there are more than ~5 projects, use one subagent per project. Produce: per-project themes and status, a weekly timeline, effort, friction, and recommendations (CLAUDE.md, hooks, skills, agents, lint, settings) with evidence.
5. Write ~/claude-session-report.md with a TL;DR of at most 5 bullets, tables for stats, "(inferred)" on anything not directly observed, and these sections:
   - Rules that exist but were not followed: read ~/.claude/CLAUDE.md, the agents, hooks and each repo's CLAUDE.md, and list each rule that a session broke, with the session and the correction that followed.
   - Dormant projects: projects with no session in the last 30 days, and what was left open.
   - Security: secrets or credentials that appear anywhere on disk (count and file, never the value), and whether transcripts are being deleted.
```

To reuse: save as `~/.claude/commands/session-report.md` and run `/session-report`.

## Reading the report

- **Rules you stated in chat** (always / never / remember). If one recurs, it never reached config.
- **Rules that exist but weren't followed.** A skipped CLAUDE.md rule needs a hook. First check the
  rule is actually installed: a template line that never reached `~/.claude/CLAUDE.md` can't be tested.
- **Recurring themes across projects.** Many projects → global rule or hook; one project → that repo's
  config or its advisor.
- **Repeated errors**, ignoring grep/ls probes that simply found nothing.
- **Hook denials.** Each one is a rule that moved from chat to code and fired; count them per rule.
- **Long-lived sessions.** Wall-clock far above active hours means corrections cluster late.
- **Dormant projects.** Close them or write their checkpoint; don't let half-done work rot.
- **Security and retention.** Secrets on disk come first: rotate, then scrub, then delete backups.
  Transcripts being deleted means raise `cleanupPeriodDays`.

Fix order: per-repo fact → hook → skill → lint rule → global habit → setting.
