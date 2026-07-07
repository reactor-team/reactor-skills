---
name: lingbot-2-prompts
description: >
  Turn a loose scene idea (even a single short sentence, English or Chinese)
  into high-quality LingBot-World V2 prompts: either a single-shot standalone
  prompt, or a full session package (one advanced base prompt plus action-key
  prompts — the f and g slots, a variable set of numbered event keys 1..N,
  and the space jump — emitted as prompt.txt content and a ready-to-use
  actions.json). Use whenever the user mentions LingBot 2, LingBot-World V2,
  lingbot-worldV2, action slots, actions.json, event keys, key-triggered
  events, a "playable character" video prompt, or gives a rough idea they
  want expanded into an interactive world-model prompt ("make a lingbot 2
  prompt for a knight in the desert"). This is for the V2 session format;
  the separate lingbot-world skill covers the V1 JSON state-machine format.
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

0. Decide the **deliverable**: a full session package (default), or a
   **single-shot prompt** when the user asks for just one prompt with no
   actions ("just the prompt", "no action keys", "single-shot", "one prompt
   only"). A single-shot prompt is the base prompt standing alone — all of
   §1 and §2 apply to it unchanged, then skip §3 and emit only the prompt.
   The base prompt is where the craft lives; the slots are an optional layer
   on top of it, not the reason for it.
1. Pick the **camera regime** from the idea (§1).
2. Write the **base prompt** (§2).
3. Write the **action keys** (§3) — package deliverable only.
4. Assemble the **output** (§4).
5. Generate the **seed image** (§5) — Reactor-internal only, on by default.
   LingBot-World V2 needs a prompt and an image together to start a session;
   don't skip this unless the user says they already have their own image.

For a one-line ask, do all of this without interrogating the user; only ask
when the idea is genuinely ambiguous between regimes (e.g. "a dragon" could be
playable or orbited). Language: write everything in **English** — base
prompt, addenda, labels. The Chinese scattered through the lab's exports is
the operators' hand-typed working language, not a model requirement; the
model handles both and the same sessions mix them freely. Only write Chinese
when the user's own idea is in Chinese (keep their base prompt in their
words) or when they explicitly ask for it.

## 1. Pick the camera regime

Three regimes cover the production examples. Choose by what the user's idea
implies the player *does*:

| Regime | The player... | Signals in the idea |
|---|---|---|
| **Playable character** | drives a subject around with WASD, camera follows behind | "playable", "controls", "drives", "game", a vehicle/creature/object that travels |
| **Orbit (third-person centred subject)** | orbits the camera around a stable centred subject with arrow keys | a character/creature/object to *look at*; portraits, statues, standing figures |
| **First-person anchor** | orbits the view around a stable in-frame anchor with arrow keys | "POV", "from the cockpit", "looking out over", vistas, dioramas, hands-in-frame setups |

First-person prompts anchor on a **named foreground element** — the driver's
wheel and dashboard, gloved hands on a tool, a flashlight beam, even a
landmark filling the vista — and reuse the orbit contract around that anchor.
(Older exports instead wrote "the viewpoint is fixed in place… panning the
first-person view across the stationary scene"; that variant still works, but
the newest lab sessions all use the anchor form. Prefer the anchor form.)

When the idea names no player verb at all, default: a mobile subject →
playable character; a stationary subject → orbit; a place → first-person
anchor, picking a plausible foreground element to anchor on.

These regimes set the *default* look-input behaviour. A camera move the user
asks for by name (orbit sweep, push-in, crane up, pull back to a wide shot) is
layered on top of the chosen regime — see **Requested camera moves** at the end
of §2.

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
> [posed] in [environment]. [Atmosphere phrase.] The [subject] remains at
> the exact centre of the frame at constant size and distance. Neither the
> [subject] nor the camera moves on its own; arrow-key look-input is the only
> source of camera motion, orbiting around the stable [subject] only while
> held. With no event key pressed, [idle clause: the subject holds a specific,
> interaction-ready rest pose, plus one or two ambient details explicitly
> still, e.g. "the snowboarder stands balanced on the board, arms relaxed at
> their sides, ready to carve."]

**First-person anchor:**

> This is a first-person-view video of [scene from the standpoint, naming the
> foreground anchor: hands on a tool, wheel and dashboard, a flashlight beam,
> a landmark]. [Atmosphere phrase.] The [anchor] remains at the exact centre
> of the frame at constant size and distance. Neither the [anchor] nor the
> camera moves on its own; arrow-key look-input is the only source of camera
> motion, orbiting around the stable [anchor] only while held. With no event
> key pressed, [idle clause, e.g. "the driver's gloved hands stay relaxed on
> the wheel, ready to steer or shift gears."]

Why the idle clause matters: it is the negative space of the motion contract
and the rest state every event key returns to. Without it the model animates
rain, fish, traffic on its own and the keys stop feeling causal. Name two or
three *specific* things that stay still rather than saying "everything is
static". An older generation of exports ended with a freeze clause instead
("the rain and steam held frozen in the air") and hard-locked wording ("is
locked at the exact centre… the stationary officer"); that form still works,
but the newest lab sessions use "remains … stable …" plus the "With no event
key pressed" idle clause — use those unless matching an existing session.

Populate the scene while you're at it: mention one or two concrete secondary
objects (a discarded filter, a distant fire escape, a moss-covered castle).
The action addenda will need nearby and distant targets, and targets work far
better when the base already placed them or the scene plausibly contains them.

### Requested camera moves

The regimes above describe the *default* camera behaviour. When the idea also
asks for a **specific directed camera move** — "orbit around it", "push in",
"crane up and look down", "pull back to a wide shot", "arc around", "whip-pan",
"dolly toward" — one rule governs every one of them:

**The camera performs the move; the subject stays perfectly still and the
environment stays consistent.** Name the *camera* as the thing that moves, and
say the subject holds its pose, position, and identity while the scene around it
stays fixed. Omit this and the model drags the subject along with the camera — a
"crane up" becomes the subject sinking, an "orbit" spins the subject instead of
the view. It is the idle clause again, now stated against a moving camera
rather than against held look-input.

Phrasing (present tense, same subject noun the base uses):

> The camera [orbits around / pushes straight in toward / cranes up above /
> pulls back from] the [subject], which stays perfectly still, holding its pose
> and position while the [environment] stays fixed around it[, framing detail].

Keep the framing detail honest to the move:

- **Framing-preserving (orbit, arc):** add "at the exact centre of the frame at
  constant size and distance."
- **Framing-changing (push-in, crane, pull-back / reveal):** state how the
  subject's size or position in the frame changes ("growing larger in the
  frame", "sinking lower as the viewpoint climbs", "growing smaller as the
  viewpoint retreats") — never "constant size and distance", which would
  contradict the move.

Place it by scope. If the move is the *standing* behaviour the user wants
throughout, fold it into the base's motion contract in place of the look-input
clause. If it is a *triggered* or one-time move, write it as an addendum under
the §3 discipline — one bounded beat that settles, subject and environment
preserved, so releasing the key returns cleanly to the base. Either way, one
sentence naming the camera's move and the subject staying still is enough; don't
restate the whole camera contract.

## 3. Write the action keys

The layout is `f`, `g`, a run of **numbered event keys** `1..N`, then
`space`. Choose N to fit the idea — production sessions run from zero
numbered keys (just `f` and `g`) up to seven; 2–5 is typical. Default to
around 3 for a casual ask, more when the idea implies a sequence or arsenal.
Every addendum is present tense and repeats the subject by the same noun
phrase the base uses. `f`/`g` labels are 2–4 words in Title Case; numbered
keys are labelled `Key 1`, `Key 2`, … (or, for very short addenda, the
addendum text itself, as production data does).

**`f` — contextual scene event.** Something happens *around* the subject: a
secondary creature appears, or the subject performs a small in-character
interaction with a nearby object. 1–3 sentences (roughly 25–60 words). When
a new entity enters, open with the subject-preservation clause so the model
doesn't re-imagine the frame: "The original focal subject remains the main
subject, unchanged in pose and position, while [a small tan puppy emerges
from the dunes to the right…]". Examples: *Fluttering Moths*, *Dolphin
Leap*, *Wandering Fox*, *Friendly Camel Approach*.

**`g` — environment transformation.** A global weather / lighting / season
change sweeping the whole scene while the subject stays untouched: snowfall
blanketing the dunes, sunset shifting the palette, a district flooding — up
to a full scene-identity swap (a dim bar dissolving into a grand library).
Describe what the transformation does to two or three named surfaces of the
scene ("covering the wet cobblestones, brick walls, and streetlamps in thick
white drifts"). Examples: *Shifting Dunes*, *Sunset Glow*, *Snowy Blizzard*,
*Bar Transforms to Library*.

`f` and `g` can also be a **paired toggle** when the subject has an obvious
binary state: flashlight on (`f`) / flashlight off (`g`), headlights on /
wipers sweeping. Toggle addenda can be a single short sentence.

**Numbered keys `1..N` — freeform event keys.** Each is one discrete event,
and this is where the session's personality lives. Recurring shapes in the
production data:

- **Single beat** — a boost with light trails, a prop appearing, a spat
  projectile, a melee strike on a nearby object, a light effect. Follows the
  full addendum discipline below. For attack beats keep the classic shape:
  wind-up → trajectory → named target → material aftermath (sparks, debris,
  scorch marks); fit the weapon to the world's tone.
- **Subject transformation** — the sandboard becomes a flying carpet and the
  rider soars above the dunes. State the new stable behaviour it settles into.
- **Scene teleport** — a fog/light/water transition swallows the frame and
  the world arrives somewhere new ("Thin mist covers the frame; as it clears,
  the view arrives before the Pyramids of Egypt…"). Name the transition
  device, then establish the new scene's key elements.
- **Chained sequence** — keys designed to be pressed in order, each link
  opening by resolving the previous one ("the zombie is swallowed by
  darkness and fades… the ward door swings open and a vampire stands
  inside…") and closing with the new state established. Use when the idea is
  a journey, an escalation, or a boss gauntlet; write the whole chain as one
  storyboard so the hand-offs are explicit.

**`u` / `o` — legacy combat slots.** Earlier exports used fixed `u` (melee
strike on a nearby object) and `o` (ranged attack on a distant target)
slots; the newest sessions fold those beats into numbered keys instead.
Only emit `u`/`o` slots when the user asks for that layout or wants a pool
of attack candidates on one key (combat-heavy sessions still ship `o` with
many `cand_index` variants).

**`space` — jump.** Always exactly:
`The current controllable subject springs upward into the air.` with label
`Jump`. This is a runtime convention; do not customize it. (The older string
"The character jumps high into the air." appears in earlier exports.)
Include `space` by default; drop it only if the user says they don't want a
jump key.

**Addendum discipline** (the appended-after-base consequence):

- Never contradict the base's idle clause except for the one thing the
  action animates.
- You don't need to restate the camera lock or the input contract inside an
  addendum — the base already says it. The one required restatement is the
  `f` subject-preservation clause (subject stability only). Newer lab
  exports sometimes re-open `f`/`g` addenda with the full centre-lock
  sentence too; that's tolerated by the model but adds nothing — don't
  imitate it.
- For **single-beat** keys, end on a settled note ("before coming to rest
  beside the pack") so the world can revert to the base on release, and keep
  the beat completable in a few seconds. Live-session testing shows the
  model conditions on its own recent frames: during a long hold, drift
  accumulates (subject identity morphs, colors smear) and releasing the key
  cannot restore a world that has already drifted. The same applies to
  camera input, which is why the base prompt's "only while held" contract
  matters: brief inputs, settled world between them.
- **Transformation, teleport, and chain keys** intentionally move the world
  forward and do not revert — that is their design. Still end each one in a
  new *stable* state (the carpet glides steadily, the new vista stands
  still), never in open-ended accelerating motion, so the next input starts
  from a settled frame.

## 4. Assemble the output

**Single-shot deliverable:** emit the prompt alone (as `prompt.txt` when the
user gives a directory, otherwise inline) and stop — no actions.json, no
action keys. Close by offering to extend it into a full package if they later
want key-triggered events.

**Package deliverable:** emit two blocks, in this order. If the user gives a
directory, write the files (`prompt.txt`, `actions.json`) there instead and
confirm the paths.

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

Rules: one entry per key in order `f, g, 1, 2, …, N, space` (legacy `u`/`o`
entries, when requested, go between `g` and the numbered keys); `id` is
`<slot>#<cand_index>` with `cand_index` 0 unless the user asks for multiple
candidates for a slot; `prompt_en` is the base prompt, a single space, then
the addendum, verbatim, build it mechanically, never paraphrase; `_zh` fields
duplicate `_en` unless the user supplies Chinese labels/addenda (for a
Chinese addendum, put it in both `_en` and `_zh` fields, as production
exports do).

Then close with one short line inviting targeted edits ("want a different
Key 2 event or a second `f` candidate?"). On feedback, edit only the named
fields and rebuild the affected `prompt_en` strings.

## 5. Generate a seed image (Reactor-internal)

LingBot-World V2 starts a session from a **prompt and an image together**;
the prompt alone can't be handed to the model. Generate the matching seed
image as a standard part of every deliverable (single-shot or package),
right after the base prompt is finalized. One seed image per deliverable —
it seeds the base prompt only, since the slot addenda modify an
already-running session rather than starting a new one.

**Derive the image prompt from the base prompt**, don't write it from
scratch. Take the finished base prompt and:

- Drop every input/motion-contract clause: "in response to keyboard arrow
  keys", "the camera follows", "arrow-key look-input is the only source of
  camera motion", the "With no event key pressed" idle clause, freeze
  clauses, anything conditioned on a key being held. A still image has no
  input to react to — but keep the *pose* the idle clause describes, recast
  as plain description ("standing balanced on the board, arms relaxed").
- Keep every concrete visual noun, the framing/positioning language, the
  atmosphere phrase, and any render-style tags (Unreal Engine 5 style,
  realistic lighting, cinematic) — these carry over unchanged and are what
  keep the image and the base prompt visually consistent.
- Recast the opening as a still frame: "A third-person-view still frame
  of…" / "A first-person-view still photo of…" rather than "a video of…".
- Keep it one paragraph, same subject noun phrase as the base prompt.

Then call the generation tool:

```
python3 <skill-dir>/tools/generate_seed_image.py "<derived image prompt>" seed.png
```

Pass `--aspect-ratio` (default `16:9`) to match the intended frame; use
`9:16` for a portrait/mobile session. The script fetches the Replicate API
token from the shared Reactor 1Password vault ("Replicate API Token" item)
via the `op` CLI and calls Replicate's `google/imagen-4`, so it only works
from a machine signed into that vault (`op account list` to check) — it's
not part of the portable skill definition if this ever moves to a
public/external repo.

If the script fails (no `op` session, vault access, network), don't block
on it: still deliver `prompt.txt`/the single-shot prompt and `actions.json`,
tell the user the seed image generation failed and why, and give them the
derived image prompt so they can generate it another way.

## Worked example

Idea: *"a rubber duck in a bathtub"*.

Regime: small stationary subject to look at → **orbit**.

Base: "This is a third-person-view video of a bright yellow rubber duck
floating at the centre of a white porcelain bathtub filled with still,
soap-clouded water. Cozy bathroom atmosphere, warm light from a frosted
window. The duck remains at the exact centre of the frame at constant size
and distance. Neither the duck nor the camera moves on its own; arrow-key
look-input is the only source of camera motion, orbiting around the stable
duck only while held. With no event key pressed, the duck bobs gently in
place on the still water, the soap bubbles along the rim and the drips on
the chrome faucet holding still."

Actions: `f` *Bubble Drifts By* (preservation clause + a single soap bubble
drifting past and popping on the rim); `g` *Steam Fills Room* (steam fogging
the mirror and softening the light); `1` a single beat — the duck spits a
thin water jet that arcs across the tub and knocks a shampoo bottle off the
far rim, ending settled; `2` a transformation — the duck grows to fill the
tub, the bathroom now toy-sized around it, settling into a steady float;
`3` a teleport — the bathwater swells into open ocean at sunset, the duck
bobbing on gentle swells with the bathroom gone; `space` Jump, fixed string
"The current controllable subject springs upward into the air."

Seed image prompt (derived per §5, motion/input clauses dropped): "A
third-person-view still frame of a bright yellow rubber duck floating at
the centre of a white porcelain bathtub filled with still, soap-clouded
water. Cozy bathroom atmosphere, warm light from a frosted window. The duck
is centred in frame at medium distance, soap bubbles along the rim and
drips on the chrome faucet."

## References

- `references/examples.md` — five complete production sessions verbatim from
  the model team's export data, covering all three regimes, toggle keys,
  transformation and chained numbered keys, and the legacy `u`/`o` slot
  layout. Read it when unsure how a regime or key should sound.
- `tools/generate_seed_image.py` — Reactor-internal script that turns a
  derived image prompt into a downloaded seed image via Replicate. See §5.
