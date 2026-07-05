Here is your LingBot-World V2 session package for a golden retriever puppy you drive around a sunny beach. Since the puppy is a mobile subject you steer, I used the playable character regime: chase camera behind and slightly above, WASD drives the puppy, and the base fixes a motion contract ("It always stays on all four paws while running") so the puppy's identity stays stable between inputs. The base also plants the props the actions need: a half-built sandcastle at paw's reach for the melee slot and a distant lifeguard tower as the ranged target.

## prompt.txt (base prompt)

> A third-person gameplay video where a fluffy golden retriever puppy with floppy ears and a wagging tail is the playable character. The camera follows from behind and slightly above, like a modern 3D game. The puppy runs and bounds across a sunny beach of pale golden sand, past a half-built sandcastle and a striped beach ball, with a distant wooden lifeguard tower near the waterline, in response to keyboard arrow keys (or WASD), changing direction naturally with game-like movement and physics. It always stays on all four paws while running. The scene looks like real gameplay with realistic lighting, smooth camera tracking, high-quality graphics, and an Unreal Engine 5 style.

## Action slots (actions.json)

- **f — Crab Scuttles Past.** The golden retriever puppy remains the main subject, unchanged in pose and position, while a small orange crab pops out of the wet sand to the right, scuttles sideways across the puppy's path, and burrows back under the sand with a tiny puff of grains.
- **g — Golden Sunset.** The bright midday light shifts into a warm golden sunset, washing the pale sand, the rolling shoreline, and the wooden lifeguard tower in deep orange and pink hues while long soft shadows stretch across the beach.
- **u — Sandcastle Pounce.** The golden retriever puppy pounces onto the nearby half-built sandcastle with both front paws, the impact crumbling its towers and walls into a spray of loose sand that settles in a soft heap around its paws.
- **o — Flings Beach Ball.** The golden retriever puppy scoops its snout under the striped beach ball and flings it forward, sending the ball arcing high across the beach until it bounces off a wooden post of the distant lifeguard tower with a puff of sand and rolls to a stop.
- **space — Jump.** The character jumps high into the air. (fixed runtime convention)

Each addendum is a bounded beat that settles on its own (the crab burrows back, the ball rolls to a stop), so a press-release cycle returns cleanly to the base world. The `prompt_en` strings in actions.json are built mechanically as base + space + addendum, and the `_zh` fields mirror the English.

Files:
- `prompt.txt` — the base prompt
- `actions.json` — the five-slot action package, ready to drop into tooling

Want a different `o` projectile (a flung stick or a spray of seawater), a second `u` candidate, or a demo-app world JSON to load via the "Upload world JSON" button?
