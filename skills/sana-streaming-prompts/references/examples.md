# SANA-Streaming Production Exemplars

Ground-truth instructions from NVIDIA's SANA-Streaming model page, grouped by edit type. Use these as few-shot models — match their tone, concreteness, and density. Notice how each names a specific target, gives a capped specification, ties new material to the existing light, and enumerates what stays fixed. None of them say "keep everything else the same."

## Table of Contents

- [Local — remove](#local--remove)
- [Local — replace](#local--replace)
- [Local — add / overlay](#local--add--overlay)
- [Background](#background)
- [Style transfer](#style-transfer)
- [Scene transform (composite)](#scene-transform-composite)
- [One source → multiple edits](#one-source--multiple-edits)
- [Physical AI](#physical-ai)

---

## Local — remove

- Remove the thick textured gold hoop earrings; reconstruct the exposed earlobes to match the surrounding skin tone and texture, blending lighting and shadows naturally, leaving no metallic trace or reflection.
- Remove the white "GagaOOLala" watermark logo in the top-left corner; seamlessly blend the region with the surrounding sky, foliage, and building edges, with temporally consistent inpainting.
- Remove the woman with shoulder-length blonde hair in a black blazer from the entire sequence; fill the space with temporally consistent background inpainting, leaving all other content unchanged.

**Pattern:** name the target precisely → reconstruct the revealed region to match its surroundings → assert no trace and temporally consistent inpainting.

## Local — replace

**Garment / object:**

- Replace the white button-up shirt with a dark navy silk blouse featuring a draped ruffled collar and iridescent pearl buttons; the silk should have a subtle sheen reflecting the warm golden lamp light throughout the sequence. Preserve the subject's pose, motion, identity, the background, and the scene's depth of field and lighting.
- Replace the white-and-red track jacket with a vintage dark-brown leather aviator jacket with a cream shearling collar, distressed leather, and an antique brass zipper, interacting naturally with the warm golden ambient light. Preserve pose, motion, identity, background, and lighting.
- Replace the green muscle car with a sleek metallic red muscle car in the same position and pose, its glossy paint catching the existing light. Keep the background, camera motion, and lighting unchanged.

**Subject / creature:**

- Transform the middle-aged man into an elderly gentleman with silver hair and natural wrinkles, in the same position and pose. Preserve his exact body and head motion, the background, and the original camera movement and lighting across all frames.

**Pattern:** old → new with a rich-but-capped attribute stack → one material-physics clause tying it to the existing light → enumerated preservation. Garment/object preserves *identity*; subject preserves *pose and the subject's own motion*.

## Local — add / overlay

- Add delicate round gold-wire eyeglasses resting on the bridge of the nose, the clear lenses catching soft reflections from the ambient light; preserve the subject's tearful expression and all other content, keeping the glasses tracked to the face as the head moves.
- Overlay an animated colorful kite in the upper-left sky; it flutters and sways with its tail moving in the wind, staying tracked to the sky as the camera moves, with dynamic lighting and shadows. All other parts of the video remain unchanged.

**Pattern:** add the element with attributes → say how it rests/moves and that it stays tracked as the camera moves → lenses/surfaces catch realistic reflections → everything else unchanged.

## Background

- Replace the black studio background with a minimalist white-and-gray showroom with light-gray paneled walls and an overhead softbox. Keep the subject perfectly still — preserve her pose, hand motion, top, jewelry, and skin tone, and maintain the shallow depth of field.
- Replace the background with a rain-streaked windowpane at dusk, with out-of-focus teal and amber city lights, condensation, and raindrops trickling down the glass; keep a shallow depth of field. Do not alter the subject's lighting or appearance, and maintain seamless consistency across all frames.
- Replace the background with an overcast European street with stone buildings, a wrought-iron lamp, and wet cobblestones; match the soft diffused daylight to the existing light on the subject, keeping the subject and foreground perfectly still.
- Replace the background with [a modern art gallery / an ancient Roman forum / a celestial night sky / a tropical beach at sunset], injecting subtle background motion ([passing footsteps / fluttering banners / shooting stars / rolling waves]) while keeping the subject perfectly still and matching the new environment's light to the subject.

**Pattern:** new scene with enumerated elements and mood → optional *deliberate* background-motion injection → subject and foreground held unchanged → match new-scene light to the subject → temporal consistency. (These exemplars use posed, static subjects, so "perfectly still" fits them. You can't see the user's source — so preserve the subject's *existing* motion rather than asserting stillness, unless the user said the subject is static.)

## Style transfer

- Apply an impressionist oil-painting style to this video, ensuring seamless temporal consistency across all frames. The output should mirror visible brushstrokes and broken color while preserving all original motion, character actions, camera movement, and composition, with no jarring frames.
- Apply a Fauvist painting style with electric blues, greens, and oranges, thick brushstrokes, bold outlines, and flat saturated color blocks. Preserve all original motion, actions, camera movement, and composition, with seamless temporal consistency and no jarring frames.
- Apply a sci-fi digital-painting style with holographic bokeh, luminescent skin, and neon blues, cyans, and purples. Preserve all original motion, actions, camera movement, and composition across all frames.
- Other demonstrated styles: watercolor, Chinese ink wash, ancient-scroll / temple-mural aesthetic, a "dawn" aesthetic. All assert seamless temporal consistency and preserve motion, actions, and camera.

**Pattern:** name the style → describe its concrete visual characteristics → preserve motion/actions/camera/composition → assert temporal consistency. Style recolors and repaints; it does not move anything.

## Scene transform (composite)

- Re-render the office as a warm antique wall fresco: convert the man, desk, laptop, notebook, shelves, plants, and lamp into hand-painted ochre and faded-blue forms with visible brush texture, a gilded border, plaster grain, and fine cracks. Preserve the original composition, gestures, object layout, and temporal motion.

**Pattern:** SCENE_TRANSFORM goes beyond STYLE — it lists the object inventory and rebuilds each item as the new medium, then adds medium artifacts (border, cracks, grain). Still preserves composition, gestures, layout, and motion.

## One source → multiple edits

Independent instructions run separately over the same source — write them as separate prompts, not one combined instruction:

- Source A: (1) swap the background to a 1920s speakeasy; (2) replace the jacket with a burgundy velvet smoking jacket.
- Source B: (1) swap the background to a high-rise office; (2) remove the flower arrangement.

## Physical AI

- Transform this driving-camera feed into a scene with light snowfall at dawn, adding soft falling snow and a cool pale light; keep all vehicles, road geometry, lane markings, signs, and motion unchanged, and maintain temporal consistency throughout.
- Transform this driving feed into cold rain at dusk, adding wet road reflections and a dim blue cast; keep all vehicles, road geometry, lane markings, signs, and trajectory unchanged.
- In this egocentric manipulation video, replace the human limbs with articulated dark-silver robot arms and hands with exposed joints and visible cables; keep the objects, tools, lighting, camera motion, shadows, contacts, and timing unchanged, with temporal consistency throughout.

**Pattern:** Physical AI is domain-rigorous — preservation is maximal and specific (lanes, geometry, signs, trajectory for driving; objects, tools, contacts, timing for manipulation). The restyle changes appearance only; nothing about the physics or geometry shifts.
