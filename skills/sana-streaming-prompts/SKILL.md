---
name: sana-streaming-prompts
description: Turn rough video-editing intent into precise, production-grade instructions for NVIDIA's SANA-Streaming real-time video-to-video editing model. Use whenever the user wants to edit, restyle, or transform an existing video with SANA-Streaming — swapping outfits, changing backgrounds, removing objects or watermarks, adding tracked overlays, applying an art style, re-rendering a whole scene, or restyling driving/robotics footage. Trigger on any mention of SANA, SANA-Streaming, "video edit prompt," or a request to write or improve a video-editing instruction, even when the user doesn't name the model.
---

# SANA-Streaming Prompt Writing

SANA-Streaming **edits an existing video**; it does not generate one from scratch. Every instruction describes a *change to a source* while the motion, geometry, and untouched content carry through unchanged. The model takes one self-contained natural-language instruction and holds it constant across the whole clip.

This skill converts a vague edit request ("make the jacket leather," "give it a watercolor look") into a concrete, bounded instruction the model can execute reliably. The model has **no way to resolve ambiguity** — underspecified prompts produce inconsistent or wrong edits — so the enhancer's whole job is to replace vague intent with specific, physically-grounded detail without over-embellishing.

## Your output

Produce **one self-contained instruction**, typically **2–5 sentences**, phrased as a change to the source — and nothing else. The deliverable is meant to be pasted straight into the model, so it must be *only* the editing instruction: no preamble, no labels, no "Assumptions" note, no trailing commentary riding along inside it. If the user describes several independent edits, write one instruction per edit (the model runs them separately over the same source).

The user often won't describe their source video, and you can't see it. Don't block on it, and don't clutter the prompt with caveats — just write a complete, clean instruction. The one thing genuinely worth **inferring is the lighting** (temperature and direction), because the *material-physics* clause names it concretely — "catches the warm golden light" — and no generic phrasing substitutes. Pick the most likely lighting and fold it straight into the instruction.

Do **not** guess at motion or camera and bake in a specific state ("perfectly still," "walking," "slow pan") — you can't see the footage, and a wrong guess is exactly what freezes a moving subject or animates a still one. Preserve them *generically* instead — "preserve the subject's existing motion," "stays tracked as the camera moves" — which holds true whatever the source does. Name a specific motion only when the user told you what it is.

## Workflow

1. **Classify** the edit into one of the seven types below — this picks the template and the preservation set.
2. **Reconstruct the source**: note (or infer) the lighting, camera, and subject motion you'll need to reference.
3. **Build** the instruction from the grammar slots for that type.
4. **Verify** against the four quality axes and guardrails before returning it.

## Step 1 — Classify the edit

| Type | What it does | Route when the user wants to… |
|---|---|---|
| **LOCAL_REMOVE** | Delete an element, inpaint behind it | remove an object, person, watermark, logo, blemish |
| **LOCAL_REPLACE** | Swap a garment, object, or the subject itself | change an outfit, recolor/repattern clothing, swap a car, age a person, turn subject into a creature/character |
| **LOCAL_ADD** | Add or overlay a new tracked element | add glasses, jewelry, a kite, a lantern — something that tracks the scene |
| **BACKGROUND** | Replace the scene behind a preserved subject | change the setting while keeping the subject still |
| **STYLE** | Apply an art style to the whole video | watercolor, oil painting, Fauvist, sci-fi, ink wash, a named aesthetic |
| **SCENE_TRANSFORM** | Re-render the entire scene as a medium, with an object inventory | "turn this office into a fresco/mural" — every object converted |
| **PHYSICAL_AI** | Domain-rigorous restyle of sensor/robotics footage | change weather/time-of-day on driving footage, swap human limbs for robot arms |

LOCAL_REPLACE has two flavors with different preservation needs: **object/garment** (preserve identity) and **subject/creature** (preserve pose and the subject's own motion). STYLE recolors/repaints; SCENE_TRANSFORM goes further and rebuilds every object as the new medium.

## Step 2 — Reconstruct the source

You're working blind, so be deliberate about what you pin down versus what you leave generic:

- **Lighting — infer it.** Temperature and direction (e.g. "warm golden lamp light from the left," "soft diffused overcast daylight," "cool neon from below"). The material-physics clause names this concretely, so a vague guess won't do — pick the most likely lighting for the described scene and fold it straight into the instruction. A plausible, specific guess beats a hole.
- **Motion and camera — keep them generic.** Don't assert a state you can't see. Preserve them with phrasing that's true regardless — "preserve the subject's existing motion," "stays tracked to the face as the camera moves" — rather than naming "perfectly still" or "walking." Name a specific motion only when the user told you what it is.

## Step 3 — Build the instruction (grammar slots)

Assemble the applicable slots in order. Not every slot applies to every type — the templates below show which.

1. **Target + action** — name what changes with 1–3 disambiguating attributes, then the verb. "The white button-up shirt" not "the shirt."
2. **Specification** *(replace / add)* — the new content with 2–4 concrete sub-details (see vocabulary below).
3. **Material physics** *(replace / add)* — **one** sentence on how the new material behaves under the *existing* light (catches, reflects, scatters, stays matte).
4. **Consequence** *(remove)* — reconstruct what's revealed to match the surrounding surface and lighting, leaving no trace, outline, or reflection.
5. **Motion behavior** *(add)* — how the element moves and that it stays tracked to the face/sky/surface as the camera moves.
6. **Preservation** *(always)* — enumerate the specific axes held constant. Never write "keep the rest the same"; name them.
7. **Temporal** *(style / scene / background)* — assert seamless consistency across all frames, no frame-to-frame jumps.

### Concrete-detail vocabulary

Specification should draw from these dimensions (use the ones that matter; don't force all six):

- **Material** — silk, leather, velvet, scales, plaster, brushed metal, woven wool
- **Color** — named and specific: dark navy, cream shearling, muted teal, faded ochre (not "blue")
- **Silhouette / shape** — draped ruffled collar, round wire frames, peak lapels, boxy cut
- **Texture** — distressed, brushed, iridescent, woven, cracked, grainy
- **Lighting interaction** — how it catches the *existing* light (subtle sheen, soft reflections, matte)
- **Style coherence** — consistent with the scene's overall look

### Preservation sets by type

Enumerate the axes that fit the edit. Defaults:

| Type | Preserve |
|---|---|
| Replace (subject/creature) | exact pose, body & head motion, background, camera movement, lighting |
| Replace (object/garment) | pose, motion, identity, background, depth of field, lighting |
| Remove | all other content unchanged; temporally consistent background inpainting |
| Add | all other parts of the video unchanged |
| Background | subject + foreground unchanged, existing motion and position preserved; match new-scene light to the subject's existing light |
| Style / scene | original motion, character actions, camera movement, composition; no jarring frames |
| Physical AI | lanes, vehicles, road geometry, signs, camera motion, trajectory (or objects, tools, contacts, timing) |

## Per-category templates

Fill the brackets. These produce the 2–5 sentence shape the model expects.

```
LOCAL_REMOVE
Remove [TARGET + attributes] from [LOCATION]. Reconstruct the revealed region to match the
surrounding [skin / surface / texture] and lighting, leaving no trace, outline, or reflection.
Leave all other video content unchanged with temporally consistent background inpainting.

LOCAL_REPLACE (object / garment)
Replace [OLD + attributes] with [NEW + 2–4 sub-details]. Ensure the [MATERIAL] catches and
reflects the [light temperature / direction] from [light source] throughout the sequence.
Preserve the subject's pose, motion, identity, the background, and the scene's depth of field
and lighting.

LOCAL_REPLACE (subject / creature)
Transform the subject into [NEW FORM], replacing [skin / features] with [attributes] and
[reshape detail]. Ensure [surface] catches the existing ambient light with [sheen / shimmer]
that follows the subject's movement. Preserve the subject's exact pose, body and head motion,
the background, and the original camera movement and lighting across all frames.

LOCAL_ADD
Add [ELEMENT + attributes] in [LOCATION], [resting / behaving] naturally, with [lenses /
surfaces] catching realistic reflections from the ambient lighting. It must stay tracked to
[face / sky / surface] as the camera moves, with lighting and shadows adjusting. All other
parts of the video remain unchanged.

BACKGROUND
Replace the background with [NEW SCENE + mood + attributes], featuring [enumerated elements]
[optional: with subtle motion of X, Y, Z]. Keep the subject and all foreground elements
unchanged, preserving their existing motion and position, and match the new environment's
light to the existing light on the subject, maintaining seamless consistency across all frames.

STYLE
Apply [STYLE] to this video, ensuring seamless temporal consistency across all frames. The
output should [emulate / mirror] [AESTHETIC TARGET], with [visual characteristics]. Preserve
all original motion, character actions, camera movement, and composition, with no jarring frames.

SCENE_TRANSFORM
Transform the entire scene into [STYLE / MEDIUM]. Convert [OBJECT INVENTORY] into [STYLE] forms
with [tones / outlines / texture] and [added artifacts: border / cracks / grain]. Preserve the
original composition, gestures, object layout, and temporal motion.

PHYSICAL_AI
Transform this [sensor feed] into [new condition + attributes], adding [condition effects].
Keep all [lanes / vehicles / geometry / signs / trajectory] (or [objects / tools / contacts /
timing]) unchanged, and maintain temporal consistency throughout.
```

## Worked example

**User:** "make her shirt into a nice silk blouse"

**Classify:** LOCAL_REPLACE (garment). **Reconstruct:** source not described → infer a warm indoor lamp and a gently-moving subject.

**Output:**
> Replace the white button-up shirt with a dark navy silk blouse featuring a draped ruffled collar and iridescent pearl buttons. Ensure the silk catches and reflects the warm golden lamp light with a subtle sheen throughout the sequence. Preserve the subject's pose, body and head motion, her identity, the background, and the scene's depth of field and lighting.
>
That's the whole deliverable — clean, ready to paste, no caveats attached. The specification (navy / silk / draped ruffled collar / pearl buttons) is concrete but capped, the inferred warm lamp light is folded straight into the material-physics clause, and the preservation clause names axes (including "body and head motion," which keeps whatever motion is there without guessing at it) instead of saying "keep everything else." If the user needs to know the lighting was an assumption, that goes in a line of chat — never in the prompt.

## Verify against the four quality axes

The model's own training rubric scored edits on these four. A good instruction serves all four — use them as a final check:

1. **Instruction alignment** — is the requested change unambiguous? (specific target + action + enumerated specification)
2. **Non-edit consistency & temporal stability** — did you enumerate preservation and assert temporal consistency where it matters?
3. **Physical plausibility** — does the new content interact correctly with the existing light/geometry/motion? (material-physics clause; for Physical AI, geometry/contacts/timing)
4. **Video quality** — is every detail concrete and unambiguous? Vague adjectives degrade output.

## Guardrails

- **Specific, but bounded.** Detail helps; runaway adjective stacking hurts. Keep material-physics to one clause and the whole instruction to ~2–5 sentences. The production examples are tight.
- **Respect the motion contract.** You can't see the source, so preserve the subject's *existing* motion rather than asserting a state ("perfectly still," "walking") you're only guessing at — a wrong guess freezes a moving subject or animates a still one. Background-motion injection (waves, footsteps, shooting stars behind the subject) is a *deliberate, separate* choice — only add it when asked or when it clearly serves the edit, and say so.
- **Don't invent content.** No text, logos, watermarks, or brand names unless the user names them.
- **Editing, not authoring.** Always phrase as a change to the source. The source's motion and geometry are preserved by design *and* by your preservation clause — both, not one.
- **Keep the prompt pristine.** The deliverable is only the editing instruction — no "Assumptions" note, labels, or commentary attached, so it can be pasted straight into the model. Inferences (like the lighting) are folded silently into the instruction. If a judgment call genuinely warrants a heads-up — say you held the original timing constant when a requested style implied a timing change — put it in a line of chat around the prompt, not inside it.

## Checklist

Before returning an instruction, verify:

- [ ] Phrased as a change to an existing source, not a scene from scratch
- [ ] Edit classified; correct template and preservation set used
- [ ] Target named with disambiguating attributes (not just "the shirt")
- [ ] Specification is concrete (material/color/shape/texture) but capped — no adjective pileup
- [ ] Material-physics clause references the *existing* light (replace/add)
- [ ] Removed elements: revealed region reconstructed, no trace/outline/reflection
- [ ] Added elements: motion described + stays tracked as the camera moves
- [ ] Preservation clause enumerates specific axes (never "keep the rest the same")
- [ ] Temporal-consistency asserted for style/scene/background edits
- [ ] Motion preserved generically — no asserted state ("perfectly still," "walking") unless the user said so
- [ ] No invented text/logos/brands
- [ ] Length is ~2–5 sentences
- [ ] Deliverable is the clean instruction only — no "Assumptions" note or commentary attached to the prompt

For the full library of production exemplars grouped by edit type — useful as few-shot models to match tone and density — see [references/examples.md](references/examples.md).
