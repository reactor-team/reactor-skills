# Events, overlay vs transition, override scope, invariants

Read this when designing an event, or when feedback implies an event's shape is
wrong. An event is `(name, kind, from[], to?, layer overrides, detail)`
(SKILL.md §1.2). Authoring one is three decisions: **kind**, **scope** (which
layers it overrides), and **detail**.

---

## 1. Kind, overlay vs transition

| | overlay | transition |
|---|---|---|
| What it is | something that happens *within* the current world | something that *moves you to another world* |
| Release | reverts to the pre-press composition | commits `currentState = to` |
| `to` | forbidden | required |
| Stacks? | yes, multiple overlays can be held together | no, one transition in flight at a time |
| Examples | *Lightning storm*, *Eclipse*, *Sit down*, *Fireballs* | *Storm break*, *Submerge*, *Take off*, *Surface*, *Land* |

If the world is the same after release → overlay. If the user is now somewhere
new (a different form, a different place) that they keep navigating → transition.

---

## 2. Scope, which layers the event overrides

Three shapes, cheapest first. Reach for heavier scope only when forced.

### 2.1 Detail-only (the default)

No layer overrides, just `detail` appended onto the inherited state. The world
is unchanged; the event adds atmosphere or action.

- Don't restate subject or environment, the state carries them.
- Must coexist with any *other* overlay held at the same time, never reference
  another event's presence or absence (*"with no eclipse active…"* is wrong).
- Back-couple to preserved surfaces when the event has light/material/sound that
  physically interacts (lightning silvering the wet deck).
- **Target ~80 tok** (range 45-150). Examples: *Lightning storm*, *Eclipse*, *Royal procession*, *Sit down*.

### 2.2 Atmospheric override (one layer)

Override one layer, almost always `base`, because appending alone would
**contradict** the scaffold. *Storm break* clears the sky: appending "now sunny"
onto a "storm clouds fill the sky" base puts two contradictory sentences in one
prompt. So it overrides `base` with the cleared-sky prose; `camera` and
`movement` inherit (the boat and stern view are unchanged); `detail` adds short
back-coupling (sun-shafts on the wet deck, sea birds). Target: base override
~140 tok, detail ~45 tok.

### 2.3 High-density override (two or three layers)

Override multiple layers because the event needs its **own** framing, world, or
motion that the state's layers can't supply:

- *Submerge* / *Surface* (**medium-crossing transformations**): override `base`
  (transformation prose contradicts the source identity), `movement` (the
  crash/dive sequence), and **`camera`**. Crossing a surface (waterline, ice)
  needs a through-the-surface continuity lock, so the camera override carries the
  full rear-view lock itself. `detail` is usually empty; the overrides carry it.
- *Take off* / *Land* (**same-medium transformations**): override `base` and
  `movement`, but **inherit `camera`**. The rear-view lock is unchanged through
  open air, so let it pass through from the state.
- *Fire breath* / *Portal*, **wide-framing overlays**: override `camera` (wider
  aerial), `base` (different focal world), and `movement` (jaws open, hovering).
  Highest density.

A transition that is purely atmospheric (*Storm break*) can override `base` only,
or even **nothing** (inherit all three, with the change in `detail`), inheriting
is the cheapest transition shape. Pick the smallest scope that avoids
contradiction (see self-check R6 in `references/validation.md`: put the
becoming-prose in the *layer that's changing*, not in `detail`).

### Choosing scope

- Only `base` content conflicts, camera/movement still apply → **override `base`**.
- Camera framing or subject behavior must differ from the state → **override
  those layers too**.
- Detail alone would exceed budget on top of the full scaffold → override (and
  possibly suppress) the layers it displaces, but trim `movement`/`camera` first
  (`references/token-budget.md`) before reaching for suppression.

**Avoid suppression** (`""`). Prefer a positive override. Suppressing `camera`
makes the scene-wide lock fragile across edits (self-check R3).

---

## 3. Split vs. single, one event or a sequence?

When the user's idea spans stages ("submerges *and then* a reef", "takes off
*and then* cruises", "roars *and then* a portal opens"), surface the **option to
split** as a recommendation, do **not** push it; the user decides.

- **Split** (recommended default): a transition for stage 1 (into a new state)
  plus an overlay (or the new state's resting prose) for stage 2. Each stage's
  prose is physically specific and renders reliably; the user gets a navigable
  state to rest in plus a decorating overlay. Cost: more keys; the user presses
  the second after the first commits.
- **Single event**: one trigger, more cinematic continuity *if* the model renders
  both stages. Cost: the model commonly renders one stage and skips the other, a real production failure (a "submerge into a reef" single event rendered the
  reef but left the boat on the surface). The user accepts this for simpler
  control.

Other legitimate reasons to keep it single: the stages are too brief to be
useful apart; the user wants the model to pace itself; it's a one-key-per-moment
demo. Note the failure mode once, then build what they chose.

---

## 4. Action events, `{static, dynamic}` detail

Use the object form for `detail` (or for an overridden `movement`) when the event
**itself** looks different depending on whether the subject is moving:

```jsonc
{ "name": "Sit down", "kind": "overlay", "from": ["meadow"], "detail": {
    "static":  "The retriever lowers itself into an upright sit, tail curling...", "dynamic": "The retriever skids to a halt, paws planting, tail still settling..."
  } }
```

Use a single string when the event looks the same regardless of motion (an
environmental event, eclipse, nightfall). Both detail-only and override-scoped
events can be action-typed.

---

## 5. Four invariants for high-density override prose

When an event overrides multiple layers (or its prose is the bulk of the
composition), the override + detail is effectively a standalone prompt. It must
satisfy:

1. **Anchor density**, carry all six anchors itself (POV, subject, near, mid, far, atmosphere/sensation). *Portal* and *Fire breath* both do.
2. **Back-coupling onto preserved surfaces**, name **≥2** ways the event's
   light/atmosphere touches surfaces the user expects to persist (*"the
   afterglow dances across the dragon's outstretched wings and glints off its
   obsidian scales"*; *"the forest far below is bathed in flickering
   firelight"*). One is not enough.
3. **State-delta minimality**, change only what the event physically forces.
   *Fire breath* opens the jaws and stretches the neck; the saddle, reins, and
   armour are not re-described. Prevents drift (polishing un-asked anchors and
   dropping load-bearing ones) and contradiction.
4. **Camera-lock language when framing changes**, state the new framing
   positively, what the camera must **not** do, and **why** (what must stay
   visible): *"a high wide aerial from behind and above; the lens never zooms in
   on the head, so the dragon's full wingspan is never cropped."* All three parts
   are load-bearing.

---

## 6. Gating and rescoping

- **`from[]`** gates which states an event is triggerable in. The runtime shows
  the user only the events gated to the current state, renumbered per state, so
  `events[]` order is free; gate by `from`, not by position.
- **Rescoping**, if feedback shows an event needs more/fewer layers than it has
  (an overlay that should be a transition; a detail-only event that needs a
  `base` override to stop contradicting the scaffold), that's a rescope. Run it
  back through the discuss-then-write loop (SKILL.md §4.2): surface the new shape
  plan and outline before rewriting prose.

The baseline contract validates **per-event-alone** safety (each event over each
`from`-state ≤512 tok). Multi-event holds are user-driven and checked only on
request (`--held`, see `references/token-budget.md`).
