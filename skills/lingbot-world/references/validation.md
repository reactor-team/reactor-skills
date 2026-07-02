# Validation, anchors, red flags, rationalization defense, self-checks

Read this when validating a world (after writing or iterating) or when something
feels off but the failure mode isn't obvious. Four parts: the **anchor
checklist** (what must be present), the **red-flag catalog** (what to strip), the
**rationalization defense** (tempting mistakes vs. reality), and the **R1-R9
self-checks** (whole-scene structural rules, mostly for multi-state JSON worlds).

---

## Part A, Anchor density checklist

Apply to every **composed** prompt (not to a single fragment): each state at
rest (`base + camera.static + movement.static`) and in motion
(`…dynamic`), and any high-density event's override-plus-detail taken alone.

The six anchors:

- **POV**, the framing. Third-person: *"rear view", "stern view", "over-the-
  shoulder"*. First-person: *"first-person view from…"*. Spectator: the **fixed
  framing** statement stands in for POV (there's no subject framing to lock).
  Carried by `camera` (+ the `base` opener).
- **Subject identity**, what the subject is, vivid enough to recognize. Carried
  by `base`. **Spectator worlds have no driven subject**, the anchor becomes the
  scene's principal feature (the lake, the garden) instead.
- **Near-plane**, what's directly around / on the subject or in the foreground.
- **Mid-plane**, the focal element ahead.
- **Far-plane**, backdrop / horizon / depth anchor.
- **Atmosphere / sensation**, light, weather, physical cause-and-effect. The
  most load-bearing and most-skipped. Sensation tells the model the physics
  governing how the world reacts to motion; without it, motion feels detached.

Missing an anchor → the input is under-specified; invent it. Place the single
mood phrase as the closing clause of `base`. Near/mid/far must all be named, or
parallax collapses to flat wallpaper-scroll.

**What works:** dense clausal anchors (each sentence ≥2 anchors + a concrete
detail); style words as domain switches ("watercolor", "pixel art", "steampunk")
inside the mood phrase; explicit named style (photoreal / cartoon / sci-fi /
painterly are all well-supported).

**What doesn't:** imperative camera verbs; multiple focal elements in one event
(split, or demote one to background); object-level interaction ("pick up", "open
the door"); overloaded mood (three descriptors average into mush); multi-character
scenes; sessions longer than ~60s (spatial memory drifts, design bounded
experiences).

---

## Part B, Red flags (run on every fragment you write or re-write)

### Cross-fragment

1. **POV phrasing in `base`** beyond the viewpoint opener → move to `camera`.
2. **Motion verbs in `base`** (*"glides forward"*) → move to `movement.dynamic`.
3. **Subject restated in `movement` or `detail`** → drop it; `base` carries
   identity.
4. **Imperative camera verbs anywhere** (*pan/tilt/dolly/track/orbit/rotate*) →
   strip; positional only.
5. **Input vocabulary anywhere** (*arrow-key/look-input/WASD/while held*) →
   remove entirely; restate as a geometric invariant.
6. **Tag-soup stack at the end** (*"cinematic, 8k, photoreal"*) → bake into
   physical language.

### Camera-axis

7. **`camera.static` with unqualified motion verbs** (*"the camera orbits the
   subject"*) → rewrite without motion verbs (and never qualify with "while
   held", see invariant 5).
8. **`camera.dynamic` describing rotation around the subject** → strip;
   third-person dynamic is strict rear view, the heading invariant does the work.

### Event-axis

9. **Action event missing `{static, dynamic}`** when it should differ in motion →
   split into the object form.
10. **Detail-only event referencing another event's presence/absence** → rewrite
    to coexist with any other held event.
11. **High-density override with <6 anchors** → add the missing anchors; it's a
    standalone prompt.
12. **Framing-change override without explicit camera-lock language** → add the
    three-part lock (positive framing / what the camera must not do / why).
13. **Atmosphere/lighting override without back-coupling onto ≥2 preserved
    surfaces** → add the interaction effects.

### Token-budget (JSON worlds)

14. **Declared done without running `scene_report.py`** → measure. Estimating is
    unreliable on UMT5 and skips structural warnings.
15. **A composition >480 soft target** → rebalance (`references/token-budget.md`):
    trim `movement`, then `camera`, never `base` geometry.
16. **A composition >512** (`BASELINE VIOLATION`) → hard fail; the tail truncates.
    Rescope or trim aggressively.
17. **Auto-probing multi-event combinations no one asked about** → stop; validate
    per-event-alone, check combos only on request.

### Iteration

18. **Edited a field the user didn't name** → revert. Validated prose is sacred.
19. **Paraphrased an unchanged layer while editing another** → revert the
    paraphrase; surface drift accumulates across turns.

---

## Part C, Rationalization defense

| Tempting thought | Reality |
|---|---|
| *"The user said 'zoom in slowly', so I'll keep it."* | Camera verbs in text degrade output regardless of intent. Strip silently; mention only if they ask for annotations. |
| *"A tracking shot would be more cinematic."* | The model can't gate camera motion on input, it renders it always. All camera operation lives in control signals, never in text. |
| *"They gave me four mood words; I'll honor them all."* | Multiple moods average into mush. Pick the most physically anchored one; translate the rest into world anchors. |
| *"I'll add 'photoreal, 8k, volumetric' for fidelity."* | Image-model tags don't steer this model. Replace with specific physical light ("warm low-angle sunlight"). |
| *"Six sentences gives the model more to work with."* | The 2-4 sentence cap holds; densify within clauses, not by adding sentences. |
| *"'A dragon flying over a castle' → watch it from outside."* | For an interactive world, default to the subject being the *controllable* thing (third-person from above-and-behind, or first-person rider) unless the user wants a spectator. |
| *"WASD scene → write 'rear-view tracking as it moves' in `base`."* | That's `camera.dynamic`. `base` is constant across movement and carries no POV beyond its opener. |
| *"I'll restate the subject in each event so it's self-contained."* | Don't, the encoder gets identity from the composed `base`; restating burns budget and risks contradiction. |
| *"For interactivity, every event should override all layers to be safe."* | The default is detail-only. Override only when appending would contradict or under-fit. Detail-only events stack and iterate more easily. |
| *"The target says base ~140; the user wants 180, I'll cut it."* | Targets are starting values, not caps. If the worst-case composition fits ≤480, leave it. |
| *"I'll estimate tokens by character count."* | UMT5 varies 50+ tok by vocabulary. Run `scene_report.py` / `token_count.py`; never estimate. |
| *"Small JSON change, I'll skip the report this time."* | The report is cheap and catches orphan state references, over-budget shifts, dead-ends. Re-run after every edit. |
| *"This is a spectator scene, but let me add a rear-view camera lock anyway."* | Spectator has no driven subject; don't import the third-person rear-view lock. Use a fixed-framing statement (`references/viewpoints.md` §3). |

---

## Part D, Self-checks (R1-R9)

Run after any new event or substantive edit. R1, R6b, R7 are mechanically
checked by `scene_report.py`; the rest are read-throughs. (R1-R6 mostly concern
multi-state worlds; single-state overlay scenes still run R7-R9.)

- **R1, No dead-end states.** Every state (in a multi-state world) needs ≥1
  outgoing transition. A state you can enter but never leave is a trap.
  *(scene_report.py flags this.)* Example: storm_crossing's `flying_calm` was a
  trap until *Land* was added.

- **R2, Identity continuity across transformations.** A transition that
  transforms the subject must leave the destination state's `base` describing the
  *post*-transformation form, `underwater_calm.base` describes a submarine
  (sealed shutters, folded antennas, periscope), not still "a boat".

- **R3, Camera invariant preserved across all events.** The rear-view /
  subject-centred lock (third-person) is scene-wide. Default to **inheriting**
  `camera`. If an event overrides it, the override must carry the full lock
  language; if it suppresses it, prefer rewriting to inherit (suppression is
  fragile). (Spectator: the fixed-framing statement is the invariant instead.)

- **R4, Transformations need progressive detail.** A cross-form transition must
  describe an articulated sequence (≥3-4 micro-events), *"concealed bays crack
  open → panels rotate outward → segments hinge into place → jet pods slide out →
  ignition"*, not "the wings appear". Hand-waved transformations render as stiff
  teleportation.

- **R5, Transition end-state matches the destination's first frame.** Inventory
  the visible features at the end of the transition prose (antennas folded, deck
  cased, periscope extended) and confirm they line up with the destination
  state's `base + movement.static`. Mismatches pop on commit.

- **R6, Put the becoming-prose in the layer that's changing; states describe the
  stable condition.**
  - (a) *Verb discipline:* transitions use becoming-verbs (*begins, parts, widens, ignites, retracts*); states use being-verbs (*spans, rolls, glows, drifts*). A state's `base` must read as a stable snapshot, not "the storm is
    clearing now".
  - (b) *Layer placement:* override the layer the change acts on, sky/weather →
    `base`; subject form/motion → `movement`; framing → `camera`. **Not
    `detail`.** If becoming-prose sits in `detail` while `base` inherits the
    pre-change stable prose, both reach the encoder and contradict. `detail` is
    for supplementary back-coupling that doesn't contradict. *(This is the most
    common authoring error, see storm_crossing's* Storm break *for the canonical
    right-shape.)*
  - (c) *Inter-layer consistency:* within a state, the three layers describe one
    scene at rest and must not contradict; subject-specific framing words ("square
    transom", "saddle horn") must not leak into a state where the subject lacks
    that feature.

- **R7, Token budget on every composition.** Every state (rest + motion) and
  every event over every `from`-state (both branches) must fit ≤480 soft / 512
  hard. *(scene_report.py sweeps all of these.)* Common bloat: verbose camera
  prose, heavy negation in `movement.static`, detail that restates state content.

- **R8, Event signal share.** An event's own authored prose must be a meaningful
  fraction of its composed-while-held prompt, or the model drowns it in the
  inherited state. Bands and fixes in `references/token-budget.md`. Fix by
  trimming the state's inherited layers (highest leverage), moving content into a
  layer override, or making the detail more concrete and distinctive.

- **R9, One persistent subject noun; form variants by modifier, not head-noun
  swap.** Across every layer and detail, refer to the driven subject by **one**
  head noun (storm_crossing: "boat" everywhere). Describe forms as modifiers, *"the boat in submarine form"*, *"the now-winged boat"*, not *"the
  submarine"/"the aircraft"*. The slight awkwardness preserves the model's track
  on a single controllable subject (and keeps the WASD target stable). Each
  non-default form's `base` needs ≥3-4 concrete distinguishing features, ≥1 of
  them interacting with the environment.
