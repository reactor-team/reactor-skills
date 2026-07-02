# Token budget, calibration, shares, rebalancing

The encoder is **UMT5-XXL, hard cap 512 tokens**, beyond it the tail is
silently truncated. Soft target **≤480** (leaves headroom for special tokens and
iteration drift). All numbers are **measured** with `tools/scene_report.py` (JSON
worlds) or `tools/token_count.py` (a fragment), never estimated. UMT5 runs
~1.5-1.6 tok/word on this descriptive prose and varies sharply with vocabulary,
so word-count multipliers are off by enough (50+ tok) to silently breach 512.

---

## Per-layer starting targets

Starting values from the production reference scenes, **not caps**. A heavier
layer is fine if every composition still fits ≤480.

| Layer | Start | Observed range |
|---|---|---|
| `base` (per state) | ~140 | 129-199 |
| `camera.static` | ~30-60 | 31-120 |
| `camera.dynamic` | ~60 | 44-120 |
| `movement.static` | ~80 | 41-167 |
| `movement.dynamic` | ~60 | 41-84 |
| detail-only event `detail` | ~80 | 40-150 |
| high-density override (base+cam+mov, ± detail) | ~260-400 total | 250-400 |

## Composition targets

| Composition | Soft target | Observed |
|---|---|---|
| state at rest | ≤380 | 290-394 |
| state in motion | ≤380 | 286-397 |
| state + detail-only event | ≤460 | 362-468 |
| state + high-density override | ≤480 | 294-500 |

Storm Crossing's tightest single-event composition is *Fireballs* over
`flying_calm` at **500 tok in motion**, fits, but no headroom. Anything that
pushes such a composition over 512 is a hard fail.

---

## Cap-share reading (composition tokens / 512)

| Share | Reading | Action |
|---|---|---|
| < 50% | under-filled, prompt is thin | grow the `base` scaffold / add anchors |
| 50-75% | comfortable working range | fine |
| 75-94% | tight, fits, no headroom | fine alone; watch before stacking |
| ≥ 95% / > 480 | at cap | trim before adding anything |

`scene_report.py` prints "tight" above 480 and "EXCEEDS" above 512.

---

## Event signal share (R8)

`scene_report.py` reports, per event over each from-state and branch:

```
event_signal_share = event-authored tokens / composed-while-held tokens
```

where event-authored = the event's overridden-layer prose + its detail (the
inherited state layers are *not* event signal). It is a per-piece approximation,
so a full-override event (all three layers + detail, nothing inherited) reads
~100% and may print slightly over (101%) from token-boundary effects, that's
expected, not a bug.

| Share | Reading | Action |
|---|---|---|
| < 20% | drowned, the model often skips it | fix required |
| 20-30% | at risk; renders only if very concrete | fix recommended |
| 30-50% | healthy for an overlay | ok |
| 50%+ | healthy for a transition / high-density override | ok |

**Fixing a drowned event**, in order of leverage:

1. **Trim the state's inherited layers** if bloated, one trim helps every event
   held in that state.
2. **Move the event's content into a layer override** instead of `detail`, a
   `base` override that re-asserts the world with the event's atmosphere baked in
   raises the share sharply (and closes R6's contradiction gap).
3. **Make the detail more concrete**, named imagery, articulated micro-events, back-coupling onto surfaces. Generic detail ("the dog runs around") gets
   dropped; specific detail ("paws plant among the wildflowers, tail still
   settling") survives.

---

## Rebalancing order

When a composition is over budget, trim in this order, protect `base` last
because it feeds every event:

1. `movement.{static, dynamic}`, usually the most fat (heavy negation, over-described idle behavior).
2. `camera.{static, dynamic}`, repeated invariant language; tighten without
   losing the lock.
3. `base`, last resort, and never compress its near/mid/far geometry to make
   room for an event (that's the wrong direction, rescope the event instead).

---

## Multi-event combinations

The baseline contract guarantees **per-event-alone** safety only. With N overlays
there are 2^N−1 holdable subsets, un-trackable, and auto-probing leads to
compressing every event to a sentence just to make the cartesian product fit.

Do **not** auto-validate combinations. When the user explicitly wants to hold
specific overlays together, check that one:

```
pipx run tools/scene_report.py scene.json --held 0,3 --state flying_calm
```

If it overruns, surface three options and let the user pick: (a) shrink the
events involved, (b) accept truncation when held together, or (c) document the
combination as unsupported. Never pre-shrink for a combination the user only
mentioned in passing.
