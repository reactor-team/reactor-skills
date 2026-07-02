# Schema details, the JSON shape and composition algorithm

The authoritative definition is `composeForRender()` + `validateStructuredScene()`
in `public-demos/lib/lingbot-world-prompts.ts`. This file documents the edge
cases an author hits. The skeleton is in SKILL.md §2.1.

---

## 1. Top-level shape

```jsonc
{
  "id":          "<kebab-case-slug>", // required, stable across edits
  "name":        "<human-readable>", // required
  "description": "<one-line>", // optional
  "entrance": {                          // required for a full example
    "image": { "label": "<caption>", "src": "<path or ''>" }, "state": "<a key in scene.states>"   // the boot state
  }, "scene": { "states": { ... }, "events": [ ... ] }
}
```

A **bare scene** (`{ "states": {...}, "events": [...] }` with no `entrance`) is
also accepted by the validator and the report tool, the first declared state
becomes the entrance. Prefer the full example shape when you know the seed image.

- `entrance.state` **must** be a key in `scene.states`, or the runtime can't boot.
- `entrance.image.src` is a path served by the app (e.g. `./images/<id>.png`).
  Leave `""` if the user hasn't supplied a seed image yet; tell them where to
  drop it.

---

## 2. States

```jsonc
"states": {
  "<state_key>": {
    "base":     "<prose>", // required string
    "camera":   { "static": "<prose>", "dynamic": "<prose>" }, // required
    "movement": { "static": "<prose>", "dynamic": "<prose>" }  // required
  }
}
```

At least one state is required. Both `camera` and `movement` must have **both**
`static` and `dynamic` string keys. State keys are stable identifiers (referenced
by `entrance.state`, `event.from`, `event.to`), renaming one means updating
every reference.

---

## 3. Events

```jsonc
{
  "name": "<1-3 word label>", // required
  "kind": "overlay" | "transition", // required
  "from": ["<state_key>", ...], // required, non-empty, valid keys
  "to":   "<state_key>", // required iff transition; forbidden on overlay
  "base":     "<prose>", // optional layer override
  "camera":   { "static": "<prose>", "dynamic": "<prose>" }, // optional
  "movement": { "static": "<prose>", "dynamic": "<prose>" }, // optional
  "detail":   "<prose>" | { "static": "<prose>", "dynamic": "<prose>" }  // optional
}
```

- `events[i]` binds to **hold-key `i+1`**. But the runtime renumbers chips
  **per state** (it shows only events whose `from` includes the current state), so authoring order is free; gate with `from`.
- An action `detail` (or override) uses `{static, dynamic}`; an environmental one
  uses a plain string.

### Override semantics (per layer: base, camera, movement)

| Field state | Meaning |
|---|---|
| **omitted** | **inherit** the current state's layer |
| **string / `{static,dynamic}`** | **replace** the state's layer while held |
| **`""` / `{static:"",dynamic:""}`** | **suppress** the layer (contributes nothing) |

Suppress is rarely correct, prefer a positive override (a suppressed `camera`
makes the scene-wide lock fragile). There is no separate "takeover" mode;
overriding all three layers *is* a takeover.

---

## 4. Composition algorithm (`composeForRender`)

Inputs: `(scene, currentState, isMoving, heldOverlaySlots[], transitionSlot|null)`.

1. **Contributors:**
   - If `transitionSlot != null` → contributors = `[events[transitionSlot]]`.
   - Else → contributors = each `events[slot]` for `slot in heldOverlaySlots`
     that is an **overlay** *and* whose `from` includes `currentState`. (Overlays
     gated to other states, or non-overlays, are ignored.)
2. **State for layer resolution** = `scene.states[currentState]`. During a held
   transition you pass the **from-state** as `currentState` (the cursor commits to
   `to` only on release), and the transition event's overrides apply on top.
3. **Each layer** `base → camera → movement`: the *latest* contributor that
   overrides it wins; else the state's prose. For `camera`/`movement`, pick
   `dynamic` if `isMoving` else `static`.
4. **Append** each contributor's `detail` (matching branch).
5. **Trim, drop empties, join with single spaces.**

Consequences:

- A held transition suppresses other event prose (only the transition
  contributes), by passing a single `transitionSlot`.
- Multiple held overlays stack in slot order; later overlays win per-layer and
  append their detail after earlier ones.
- An overlay held in a state not in its `from` contributes nothing (it's
  filtered), so the same overlay can be safely listed for multiple states via
  `from`.

---

## 5. Baseline contract

Every **single-event** composition must fit the 512-token cap:

- each state at rest and in motion,
- each event held over each state in its `from`, both `isMoving` branches.

`scene_report.py` sweeps exactly these and emits `BASELINE VIOLATION` on any
overrun (and exits non-zero). Multi-event holds are **not** part of the contract, they're user-driven and checked only via `--held` (`references/token-budget.md`).

---

## 6. Validation checklist the tool enforces

`scene_report.py` mirrors `validateStructuredScene` plus self-check R1:

- `scene.states` is a non-empty object; each state has string `base` and
  `{static,dynamic}` `camera`/`movement`.
- each event: string `name`; `kind` ∈ {overlay, transition}; non-empty `from`
  with valid keys; `to` required+valid for transitions, absent on overlays;
  action `detail` has both branches.
- `entrance.state` is a valid key.
- **R1:** in a multi-state world, every state has ≥1 outgoing transition (no
  dead-ends).

Structural prose-quality rules (R2-R9) are read-throughs in
`references/validation.md`, not enforced by the tool.
