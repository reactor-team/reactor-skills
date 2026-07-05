# LingBot-World v2 session: old lighthouse keeper at the cliff edge at dusk

Here is a complete v2 session for this scene. I set it up as a **fixed-subject spectator world**: the keeper is the anchor and never moves from the cliff edge, and all the interactivity lives in the camera (orbit, dolly, crane) plus a few scene events. That is the composition that stays most stable for a "person standing still in a dramatic landscape" scene, and it makes the orbit reads clean because the subject is planted while the background rotates behind him.

## Design choices

- **Viewpoint: spectator.** The keeper is not navigable and should not be, so WASD is mapped to camera moves, not subject locomotion.
- **Strong anchors for consistency.** The prompt pins three landmarks (lighthouse behind and to his right, burnt-orange horizon band, black rocks below) so that when the camera orbits, the model has a spatial order to preserve rather than reinventing the background each frame.
- **Dusk is stated as a stable gradient, not a process.** "The sun has just set" plus explicit sky colors keeps the model from time-lapsing into night mid-session.
- **Idle is written explicitly.** When nothing is held, the camera holds and the world keeps living: wind, waves, beam rotation, breathing. This prevents freeze-frames and prevents drift.
- **Every hold prompt re-states what must NOT change** (keeper planted, horizon level, lighting logic), because holds are where consistency usually breaks.
- **Events are overlays**, one persistent (lighting the lantern, which permanently adds a warm light source and gets folded into the composed state) and three transient (beam sweep, big wave, gull) for life and drama on demand.

## Base prompt

> An old lighthouse keeper stands motionless at the very edge of a sea cliff at dusk. He is in his seventies, weather-beaten face, white beard, dark navy wool peacoat with the collar turned up, a flat wool cap, one hand gripping an unlit brass lantern at his side. Behind him and slightly to the right, a white stone lighthouse with a red-capped gallery rises from the headland, its lamp just beginning to rotate, throwing a slow pale beam through the thickening dusk. Below the cliff, dark slate-blue ocean swells roll in and burst against black rocks, sending up spray. The sky is a dusk gradient: deep indigo overhead fading through violet to a band of burnt orange and amber on the horizon where the sun has just set. A few gulls drift on the wind. Long grass and thrift flowers at the cliff edge ripple in a steady onshore wind that also tugs at the keeper's coat and beard. Cinematic wide shot, the keeper framed against the glowing horizon, volumetric haze in the beam, soft film grain, moody naturalistic color grade. The camera hangs in the air at the keeper's eye level, a spectator view that can circle him; the keeper himself stays planted at the cliff edge, only shifting his weight, breathing, and turning his head slowly to watch the sea.

## Controls (hold-prompts)

| Key | Move | Summary |
|-----|------|---------|
| A | Orbit left | Counterclockwise orbit at constant radius and eye level; keeper centered, background rotates in correct spatial order, lighting changes plausibly with angle |
| D | Orbit right | Clockwise orbit, same constraints |
| W | Dolly in | Slow push from wide to chest-up close shot; coat weave, beard texture, amber rim light on his face |
| S | Dolly out | Slow pull back; keeper becomes a small resolute figure against the horizon, full lighthouse and cliff line in frame |
| Q | Crane up | Rise and tilt down; reveals the drop to the rocks, comes level with the lighthouse gallery and its beam |
| E | Crane down | Descend to grass level, low-angle hero shot through windblown grass |
| (idle) | Hold | Camera holds position; wind, waves, beam rotation, and breathing continue |

## Events (overlay mode)

| Key | Event | Persist |
|-----|-------|---------|
| 1 | Light the lantern — warm orange glow joins the cool dusk ambience, stays lit afterward | yes |
| 2 | Beam sweep — the lighthouse beam rakes across keeper and camera as a volumetric blade | no |
| 3 | Big wave — spray bursts up past the cliff edge, backlit by the horizon | no |
| 4 | Gull flyby — a gull swoops between camera and keeper with a cry | no |

## Negatives / guardrails

No sudden day-night jumps, no sun above the horizon, no extra people, the keeper never walks or leaves the cliff edge, no camera teleports or cuts, horizon stays level, lighthouse stays fixed on the headland.

## Composition rule

Per frame: `base` + (active hold prompt, or the idle prompt if nothing is held) + any active event overlays + negatives. Exactly one hold is active at a time; on release, fall back to idle. The persistent lantern event appends a one-line state to the base for all subsequent frames ("The keeper's brass lantern is lit, casting a warm orange glow on his hands and coat.").

## Files

- `base_prompt.txt` — the base prompt as plain text
- `world.json` — the full v2 world spec (base, anchors, idle, holds, events, negatives, compose rule)
