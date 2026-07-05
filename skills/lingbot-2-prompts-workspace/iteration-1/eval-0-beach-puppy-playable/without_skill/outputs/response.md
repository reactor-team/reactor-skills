# LingBot 2 prompt: driveable golden retriever puppy on a sunny beach

Here is a production-ready prompt set for a third-person navigable-subject world where the player drives a golden retriever puppy around a sunny beach with WASD.

## Base prompt

> Third-person chase camera locked behind a fluffy golden retriever puppy standing on a wide sunny beach at midday. The camera floats about one meter behind and slightly above the puppy, always keeping it centered in frame. The puppy has soft cream-gold fur, floppy ears, a wagging tail, and oversized paws that kick up little sprays of dry sand. The beach stretches endlessly: pale golden sand in the foreground, a bright turquoise ocean with small rolling white-foam waves on the right, low grassy dunes on the left, and a clear blue sky with a few small white clouds. Harsh cheerful midday sunlight, crisp shadows under the puppy, sparkling highlights on the wet sand near the waterline. Occasional seagulls drift overhead and a few scattered shells and pieces of driftwood dot the sand. The puppy idles in place, panting happily, ears twitching, tail wagging, waiting for movement input. Bright, playful, photoreal style with shallow depth of field kept subtle so the whole beach stays readable.

## Hold prompts (movement inputs)

**Hold W (forward):** The golden retriever puppy bounds forward across the sand in a happy gallop, ears flapping, tongue out, paws throwing up small puffs of dry sand. The chase camera glides forward with it at constant distance, staying one meter behind and slightly above. New beach scrolls in from the horizon: more pale sand, the turquoise surf staying on the right, dunes staying on the left. Sunlight and shadow direction stay fixed.

**Hold S (backward):** The puppy slows, plants its front paws, and trots backward a few steps toward the camera, then settles into an alert stance. The camera eases back with it, keeping the framing identical. Sand kicks lightly off its rear paws. Ocean stays on the right, dunes on the left, lighting unchanged.

**Hold A (turn left):** The puppy leans and curves to the left in a playful arc toward the grassy dunes, tail out for balance, paws digging into the sand on the turn. The camera swings smoothly with it, staying locked behind the puppy so the dunes rotate into the center of frame and the ocean slides toward the right edge. Same midday sun, same crisp shadows.

**Hold D (turn right):** The puppy leans and curves to the right in a playful arc toward the waterline, splashing through the thin sheet of wet reflective sand at the surf's edge, tiny droplets and foam flicking off its paws. The camera swings smoothly with it, staying locked behind the puppy so the sparkling turquoise water rotates into the center of frame. Same midday sun, same crisp shadows.

**Idle (no input):** The puppy stands still on the sand, panting happily, tail wagging, occasionally cocking its head or sniffing the ground. Waves keep rolling in on the right, seagulls drift overhead, gentle heat shimmer near the horizon. Camera holds steady one meter behind and slightly above.

## Design notes

- **Chase camera anchoring:** the camera offset ("one meter behind and slightly above, puppy centered") is repeated in the base and every hold so the framing never drifts between generated segments.
- **Spatial consistency anchors:** ocean on the right, dunes on the left, and a fixed midday sun with crisp shadows are restated in each hold. These act as landmarks so turning left vs right produces visibly different, coherent world rotation.
- **Subject consistency:** the puppy's identity traits (cream-gold fur, floppy ears, wagging tail, oversized paws) are described once in the base and referenced consistently, so the model keeps the same dog across states.
- **Motion cues per input:** each direction has a distinct locomotion verb (gallop forward, backpedal, arcing lean left/right) plus a physical sand/water interaction, which gives the model strong per-input differentiation.
- **Idle state:** included so the world stays alive (waves, gulls, panting) when no key is held instead of freezing.

## Files

- `base_prompt.txt` - the base scene prompt on its own
- `hold_prompts.txt` - all five input-state prompts
- `world.json` - the full structured world (base + holds + camera + consistency anchors) for lingbot-world-fast-v1
