# LingBot-World V2 session: old lighthouse keeper at the cliff edge

A stationary standing figure to look at, so this uses the **orbit** regime: the keeper is locked at frame centre and arrow keys orbit the camera around him. The base freezes the gulls and the waves so the arrow keys stay the only source of motion, and it pre-places a rotten fence post (nearby, for the `u` strike), a bell buoy (distant, for the `o` flare), and the brass lantern (the `u` weapon).

## `prompt.txt`

```
This is a third-person-view video of an old lighthouse keeper in a weathered oilskin coat, standing at the edge of a cliff at dusk, holding a brass lantern. Cinematic maritime dusk atmosphere. A lighthouse rises behind him, a rotten fence post leans by the path, a bell buoy far out on the water. The keeper is locked at the exact centre of the frame at constant size and distance. Neither the keeper nor the camera moves on its own; arrow-key look-input is the only source of camera motion, orbiting the camera around the stationary keeper only while held. The keeper stands perfectly still, gulls frozen mid-air, the waves below held motionless.
```

## `actions.json`

```json
{
  "actions": [
    {
      "id": "f#0",
      "slot": "f",
      "cand_index": 0,
      "label_en": "Gull Lands Nearby",
      "addendum_en": "The original focal subject remains the main subject, unchanged in pose and position, while a grey seagull glides in from over the cliff edge, circles once, and settles onto the rotten fence post beside the path, folding its wings before going still.",
      "prompt_en": "This is a third-person-view video of an old lighthouse keeper in a weathered oilskin coat, standing at the edge of a cliff at dusk, holding a brass lantern. Cinematic maritime dusk atmosphere. A lighthouse rises behind him, a rotten fence post leans by the path, a bell buoy far out on the water. The keeper is locked at the exact centre of the frame at constant size and distance. Neither the keeper nor the camera moves on its own; arrow-key look-input is the only source of camera motion, orbiting the camera around the stationary keeper only while held. The keeper stands perfectly still, gulls frozen mid-air, the waves below held motionless. The original focal subject remains the main subject, unchanged in pose and position, while a grey seagull glides in from over the cliff edge, circles once, and settles onto the rotten fence post beside the path, folding its wings before going still.",
      "label_zh": "Gull Lands Nearby",
      "addendum_zh": "The original focal subject remains the main subject, unchanged in pose and position, while a grey seagull glides in from over the cliff edge, circles once, and settles onto the rotten fence post beside the path, folding its wings before going still.",
      "prompt_zh": "This is a third-person-view video of an old lighthouse keeper in a weathered oilskin coat, standing at the edge of a cliff at dusk, holding a brass lantern. Cinematic maritime dusk atmosphere. A lighthouse rises behind him, a rotten fence post leans by the path, a bell buoy far out on the water. The keeper is locked at the exact centre of the frame at constant size and distance. Neither the keeper nor the camera moves on its own; arrow-key look-input is the only source of camera motion, orbiting the camera around the stationary keeper only while held. The keeper stands perfectly still, gulls frozen mid-air, the waves below held motionless. The original focal subject remains the main subject, unchanged in pose and position, while a grey seagull glides in from over the cliff edge, circles once, and settles onto the rotten fence post beside the path, folding its wings before going still.",
      "selected": false
    },
    {
      "id": "g#0",
      "slot": "g",
      "cand_index": 0,
      "label_en": "Sea Fog Rolls In",
      "addendum_en": "A dense bank of sea fog rolls up over the cliff edge and spreads across the whole scene, wrapping the clifftop, the fence post, and the base of the lighthouse in drifting grey mist, dimming the dusk light to a pale glow around the keeper's lantern.",
      "prompt_en": "This is a third-person-view video of an old lighthouse keeper in a weathered oilskin coat, standing at the edge of a cliff at dusk, holding a brass lantern. Cinematic maritime dusk atmosphere. A lighthouse rises behind him, a rotten fence post leans by the path, a bell buoy far out on the water. The keeper is locked at the exact centre of the frame at constant size and distance. Neither the keeper nor the camera moves on its own; arrow-key look-input is the only source of camera motion, orbiting the camera around the stationary keeper only while held. The keeper stands perfectly still, gulls frozen mid-air, the waves below held motionless. A dense bank of sea fog rolls up over the cliff edge and spreads across the whole scene, wrapping the clifftop, the fence post, and the base of the lighthouse in drifting grey mist, dimming the dusk light to a pale glow around the keeper's lantern.",
      "label_zh": "Sea Fog Rolls In",
      "addendum_zh": "A dense bank of sea fog rolls up over the cliff edge and spreads across the whole scene, wrapping the clifftop, the fence post, and the base of the lighthouse in drifting grey mist, dimming the dusk light to a pale glow around the keeper's lantern.",
      "prompt_zh": "This is a third-person-view video of an old lighthouse keeper in a weathered oilskin coat, standing at the edge of a cliff at dusk, holding a brass lantern. Cinematic maritime dusk atmosphere. A lighthouse rises behind him, a rotten fence post leans by the path, a bell buoy far out on the water. The keeper is locked at the exact centre of the frame at constant size and distance. Neither the keeper nor the camera moves on its own; arrow-key look-input is the only source of camera motion, orbiting the camera around the stationary keeper only while held. The keeper stands perfectly still, gulls frozen mid-air, the waves below held motionless. A dense bank of sea fog rolls up over the cliff edge and spreads across the whole scene, wrapping the clifftop, the fence post, and the base of the lighthouse in drifting grey mist, dimming the dusk light to a pale glow around the keeper's lantern.",
      "selected": false
    },
    {
      "id": "u#0",
      "slot": "u",
      "cand_index": 0,
      "label_en": "Lantern Smash",
      "addendum_en": "The keeper draws the brass lantern back and swings it hard against the rotten fence post beside him; the impact splinters the post's weathered crown, scattering damp wood chips into the grass as the post settles at a crooked lean.",
      "prompt_en": "This is a third-person-view video of an old lighthouse keeper in a weathered oilskin coat, standing at the edge of a cliff at dusk, holding a brass lantern. Cinematic maritime dusk atmosphere. A lighthouse rises behind him, a rotten fence post leans by the path, a bell buoy far out on the water. The keeper is locked at the exact centre of the frame at constant size and distance. Neither the keeper nor the camera moves on its own; arrow-key look-input is the only source of camera motion, orbiting the camera around the stationary keeper only while held. The keeper stands perfectly still, gulls frozen mid-air, the waves below held motionless. The keeper draws the brass lantern back and swings it hard against the rotten fence post beside him; the impact splinters the post's weathered crown, scattering damp wood chips into the grass as the post settles at a crooked lean.",
      "label_zh": "Lantern Smash",
      "addendum_zh": "The keeper draws the brass lantern back and swings it hard against the rotten fence post beside him; the impact splinters the post's weathered crown, scattering damp wood chips into the grass as the post settles at a crooked lean.",
      "prompt_zh": "This is a third-person-view video of an old lighthouse keeper in a weathered oilskin coat, standing at the edge of a cliff at dusk, holding a brass lantern. Cinematic maritime dusk atmosphere. A lighthouse rises behind him, a rotten fence post leans by the path, a bell buoy far out on the water. The keeper is locked at the exact centre of the frame at constant size and distance. Neither the keeper nor the camera moves on its own; arrow-key look-input is the only source of camera motion, orbiting the camera around the stationary keeper only while held. The keeper stands perfectly still, gulls frozen mid-air, the waves below held motionless. The keeper draws the brass lantern back and swings it hard against the rotten fence post beside him; the impact splinters the post's weathered crown, scattering damp wood chips into the grass as the post settles at a crooked lean.",
      "selected": false
    },
    {
      "id": "o#0",
      "slot": "o",
      "cand_index": 0,
      "label_en": "Fires Signal Flare",
      "addendum_en": "The keeper raises a flare gun in his free hand and fires a crimson signal flare that arcs out over the water, trailing red smoke, before striking the distant bell buoy in a burst of sparks that scatter across the waves and fade into the dusk.",
      "prompt_en": "This is a third-person-view video of an old lighthouse keeper in a weathered oilskin coat, standing at the edge of a cliff at dusk, holding a brass lantern. Cinematic maritime dusk atmosphere. A lighthouse rises behind him, a rotten fence post leans by the path, a bell buoy far out on the water. The keeper is locked at the exact centre of the frame at constant size and distance. Neither the keeper nor the camera moves on its own; arrow-key look-input is the only source of camera motion, orbiting the camera around the stationary keeper only while held. The keeper stands perfectly still, gulls frozen mid-air, the waves below held motionless. The keeper raises a flare gun in his free hand and fires a crimson signal flare that arcs out over the water, trailing red smoke, before striking the distant bell buoy in a burst of sparks that scatter across the waves and fade into the dusk.",
      "label_zh": "Fires Signal Flare",
      "addendum_zh": "The keeper raises a flare gun in his free hand and fires a crimson signal flare that arcs out over the water, trailing red smoke, before striking the distant bell buoy in a burst of sparks that scatter across the waves and fade into the dusk.",
      "prompt_zh": "This is a third-person-view video of an old lighthouse keeper in a weathered oilskin coat, standing at the edge of a cliff at dusk, holding a brass lantern. Cinematic maritime dusk atmosphere. A lighthouse rises behind him, a rotten fence post leans by the path, a bell buoy far out on the water. The keeper is locked at the exact centre of the frame at constant size and distance. Neither the keeper nor the camera moves on its own; arrow-key look-input is the only source of camera motion, orbiting the camera around the stationary keeper only while held. The keeper stands perfectly still, gulls frozen mid-air, the waves below held motionless. The keeper raises a flare gun in his free hand and fires a crimson signal flare that arcs out over the water, trailing red smoke, before striking the distant bell buoy in a burst of sparks that scatter across the waves and fade into the dusk.",
      "selected": false
    },
    {
      "id": "space#0",
      "slot": "space",
      "cand_index": 0,
      "label_en": "Jump",
      "addendum_en": "The character jumps high into the air.",
      "prompt_en": "This is a third-person-view video of an old lighthouse keeper in a weathered oilskin coat, standing at the edge of a cliff at dusk, holding a brass lantern. Cinematic maritime dusk atmosphere. A lighthouse rises behind him, a rotten fence post leans by the path, a bell buoy far out on the water. The keeper is locked at the exact centre of the frame at constant size and distance. Neither the keeper nor the camera moves on its own; arrow-key look-input is the only source of camera motion, orbiting the camera around the stationary keeper only while held. The keeper stands perfectly still, gulls frozen mid-air, the waves below held motionless. The character jumps high into the air.",
      "label_zh": "Jump",
      "addendum_zh": "The character jumps high into the air.",
      "prompt_zh": "This is a third-person-view video of an old lighthouse keeper in a weathered oilskin coat, standing at the edge of a cliff at dusk, holding a brass lantern. Cinematic maritime dusk atmosphere. A lighthouse rises behind him, a rotten fence post leans by the path, a bell buoy far out on the water. The keeper is locked at the exact centre of the frame at constant size and distance. Neither the keeper nor the camera moves on its own; arrow-key look-input is the only source of camera motion, orbiting the camera around the stationary keeper only while held. The keeper stands perfectly still, gulls frozen mid-air, the waves below held motionless. The character jumps high into the air.",
      "selected": false
    }
  ]
}
```

Files written: `prompt.txt` and `actions.json` in this directory.

Want a different `o` projectile (say, a thrown storm bottle instead of the flare gun) or a second `u` candidate?
