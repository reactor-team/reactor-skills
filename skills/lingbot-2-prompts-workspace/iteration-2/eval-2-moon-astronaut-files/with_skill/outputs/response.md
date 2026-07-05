Done. I built a LingBot-World V2 session package for a playable astronaut on the moon and saved both files:

- `/Users/whp/Reactor/reactor-skills/skills/lingbot-2-prompts-workspace/iteration-2/eval-2-moon-astronaut-files/with_skill/outputs/prompt.txt`
- `/Users/whp/Reactor/reactor-skills/skills/lingbot-2-prompts-workspace/iteration-2/eval-2-moon-astronaut-files/with_skill/outputs/actions.json`

**Regime:** playable character (mobile subject, "playable" stated), so the base uses the third-person gameplay skeleton with a WASD motion contract.

**Base prompt** (109 words):

> A third-person gameplay video where an astronaut in a bulky white spacesuit with a gold reflective visor is the playable character. The camera follows from behind and slightly above, like a modern 3D game. The astronaut bounds across the grey, cratered lunar surface in slow low-gravity leaps in response to keyboard arrow keys (or WASD), changing direction naturally with game-like movement and floaty moon physics. The astronaut always lands upright on both boots. A parked lunar rover and a planted flag stand motionless nearby under a black star-filled sky. The scene looks like real gameplay with realistic lighting, smooth camera tracking, high-quality graphics, and an Unreal Engine 5 style.

Low gravity is encoded as the travel verb itself ("bounds... in slow low-gravity leaps", "floaty moon physics"), with "always lands upright on both boots" as the identity-stabilizing constraint. The rover and flag are placed in the base so the addenda have grounded targets, and they are explicitly "motionless" so they don't animate on their own.

**Action slots** (all five, order f/g/u/o/space):

- `f` **Survey Bot Rolls Past** — opens with the subject-preservation clause; a small six-wheeled survey robot trundles past and parks beside a shallow crater.
- `g` **Lunar Dawn** — sunlight sweeps the plain, dragging long hard-edged shadows from the rover, flag, and boulders and shifting the dust from blue-grey to warm gold.
- `u` **Hammer Smash** — geology hammer into a nearby basalt boulder; fragments tumble in slow low-gravity arcs before settling.
- `o` **Fires Signal Flare** — flare gun shot arcing long and flat through the airless sky, striking a distant crater rim in a silent burst of sparks and a slow dust plume.
- `space` **Jump** — the fixed string "The character jumps high into the air."

Each addendum ends settled so the world can revert cleanly on key release, and every `prompt_en`/`prompt_zh` is the base plus a single space plus the addendum, built mechanically and verified.

Want a different `o` projectile (e.g. a thrown core-sample spike) or a second `u` candidate?
