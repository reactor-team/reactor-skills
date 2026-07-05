Here's your LingBot-World V2 session package. A drivable puppy on a beach is a **playable character** regime: WASD drives the puppy, the camera follows from behind. The base prompt seeds a nearby sandcastle and beach ball plus a distant lifeguard tower so the strike and ranged actions have in-scene targets.

**`prompt.txt`** (base prompt):

> A third-person gameplay video where a fluffy golden retriever puppy with floppy ears and a wagging tail is the playable character. The camera follows from behind and slightly above, like a modern 3D game. The puppy runs and bounds across the pale sand of a sunny beach, past a half-built sandcastle and a striped beach ball, with a weathered wooden lifeguard tower in the distance, in response to keyboard arrow keys (or WASD), changing direction naturally with game-like movement and physics. It always stays on all four paws while running. The scene looks like real gameplay with realistic lighting, smooth camera tracking, high-quality graphics, and an Unreal Engine 5 style.

**`actions.json`** (the five key slots):

- `f` **Crab Scuttles Past** — The original focal subject remains the main subject, unchanged in pose and position, while a small orange crab emerges from the wet sand to the right and scuttles sideways past the puppy, kicking up tiny grains of sand before slipping into a shallow tide pool.
- `g` **Golden Sunset** — The bright midday sun sinks into a deep golden sunset, washing the pale sand, the rolling surf, and the wooden lifeguard tower in warm orange and pink light, while long soft shadows stretch across the beach.
- `u` **Sandcastle Pounce** — The golden retriever puppy rears back and pounces onto the half-built sandcastle with both front paws, the impact collapsing its towers into a spray of loose sand that scatters across the beach before settling.
- `o` **Flings Beach Ball** — The golden retriever puppy scoops the striped beach ball with its snout and flicks its head upward, launching the ball in a high arc across the sand until it strikes the distant wooden lifeguard tower, bouncing off the railing with a puff of dry sand before rolling to a stop at its base.
- `space` **Jump** — The character jumps high into the air. (fixed runtime convention)

Each entry's `prompt_en` is the base prompt plus a single space plus the addendum, built verbatim, so the JSON drops straight into your tooling.

Files written:
- `prompt.txt` — the base prompt, nothing else
- `actions.json` — one entry per slot in order f, g, u, o, space

Want a different `o` projectile (e.g. the puppy kicking up a shell instead of the beach ball) or a second `u` candidate?
