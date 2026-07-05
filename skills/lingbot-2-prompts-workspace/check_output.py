#!/usr/bin/env python3
"""Programmatic checks for lingbot-2-prompts eval outputs.

Usage: python3 check_output.py <outputs_dir>
Prints one line per check: PASS/FAIL <check-name> -- evidence
"""
import json
import re
import sys
from pathlib import Path

JUMP = "The character jumps high into the air."
SLOTS = ["f", "g", "u", "o", "space"]


def main(outdir: Path):
    results = []

    def check(name, passed, evidence):
        results.append((name, passed, evidence))

    # find actions.json (allow nested)
    candidates = list(outdir.rglob("actions.json"))
    prompt_files = list(outdir.rglob("prompt.txt"))
    check("prompt_txt_exists", bool(prompt_files),
          str(prompt_files[0].relative_to(outdir)) if prompt_files else "no prompt.txt found")
    check("actions_json_exists", bool(candidates),
          str(candidates[0].relative_to(outdir)) if candidates else "no actions.json found")

    actions = None
    if candidates:
        try:
            data = json.loads(candidates[0].read_text())
            actions = data.get("actions") if isinstance(data, dict) else None
            check("actions_json_valid", isinstance(actions, list) and len(actions) > 0,
                  f"{len(actions) if isinstance(actions, list) else 0} actions")
        except Exception as e:
            check("actions_json_valid", False, f"parse error: {e}")

    if actions:
        slots_present = {a.get("slot") for a in actions}
        check("all_slots_covered", set(SLOTS) <= slots_present,
              f"present: {sorted(slots_present)}")

        base = prompt_files and prompt_files[0].read_text().strip()
        if base:
            bad = [a.get("id") for a in actions
                   if a.get("prompt_en", "").strip() != f"{base} {a.get('addendum_en','').strip()}"]
            check("prompt_en_is_base_plus_addendum", not bad,
                  "all composed correctly" if not bad else f"mismatched: {bad}")

        space = [a for a in actions if a.get("slot") == "space"]
        ok = space and space[0].get("addendum_en", "").strip() == JUMP \
            and space[0].get("label_en", "").strip().lower().endswith("jump")
        check("space_is_fixed_jump", bool(ok),
              space[0].get("addendum_en", "missing")[:60] if space else "no space action")

        required = {"id", "slot", "cand_index", "label_en", "addendum_en", "prompt_en"}
        missing = [a.get("id", "?") for a in actions if not required <= set(a)]
        check("schema_fields_present", not missing,
              "all fields present" if not missing else f"missing fields in: {missing}")

        long_addenda = []
        for a in actions:
            if a.get("slot") == "space":
                continue
            sents = len(re.findall(r"[.!?](?:\s|$)", a.get("addendum_en", "")))
            if sents > 3:
                long_addenda.append(f"{a.get('id')}({sents} sentences)")
        check("addenda_max_3_sentences", not long_addenda,
              "ok" if not long_addenda else ", ".join(long_addenda))

    if prompt_files:
        base = prompt_files[0].read_text().strip().lower()
        has_contract = ("only while held" in base
                        or "in response to keyboard" in base
                        or "wasd" in base)
        check("base_has_motion_contract", has_contract,
              "found input clause" if has_contract else "no WASD/arrow-key/only-while-held clause")

    for name, passed, evidence in results:
        print(f"{'PASS' if passed else 'FAIL'} {name} -- {evidence}")
    print(f"\n{sum(p for _, p, _ in results)}/{len(results)} passed")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
