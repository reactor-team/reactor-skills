---
name: lingbot-prompts
description: Use when writing a text prompt for LingBot-World (the open-source interactive world model) from a rough scene or experience idea, for example "make me an experience where you ride a dragon." Covers the shape of a good single prompt: scene, physical sensation, one focal event, mood, and the camera rules the model needs.
---

# LingBot-World Prompts

LingBot-World is an open-source world model that generates interactive, navigable
video from three inputs: a **seed image**, **control signals** (camera poses or
WASD/mouse actions that drive movement), and a **text prompt**. This skill turns
a rough idea into one well-shaped text prompt.

Your job: take a loose input (a single noun, a sentence, "an experience where you
ride a dragon") and return a single, dense, production-ready prompt. Output the
prompt only, with no labels or explanation, unless the user asks for more.

## What the text prompt is for

The text prompt steers **content, style, physical dynamics, and atmosphere**, and
it states **where the camera sits relative to the subject**. It does **not** drive
the camera. Movement comes from the control signals, not from words.

**The single most important rule: no imperative camera verbs in the prompt.**
Words like *pan, tilt, zoom, dolly, track, push in, pull back, orbit, fly through*
make the model move the camera continuously whether or not anyone is steering.
Describe **position** ("a rear view," "the subject centered in frame," "a
low-angle view from the saddle"), never **operation**.

## The shape of a good prompt

```
{scene}. {sensation}. {focal event}. {mood}.
```

Two to four sentences. Densify by extending clauses inside sentences, not by
adding more sentences.

| Part | What it does | Example |
|---|---|---|
| **scene** | Where we are, and if moving, how we move through it | "a soaring flight over a fantasy jungle" / "a serene lakeside at dusk" |
| **sensation** | One physical cause-and-effect detail that grounds the world. The most important and most-skipped part. | "wind tears past, vibrating the leather reins" |
| **focal event** | The one thing that moves, resolves, or reveals. One only. In motion, name what sharpens as you approach, against a backdrop. | "a distant castle resolves steadily against a hazy horizon" |
| **mood** | One closing atmosphere phrase. Not three stacked adjectives. | "vast and windswept" |

## First-person vs. watching

Decide who the viewer is, because it sets the point of view and the opening words:

- **First-person (you are in it)**: riding the dragon, piloting the craft, walking
  the corridor. Open with **"The video presents..."** and name what is right
  around the viewer (saddle, reins, gauntleted hands, a cockpit edge).
- **Spectator (you watch from a fixed point)**: a creature crossing a valley you
  observe, a quiet room. Open directly with the scene, no "The video presents."

When the input is ambiguous ("a dragon over a castle"), default to first-person
and put the viewer on the subject. It produces richer, more dynamic results.

## What every prompt needs

Make sure all of these are present. If one is missing, the input is
under-specified, so invent it rather than skip it:

- **Point of view** (first-person or spectator; framing)
- **Subject and your vantage** (the dragon and the saddle/reins you ride it with)
- **Near plane** (what is directly around the viewer)
- **Mid plane** (the focal element you move toward or watch)
- **Far plane** (backdrop, horizon, depth)
- **Atmosphere** (light quality, weather)
- **Sensation** (a physical detail, how the world reacts to motion)

### Sensation lookup

If the grounding sensation is not obvious, pull one from here:

| Environment | Sensation |
|---|---|
| Forest / jungle | Wind through the canopy swaying branches; moisture beading on leaves |
| Desert / arid | Dust spinning off the surface in thermals; heat haze warping the horizon |
| Underwater | Pressure against a viewport; sediment drifting like slow snow |
| Urban / city | Rain fracturing neon in puddles; steam rising from grates |
| Mountain / alpine | Cold pressing through stone; thin air giving light a bleached edge |
| Cave / interior | Torchlight flickering across walls; dust motes in a shaft of light |
| Sky / aerial | Wind tearing at loose objects; cloud wisps shredding as you pass |
| Space / void | Silence felt as absence; distant lights fixed while near objects drift |

## Worked example

**Input:** "make me an experience where you ride a dragon"

**Output:**

> The video presents a first-person flight from the back of a colossal dragon, the
> rider's gauntleted hands gripping thick leather reins lashed to an iron-studded
> bridle. Wind tears past in cold ribbons and the saddle pitches with every
> wingbeat, the leather creaking as the great shoulders rise and fall. Far below, a
> patchwork of misted valleys and a distant castle on a crag sharpen steadily
> through the haze. Vast and windswept.

Why it works: first-person POV; subject and vantage (dragon, reins, bridle,
saddle); near plane (gauntleted hands); mid plane (the dragon's working
shoulders); far plane (valleys, distant castle); atmosphere (cold, misted); a
strong sensation (wind, the saddle pitching, leather creaking); one focal event
(the castle resolving); one mood phrase; no camera verbs; four sentences.

**Spectator variant ("a quiet mountain lake at dusk"):**

> A serene mountain lake at dusk, the water glass-still and mirroring a sky banded
> in cold violet. Mist curls low off the surface and a loon's call carries across
> the basin, ripples spreading where it dips. Dark pines crowd the far shore
> beneath the first stars. Hushed and glacial.

## Common mistakes

| Tempting | Do this instead |
|---|---|
| Keeping "zoom in slowly" because the user said it | Strip all camera operation silently. The user wants a better prompt, not a transcription. |
| Adding "the camera tracks/dollies/glides" to feel cinematic | Never. Camera motion lives in the control signals. No "the camera does X" sentences. |
| Ending with "cinematic, 8k, photoreal, volumetric lighting" | Cut the tag stack. Translate to physical language: "warm low-angle sunlight," not "volumetric lighting." |
| Two destinations or focal points | Pick one. Demote the other to background world detail. |
| Stacking mood words ("eerie, melancholy, desolate, vast") | One mood phrase. Turn the rest into concrete world anchors (desolate becomes drifting silt, no life, abandoned). |
| Skipping the physical sensation | Never skip it. It is what makes the world feel alive. Use the lookup table. |
| Writing five or more sentences | Keep it to two to four. Add detail inside clauses, not new sentences. |

## Output

Return the prompt as plain prose, nothing else: no point-of-view label, no
breakdown of the parts, no note about what you stripped. If the user explicitly
asks for your reasoning or alternates, then provide them.
