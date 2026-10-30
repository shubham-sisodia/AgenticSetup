---
name: brief
description: Turn an issue key from <TRACKER> or a one-line idea into a structured design brief in briefs/. Use when starting any new design effort, or when the user says "write a brief", "kick off", or gives an issue key like ABC-123.
---

# /brief: create a design brief

Input: `$ARGUMENTS`, either a <TRACKER> issue key (e.g. `ABC-123`) or a free-text idea.

<TRACKER> is your issue tracker, reached through its MCP server (Jira, Linear, GitHub Issues). <WIKI>
is where product docs live (Confluence, Notion), if anywhere.

1. If the input looks like an issue key, fetch the issue and its comments through the <TRACKER> MCP
   tools (load them with ToolSearch if deferred). Also search <WIKI> for pages mentioning the issue
   title and pull anything relevant (PRDs, meeting notes).
2. Check `research/` and `teardowns/` for related artifacts and cite them.
3. If the problem, the target user or the success measure is genuinely unknowable from these sources,
   ask the user: at most one round of questions.
4. Write `briefs/YYYY-MM-DD-<slug>.md`:
   - **Problem**: one paragraph, in the user's words, not solution words
   - **Users and context**: who, where, device, frequency
   - **Jobs to be done**: 3 to 5, verb first
   - **Constraints**: technical (platform, design system), business, regulatory
   - **Out of scope**: explicit non-goals
   - **Success metrics**: how we'd know the design worked
   - **Open questions**: each with an owner and a suggested way to resolve it
   - **Sources**: links to the issue, wiki pages and research artifacts used
5. Reply with the brief's TL;DR and file path. Suggest the next step: `/research` for open questions,
   or straight to the design tool if the problem is well trodden.
