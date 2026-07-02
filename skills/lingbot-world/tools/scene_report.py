# Copyright (c) 2026 Reactor Technologies, Inc. All rights reserved.
#
# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "transformers>=4.40",
#   "sentencepiece",
#   "ftfy",
# ]
# ///

"""Analyze a LingBot virtual-world JSON file (FSM schema).

Reports per-layer token counts, every composition the runtime can
produce, each event's token share of its composed-while-held prompt,
and budget / structural warnings. Designed so the lingbot-world skill
never has to count tokens or replay composition math in-context — it
edits the JSON and reads this report.

Schema follows ``public-demos/lib/lingbot-world-prompts.ts`` — a finite
state machine per scene with layered events::

    {
      "id": "...",
      "name": "...",
      "description": "...",                       (optional)
      "entrance": { "image": {...}, "state": "<state key>" },
      "scene": {
        "states": {
          "<stateKey>": {
            "base":     "...",
            "camera":   { "static": "...", "dynamic": "..." },
            "movement": { "static": "...", "dynamic": "..." }
          }
        },
        "events": [
          {
            "name": "...",
            "kind": "overlay" | "transition",
            "from": ["<stateKey>", ...],          (non-empty)
            "to":   "<stateKey>",                  (required iff transition)
            "base":     "...",                     (optional layer override)
            "camera":   { "static": "...", "dynamic": "..." },
            "movement": { "static": "...", "dynamic": "..." },
            "detail":   "..." | { "static": "...", "dynamic": "..." }
          }
        ]
      }
    }

An omitted override field inherits the current state's layer; a field
set to "" (or {static:"",dynamic:""}) suppresses that layer.

CLI::

    pipx run tools/scene_report.py path/to/scene.json
    pipx run tools/scene_report.py -                       # stdin
    pipx run tools/scene_report.py scene.json --json       # machine-readable
    pipx run tools/scene_report.py scene.json --held 0,3 --state flying_calm
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent))
from token_count import count_tokens  # noqa: E402

# Encoder hard cap. Matches DEFAULT_MAX_SEQUENCE_LENGTH in token_count.py
# and wan_shared_cfg.text_len. This is the only quantitative threshold
# the tool enforces — every other "is this number good or bad?" question
# is intentionally pushed to the skill (references/token-budget.md), so
# recalibrating recommendations does not require code changes.
CAP = 512


# ---------- Loading ----------

def load_scene(source: str | Path) -> dict[str, Any]:
    if source == "-":
        return json.load(sys.stdin)
    with open(source, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------- Composition (ports composeForRender from lingbot-world-prompts.ts) ----------

def _shot_of(v: dict[str, str] | None, is_moving: bool) -> str:
    if not v:
        return ""
    return v.get("dynamic" if is_moving else "static", "")


def _detail_of(ev: dict[str, Any], is_moving: bool) -> str:
    d = ev.get("detail")
    if d is None:
        return ""
    if isinstance(d, str):
        return d
    return d.get("dynamic" if is_moving else "static", "")


def _resolve_base(state: dict[str, Any] | None, contributors: list[dict[str, Any]]) -> str:
    # Later contributors win; an override is "present" when the key exists
    # (even as "" — that suppresses the layer). Mirrors `v !== undefined`.
    for ev in reversed(contributors):
        if "base" in ev and ev["base"] is not None:
            return ev["base"]
    return (state or {}).get("base", "")


def _resolve_branched(
    layer: str, state: dict[str, Any] | None, contributors: list[dict[str, Any]], is_moving: bool
) -> str:
    for ev in reversed(contributors):
        if layer in ev and ev[layer] is not None:
            return _shot_of(ev[layer], is_moving)
    return _shot_of((state or {}).get(layer), is_moving)


def compose_for_render(
    scene: dict[str, Any],
    current_state: str,
    is_moving: bool,
    held_overlay_slots: list[int],
    transition_slot: int | None,
) -> str:
    """Replay composeForRender() from lingbot-world-prompts.ts.

    transition_slot takes precedence over held_overlay_slots: at most one
    transition is in flight at a time, and while it is, other event prose is
    suppressed. The composed prompt during a held transition resolves layers
    against the *from*-state (the cursor only commits to `to` on release), with
    the transition event's own overrides applied on top.
    """
    states = scene.get("states", {})
    events = scene.get("events", [])
    state = states.get(current_state)

    contributors: list[dict[str, Any]] = []
    if transition_slot is not None:
        if 0 <= transition_slot < len(events):
            contributors = [events[transition_slot]]
    else:
        for slot in held_overlay_slots:
            if 0 <= slot < len(events):
                ev = events[slot]
                if ev.get("kind") == "overlay" and current_state in ev.get("from", []):
                    contributors.append(ev)

    if state is None and not contributors:
        return ""

    parts = [
        _resolve_base(state, contributors),
        _resolve_branched("camera", state, contributors, is_moving),
        _resolve_branched("movement", state, contributors, is_moving),
    ]
    for ev in contributors:
        parts.append(_detail_of(ev, is_moving))
    return " ".join(p.strip() for p in parts if p and p.strip())


# ---------- Event introspection ----------

def event_overrides(ev: dict[str, Any]) -> list[str]:
    return [layer for layer in ("base", "camera", "movement") if layer in ev]


def event_shape(ev: dict[str, Any]) -> str:
    return "action" if isinstance(ev.get("detail"), dict) else "environmental"


def event_signal_tokens(ev: dict[str, Any], is_moving: bool) -> int:
    """R8: the event's own authored prose in the composition — its overridden
    layers (their content, not suppressions) plus its detail. Inherited state
    layers are NOT event signal."""
    total = 0
    if "base" in ev and ev["base"]:
        total += count_tokens(ev["base"])
    for layer in ("camera", "movement"):
        if layer in ev and ev[layer]:
            txt = _shot_of(ev[layer], is_moving)
            if txt:
                total += count_tokens(txt)
    d = _detail_of(ev, is_moving)
    if d:
        total += count_tokens(d)
    return total


# ---------- Report rows ----------

@dataclass
class FragmentCount:
    label: str
    tokens: int


@dataclass
class CompositionRow:
    label: str
    tokens: int
    context: str
    is_requested: bool = False


@dataclass
class ShareRow:
    event_label: str
    signal_tokens: int
    composed_tokens: int

    @property
    def share(self) -> float:
        return 0.0 if self.composed_tokens == 0 else self.signal_tokens / self.composed_tokens


def per_layer_fragments(scene: dict[str, Any]) -> list[FragmentCount]:
    out: list[FragmentCount] = []
    for skey, st in scene.get("states", {}).items():
        out.append(FragmentCount(f"state[{skey}].base", count_tokens(st["base"]) if st.get("base") else 0))
        for layer in ("camera", "movement"):
            shot = st.get(layer, {}) or {}
            for branch in ("static", "dynamic"):
                txt = shot.get(branch, "")
                out.append(FragmentCount(f"state[{skey}].{layer}.{branch}", count_tokens(txt) if txt else 0))
    for i, ev in enumerate(scene.get("events", [])):
        ov = ",".join(event_overrides(ev)) or "detail-only"
        tag = f"event[{i}] {ev['name']!r} [{ev.get('kind')}; overrides: {ov}]"
        if event_shape(ev) == "environmental":
            d = ev.get("detail") or ""
            out.append(FragmentCount(f"{tag} detail", count_tokens(d) if d else 0))
        else:
            for branch in ("static", "dynamic"):
                d = (ev.get("detail") or {}).get(branch, "")
                out.append(FragmentCount(f"{tag} detail.{branch}", count_tokens(d) if d else 0))
    return out


def compositions(scene: dict[str, Any], held_combo: list[int] | None, combo_state: str | None) -> list[CompositionRow]:
    """Sweep every composition the runtime can produce (self-check R7):
      - each state at rest and in motion (no event)
      - each event held over each state in its `from`, both isMoving branches
    Plus, when requested, one explicit overlay combination in a given state.
    """
    rows: list[CompositionRow] = []
    states = scene.get("states", {})
    events = scene.get("events", [])

    for skey in states:
        rows.append(CompositionRow(
            f"state[{skey}] at-rest", count_tokens(compose_for_render(scene, skey, False, [], None)),
            f"state={skey}, isMoving=false",
        ))
        rows.append(CompositionRow(
            f"state[{skey}] in-motion", count_tokens(compose_for_render(scene, skey, True, [], None)),
            f"state={skey}, isMoving=true",
        ))

    for i, ev in enumerate(events):
        kind = ev.get("kind")
        for skey in ev.get("from", []):
            for is_moving in (False, True):
                state_label = "in-motion" if is_moving else "at-rest"
                if kind == "transition":
                    toks = count_tokens(compose_for_render(scene, skey, is_moving, [], i))
                    ctx = f"state={skey}->{ev.get('to')}, transition held, isMoving={str(is_moving).lower()}"
                else:
                    toks = count_tokens(compose_for_render(scene, skey, is_moving, [i], None))
                    ctx = f"state={skey}, overlay held, isMoving={str(is_moving).lower()}"
                rows.append(CompositionRow(
                    f"event[{i}] {ev['name']!r} over [{skey}] {state_label}", toks, ctx,
                ))

    if held_combo:
        skey = combo_state or next(iter(states), "")
        names = " + ".join(f"event[{i}] {events[i]['name']!r}" for i in held_combo if 0 <= i < len(events))
        for is_moving in (False, True):
            rows.append(CompositionRow(
                f"requested combo over [{skey}] ({'in-motion' if is_moving else 'at-rest'}): {names}",
                count_tokens(compose_for_render(scene, skey, is_moving, held_combo, None)),
                f"state={skey}, heldOverlaySlots={held_combo}, isMoving={str(is_moving).lower()}",
                is_requested=True,
            ))
    return rows


def event_shares(scene: dict[str, Any]) -> list[ShareRow]:
    """Each event's signal-share of its composed-while-held prompt, per from-state
    and isMoving branch. Interpretation (drowning/healthy bands) lives in
    references/token-budget.md, not here."""
    rows: list[ShareRow] = []
    events = scene.get("events", [])
    for i, ev in enumerate(events):
        kind = ev.get("kind")
        for skey in ev.get("from", []):
            for is_moving in (False, True):
                if kind == "transition":
                    composed = compose_for_render(scene, skey, is_moving, [], i)
                else:
                    composed = compose_for_render(scene, skey, is_moving, [i], None)
                n_composed = count_tokens(composed) if composed else 0
                rows.append(ShareRow(
                    f"event[{i}] {ev['name']!r} over [{skey}] {'in-motion' if is_moving else 'at-rest'}",
                    event_signal_tokens(ev, is_moving), n_composed,
                ))
    return rows


# ---------- Structural validation (ports validateStructuredScene + self-check R1) ----------

def warnings(scene: dict[str, Any], comps: list[CompositionRow], entrance_state: str | None) -> list[str]:
    warns: list[str] = []
    states = scene.get("states", {})
    events = scene.get("events", [])
    state_keys = set(states)

    # Budget: every swept composition must fit the encoder cap.
    for c in comps:
        if c.tokens > CAP:
            kind = "REQUESTED COMBINATION OVERRUNS" if c.is_requested else "BASELINE VIOLATION"
            warns.append(
                f"{kind}: {c.label!r} = {c.tokens} tok EXCEEDS the {CAP}-tok encoder cap — "
                f"the tail is silently truncated. Trim per references/token-budget.md before shipping."
            )

    # Structure.
    if not isinstance(states, dict) or not states:
        warns.append("scene.states must be a non-empty object")
    for skey, st in states.items():
        if not isinstance(st.get("base"), str):
            warns.append(f"state[{skey}].base must be a string")
        for layer in ("camera", "movement"):
            shot = st.get(layer)
            if not isinstance(shot, dict) or "static" not in shot or "dynamic" not in shot:
                warns.append(f"state[{skey}].{layer} must be an object with 'static' and 'dynamic' strings")

    for i, ev in enumerate(events):
        if not isinstance(ev.get("name"), str):
            warns.append(f"event[{i}].name must be a string")
        if ev.get("kind") not in ("overlay", "transition"):
            warns.append(f"event[{i}] {ev.get('name')!r} kind must be 'overlay' or 'transition'")
        frm = ev.get("from")
        if not isinstance(frm, list) or not frm:
            warns.append(f"event[{i}] {ev.get('name')!r} from must be a non-empty array of state keys")
        else:
            for k in frm:
                if k not in state_keys:
                    warns.append(f"event[{i}] {ev.get('name')!r} from references unknown state {k!r}")
        if ev.get("kind") == "transition":
            to = ev.get("to")
            if not isinstance(to, str):
                warns.append(f"event[{i}] {ev.get('name')!r} transition requires a 'to' state key")
            elif to not in state_keys:
                warns.append(f"event[{i}] {ev.get('name')!r} to references unknown state {to!r}")
        elif "to" in ev:
            warns.append(f"event[{i}] {ev.get('name')!r} is an overlay; 'to' is not allowed")
        if isinstance(ev.get("detail"), dict):
            missing = [k for k in ("static", "dynamic") if k not in ev["detail"]]
            if missing:
                warns.append(f"event[{i}] {ev.get('name')!r} action detail missing {missing}")

    # Self-check R1: no dead-end states (only meaningful with >1 state).
    if len(states) > 1:
        has_out = {sk: False for sk in states}
        for ev in events:
            if ev.get("kind") == "transition":
                for k in ev.get("from", []):
                    if k in has_out:
                        has_out[k] = True
        for sk, ok in has_out.items():
            if not ok:
                warns.append(
                    f"R1 dead-end state: [{sk}] has no outgoing transition — a state you can enter but never leave. "
                    f"Add an outgoing transition or remove the state."
                )

    # Entrance.
    if entrance_state is not None and entrance_state not in state_keys:
        warns.append(f"entrance.state {entrance_state!r} is not a key in scene.states")

    return warns


# ---------- Rendering ----------

def _bar(tokens: int) -> str:
    pct = round(100 * tokens / CAP)
    flag = "  EXCEEDS" if tokens > CAP else (" tight" if tokens > 480 else "")
    return f"{pct:3d}% of cap{flag}"


def render_text(scene_obj: dict[str, Any], path: str | None, held_combo, combo_state) -> str:
    scene = scene_obj["scene"]
    entrance_state = scene_obj.get("entrance", {}).get("state")
    lines: list[str] = []
    header = scene_obj.get("name") or scene_obj.get("id") or "<unnamed scene>"
    lines.append(f"=== {header} ==={f'  (from {path})' if path else ''}")
    lines.append(f"states: {list(scene.get('states', {}))}   entrance: {entrance_state}")
    lines.append("")

    lines.append("per-layer tokens:")
    for f in per_layer_fragments(scene):
        lines.append(f"  {f.label:54s}  {f.tokens:4d} tok")
    lines.append("")

    comps = compositions(scene, held_combo, combo_state)
    lines.append("compositions (baseline = every single-event composition fits 512 tok; 480 soft target):")
    for c in comps:
        mark = "  <-requested" if c.is_requested else ""
        lines.append(f"  {c.label:62s}  {c.tokens:4d} tok  {_bar(c.tokens)}{mark}")
    lines.append("")

    shares = event_shares(scene)
    if shares:
        lines.append("event signal shares (event-authored tokens / composed-while-held tokens):")
        for sr in shares:
            lines.append(f"  {sr.event_label:62s}  {sr.signal_tokens:4d}/{sr.composed_tokens:<4d} = {sr.share*100:3.0f}%")
        lines.append("")

    if not held_combo:
        lines.append("note: multi-event combinations are NOT auto-checked. Use --held SLOT,SLOT [--state KEY] to verify one.")
        lines.append("")

    warns = warnings(scene, comps, entrance_state)
    if warns:
        lines.append("warnings:")
        for w in warns:
            lines.append(f"  - {w}")
    else:
        lines.append("warnings: none")
    return "\n".join(lines)


def render_json(scene_obj: dict[str, Any], held_combo, combo_state) -> str:
    scene = scene_obj["scene"]
    entrance_state = scene_obj.get("entrance", {}).get("state")
    comps = compositions(scene, held_combo, combo_state)
    payload = {
        "id": scene_obj.get("id"),
        "name": scene_obj.get("name"),
        "cap": CAP,
        "states": list(scene.get("states", {})),
        "entrance_state": entrance_state,
        "per_layer": [{"label": f.label, "tokens": f.tokens} for f in per_layer_fragments(scene)],
        "compositions": [
            {"label": c.label, "tokens": c.tokens, "context": c.context,
             "is_requested": c.is_requested, "pct_of_cap": round(100 * c.tokens / CAP, 1)}
            for c in comps
        ],
        "event_shares": [
            {"event": sr.event_label, "signal_tokens": sr.signal_tokens,
             "composed_tokens": sr.composed_tokens, "share": round(sr.share, 4)}
            for sr in event_shares(scene)
        ],
        "warnings": warnings(scene, comps, entrance_state),
    }
    return json.dumps(payload, indent=2)


# ---------- CLI ----------

def _parse_held(s: str | None) -> list[int] | None:
    if s is None:
        return None
    try:
        return [int(x) for x in s.split(",") if x.strip()]
    except ValueError as e:
        raise SystemExit(f"error: --held expects comma-separated event slot indices (e.g. --held 0,2); got {s!r}: {e}")


def main() -> int:
    ap = argparse.ArgumentParser(
        description=(
            "Report token counts, compositions, and warnings for a LingBot virtual-world JSON file (FSM schema). "
            "Baseline contract: every single-event composition must fit the 512-tok encoder. Multi-event "
            "combinations are NOT auto-checked — pass --held to verify a specific overlay combination."
        ),
    )
    ap.add_argument("path", help="Path to the JSON file, or '-' to read from stdin.")
    ap.add_argument("--json", action="store_true", help="Emit machine-readable JSON instead of plain text.")
    ap.add_argument("--held", default=None, help="Comma-separated overlay slot indices for an explicit combination check (e.g. --held 0,3).")
    ap.add_argument("--state", default=None, help="State key for the --held combination check (default: entrance, else first state).")
    args = ap.parse_args()
    held_combo = _parse_held(args.held)

    scene_obj = load_scene(args.path)
    if "scene" not in scene_obj:
        if "states" in scene_obj and "events" in scene_obj:
            scene_obj = {"scene": scene_obj}
        else:
            print(
                f"error: input is neither a StructuredExample (missing 'scene') nor a bare StructuredScene "
                f"(missing 'states'/'events'); top-level keys = {list(scene_obj.keys())}",
                file=sys.stderr,
            )
            return 2

    combo_state = args.state or scene_obj.get("entrance", {}).get("state")
    src = None if args.path == "-" else args.path
    if args.json:
        print(render_json(scene_obj, held_combo, combo_state))
    else:
        print(render_text(scene_obj, src, held_combo, combo_state))

    comps = compositions(scene_obj["scene"], held_combo, combo_state)
    return 1 if any(c.tokens > CAP for c in comps) else 0


if __name__ == "__main__":
    raise SystemExit(main())
