# Prose mode, base + holds, written as text

Read this before producing a **prose** prompt (SKILL.md §2.2). A prose prompt is
the same model as a JSON world, just not serialized: it is a **degenerate
one-state world rendered as labeled text**. The base block is the entrance state
composed at rest; each hold block is a single overlay event written out as the
full prompt it produces while held. Use prose mode for quick asks ("make me a
prompt for…", "base + a couple of holds"); use a JSON world when the user wants
something an app imports and runs (states, transitions, interactivity).

Everything in SKILL.md §3 (encoder invariants, the six anchors) and
`references/viewpoints.md` (the per-viewpoint opener) still applies. You usually
won't run the token tool for a single prose prompt, but compose mentally and
keep each block well under 512 tokens (aim ≤480).

---

## 1. The base block

A base prompt is **2-4 sentences**, every anchor present, dense clausal detail.
Assemble it with this slot template (the brackets are traversal-only):

```
{{world}}. {{sensation}}. {{event}}[, {{motion_resolution}}]. {{mood}}.
```

| Slot | What it is |
|---|---|
| `{{world}}` | Where we are (+ how, if moving). The viewpoint opener from `references/viewpoints.md` lives here. |
| `{{sensation}}` | One physical cause-and-effect grounding the dynamics. The most load-bearing and most-skipped slot, never drop it. |
| `{{event}}` | The one thing that moves, resolves, or reveals. **One only.** |
| `{{motion_resolution}}` | **Traversal only.** Far-plane detail sharpening as you approach: *"its [detail] becoming clearer against [far backdrop]."* |
| `{{mood}}` | One atmospheric phrase. Not three. Place it last. |

**Density rule:** 2-4 sentences, each carrying ≥2 anchors and ≥1 concrete
physical detail. Densify by extending clauses *within* sentences, never by
adding sentences. Over 4 sentences → fold short ones together. The six anchors
(POV, subject, near, mid, far, atmosphere/sensation) must all appear.

**Openers by viewpoint** (from `references/viewpoints.md`):

- **First-person traversal**, *"The video presents a [soaring journey / slow
  descent / low race] through [world]…"* The "video presents" narrative opener
  primes traversal.
- **Third-person navigable**, *"This is a third-person rear-view
  [driving/riding/chase] game video of [subject]…"* ("game" and "rear-view" are
  load-bearing, see viewpoints.md §1).
- **Spectator**, open **directly** with the scene: *"A serene lakeside at
  dusk…"* No POV claim, no "video presents".

### Sensation fallback

If the sensation isn't obvious from the input, anchor to the environment's
physics: forest → wind through canopy, branches swaying; desert → dust trails in
thermals, heat-haze; underwater → pressure on the viewport, drifting sediment;
urban → rain fracturing neon, steam from grates; alpine → cold through stone, ice
crystals; aerial → G-force, cloud wisps tearing past; space → silence as physical
absence, fixed far light vs. drifting near objects. Every environment has
physics, sparse input is not a license for golden-hour cliché.

---

## 2. Holds

Production prose ships as **base + 1-3 holds**. A hold is a **complete re-prompt**
that swaps the model's text condition mid-session, anchored to the base, not a
short trigger word. Each hold is the same density as the base. Two kinds (mix to
fit the scene):

- **Local**, inject one element (lightning, fireworks, fire breath, a bird).
  The world stays; the element is added.
- **Global**, replace atmosphere/lighting/style (nightfall, winter, pixel-art, steampunk). Geometry and subject stay; rendering changes.

In world terms: a local hold is a **detail-only overlay**; a global hold is an
overlay whose **`base` is re-skinned**. Either way, write the full composed
prompt the hold produces.

### The four hold invariants

1. **Anchor preservation.** Preserve the base's anchors, POV, body/vehicle, the
   near/mid/far geometry, atmosphere. Default is **verbatim**, including the
   base's opener; paraphrase only when the event mechanically forces it (a global
   relight, a framing change). Keep ≥6 of the base's anchors; dropping more than
   one requires an explicit framing-change clause.
2. **Event-anchor back-coupling.** Name how the event physically touches
   preserved surfaces, *fireworks reflecting on the dragon's wings and glinting
   off its scales*, *lightning silvering the wet deck and foam crests*, *night
   neon reflecting in the suit's chrome*. **At least two** interaction effects, or the event reads like a sticker pasted over the scene.
3. **State-delta minimality.** Change only what the event physically forces.
   Fire breath → jaws open, neck stretched (the saddle, reins, armour stay
   exactly as written). A global relight → lighting changes, geometry does not.
   Don't polish un-asked anchors, that's how load-bearing detail silently drops.
4. **Camera-lock language when (and only when) framing changes.** Most holds keep
   the base framing. When one needs a wider shot (fire breath needs the whole
   dragon in frame), state the lock in three parts: the new framing positively
   (*"a high wide aerial from behind and above"*), what the camera must **not**
   do (*"the lens never zooms in on the head"*), and **why** (*"so the dragon's
   full wingspan is never cropped"*). All three are load-bearing.

### Opener discipline for holds

Holds **preserve the base's opening anchors verbatim** (invariant 1). Do **not**
invent a fresh narrative opener for a hold or reframe it as a new video, a hold
is a state of the *same* world. (A global hold still preserves the geometry
anchors; it only re-skins lighting/style and propagates that onto surfaces per
invariant 2.)

---

## 3. Output format

Plain prose, labeled blocks, nothing else:

```
Base, [scenario name]
[base prose, 2-4 sentences, all anchors present]

Hold 1, [event name]
[hold prose, full re-prompt at base density]

Hold 2, [event name]
[hold prose]
```

**Base-only override**, if the user says "just the scene prompt" / "no holds" /
"base only", output **one** block as plain prose with no label:

```
[base prose]
```

### What never appears in prose output

- Mode/viewpoint labels ("Mode: Traversal", "Viewpoint: spectator")
- Slot breakdowns or per-sentence annotations
- Notes about camera language you stripped
- Anchor counts, token counts, red-flag check reports
- Alternate mood variants
- Any preamble, commentary, or explanation beyond the block labels

The slot template, viewpoint recipe, sensation table, anchor checklist, and
invariants are internal scaffolding, use them to build the prompt, then output
only the labeled blocks. Provide annotations or reasoning **only** if the user
explicitly asks for them.

---

## 4. Worked shape (first-person traversal, dune approach)

Input: *"a dune buggy heading toward a sand-buried temple."*

```
Base, Dune approach
The video presents a low-altitude race across a sun-baked dune sea toward a
colossal sand-buried temple. Dust trails spin off the cracked rear cowling in
fine thermal threads and the leather-wrapped throttle in the driver's gloved
hand vibrates against scoured chrome. The half-buried obelisks resolve steadily,
their carved glyphs sharpening against a horizon of heat-haze warping the distant
escarpment. Dry, blinding noon.

Hold 1, Sandstorm
[base anchors verbatim: the race, the cowling, the throttle, the obelisks] + a
wall of ochre sandstorm slams in from the windward edge, churning visibility to
inches; sand grains hammer the cowling and skip across the gloved hand, the
glyphs stuttering behind racing sheets of grit, the escarpment erased. Dry,
blinding fury.

Hold 2, Night
[base anchors verbatim] re-skinned to a moon-drenched cobalt night: dust trails
catch a cyan glow and the throttle gleams against chrome holding moonlight, the
obelisks resolving against an escarpment read as black silhouette under cold
stars. Cold, hushed, electric.
```

Hold 1 is **local** (sandstorm injected; geometry preserved; back-coupled onto
cowling and hand). Hold 2 is **global** (noon → night; geometry preserved,
surfaces re-skinned, the surface-propagation rule). The bracketed notes above
are explanatory only; in real output the preserved anchors are written out in
full, not bracketed.
