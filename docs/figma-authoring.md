# Figma authoring for one-pass builds

A contract for authoring Figma files so that Claude Code (or a design-system advisor) can read a
screen and rebuild it in React with your component library in one pass, with named gaps instead of
silent guesses. Designers follow the rules and the checklist (§3–§9, §12); agents follow the reading
protocol (§11).

It is grounded in what the Figma MCP tools actually return to an agent (checked against the live tool
schemas, §2) and in Figma's own guidance: [Structure your Figma file for better code](https://developers.figma.com/docs/figma-mcp-server/structure-figma-file/),
[Code Connect](https://developers.figma.com/docs/code-connect/).

## 1. The problem

A real, unedited fragment of what `get_metadata` returned for a working product file:

```xml
<frame id="10:5085" name="Frame 1116602300" width="1388" height="900">
  <instance id="153:111400" name="sidemenu" width="220" height="900" />
  <frame id="10:5087" name="Frame 8" width="1168" height="900">
    <frame id="10:5089" name="Frame 2" width="1168" height="820">
      <frame id="154:118884" name="Frame 54" width="1120" height="40"> ...
```

Only `sidemenu` carries meaning. `Frame 8`, `Frame 2`, `Frame 54` tell the agent nothing about
component, state, responsiveness or intent, so it guesses, and guessing is why one-pass builds fail.
The design also never encodes the route, the API, the empty state or which enum values exist, so the
agent either invents them or stops to ask.

**The fix: make three resolutions deterministic (component, variant, token) and encode the four things
pixels can't carry (state, responsiveness, flow, data).**

## 2. How an agent reads a Figma file

| Tool | Returns | The framework leans on it for |
| --- | --- | --- |
| `get_metadata` | Sparse XML: node id, **name**, type, x/y/w/h. No styles. | Structure and naming; a cheap map of a large file |
| `get_design_context` | Reference code + screenshot + variables for a node; React + Tailwind by default. With Code Connect published, your real imports and props | Component, variant and token resolution |
| `get_variable_defs` | `{ 'token/path': value }` for variables in the selection; emits **Code Syntax** if set | The token contract (§5) |
| `get_code_connect_map` | `{ nodeId: { codeConnectName, codeConnectSrc } }` | Enforced component mapping (§10) |
| `get_screenshot` | PNG of a node | Visual ground truth and critique |

Three consequences drive everything:
1. **Names are the agent's primary signal.** `get_metadata` carries little else. `Frame 54` is noise;
   `ui/Button` is an instruction.
2. **Code Connect turns "guessed markup" into "your component".** Without it the agent writes
   design-informed code from scratch; with it, Figma hands over the exact import and props
   ([MCP and Code Connect](https://developers.figma.com/docs/figma-mcp-server/code-connect-integration/)).
3. **Prototypes are invisible.** No tool exposes Smart Animate or interaction data, so motion must be
   annotated (§6.5), never read off a prototype.

## 3. C1: Naming (the load-bearing rule)

| Prefix | Means | Agent resolves to | Example |
| --- | --- | --- | --- |
| `ui/<ExportName>` | A library component | The exact symbol in the library's export barrel | `ui/Button`, `ui/DataTable`, `ui/Sheet` |
| `pattern/<Doc>` | A composition that maps to a pattern doc, not one component | The named doc in the library's `patterns/` | `pattern/AppShell`, `pattern/ListPage`, `pattern/FormInSheet` |
| `region/<Name>` | A semantic layout region inside a screen | A slot in the pattern layout | `region/PageHeader`, `region/FilterBar` |
| `screen/<route>` | A top-level screen frame, named by route | A route | `screen/invoice-list`, `screen/invoice-detail` |

1. The part after `ui/` is PascalCase and identical to the export; the agent matches by string
   equality, never fuzzily.
2. Instances keep their main-component name. To wrap one, name the wrapper `region/<something>`.
3. **Forbidden:** any name matching `^(Frame|Group|Rectangle|Vector|Component) \d+$`. The agent treats
   it as unresolved and reports a gap; it never maps it silently.

## 4. C2: Components and variants (the props schema)

A Figma component's variant and component properties **are** the React prop signature. Every enum
prop is a Figma variant property whose option values are the exact library string literals:
`variant=primary`, not `Style=Filled`. A value outside the library's set is a contract violation the
agent flags, not coerces.

| Component | Properties to expose |
| --- | --- |
| `Button` | `variant`, `size`, `disabled`, `isLoading`, leading / trailing icon (bool) |
| `Badge` | `variant`: **one Badge with every status as a variant**, not one component per status |
| `Input` | `size`, `isInvalid`, `disabled`, `label`, `required`, `helperText` |
| `DataTable` | `isLoading`, row selection, pagination; per column: header, align, cell kind |
| `Dialog` / `Sheet` | Dialog role (confirm / form); Sheet `side` |
| `Stepper` | `orientation`, `activeStep`: map every wizard to it |

Not drawable as components (annotate instead, §8): imperative toasts, charts (annotate the data
shape), maps (annotate the source). Name variant properties like props (`variant`, `size`, `state`).
If you can't describe the matrix in one phrase ("size × state"), nest instances instead of adding
variants.

## 5. C3: Tokens (resolve to classes, never hex)

Name every Figma variable as the exact path into the library's token tree and set its **Code Syntax**
to the class. The agent then emits the class and never reads the hex.

| Namespace | Figma variable | Class |
| --- | --- | --- |
| Text | `text/primary`, `text/brand/moderate` | `text-primary`, `text-brand-moderate` |
| Surface | `surface/background/white` | `bg-surface-background-white` |
| Stroke | `stroke/grey/subtle` | `border-grey-200` |
| Raw scale | `color/blue/500` | `bg-blue-500` |
| Radius | `radius/small｜medium｜large` | `rounded-small｜medium｜large` |
| Spacing | `space/4｜8｜16｜24` | `p-1｜p-2｜p-4｜p-6` |
| Type | presets: `bodyMedium`, `headingMedium` | the Typography component's `variant` |
| Motion | `motion/duration/*`, `motion/easing/*` | the motion layer (§6.5), not a class |

1. Set Code Syntax on every variable; without it the agent gets a raw value and invents a name.
2. A variable name that isn't a real token path is a gap.
3. A hex value in `get_variable_defs` output means an unmapped variable: flag it, don't hardcode it.
4. Designers pick a named type preset, never a raw size.

## 6. C4: States (draw what can't be inferred)

**Must be drawn:**
- Four sibling frames per screen: `screen/<x>`, `screen/<x>#empty`, `screen/<x>#loading`,
  `screen/<x>#error`. Tables often have a loading prop but no empty or error prop; if you don't draw
  them, the agent invents the copy and layout.
- Every enum value as a variant, including values no current screen shows.
- Form validation with the actual error copy.
- Wizard step states, and the active nav item and breadcrumb.

**Inferable, don't draw:** hover, focus, pressed, disabled, switch on/off, indeterminate checkbox,
pagination internals, toast appearance.

Rule of thumb: draw a state if and only if the library has no prop or default that produces it, or it
carries content the agent can't author (error copy, empty messaging, which enum values exist).

### 6.5 Motion

| If the motion is… | It's a… | Authored where | Agent does |
| --- | --- | --- | --- |
| A raw value reused everywhere (duration, easing, distance, stagger) | Token | A `motion/` variable | Emits the CSS variable or the `motion.ts` value |
| Built into a component's own states (hover, press, focus) | Component default | Nowhere | Infers it |
| Orchestrated (enter/exit, list stagger, route transition, overlay, collapse) | Preset | A named entry in `motion.ts`, referenced from `meta/motion` | Wires the named preset |

Durations, easings and presets are a **closed set**. Adding one is a reviewed change to the library,
never an inline decision on one frame. A raw `240ms` is the motion version of a hex: a gap. A preset
name not in `motion.ts` is a gap.

```
duration: instant 100 · fast 180 · base 240 · slow 400 · deliberate 600  (ms)
easing:   standard · decelerate (enter) · accelerate (exit) · spring
presets:  fadeIn · slideUp · slideInRight · staggerList · pageEnter · drawerSlide · modalScale · collapse
```

## 7. C5: Responsive intent

**Auto Layout sizing is the per-element signal:** Hug → `fit-content`, Fill → `flex: 1`, Fixed →
fixed size, Fill with min/max → `clamp()`. Use Auto Layout everywhere; keep absolute positioning for
intentional decorative overlap only (it is the most common design-to-code failure).

**Breakpoint frames are the per-layout signal:** the same screen at several widths, same prefix,
width in the suffix, in one Section (`screen/inbox — Desktop-1440`, `screen/inbox — Mobile-375`).
Minimum two per screen, or the `meta` block says desktop-only. Silence reads as "unknown".

## 8. C6: Flow and the `meta` block

Pixels never carry route, API, roles or enums. Encode them in Dev Mode annotations (the MCP surfaces
them), or a pinned text layer named `meta/` as a fallback:

```
meta/route:   /invoices
meta/nav:     Billing > Invoices
meta/tabs:    ?tab=open|paid ; ?view=board|table
meta/filters: ?status= ?customer= ?q=   (persist to URL)
meta/roles:   Admin (full), Viewer (read)
meta/api:     GET /api/invoices -> { id, number, customer, amount, status, dueDate }
meta/states:  empty="No invoices yet" ; error=retry
meta/enums:   status = draft|sent|paid|overdue|void
meta/motion:  list=staggerList ; route=pageEnter ; drawer=drawerSlide
```

The user flow lives on a **Flow** page with numbered steps and routes (`2.0 Invoice list → /invoices`,
`2.1 Invoice detail → /invoices/:id (trigger: tap row)`). The frame name carries the route; the
prototype connection carries the trigger.

## 9. C7: File and page structure

Pages: Cover (status, links) · Flow · Design: `<Feature>` · Components · Prototype · Archive (never
delete). One Section per screen holding its breakpoints and data states. Keep the tree shallow (6
levels or fewer), no hidden layers, no images of text, no detached instances.

## 10. Code Connect: the enforcement layer

Naming and props are the manual contract; Code Connect makes them tool-enforced, served through
`get_code_connect_map` and folded into `get_design_context`.

1. Add `@figma/code-connect` (dev) and a `figma.config.json` that includes `**/*.figma.tsx`.
2. One `<Component>.figma.tsx` per component, next to it, mapping each Figma property with
   `figma.enum`, `figma.boolean`, `figma.string`.
3. The Figma library must already satisfy §3 and §4: Code Connect maps property by property, so parity
   is a prerequisite, not a substitute.
4. `npx figma connect publish` in CI on each library release, so mappings track the version
   consumers pin.

Start with the dozen components with the highest instance count and the largest guess surface
(button, badge, table, input, select, sheet, dialog, tabs, sidebar, stat card, stepper, alert).

## 11. The agent reading protocol

1. **Map first:** `get_metadata` on the page; find the `screen/` frames and their Sections.
2. **Read the annotations:** each screen's `meta` block is the routing and data contract. Don't build
   without it.
3. **Resolve components:** `get_code_connect_map`; if mapped, use the import and props verbatim; else
   the `ui/` or `pattern/` name; `Frame N` is a gap.
4. **Resolve tokens:** `get_variable_defs`, emit the Code Syntax; a hex is a gap.
5. **Resolve variants to props;** an off-contract value is a gap.
6. **Cover states:** every drawn data-state frame and every enum variant; infer interaction states.
7. **Wire responsive** from Auto Layout sizing and breakpoint frames.
8. **Screenshot last,** as a visual check, not the source of truth.

**Stop and flag, never guess.** The agent emits a gap report for: a `Frame N` name, a hex-only token,
an off-contract variant, a missing `meta` block, a missing empty / loading / error frame, an enum value
referenced but never drawn. A clean one-pass build is claimed only when the gap report is empty.

## 12. Per-screen checklist (designer-facing)

- [ ] Screen frame named `screen/<route>`; route also in `meta`.
- [ ] Every reusable element is a `ui/<Export>` instance (no detached instances, no `Frame N`).
- [ ] Compositions named `pattern/<Doc>`; regions named `region/<Name>`.
- [ ] Variant properties use the library's exact literals.
- [ ] Colours, spacing, radius and type are variables named as token paths, with Code Syntax.
- [ ] Auto Layout on every container; Fill / Hug / Fixed and min / max set on purpose.
- [ ] Two or more breakpoint frames, or `meta` says desktop-only.
- [ ] Default, `#empty`, `#loading` and `#error` frames present.
- [ ] Every enum value drawn as a variant.
- [ ] Form errors show the actual validation copy.
- [ ] `meta` complete: route, nav, tabs, filters, roles, api, states, enums, motion.
- [ ] Screen sits in its Section; flow step and route on the Flow page.

## 13. Anti-patterns (auto-fail)

- Absolute positioning instead of Auto Layout.
- `Frame N` / `Group N` names, detached instances, images of text.
- Five near-duplicate frames instead of one component with variants.
- Hardcoded hex or px instead of variables with Code Syntax.
- A single default frame with no empty, loading or error siblings.
- A toast drawn as a static frame (it is an imperative API: annotate it).
- No `meta` block.

## 14. Rollout

1. Pilot one feature end to end; run the agent; measure how close the one-pass build is and which gaps
   fire.
2. Stand up Code Connect for the first dozen components: the biggest single reliability jump.
3. Once it holds, move this doc into the library's `patterns/` as a numbered doc
   ([design-system loop](design-system-loop.md)).
