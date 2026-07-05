LingBot-World V2 session package for "an old lighthouse keeper standing at the edge of a cliff at dusk".

**Regime: orbit.** The idea is a stationary figure to look at, so the camera stays locked on the centred keeper and arrow keys orbit around him; nothing moves on its own.

**Base prompt** (`prompt.txt`):

> This is a third-person-view video of a white-bearded old lighthouse keeper in a weathered navy peacoat, a brass lantern in one hand, standing at the edge of a grassy cliff beside a leaning wooden fence post. Dusk atmosphere: a white lighthouse against an orange-violet sky, a rusted bell buoy on the dark water below. The keeper is locked at the exact centre of the frame at constant size and distance. Neither the keeper nor the camera moves on its own; arrow-key look-input is the only source of camera motion, orbiting the camera around the stationary keeper only while held. The keeper stands perfectly still, the gulls over the water and the sea spray held frozen in mid-air.

The base deliberately places the action targets: the fence post (arm's-reach target for `u`, perch for `f`), the lantern (the keeper's melee tool), and the bell buoy (distant target for `o`). The freeze clause pins the gulls and sea spray so arrow-key input stays the only cause of motion.

**Actions** (`actions.json`, slots f / g / u / o / space, mapped to keys 1-4 and space in the demo app):

- `f` **Gull Lands Nearby** — preservation clause, then a grey seagull swoops in and settles on the fence post, folding its wings and going still.
- `g` **Sea Fog Rolls In** — thick grey fog climbs the cliff and mutes the sky, grass, and lighthouse tower to pale silhouettes, the lamp glowing as a halo through the mist.
- `u` **Lantern Smash** — the keeper swings the brass lantern into the leaning fence post; the rotted timber cracks and splinters, the top half tumbling into the grass, then he lowers the lantern back to his side.
- `o` **Fires Signal Flare** — a flare gun from his coat, a crimson flare arcing through the dusk sky trailing red smoke, striking the bell buoy in a burst of sparks that fade on the water.
- `space` **Jump** — fixed string: "The character jumps high into the air."

Every `prompt_en` is built mechanically as base + space + addendum (verified programmatically), each addendum is a bounded beat that settles so the world reverts cleanly on key release, and none restate the camera contract.

Files written:
- `prompt.txt` — the base prompt
- `actions.json` — the five-slot action package in the inference-session export shape

Want a different `o` projectile (say, a thrown lantern or a lighthouse-beam sweep) or a second `u` candidate?
