Done. "Astronaut on the moon, playable, low gravity" is a mobile subject the player drives, so I used the **playable character** regime: chase camera, WASD motion contract, low-gravity moon-hop physics as the identity constraint, and a lander + flag placed in the base so the action slots have nearby and distant targets to work with.

Files written:

- `/Users/whp/Reactor/reactor-skills/skills/lingbot-2-prompts-workspace/iteration-1/eval-2-moon-astronaut-files/with_skill/outputs/prompt.txt`
- `/Users/whp/Reactor/reactor-skills/skills/lingbot-2-prompts-workspace/iteration-1/eval-2-moon-astronaut-files/with_skill/outputs/actions.json`

**prompt.txt** (the base prompt, 112 words):

> A third-person gameplay video where an astronaut in a bulky white spacesuit and gold-visored helmet is the playable character. The camera follows from behind and slightly above, like a modern 3D game. The astronaut bounds across the crater-pocked lunar surface in response to keyboard arrow keys (or WASD), changing direction naturally with game-like movement and low-gravity physics, each long, floaty moon-hop kicking up slow-settling dust. The astronaut always lands upright on both feet. A lunar lander and a planted flag stand nearby under a black, star-filled sky, Earth hanging above the horizon. The scene looks like real gameplay with realistic lighting, smooth camera tracking, high-quality graphics, and an Unreal Engine 5 style.

**actions.json** — one entry per slot in order `f, g, u, o, space`; each `prompt_en` is the base prompt plus a single space plus the addendum, built mechanically; `_zh` fields duplicate `_en`:

| Slot | Label | What happens |
|---|---|---|
| `f` | Rover Rolls Past | Subject-preservation clause, then a six-wheeled lunar rover rolls past on the right, pressing fresh tracks into the regolith and parking beside the lander. |
| `g` | Lunar Sunrise | The sun crests the horizon, sweeping long hard-edged shadows and washing the regolith, lander, and flag in golden light while Earth brightens. |
| `u` | Hammer Smash | The astronaut slams a geological hammer into a nearby basalt boulder; it cracks apart, fragments tumbling in slow low-gravity arcs before settling. |
| `o` | Fires Flare Gun | A red flare streaks in a long slow arc across the black sky, strikes a boulder on a distant crater rim, and bursts in sparks and a slow-rising dust plume. |
| `space` | Jump | Fixed string: "The character jumps high into the air." |

The full addenda:

- **f — Rover Rolls Past:** "The original focal subject remains the main subject, unchanged in pose and position, while a small six-wheeled lunar rover rolls slowly past on the right, its wire-mesh wheels pressing fresh tracks into the regolith before it parks quietly beside the lander."
- **g — Lunar Sunrise:** "The sun crests the lunar horizon, sweeping long hard-edged shadows across the crater-pocked surface and washing the grey regolith, the lunar lander, and the planted flag in brilliant golden light while Earth brightens against the black, star-filled sky."
- **u — Hammer Smash:** "The astronaut raises a geological hammer and slams it down on a nearby basalt boulder; the rock cracks apart in a burst of grey dust, its fragments tumbling away in slow, floating low-gravity arcs before settling back onto the regolith."
- **o — Fires Flare Gun:** "The astronaut raises a flare gun and fires; the glowing red flare streaks in a long, slow arc across the black sky and strikes a boulder on a distant crater rim, bursting in a shower of sparks and a slow-rising plume of lunar dust."

Want a different `o` projectile (e.g. a thrown moon rock instead of the flare gun) or a second candidate for any slot?
