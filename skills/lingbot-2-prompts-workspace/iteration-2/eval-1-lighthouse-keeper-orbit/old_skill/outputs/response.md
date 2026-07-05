A stationary figure to look at, so this is the **orbit** regime: the keeper is locked at frame centre and arrow keys orbit the camera around him. Files are written to `/Users/whp/Reactor/reactor-skills/skills/lingbot-2-prompts-workspace/iteration-2/eval-1-lighthouse-keeper-orbit/old_skill/outputs/` (`prompt.txt`, `actions.json`).

**`prompt.txt`** — the base prompt:

> This is a third-person-view video of an old, white-bearded lighthouse keeper in a weathered oilskin coat standing at the edge of a sea cliff at dusk, the lighthouse tower behind him and a rusted hand lantern on the wooden fence post beside him. Amber-and-violet coastal dusk atmosphere, a distant bell buoy on the dark sea. The keeper is locked at the exact centre of the frame at constant size and distance. Neither the keeper nor the camera moves on its own; arrow-key look-input is the only source of camera motion, orbiting the camera around the stationary keeper only while held. The keeper stands perfectly still, the sea spray and the gulls overhead held frozen in the air.

The base pre-places the action targets: the rusted hand lantern on the fence post (nearby, for `u`) and the bell buoy out on the dark sea (distant, for `o`). The freeze clause names the sea spray and gulls specifically so ambient coastal motion stays gated on input.

**`actions.json`** — one candidate per slot:

- `f` **Gull Lands Nearby** — The old lighthouse keeper remains the main subject, unchanged in pose and position, while a grey herring gull swoops down out of the dusk sky and lands on the wooden fence post beside him, folding its wings and settling next to the rusted hand lantern.
- `g` **Sea Fog Rolls In** — A thick sea fog rolls in off the water, wrapping the cliff edge, the wooden fence post, and the base of the lighthouse tower in drifting grey mist, muting the amber dusk to a soft silver gloom while the lantern-room glow blooms into a hazy halo.
- `u` **Lantern Smash** — The keeper snatches the rusted hand lantern off the fence post and slams it down against a flat rock at his feet, the glass panes shattering and scattering glinting shards across the grass before the bent metal frame comes to rest at the cliff edge.
- `o` **Fires Flare Gun** — The keeper draws a brass flare gun from inside his oilskin coat and fires it out over the water, the red flare arcing high through the dusk with a thin trail of smoke before striking the distant bell buoy in a burst of crimson sparks that scatter across the waves and fade.
- `space` **Jump** — The character jumps high into the air. (fixed runtime string)

Each `prompt_en` in the JSON is the base prompt plus a single space plus the addendum, built mechanically; `_zh` fields duplicate `_en`.

Want a different `o` projectile (a thrown signal rocket, a slung stone) or a second `u` candidate against the fence post instead of the lantern?
