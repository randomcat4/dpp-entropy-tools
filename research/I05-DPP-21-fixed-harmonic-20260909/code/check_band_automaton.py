#!/usr/bin/env python3
"""Exact small-size cross-check of the width-two determinant automaton.

This is independent of the Mobius check inside the main certificate in the
following sense: it compares the automaton's complete multiset of event
numerators with direct Bareiss determinants of every signed event matrix.
No entropy, logarithm, or floating-point operation is used.
"""

from __future__ import annotations

import importlib.util
import json
from collections import Counter
from pathlib import Path


def load_certificate_module():
    source = Path(__file__).with_name("certify_midpoint_rate_gap.py")
    spec = importlib.util.spec_from_file_location("dpp21_midpoint_certificate", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load certificate module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def direct_counts(module, n: int, nearest: int) -> Counter[int]:
    counts: Counter[int] = Counter()
    for mask in range(1 << n):
        bits = tuple((mask >> i) & 1 for i in range(n))
        numerator = module.signed_event_numerator_direct(bits, nearest)
        if numerator <= 0:
            raise AssertionError(
                f"nonpositive direct numerator: n={n}, nearest={nearest}, mask={mask}"
            )
        counts[numerator] += 1
    return counts


def main() -> None:
    module = load_certificate_module()
    checked = []
    for nearest in (1, 2, 3):
        for n in range(1, 9):
            automaton = module.determinant_counts(n, nearest)
            direct = direct_counts(module, n, nearest)
            if automaton != direct:
                raise AssertionError(
                    f"automaton/direct multiset mismatch for n={n}, nearest={nearest}"
                )
            checked.append(
                {
                    "nearest_scaled_entry": nearest,
                    "t": {1: "1/2", 2: "1", 3: "3/2"}[nearest],
                    "n": n,
                    "events": 1 << n,
                    "distinct_numerators": len(automaton),
                    "normalization_numerator": str(
                        sum(value * multiplicity for value, multiplicity in automaton.items())
                    ),
                    "normalization_denominator": str(32**n),
                }
            )

    report = {
        "status": "PASS",
        "scope": "exact determinant-automaton cross-check only",
        "maximum_length": 8,
        "parameters": ["1/2", "1", "3/2"],
        "checked_cases": checked,
    }
    target = Path(__file__).resolve().parents[1] / "output" / "band_automaton_exact.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
