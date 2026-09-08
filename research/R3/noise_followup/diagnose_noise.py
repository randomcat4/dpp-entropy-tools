"""High-precision audit of a float64 midpoint-gap record.

The entropy is recomputed from the group-count L-ensemble formula with mpmath.
This script is diagnostic: it does not certify a global concavity statement.
"""
import argparse
import csv
import itertools
import json
import math
from pathlib import Path

import mpmath as mp
import numpy as np


def read_row(path, index):
    with Path(path).open(newline="") as handle:
        for row in csv.DictReader(handle):
            if int(row["index"]) == index:
                return row
    raise KeyError(f"ledger index {index} not found in {path}")


def unpack(values, groups):
    a = list(values[:groups])
    C = mp.matrix(groups)
    offset = groups
    for i in range(groups):
        for j in range(i, groups):
            C[i, j] = values[offset]
            C[j, i] = values[offset]
            offset += 1
    return a, C


def entropy_count_formula(sizes, values, dps):
    """Return entropy and normalization using exact integer multiplicities."""
    with mp.workdps(dps):
        groups = len(sizes)
        a, C = unpack([mp.mpf(str(v)) for v in values], groups)
        eye = mp.eye(groups)
        ell = [value / (1 - value) for value in a]
        T = (eye - C) ** -1 - eye
        for i in range(groups):
            T[i, i] -= ell[i]
        det_i_minus_c = mp.det(eye - C)
        if det_i_minus_c <= 0:
            raise ArithmeticError("det(I-C) is not positive")
        log_pre = mp.log(det_i_minus_c)
        for m, value in zip(sizes, a):
            log_pre += (m - 1) * mp.log1p(-value)

        total = mp.mpf("0")
        entropy = mp.mpf("0")
        min_probability = mp.inf
        max_probability = mp.mpf("0")
        for counts in itertools.product(*[range(m + 1) for m in sizes]):
            W = mp.diag([mp.sqrt(mp.mpf(c) / (m * e)) for c, m, e in zip(counts, sizes, ell)])
            det_z = mp.det(eye + W * T * W)
            if det_z <= 0:
                raise ArithmeticError(f"nonpositive count determinant at {counts}: {det_z}")
            log_probability = log_pre + mp.log(det_z)
            for count, e in zip(counts, ell):
                log_probability += count * mp.log(e)
            probability = mp.exp(log_probability)
            multiplicity = math.prod(math.comb(m, c) for m, c in zip(sizes, counts))
            weight = multiplicity * probability
            total += weight
            entropy -= weight * log_probability
            min_probability = min(min_probability, probability)
            max_probability = max(max_probability, probability)
        return entropy, total, min_probability, max_probability


def mp_text(value, digits=70):
    return mp.nstr(value, digits, strip_zeros=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--index", type=int, default=783)
    parser.add_argument("--out", required=True)
    parser.add_argument("--dps", type=int, default=140)
    args = parser.parse_args()

    row = read_row(args.ledger, args.index)
    sizes = json.loads(row["sizes"])
    x_text = json.loads(row["parameters"])
    direction_text = json.loads(row["direction"])
    step_text = row["step"]
    x_float = np.asarray(x_text, dtype=float)
    direction_float = np.asarray(direction_text, dtype=float)
    step_float = float(step_text)

    convergence = []
    for dps in (50, 80, 110, args.dps):
        with mp.workdps(dps):
            x = [mp.mpf(str(v)) for v in x_text]
            direction = [mp.mpf(str(v)) for v in direction_text]
            step = mp.mpf(step_text)
            hm, nm, _, _ = entropy_count_formula(
                sizes, [v - step * d for v, d in zip(x, direction)], dps
            )
            h0, n0, pmin, pmax = entropy_count_formula(sizes, x, dps)
            hp, np_, _, _ = entropy_count_formula(
                sizes, [v + step * d for v, d in zip(x, direction)], dps
            )
            gap = (hm + hp) / 2 - h0
            convergence.append(
                {
                    "dps": dps,
                    "H_minus": mp_text(hm),
                    "H_mid": mp_text(h0),
                    "H_plus": mp_text(hp),
                    "gap": mp_text(gap),
                    "centered_curvature": mp_text(2 * gap / step**2),
                    "normalization_errors": [
                        mp_text(nm - 1),
                        mp_text(n0 - 1),
                        mp_text(np_ - 1),
                    ],
                    "center_min_event_probability": mp_text(pmin),
                    "center_max_event_probability": mp_text(pmax),
                }
            )

    scales = [mp.mpf(2) ** power for power in range(-8, 3)]
    scale_scan = []
    with mp.workdps(args.dps):
        x = [mp.mpf(str(v)) for v in x_text]
        direction = [mp.mpf(str(v)) for v in direction_text]
        base_step = mp.mpf(step_text)
        h0, _, _, _ = entropy_count_formula(sizes, x, args.dps)
        for scale in scales:
            step = base_step * scale
            xm = [v - step * d for v, d in zip(x, direction)]
            xp = [v + step * d for v, d in zip(x, direction)]
            hm, _, _, _ = entropy_count_formula(sizes, xm, args.dps)
            hp, _, _, _ = entropy_count_formula(sizes, xp, args.dps)
            gap = (hm + hp) / 2 - h0
            scale_scan.append(
                {
                    "scale": mp_text(scale, 20),
                    "step": mp_text(step),
                    "gap": mp_text(gap),
                    "centered_curvature": mp_text(2 * gap / step**2),
                }
            )

    # Repeat the literal float64 subtraction to expose its quantization scale.
    sys_path = Path(__file__).resolve().parents[1] / "structure"
    import sys

    sys.path.insert(0, str(sys_path))
    from structure_search import Family

    family = Family(sizes)
    h_minus_float = family.evaluate(x_float - step_float * direction_float)[0]
    h_mid_float = family.evaluate(x_float)[0]
    h_plus_float = family.evaluate(x_float + step_float * direction_float)[0]
    gap_float = (h_minus_float + h_plus_float) / 2 - h_mid_float
    ulp = float(np.spacing(h_mid_float))

    result = {
        "source_ledger": str(Path(args.ledger).resolve()),
        "index": args.index,
        "sizes": sizes,
        "parameters_as_recorded": x_text,
        "direction_as_recorded": direction_text,
        "step_as_recorded": step_text,
        "float64": {
            "H_minus": h_minus_float,
            "H_mid": h_mid_float,
            "H_plus": h_plus_float,
            "gap": gap_float,
            "ulp_at_H_mid": ulp,
            "gap_in_ulps": gap_float / ulp,
        },
        "high_precision_convergence": convergence,
        "high_precision_scale_scan": scale_scan,
        "interpretation_guardrail": (
            "A stable negative high-precision gap explains this float64 sign flip, "
            "but does not prove global concavity."
        ),
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result["float64"], indent=2), flush=True)
    print(json.dumps(convergence[-1], indent=2), flush=True)
    print(f"wrote {out}", flush=True)


if __name__ == "__main__":
    main()
