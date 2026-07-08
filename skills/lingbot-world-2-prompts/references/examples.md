# Production layered scenes (verbatim from the lingbot-v2 frontend)

The three shipped scenes from `lingbot-v2-frontend/lib/lingbot-cases/`,
reproduced verbatim. Each was authored in the layered-composition form the
skill targets and then field-refined against live sessions, so the exact
wording is production-validated. Notes after each scene point out what it
demonstrates.

## 1. Noir Alley Patrol (`noir-alley-patrol.json`)

```json
{
  "id": "case1_0036",
  "name": "Noir Alley Patrol",
  "description": "Third-person noir alley — key 1 = fires pistol, key 2 = flamethrower, key 3 = fires rocket launcher, key 4 = knife attack, key 5 = forward roll",
  "image": {
    "label": "Noir Alley Patrol",
    "src": "/lingbot-cases/case1_0036.jpg"
  },
  "scene": {
    "base": {
      "default": "A lone uniformed police officer in dark blue tactical gear in a narrow urban alley at night. The world contains EXACTLY ONE tall street lamp on the right at a fixed position AND EXACTLY ONE glowing neon shop sign on the left at a fixed position AND EXACTLY ONE shop door straight ahead at a fixed position AND EXACTLY ONE green dumpster on the right at a fixed position. Dark brick walls, heavy rain falling, shiny puddles on the wet asphalt, yellow police tape, blue and red ambient light. Cinematic noir night, reflective wet surfaces."
    },
    "camera": {
      "default": {
        "static": "Third-person view from behind the officer, his back and body centred in frame at constant size, any weapon in his hands visible ahead — never a first-person view. Neither officer nor camera moves; look-input is the only camera motion, arcing around the stationary centred officer while held.",
        "dynamic": "Strict third-person rear view from close behind and slightly above the officer, his back and body filling frame centre, any weapon in his hands visible ahead — never first-person. It holds a fixed rear position and does not rotate around him; look-input becomes the officer changing heading."
      }
    },
    "movement": {
      "default": {
        "static": "The officer stands still on the wet asphalt, weight settled, only his shoulders rising and falling with slow breaths as rain streams off his tactical gear and drips from his fingertips into the spreading puddles.",
        "dynamic": "The officer advances at a steady patrol pace down the alley, boots splashing through the puddles and kicking up fine spray, his gear shifting with each stride as the rain streaks past and the wet asphalt slides beneath him."
      }
    },
    "events": [
      {
        "name": "Fire Pistol",
        "detail": "The officer raises his service pistol in both gloved hands, arms extended ahead of him, and fires down the dark alley; the muzzle flash lights the falling rain, the recoil kicks the pistol back in his grip, and a spent casing clatters onto the wet asphalt."
      },
      {
        "name": "Flamethrower",
        "detail": "The officer levels a flamethrower in both hands and unleashes a long, continuous jet of roaring flame straight ahead down the alley — one sustained, billowing stream of orange fire and black smoke that pours forward without pause, not separate shots, lighting up the wet brick walls and hissing against the falling rain."
      },
      {
        "name": "Fire Rocket Launcher",
        "detail": "The officer hoists a shoulder-fired rocket launcher — an RPG: a long, heavy cylindrical steel tube resting across his shoulder, its wide bore pointing down the alley, gripped with both hands, not a handheld gun — and fires; the rocket blasts from the tube's mouth and flies off into the distance down the rain-slicked alley, dragging a long tail of orange flame and white smoke behind it, then slams into the distant brickwork and erupts in a massive fireball of flame, smoke, and flying debris."
      },
      {
        "name": "Knife Attack",
        "detail": "The officer draws a combat knife into his gloved hand and slashes at the air in a swift, practiced motion; the steel blade flashes in the ambient light as it cuts through the rain and his grip tightens on the handle."
      },
      {
        "name": "Forward Roll",
        "detail": "The officer drops into a low crouch and executes a forward roll across the wet asphalt, tucking his shoulder and rising smoothly back to his feet."
      }
    ],
    "jumpPrompt": "The officer springs upward off both feet, leaping high off the wet asphalt, his boots lifting clear of the ground before he drops back down and lands in a low crouch.",
    "crouchPrompt": "The camera lowers toward the ground as the character crouches down low, bending the knees and ducking the head into a compact, hunched stance; the viewpoint sinks smoothly to a low, near-ground vantage and settles there, close to the floor.",
    "standPrompt": "The character straightens back up out of the crouch, rising to full standing height as the camera lifts smoothly back to its normal eye-level vantage."
  }
}
```

**What it demonstrates.** Object-count pinning in the base ("EXACTLY ONE …
at a fixed position AND …") for the four landmarks that define the alley,
with texture (rain, puddles, tape) left unpinned. The weapon-framing guard
in *both* camera variants ("any weapon in his hands visible ahead — never a
first-person view") — this scene's keys put guns in his hands, which is
exactly when the model drifts into FPS framing. An events kit grouped by
type: ranged (pistol / flamethrower / rocket), melee (knife), maneuver
(roll). Disambiguation guards on the two riskiest props: the flamethrower's
"one sustained … stream … not separate shots" and the RPG's full "a long,
heavy cylindrical steel tube … not a handheld gun" spec. Action beats that
end settled ("rising smoothly back to his feet"). A scene-appropriate jump
that launches and lands.

## 2. Battlefield Horseman (`battlefield-horseman.json`)

```json
{
  "id": "case1_0038",
  "name": "Battlefield Horseman",
  "description": "Third-person mounted warrior — key 1 = snowstorm approaches, key 2 = horse lunge strike, key 3 = casts fire magic",
  "image": {
    "label": "Battlefield Horseman",
    "src": "/lingbot-cases/case1_0038.jpg"
  },
  "scene": {
    "base": {
      "default": "A warrior in green armor and a hood, mounted on a brown horse and holding a large curved blade, on a muddy battlefield strewn with scattered debris and a distant burning campfire. Somber, war-torn atmosphere under a heavy grey sky."
    },
    "camera": {
      "default": {
        "static": "Third-person view, the warrior and horse locked at the exact centre of the frame at constant size and distance. Neither the pair nor the camera moves on its own; arrow-key look-input is the only source of camera motion, arcing the camera around the stationary, centred pair only while held.",
        "dynamic": "Strict third-person rear view, the warrior and horse locked at the exact centre of the frame as the camera holds a fixed position behind them and tracks them forward. The camera does not rotate around the pair; look-input becomes the horse changing heading."
      }
    },
    "movement": {
      "default": {
        "static": "The warrior and horse stand completely still, the horse's tail and the warrior's cloak hanging undisturbed in the calm air, the horse's breath steaming faintly and one hoof shifting in the mud.",
        "dynamic": "The horse walks forward across the muddy field, moving directly away from the camera so the pair stay in strict rear view — the horse's hindquarters, rump, and streaming tail toward the viewer — hooves sinking and pulling free of the churned mud with each step as the warrior sways in the saddle and the cloak trails behind."
      }
    },
    "events": [
      {
        "name": "Snowstorm Approaches",
        "detail": "The sky darkens rapidly and a heavy blizzard sweeps in across the battlefield, howling wind driving dense sheets of thick snow sideways through the air. The whirling snowfall quickly builds into a near-whiteout, snow piling up over the muddy terrain, the warrior's armor and hood, the horse's back, and the scattered debris, frost creeping across every surface as the war-torn field is swallowed by a cold, roaring, white-grey storm."
      },
      {
        "name": "Horse Lunge Strike",
        "detail": "The warrior leans forward, guiding the horse into a sudden lunge. The large curved blade swings in a wide, downward arc, cleaving through the mud and shattering a nearby wooden shield into splinters."
      },
      {
        "name": "Casts Fire Magic",
        "detail": "The warrior raises the large curved blade high overhead toward the sky, and dark storm-clouds gather above as the blade glows with channeled energy. In answer, a rain of blazing fireballs streaks down from the sky, slamming into the muddy battlefield one after another in bursts of fire, smoke, and flying debris."
      }
    ],
    "jumpPrompt": "The horse leaps upward, launching off its hind legs so all four hooves lift clear of the muddy ground, the warrior rising with it in the saddle before the horse comes back down and lands.",
    "crouchPrompt": "The camera lowers toward the ground as the character crouches down low, bending the knees and ducking the head into a compact, hunched stance; the viewpoint sinks smoothly to a low, near-ground vantage and settles there, close to the floor.",
    "standPrompt": "The character straightens back up out of the crouch, rising to full standing height as the camera lifts smoothly back to its normal eye-level vantage."
  }
}
```

**What it demonstrates.** A compound subject ("the warrior and horse", then
"the pair") cast once in the base and carried by definite reference
everywhere else. The rear-view re-assertion inside `movement.dynamic`
("moving directly away from the camera … hindquarters, rump, and streaming
tail toward the viewer") — added in the field because a walking horse
otherwise drifts to a side profile; the camera layer states the rule, the
movement layer shows the geometry. The use-ready prop: the base holds the
blade in hand, so the lunge-strike and fire-magic keys compose without
re-arming him. Fire magic staged as a visible cause-and-effect chain (blade
raised → clouds gather → fireballs rain), paced with "one after another".
The environment transformation naming the surfaces it covers (terrain,
armor and hood, horse's back, debris). A mount-appropriate jump.

## 3. Jet Ski Cruise (`jet-ski-cruise.json`)

```json
{
  "id": "case2_1012",
  "name": "Jet Ski Cruise",
  "description": "Third-person jet ski — key 1 = meteor shower, key 2 = sunset glow, key 3 = rides with torch",
  "image": {
    "label": "Jet Ski Cruise",
    "src": "/lingbot-cases/case2_1012.jpg"
  },
  "scene": {
    "base": {
      "default": "A man in a red life vest on a white and red jet ski on turquoise water near a sandy beach lined with palm trees, a distant rocky outcrop on the horizon. Sunlit coastal atmosphere with light glinting off the calm sea."
    },
    "camera": {
      "default": {
        "static": "Third-person view, the man on the jet ski locked at the exact centre of the frame at constant size and distance. Neither the man nor the camera moves on its own; arrow-key look-input is the only source of camera motion, arcing the camera around the stationary, centred rider only while held.",
        "dynamic": "Strict third-person rear view, the man on the jet ski locked at the exact centre of the frame as the camera holds a fixed position behind him and tracks him forward. The camera does not rotate around the rider; look-input becomes the jet ski changing heading."
      }
    },
    "movement": {
      "default": {
        "static": "The man sits upright on the jet ski, hands resting on the handlebars, the craft bobbing gently on the swell as small wavelets lap against the hull and the calm water settles around it.",
        "dynamic": "The jet ski surges forward across the water, its rear thruster churning the turquoise sea into a wake of white foam, spray fanning out to either side as the man leans into the ride and the hull skips over the swell."
      }
    },
    "events": [
      {
        "name": "Meteor Shower",
        "detail": "Single meteors fall from high in the sky one after another — each a giant burning ball of rock dragging a long tail of fire and smoke straight down toward the sea. One by one they crash into the water far off near the horizon, away from the rider and never on the path ahead, each erupting in a huge fiery explosion and a towering burst of white spray before the next one follows."
      },
      {
        "name": "Sunset Glow",
        "detail": "The daylight deepens into a fiery sunset: the sun sinks low and rests right on the horizon, a huge, swollen orange-red disc half-dipping into the sea, while the sky above ignites in deep bands of amber, rose, and violet. Directly beneath it, the sun's reflection blazes across the water — a brilliant, unbroken path of molten gold stretching from the horizon straight toward the viewer, the rippling sea breaking it into shimmering streaks on every wavelet, the beach glowing warm amber."
      },
      {
        "name": "Rides with Torch",
        "detail": "The rider raises a burning torch high overhead in one hand, its orange flame streaming and flickering in the wind and trailing a ribbon of smoke, while his other hand grips the handlebars and the jet ski drives forward across the water, spray fanning off the hull."
      }
    ],
    "jumpPrompt": "The man and his jet ski leap up off the water, the hull lifting clear of the sea surface and rising into the air for a moment before dropping back down with a splash.",
    "crouchPrompt": "The camera lowers toward the ground as the character crouches down low, bending the knees and ducking the head into a compact, hunched stance; the viewpoint sinks smoothly to a low, near-ground vantage and settles there, close to the floor.",
    "standPrompt": "The character straightens back up out of the crouch, rising to full standing height as the camera lifts smoothly back to its normal eye-level vantage."
  }
}
```

**What it demonstrates.** Off-path staging of a held spectacle: the meteors
land "far off near the horizon, away from the rider and never on the path
ahead" — the player steers freely under WASD, so a hazard must be pinned
away from the play axis (this is a disambiguation guard, not
scene-painting by absence). Explicit pacing ("one by one … before the next
one follows") keeping the meteors discrete instead of a continuous smear.
"Sunset Glow" as a pure lighting transformation propagated onto named
surfaces (sky bands, the reflection path on the water, the beach). "Rides
with Torch" as an event that carries motion compatible with either
movement state — the torch is the change, the driving clause matches
`movement.dynamic` without contradicting the idle. A vehicle jump that
lifts off and lands with a splash.
