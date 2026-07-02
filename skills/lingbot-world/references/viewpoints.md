# Viewpoints, per-viewpoint layer calibration

Read this before writing any `base`/`camera`/`movement` prose. The three layers
(SKILL.md §1.1) are viewpoint-general; what changes per viewpoint is the *prose
recipe* for each, the opener that primes the model's prior, and what the control
signals mean. Pick one viewpoint per world (a transition may move between
viewpoints, a third-person boat that *Submerges* into a third-person submarine
stays third-person; a boat that the user dives *into* first-person would switch
viewpoint, which is rare, keep one viewpoint unless the user explicitly wants
the shift).

The encoder invariants in SKILL.md §3 and `references/layers.md` apply to **all**
viewpoints. This file only covers what *differs* between them.

---

## Quick comparison

| | Third-person navigable | First-person traversal | Spectator |
|---|---|---|---|
| Is there a driven subject? | yes, framed from outside | yes, the viewer *is* it | no |
| Camera sits | behind/around the subject | inside the subject (its eyes/cockpit) | fixed, observing |
| `base` opener | "third-person rear-view **driving/riding/chase game** video of…" | "first-person view from…" / "The video presents a journey through…" | a plain scene statement, **no POV claim** |
| WASD (`dynamic`) | subject translates through the world | the viewer advances through the world | viewpoint eases forward, or inert |
| Arrow-keys | turn the subject's heading (camera follows) | turn the view / heading | usually nothing |
| Production examples | storm_crossing (boat), citadel (Defender), spring_valley (retriever), dragon_ride (dragon, above-and-behind) | lingbot-prompts desert flight, underwater descent | lingbot-prompts city-at-night, Japanese garden, lakeside |

Default when ambiguous: interactive JSON world with WASD → **third-person
navigable** (it gives the model the game-footage prior that keeps the subject
framed). Prose "a journey/flight/descent through X" → **first-person traversal**.
Prose "a serene/quiet X" or "watch X" → **spectator**.

---

## 1. Third-person navigable-subject

A single controllable subject, framed from outside, that the user drives. This
is the production-calibrated default and the richest viewpoint. (It is exactly
what the former `lingbot-tpv-virtual-world` skill covered.)

### base opener, declare driving-game framing

Every `base` (state and event override) opens with framing that activates the
model's **driving/racing-game** prior rather than cinematic/aerial/documentary
footage:

> *"This is a third-person rear-view **driving game** video of [subject + visible
> features], [environment], [style + one mood phrase]."*

Each word is load-bearing:

- **third-person**, camera outside the subject.
- **rear-view**, camera behind (not side/front/top); required for the
  WASD-forward → subject-forward mapping.
- **driving / riding / chase**, the subject is controlled as a vehicle. Adapt
  the verb: *riding game* for mounts (horse, dragon), *chase game* for
  non-vehicle subjects (a running retriever), *driving game* for vehicles.
- **game video**, the highest-leverage token. It pulls training data from
  racing/driving games (subject locked centre, camera bound to subject, no
  establishing shots, no aerial pull-backs) instead of cinematic film (free
  camera, wide shots). In storm_crossing testing, dropping **"game"** alone
  caused intermittent camera-detachment (the boat shrank to a distant dot).
  **Never omit "game" or "rear-view"**; only the middle verb flexes.

`base` carries subject identity + environment + style. **No POV phrasing beyond
the opener, no motion verbs**, those live in `camera`/`movement`.

### camera.static (no WASD)

Subject locked at exact frame centre, constant size and distance; neither
subject nor camera moves on its own. Describe only position.

> *"The [subject] is locked at the exact centre of the frame at constant size and
> distance; neither it nor the camera moves on its own."*

Target ~30-60 tok. Vehicles that tend to drift may need an explicit anti-drift
clause (citadel pads this to ~94 tok).

### camera.dynamic (WASD held)

Strict centred rear view; the camera tracks from behind as the subject travels
forward and never rotates independently. State the heading relationship as a
**geometric invariant**, never as input behavior:

> *"Strict centred third-person rear view: the [subject] is locked at the exact
> centre of the frame; the camera tracks it from behind as it moves forward and
> never rotates independently of it, and the [subject]'s heading turns with the
> camera so the rear-view framing is always preserved."*

Vary the framing keyword to the subject: dragon → *"rear view from above and
behind"*; boat → *"stern view"*; retriever → *"over-the-shoulder rear view"*.

### movement.static / movement.dynamic

- `static`, idle behavior: breathing, hovering, deck pitching with swells, paws planted. Rarely fully inert. If the subject tends to drift (a hovering
  dragon recedes backward), add explicit negative constraints (*"does not
  translate, does not drift backward, never recedes from the camera"*), they
  cost tokens, so use sparingly.
- `dynamic`, concrete forward-motion verbs + physical consequence: *"rolls
  forward over the cracked road, kicking up dust trails from the rear tires"*, *"wings beat in thunderous arcs driving it forward, shadow racing across the
  canopy below"*. Don't restate identity, `base` carries it.

### control semantics

WASD = forward translation of the subject (it is also a direct forward-motion
latent into the model, so `*.dynamic` prose must agree with it). Arrow-keys turn
heading, **not a model channel**, so never name them; the heading invariant in
`camera.dynamic` is what makes turning render correctly.

---

## 2. First-person traversal

The viewer *is* the subject, riding, piloting, descending, walking. POV is from
inside. (This is lingbot-prompts' "traversal mode".) A **bodiless flythrough**
through an environment with no vehicle/body is the same viewpoint with the body
anchor omitted, handle it here.

### base opener, first-person, world + visible body/vehicle

`base` carries the world + the parts of the body/vehicle that sit in the
foreground of the POV + style. Opener:

> *"First-person view from [the saddle of a colossal dragon / a submersible
> cockpit / a dune buggy], [the visible foreground: gloved hands on the reins,
> the viewport glass, the dragon's scaled neck stretching ahead], over
> [environment], [style + one mood phrase]."*

(For a **bodiless flythrough**, drop the body/vehicle clause: *"First-person
view gliding through [environment]…"*) For *prose* output, the traversal opener
*"The video presents a [soaring journey / slow descent / low race] through
[world]…"* works well and is the production prose convention, see
`references/prose-mode.md`.

### camera.static (no WASD)

First-person view holding steady; the visible foreground (hands / viewport /
the subject's neck-and-head ahead) framed; the view does not move on its own.

> *"First-person view from [the saddle]; [the dragon's head and neck] fill the
> lower frame; the view holds steady and does not move on its own."*

### camera.dynamic (WASD held)

First-person forward view; framing stays anchored to the POV as the world
streams toward and past the viewer. Heading as a geometric invariant:

> *"First-person forward view; [the foreground body/vehicle] stays anchored in
> frame as the world streams toward and past the viewer, the view always facing
> the direction of travel."*

### movement.static / movement.dynamic, the most viewpoint-specific layer

First-person motion is about **the world reacting to the viewer's advance**, and
**sensation** carries it:

- `static`, the vehicle/body idle and the world ambient: *"the dragon hovers, wings beating rhythmically, the saddle creaking and reins twitching; the
  jungle below stirs in the wind."* No net forward travel.
- `dynamic`, the world rushes past + sensation (the load-bearing anchor) + a
  **motion-resolution** clause (far-plane detail sharpening as you approach a
  destination, the traversal depth cue):

  > *"The world rushes past as the [dragon] surges forward, wind whips the
  > rider's gloved hands and the reins vibrate, the canopy streaming beneath;
  > ahead the [castle's stone spires] resolve steadily, their carved detail
  > sharpening against [the far ridge of floating islands]."*

The motion-resolution clause (*"X resolves / sharpens against [far backdrop]"*)
is what gives first-person traversal its sense of approach, include it whenever
there is a destination ahead. Omit it for aimless drift.

### control semantics

WASD = the viewer advances through the world (forward-motion latent). Arrow =
look/heading, never named; expressed as the "view faces the direction of
travel" invariant.

---

## 3. Spectator

A fixed observer of an ambient scene. **No controllable subject, no POV claim.**
(This is lingbot-prompts' "spectator mode": city-at-night, Japanese garden,
lakeside-at-dusk.) The scene is alive through ambient dynamics, wind, water,
light, drifting cloud, not through a driven subject.

### base, a plain scene statement, no POV

Do **not** open with "third-person", "first-person", or "the video presents a
journey". Open directly with the scene:

> *"A serene lakeside at dusk: [near] still water glassy in the foreground,
> [mid] a lone maple leaning over the shallows, [far] violet mountains under a
> peach sky. [style + one mood phrase]."*

`base` carries near/mid/far planes + style + the single mood phrase, exactly as
in third-person, minus any subject-identity / vehicle anchor (there is no driven
subject). If something *does* move in the scene (a distant bird, a person
walking through), it is **observed**, not driven, keep it as world detail, and
remember the single-subject / no-object-agency invariant still holds.

### camera, fixed framing

The observer holds a stable shot. State the framing and its constancy; there is
no subject to lock, so anchor on the *frame* instead:

- `camera.static`:
  > *"The camera holds a fixed [wide / medium] view of the [scene] at constant
  > distance and angle; the framing does not move on its own."*
- `camera.dynamic`: a true spectator has no driven subject, so WASD has little
  to do. Two legitimate choices, pick with the user:
  1. **Inert**, `dynamic` ≈ `static` (the framing simply holds; WASD changes
     nothing meaningful). Cleanest for "just watch the scene".
  2. **Gentle push-in**, because WASD is a forward-motion latent the model
     *will* react to, author `dynamic` as the viewpoint easing forward into the
     scene: *"the view eases forward and the [scene] draws nearer, the
     foreground [reeds] sliding past."* This shades toward a bodiless flythrough
     (§2), if the user wants WASD to meaningfully move them, prefer first-person
     traversal outright.

### movement, ambient world dynamics, not subject motion

There is no subject, so `movement` carries the scene's **ambient life**:

- `static`: *"Gentle ripples cross the water, the maple's leaves stirring
  faintly; thin mist drifts low over the far shore."*
- `dynamic`: if camera is inert, mirror `static` (or intensify the ambient
  motion slightly); if camera pushes in, describe the near plane sliding past.

### control semantics

WASD = at most a gentle forward drift of the viewpoint (or nothing). Arrow =
nothing meaningful; never named. Spectator scenes are usually **single-state,
overlay-only** worlds (atmosphere/event overlays like *nightfall*, *a
procession crossing*), transitions are rare because there is no subject to
transform.

---

## Choosing the framing keyword for `camera.dynamic`

| Subject | Keyword |
|---|---|
| Boat / ship / submarine | stern view / rear view |
| Car / vehicle | rear view (extra-strict anti-drift, see citadel) |
| Dragon / flying mount | rear view from above and behind |
| Horse / ground mount | over-the-shoulder rear view |
| Dog / running animal | over-the-shoulder rear view |
| First-person any | first-person forward view |
| Spectator | fixed [wide/medium] view |

Whatever the keyword, the invariant is the same: the framing is preserved
however the heading changes; the camera never rotates independently of the
subject; and you never name the input that drives it.
