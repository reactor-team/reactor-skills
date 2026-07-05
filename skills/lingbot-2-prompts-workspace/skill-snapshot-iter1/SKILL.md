---
name: lingbot-2-prompts
description: >
  Turn a loose scene idea (even a single short sentence, English or Chinese)
  into a complete LingBot-World V2 session package: one advanced base prompt
  plus the five keyboard-slot action prompts (f / g / u / o / space), emitted
  as prompt.txt content and a ready-to-use actions.json. Use whenever the user
  mentions LingBot 2, LingBot-World V2, lingbot-worldV2, action slots,
  actions.json, key-triggered events, a "playable character" video prompt, or
  gives a rough idea they want expanded into an interactive world-model prompt
  ("make a lingbot 2 prompt for a knight in the desert"). This is for the V2
  session format; the separate lingbot-world skill covers the V1 JSON
  state-machine format.
---

You are authoring inputs for **LingBot-World V2**, an interactive video world
model. A V2 session works like this: the model continuously generates video
conditioned on a text prompt. The **base prompt** is the standing condition,
it describes the world at rest and how input drives it. While the user holds
an **action key**, the condition is swapped for `base + " " + addendum`, one
extra sentence or three appended to the unchanged base. On release, the
condition reverts to the base.

Two consequences drive every rule below:

1. **The base prompt is always present.** Every addendum is appended after it,
   so an addendum must read as a *continuation* of the base, never contradict
   it, never re-describe it, and never re-anchor the camera.
2. **The model can only gate motion on real input channels** (WASD movement,
   arrow-key look, the action keys). Anything the base describes as moving
   will move on its own, forever. So the base states an explicit **motion
   contract**: exactly what moves, what is frozen, and which input causes what.

## Workflow

1. Pick the **camera regime** from the idea (§1).
2. Write the **base prompt** (§2).
3. Write the **five slot actions** (§3).
4. Assemble the **output package** (§4).

For a one-line ask, do all four without interrogating the user; only ask when
the idea is genuinely ambiguous between regimes (e.g. "a dragon" could be
playable or orbited). If the idea is in Chinese, keep the base prompt in the
user's Chinese and write addenda in English, that mix appears in production
data and works.

## 1. Pick the camera regime

Three regimes cover the production examples. Choose by what the user's idea
implies the player *does*:

| Regime | The player... | Signals in the idea |
|---|---|---|
| **Playable character** | drives a subject around with WASD, camera follows behind | "playable", "controls", "drives", "game", a vehicle/creature/object that travels |
| **Orbit (third-person locked subject)** | orbits the camera around a stationary centred subject with arrow keys | a character/creature/object to *look at*; portraits, statues, standing figures |
| **Fixed first-person** | pans the view from a single standpoint with arrow keys | "POV", "from the cockpit", "looking out over", vistas, dioramas, hands-in-frame setups |

A useful hybrid of orbit + first-person exists for **hands-in-frame** ideas
(rider's hands on reins, gloved hands holding a tool): treat it as orbit around
the held object, with the hands described at rest.

When the idea names no player verb at all, default: a mobile subject →
playable character; a stationary subject → orbit; a place → fixed first-person.

## 2. Write the base prompt

Target 60–110 words, one paragraph, present tense. Build it from these parts
in order. The motion-contract phrasings below are near-verbatim from
production sessions; keep their structure and substitute the bracketed parts,
they are the load-bearing sentences that make the world controllable instead
of a drifting video.

**Playable character:**

> A third-person gameplay video where [subject with concrete visual detail]
> is the playable character. The camera follows from behind and slightly
> above, like a modern 3D game. [Subject] [travels: slides/drives/runs/surfs…]
> [across environment] in response to keyboard arrow keys (or WASD), changing
> direction naturally with game-like movement and physics. [One physical
> constraint that keeps identity stable, e.g. "It always stays upright while
> sliding."] The scene looks like real gameplay with realistic lighting,
> smooth camera tracking, high-quality graphics, and an Unreal Engine 5 style.

**Orbit:**

> This is a third-person-view video of [subject with concrete visual detail]
> [posed] in [environment]. [Atmosphere phrase.] The [subject] is locked at
> the exact centre of the frame at constant size and distance. Neither the
> [subject] nor the camera moves on its own; arrow-key look-input is the only
> source of camera motion, orbiting the camera around the stationary [subject]
> only while held. [Freeze clause: the subject stands perfectly still, plus
> one or two ambient details explicitly held frozen, e.g. "the rain and steam
> held frozen in the air."]

**Fixed first-person:**

> This is a first-person-view video of [scene from the standpoint, name a
> foreground element that frames the view]. [Atmosphere phrase.] The viewpoint
> is fixed in place, framing the scene from a single standpoint. Nothing in
> the scene nor the camera moves on its own; arrow-key look-input is the only
> source of camera motion, panning the first-person view across the stationary
> [scene noun] only while held. [Freeze clause naming specific elements held
> still, e.g. "the tiny cars and trees frozen in place."]

For the hands-in-frame hybrid, use the orbit skeleton and end with an idle
clause instead of a freeze clause: "With no event key pressed, the [hands]
rest relaxed [on the tool/reins], ready to [act]."

Why the freeze clause matters: it is the negative space of the motion
contract. Without it the model animates rain, fish, traffic on its own and
the arrow keys stop feeling causal. Name two or three *specific* things that
stay still rather than saying "everything is static".

Populate the scene while you're at it: mention one or two concrete secondary
objects (a discarded filter, a distant fire escape, a moss-covered castle).
The action addenda will need nearby and distant targets, and targets work far
better when the base already placed them or the scene plausibly contains them.

## 3. Write the five slot actions

One action per slot, fixed semantics. Every addendum is 1–3 sentences
(roughly 25–60 words), present tense, and repeats the subject by the same noun
phrase the base uses. Labels are 2–4 words in Title Case.

**`f` — contextual scene event.** Something happens *around* the subject: a
secondary creature appears, or the subject performs a small in-character
interaction with a nearby object. When a new entity enters, open with the
subject-preservation clause so the model doesn't re-imagine the frame:
"The original focal subject remains the main subject, unchanged in pose and
position, while [a small tan puppy emerges from the dunes to the right…]".
Examples: *Puppy Emerges*, *Birds Flutter Past*, *Driver Engages Gearbox*,
*Ant Tips Water Droplet*.

**`g` — environment transformation.** A global weather / lighting / season
change sweeping the whole scene while the subject stays untouched: snowfall
blanketing the dunes, sunset shifting the palette, a district flooding.
Describe what the transformation does to two or three named surfaces of the
scene ("covering the wet cobblestones, brick walls, and streetlamps in thick
white drifts"). Examples: *Desert Snowfall*, *Sunset Glow*, *Snow-Covered
Alley*.

**`u` — melee strike.** The subject physically strikes a **nearby** concrete
object, with visible destruction. Shape: wind-up → impact → material
consequence (shatters, splinters, cracks, sprays). The target must be
something the scene plausibly contains at arm's reach. Examples: *Shield
Bash*, *Extinguisher Bash*, *Mandible Snap*.

**`o` — ranged attack.** A projectile event with a full visible arc. Shape:
source (hand, weapon, mouth, vehicle) → projectile with a described trajectory
("streaks across the sand", "leaving a trail of bubbles") → strikes a
**distant** named target → impact aftermath (explosion, sparks, dust plume).
Fit the projectile to the world's tone: a knight casts lightning, an F1
cockpit underwater shoots a torpedo, a jet-ski rider fires a flare gun, an
ant fires spittle. Examples: *Casts Fireball*, *Fires Flare Gun*, *Shoots
Torpedo*.

**`space` — jump.** Always exactly:
`The character jumps high into the air.` with label `Jump`. This is a fixed
runtime convention; do not customize it.

Even for non-violent or absurd subjects, still fill `u` and `o`, the
production data does (a cigarette pack slams a cigarette butt and fires a
glowing ember). Invent an in-world-plausible strike and projectile rather
than skipping the slot; keep it physical, not gory.

**Addendum discipline** (the appended-after-base consequence):

- Never restate the camera lock or the input contract inside an addendum, the
  base already says it. (Exception: the `f` subject-preservation clause,
  which restates *subject* stability only.)
- Never contradict the base's freeze clause except for the one thing the
  action animates.
- End on a settled note ("before coming to rest beside the pack"), the world
  must be able to revert to the base when the key is released.
- Write the addendum as one short, completable beat (an event that could fully
  play out in a few seconds). Live-session testing shows the model conditions
  on its own recent frames: during a long hold, drift accumulates (subject
  identity morphs, colors smear) and releasing the key cannot restore a world
  that has already drifted. An addendum that implies open-ended ongoing action
  invites exactly those long holds; a bounded beat gives a clean press-release
  cycle. The same applies to camera input, which is why the base prompt's
  "only while held" contract matters: brief inputs, settled world between them.

## 4. Assemble the output

Emit two blocks, in this order. If the user gives a directory, write the files
(`prompt.txt`, `actions.json`) there instead and confirm the paths.

**`prompt.txt`** — the base prompt, nothing else.

**`actions.json`** — this exact shape (it mirrors the inference-session export
format, so it can be dropped straight into tooling):

```json
{
  "actions": [
    {
      "id": "f#0",
      "slot": "f",
      "cand_index": 0,
      "label_en": "Puppy Emerges",
      "addendum_en": "<the addendum>",
      "prompt_en": "<base prompt> <the addendum>",
      "label_zh": "Puppy Emerges",
      "addendum_zh": "<same as addendum_en>",
      "prompt_zh": "<same as prompt_en>",
      "selected": false
    }
  ]
}
```

Rules: one entry per slot in order `f, g, u, o, space`; `id` is
`<slot>#<cand_index>` with `cand_index` 0 unless the user asks for multiple
candidates for a slot; `prompt_en` is the base prompt, a single space, then
the addendum, verbatim, build it mechanically, never paraphrase; `_zh` fields
duplicate `_en` unless the user supplies Chinese labels/addenda.

Then close with one short line inviting targeted edits ("want a different `o`
projectile or a second `u` candidate?"). On feedback, edit only the named
fields and rebuild the affected `prompt_en` strings.

## Worked example

Idea: *"a rubber duck in a bathtub"*.

Regime: small stationary subject to look at → **orbit**.

Base: "This is a third-person-view video of a bright yellow rubber duck
floating at the centre of a white porcelain bathtub filled with still,
soap-clouded water. Cozy bathroom atmosphere, warm light from a frosted
window. The duck is locked at the exact centre of the frame at constant size
and distance. Neither the duck nor the camera moves on its own; arrow-key
look-input is the only source of camera motion, orbiting the camera around
the stationary duck only while held. The duck sits perfectly still on the
water, the soap bubbles along the rim and the drips on the chrome faucet held
frozen in place."

Actions: `f` *Bubble Drifts By* (preservation clause + a single soap bubble
drifting past and popping on the rim); `g` *Steam Fills Room* (steam fogging
the mirror and softening the light); `u` *Beak Jab* (the duck jabs its beak
into a nearby soap bar, cracking off a chip that plops into the water);
`o` *Spits Water Jet* (a thin jet arcs across the tub and knocks a shampoo
bottle off the far rim); `space` Jump, fixed string.

## References

- `references/examples.md` — four complete production sessions (one per
  regime plus the hands-in-frame hybrid), verbatim from the model team's
  export data. Read it when unsure how a regime or slot should sound.
