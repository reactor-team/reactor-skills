# LingBot 2: Playable Moon Astronaut

I created a LingBot 2 world for a playable astronaut on the Moon with authentic low-gravity movement. Two files are saved in the output directory:

- `prompt.txt` - the base prompt
- `actions.json` - the action/keybinding map

## Design decisions

**Viewpoint:** Third-person over-the-shoulder game camera, about three meters behind the astronaut. Low gravity is the whole point of this world, and slow bounding hops with long hang time only read clearly when you can see the character's body. A first-person version would mostly show camera bob.

**Base prompt** (`prompt.txt`) establishes:
- The playable subject: white EVA suit, gold-mirrored visor, backpack, dusty boots
- The environment: gray regolith plain, craters, boulders, curved horizon, black star-filled sky, Earth low above the horizon, a lunar lander and flag as fixed landmarks for spatial orientation
- Lighting locked to harsh sunlight from the left with deep shadows, so it stays consistent across generated continuations
- The physics contract, stated explicitly: one-sixth gravity, slow floaty arcs, exaggerated hang time, soft landings, and dust that flies in clean ballistic arcs without billowing (no atmosphere)
- An idle state for when no key is held, so the world stays stable between inputs

**Actions** (`actions.json`) cover the playable core plus a little flavor:

| Key | Action | Mode |
|-----|--------|------|
| W / Up | Bound forward in slow low-gravity hops | hold |
| S / Down | Careful bouncing steps backward | hold |
| A / Left | Bounding turn left | hold |
| D / Right | Bounding turn right | hold |
| Space | Huge slow-motion vertical leap with hang time | press |
| Shift | Fast lunar loping (sprint) | hold |
| Q | Stop and look around the horizon | press |
| E | Wave at Earth | press |
| F | Pick up and inspect a moon rock | press |

Every movement prompt restates the low-gravity motion language (floaty arcs, hang time, soft landings, ballistic dust) so the physics stay consistent no matter which action the model is continuing from. Movement actions are flagged `isMoving: true`; the flavor actions (look, wave, rock) are stationary. A top-level `physicsNotes` field and the idle prompt reinforce continuity: same lighting, same sky, tracking camera, no cuts.

The JSON validates cleanly. If your LingBot 2 runtime expects a different actions schema (for example different field names for keys or hold vs press), the prompts themselves are drop-in and only the wrapper fields need renaming.
