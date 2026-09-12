#!/usr/bin/env python3
"""Small deterministic diagnostics used by REPORT.md."""
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

import numpy as np


def linear_diagnostic(x, y):
    x = np.asarray(x, dtype=float); y = np.asarray(y, dtype=float)
    slope, intercept = np.polyfit(x, y, 1)
    pred = intercept + slope * x
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    return float(slope), float(intercept), 1 - ss_res / ss_tot if ss_tot else 1.0


def main():
    p = argparse.ArgumentParser(); p.add_argument("--output-dir", type=Path, required=True); args = p.parse_args()
    rows = list(csv.DictReader((args.output_dir / "curvature_vs_transition.csv").open()))
    groups = defaultdict(list)
    for r in rows:
        if float(r["delta"]) == 0.05 and int(r["n"]) >= 8:
            groups[(r["family"], float(r["epsilon"]))].append(r)
    diagnostics = []
    for (family, eps), q in sorted(groups.items()):
        correction = [float(r["coherence_increment"]) for r in q]
        n = [int(r["n"]) for r in q]
        count = [int(r["transition_count"]) for r in q]
        sn, bn, rn = linear_diagnostic(n, correction)
        if len(set(count)) > 1:
            sc, bc, rc = linear_diagnostic(count, correction)
        else:
            sc = bc = rc = float("nan")
        diagnostics.append({
            "family": family, "epsilon": eps, "delta": 0.05,
            "points_n8_to_n22": len(q),
            "correction_vs_n_slope": sn, "correction_vs_n_r_squared": rn,
            "correction_vs_transition_slope": sc, "correction_vs_transition_r_squared": rc,
            "warning": "deterministic collinear finite-window diagnostic; neither R^2 is causal or a confidence statement",
        })
    with (args.output_dir / "correction_fit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(diagnostics[0])); writer.writeheader(); writer.writerows(diagnostics)
    summary = {"correction_diagnostics": diagnostics}
    (args.output_dir / "summary_diagnostics.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__": main()
