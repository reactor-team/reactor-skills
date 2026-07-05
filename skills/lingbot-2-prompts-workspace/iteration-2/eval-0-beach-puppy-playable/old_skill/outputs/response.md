Here's your LingBot 2 session package for a golden retriever puppy you can drive around a sunny beach. "Drive around" makes this the playable-character regime: WASD moves the puppy, the camera follows from behind like a modern 3D game.

**prompt.txt** (the base prompt):

```
A third-person gameplay video where a fluffy golden retriever puppy with soft golden fur and floppy ears is the playable character. The camera follows from behind and slightly above, like a modern 3D game. The puppy runs and bounds across a sunny beach of pale sand, past scattered seashells, a striped beach ball, and a small sandcastle near a wooden lifeguard tower, in response to keyboard arrow keys (or WASD), changing direction naturally with game-like movement and physics. It always stays on all four paws while running. The scene looks like real gameplay with realistic lighting, smooth camera tracking, high-quality graphics, and an Unreal Engine 5 style.
```

The base seeds the scene with the props the actions need: the beach ball and sandcastle at paw's reach, the lifeguard tower in the distance.

**actions.json** (the five key slots):

- `f` **Crab Scuttles By** — subject-preservation clause, then a small pale crab scuttles out of the wet sand, rounds a seashell, and slips into a burrow near the waterline.
- `g` **Sunset Glow** — the midday sun sinks to a warm sunset, washing the sand, lifeguard tower, and waves in orange and pink light.
- `u` **Sandcastle Smash** — the puppy pounces on the nearby sandcastle, its turrets cracking and crumbling, sand spraying then settling.
- `o` **Launches Beach Ball** — the puppy flicks the striped beach ball with its snout; it arcs high across the sand, thumps off a lifeguard-tower post, and rolls to a stop.
- `space` **Jump** — fixed string: "The character jumps high into the air."

Each `prompt_en` is built mechanically as base + " " + addendum, one entry per slot in `f, g, u, o, space` order, with `_zh` fields mirroring `_en`.

Files written:
- /Users/whp/Reactor/reactor-skills/skills/lingbot-2-prompts-workspace/iteration-2/eval-0-beach-puppy-playable/old_skill/outputs/prompt.txt
- /Users/whp/Reactor/reactor-skills/skills/lingbot-2-prompts-workspace/iteration-2/eval-0-beach-puppy-playable/old_skill/outputs/actions.json

Want a different `o` projectile (say, a flung stick or a spray of seawater) or a second `u` candidate?
