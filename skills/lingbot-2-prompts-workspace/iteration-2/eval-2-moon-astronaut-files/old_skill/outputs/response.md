LingBot-World V2 session package for "an astronaut on the moon, playable, low gravity" is written to the output directory.

Files:
- /Users/whp/Reactor/reactor-skills/skills/lingbot-2-prompts-workspace/iteration-2/eval-2-moon-astronaut-files/old_skill/outputs/prompt.txt
- /Users/whp/Reactor/reactor-skills/skills/lingbot-2-prompts-workspace/iteration-2/eval-2-moon-astronaut-files/old_skill/outputs/actions.json

Design choices:
- Regime: playable character (the idea says "playable" and the subject travels). The base uses the production playable-character skeleton: third-person gameplay video, camera behind and slightly above, WASD/arrow-key motion contract, and an identity-stability constraint ("The astronaut always lands upright on both boots").
- Low gravity is baked into the motion contract itself: "slow, floaty low-gravity physics, each hop kicking up slow-drifting moon dust", so traversal, not just events, reads lunar.
- The base pre-places action targets: a lunar lander, a planted flag, and scattered boulders (nearby melee target), plus a crater rim and Earth on the horizon (distant ranged target).

Action slots:
- f — Rover Rolls Past: opens with the subject-preservation clause; a small six-wheeled rover trundles in from behind the lander and parks by the flag (settled ending).
- g — Lunar Night Falls: global lighting transformation; earthlight washes over three named surfaces (cratered ground, the lander's gold foil panels, the planted flag).
- u — Hammer Smash: geology hammer wind-up, impact on a nearby boulder, fragments floating up in slow low-gravity arcs before settling.
- o — Hurls Moon Rock: full visible arc (scoop, long flat low-gravity throw, strike on a distant crater-rim boulder, slow-blooming dust plume aftermath).
- space — Jump: the fixed runtime string "The character jumps high into the air."

Every prompt_en/prompt_zh is built mechanically as base + single space + addendum; _zh fields duplicate _en since no Chinese was supplied; all cand_index values are 0 with ids like f#0.

Want a different o projectile (e.g. a flare-style signal charge) or a second u candidate?
