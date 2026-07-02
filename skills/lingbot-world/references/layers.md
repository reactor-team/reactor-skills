# Layers, per-layer prose recipes and token targets

Each state bundles three Layers, `base`, `camera`, `movement`, and events
override them (SKILL.md §1). This file gives the shared recipe and token target
for each Layer. The **viewpoint-specific wording** (the `base` opener, the
`camera`/`movement` phrasing for third-person vs. first-person vs. spectator)
lives in `references/viewpoints.md`, read that alongside this.

Token targets below are *starting* values from the production reference scenes,
not caps. The only real cap is the encoder: every composition ≤480 soft / 512
hard (`references/token-budget.md`). A heavier layer is fine if the worst-case
composition still fits.

---

## Encoder invariants (every layer, deeper why)

The four invariants in SKILL.md §3 in more depth:

1. **No imperative camera verbs** (*pan, tilt, zoom, dolly, track, push in, pull
   back, orbit, rotate, fly through*). The model responds to **positional**
   language and reads imperative verbs as continuous, unconditional camera
   motion it can't gate on input, so it renders that motion always. Say where
   the camera *is*, not what it *does*.
2. **No input vocabulary** (*arrow-key, look-input, WASD, while held, only while
   pressed*). Arrow-keys are not a model condition channel; the model can't hear
   "while held", so any input-conditioned clause renders unconditionally (the
   camera orbits on its own, the heading drifts). Express camera↔subject geometry
   as an **invariant**, *"the camera tracks from behind and never rotates
   independently; the subject's heading turns with the camera so the rear view is
   always preserved."* The real heading change comes from the control channel;
   the prose only states the geometry that must hold.
3. **No image-model tag soup** (*"cinematic, 8k, volumetric, photoreal"*). Bake
   quality into physical language (*"warm low-angle sunlight"*).
4. **One primary subject; no object-level agency; no multi-character coordination.**

---

## `base`

The shared world description, subject identity + environment + style, constant
across movement and (unless overridden) across events.

- **Content:** 2-4 sentences, dense clausal anchors, near/mid/far planes, one
  mood phrase as the closing clause.
- **Opener:** viewpoint-specific (`references/viewpoints.md`): driving-game
  framing (third-person), "first-person view from…" (first-person), or a plain
  scene statement with no POV (spectator).
- **Must not contain:** POV phrasing beyond the opener, motion verbs (those are
  `movement`), imperative camera verbs.
- **Starting target: ~140 tok** (production range 129-199; underwater/dense
  worlds run higher).

When a **state** other than the entrance describes a transformed subject
(submarine, flight form), its `base` must inventory the new form's concrete
distinguishing features (see self-check R9 in `references/validation.md`), at
least 3-4 visible differences and at least one that interacts with the
environment (headlights washing the seabed, contrails marking the sky).

---

## `camera.{static, dynamic}`

Where the camera sits and how it relates to the subject. `static` = no WASD;
`dynamic` = WASD held. Both describe **position only**, never camera operation,
never input behavior. The exact wording is viewpoint-specific
(`references/viewpoints.md`); the shape:

- `static`, the resting framing; nothing moves on its own. Third-person: subject
  locked at frame centre, constant size/distance. First-person: the POV view
  holds steady. Spectator: a fixed shot at constant distance.
- `dynamic`, the framing while traveling, stated as a geometric invariant.
  Third-person: strict centred rear view, camera tracks from behind, never
  rotates independently, heading follows the camera. First-person: forward view, foreground anchored, view faces the direction of travel. Spectator: inert
  (≈static) or a gentle forward ease.

In most worlds `camera` is a **scene-wide invariant**, the same prose in every
state, and events should **inherit** it. Override `camera` only for a genuine
framing change, and then carry the full lock language in the override (don't
suppress `camera` and move framing into `detail`, that makes the lock fragile).

- **Starting target: static ~30-60 tok, dynamic ~60 tok** (vehicles needing
  extra anti-drift run to ~95-120).

---

## `movement.{static, dynamic}`

What the subject (third/first-person) or the world (spectator) does. `static` =
idle; `dynamic` = WASD held.

- `static`, idle behavior, rarely fully inert: breathing, hovering, deck
  pitching, ambient ripples (spectator). If the subject tends to drift (a
  hovering dragon recedes), add explicit negative constraints, they cost tokens, so use sparingly (one or two function as anchors; more is filler).
- `dynamic`, concrete motion + physical consequence. Third-person: subject
  translates (*"rolls forward, kicking up dust"*). First-person: the world rushes
  past + sensation + a motion-resolution clause (far detail sharpening on
  approach). Spectator: ambient intensified, or the near plane sliding past if
  the camera eases forward.
- **Do not restate identity**, `base` carries it; the encoder sees both copies
  and risks contradiction.
- **Starting target: static ~80 tok** (up to ~170 if suppressing strong drift), **dynamic ~60 tok**.

---

## Alternate states vs. event overrides

Two ways a layer's prose can differ from the entrance state:

- **A different state**, a coherent world the user can be *in* (and navigate), reached by a transition. Use when the change is a place the cursor rests:
  `sea_level_calm`, `underwater_calm`, `flying_calm`. Each state's layers carry
  full anchor density.
- **An event override**, a layer's prose while an event is *held*, reverting (or
  committing, for transitions) on release. Use for things that happen *on top of*
  a state.

An alternate `base` written for a state must hold the same anchor density as the
entrance `base`, a thin state base produces a thin composed prompt for every
event held in it.
