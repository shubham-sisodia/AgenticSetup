# <Project>: project context

Owned by `<project>-advisor`. The canonical record of what this product does and why. Code wins when
this file and the code disagree; fix this file. Last reconciled: <YYYY-MM-DD>.

## 1. Product
- What it is, in two sentences.
- Users and roles: <who, how often, on what device>.
- Main jobs: <3-5, verb first>.

## 2. Business rules
Numbered, so tests and tickets can cite them (`PC-2.3`).
1. <rule>: <source (ticket, owner decision, file:line)>.
2. <rule>: <source>.

## 3. Information architecture and flows
| Route | Page | Tabs / views | Who can see it |
| --- | --- | --- | --- |
| `/<route>` | <page> | `?tab=<a\|b>` | <roles> |

Key flows, one line each: trigger, steps, end state.

## 4. Architecture
- Stack: <framework, router, state, data layer, component library>.
- Folder layout: <the folders that matter and what lives in each>.
- <Migration status, if any: which tree is legacy, which pages have moved.>

## 5. Data
| Entity | Source (endpoint or table) | Key fields | States |
| --- | --- | --- | --- |
| <entity> | `GET /api/<x>` | <id, name, status> | <draft \| active \| archived> |

## 6. Auth and permissions
- How login works, where tokens live, how a 401 is handled.
- Permission model: <roles, what gates what, where the check lives (file:line)>.

## 7. Environments and deployment
| Env | URL variable | Build command | Notes |
| --- | --- | --- | --- |
| dev | `VITE_API_URL` | `npm run build:dev` | <never point local builds at production> |

Name variables, never values.

## 8. Open questions
Numbered; each has an owner and a suggested way to resolve it. Move answers into the sections above
and strike the question.
1. <question>: owner <name or role>, resolve by <how>.
