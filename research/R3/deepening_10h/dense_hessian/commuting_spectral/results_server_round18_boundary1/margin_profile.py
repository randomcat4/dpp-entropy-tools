"""Deterministic spectrum-margin profile for the round-18 frozen ledgers."""

from __future__ import annotations

import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def compact(row: dict[str, str]) -> dict[str, object]:
    return {
        "shard": int(row["_shard"]),
        "index": int(row["index"]),
        "rho_psd": float(row["rho_psd"]),
        "spectrum_margin": float(row["spectrum_margin"]),
        "chord_gap": float(row["chord_gap"]),
        "status": row["status"],
    }


def main() -> None:
    rows: list[dict[str, str]] = []
    for shard in range(4):
        path = HERE / f"results_{shard}" / "candidate_ledger.csv"
        with path.open(encoding="utf-8", newline="") as handle:
            shard_rows = list(csv.DictReader(handle))
        for row in shard_rows:
            row["_shard"] = str(shard)
        rows.extend(row for row in shard_rows if int(row["index"]) >= 0)

    thresholds = [0.002, 0.005, 0.01, 0.015, 0.02, 0.03, 0.05]
    threshold_profile: list[dict[str, object]] = []
    for threshold in thresholds:
        eligible = [
            row for row in rows if float(row["spectrum_margin"]) >= threshold
        ]
        threshold_profile.append(
            {
                "minimum_margin": threshold,
                "eligible_rows": len(eligible),
                "best": compact(max(eligible, key=lambda r: float(r["rho_psd"])))
                if eligible
                else None,
            }
        )

    bins = [(0.002, 0.005), (0.005, 0.01), (0.01, 0.02), (0.02, 0.05)]
    bin_profile: list[dict[str, object]] = []
    for lower, upper in bins:
        eligible = [
            row
            for row in rows
            if lower <= float(row["spectrum_margin"]) < upper
        ]
        bin_profile.append(
            {
                "margin_bin": [lower, upper],
                "eligible_rows": len(eligible),
                "best": compact(max(eligible, key=lambda r: float(r["rho_psd"])))
                if eligible
                else None,
            }
        )

    overall = max(rows, key=lambda r: float(r["rho_psd"]))
    report = {
        "status": "AUTHOR_FINITE_MARGIN_DIAGNOSTIC",
        "proposal_rows": len(rows),
        "configured_margin_floor": 0.002,
        "previous_source_rho": 0.5740468373613397,
        "previous_source_margin": 0.010000000000000009,
        "overall_best": compact(overall),
        "threshold_profile": threshold_profile,
        "bin_profile": bin_profile,
        "interpretation": (
            "The best frozen proposal lies in the [0.01,0.02) margin bin, "
            "not in either lower-margin bin. This finite run does not support "
            "a monotone boundary-driven explanation; it is not a theorem."
        ),
    }
    (HERE / "margin_profile.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
