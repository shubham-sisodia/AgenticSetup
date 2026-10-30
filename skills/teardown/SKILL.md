---
name: teardown
description: Tear down a competitor product or flow in a real browser and document patterns worth stealing or avoiding. Use when the user says "teardown", "how does <product> do X", or "look at <competitor>".
---

# /teardown: competitor teardown

Input: `$ARGUMENTS`, a product name or URL, optionally with the flow to walk
(e.g. `linear.app onboarding`, `https://grafana.com dashboard creation`).

1. If no flow is named, ask which flow matters, or default to first run and onboarding, which is
   usually the most designed flow in any product.
2. Delegate to the `competitor-scout` agent with the target, the flow, today's date and the absolute
   path of `teardowns/`. One agent per product.
3. For several products, launch the scouts in parallel (one message, several Agent calls). For 3 or
   more products, offer a workflow instead.
4. When the scouts return, add a short comparison note at the top of each report's "steal / avoid"
   section if more than one product was covered.
5. Reply with the cross-product steal / avoid synthesis and the report paths.
