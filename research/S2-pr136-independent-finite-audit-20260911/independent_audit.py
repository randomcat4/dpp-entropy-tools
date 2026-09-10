#!/usr/bin/env python3
"""Independent exact audit of the frozen PR136 saved finite evidence.

This does not import the author checker.  It independently reconstructs input
enclosures, the KL tail polynomial, the DCT enclosure, and the continuum gate.
"""

from __future__ import annotations

from fractions import Fraction as F
from math import factorial
from pathlib import Path
import hashlib
import json
import time


ROOT = Path(__file__).parent
CERT = ROOT / "certificate"
EXPECTED_BLOBS = {
    "certificate_summary.json": "187d8f6c8609e3b568cb9f48ebf22bfeee911194",
    "certify_nodes.cpp": "0df668fa2d6375e9ea52788c586143adfda96409",
    "check_certificate.py": "0040029e4c31c524daadabb69c44e9d010c5a51c",
    "make_inputs.py": "a9037aecb464aa190246b1e11aa9e36462d89ba0",
    "node_output.part0.tsv": "44a1a7426bef6adf84ba3d4a3405dda2ef720c61",
    "node_output.part1.tsv": "937275fd4ac4fe25ff42859cfe35dee0b49a81b4",
    "node_output.part2.tsv": "e284d7acfaa04eae8f2def5e98d1babf0bbb88e4",
    "node_output.part3.tsv": "48c6cf862ba09081d2120946dae6bed81a90f3f6",
}


def git_blob(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def hx(text: str) -> F:
    return F.from_float(float.fromhex(text))


def iadd(a, b):
    return a[0] + b[0], a[1] + b[1]


def iscale(a, c):
    return (a[0] * c, a[1] * c) if c >= 0 else (a[1] * c, a[0] * c)


def imul(a, b):
    values = (a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1])
    return min(values), max(values)


def atan_interval(x: F, terms: int):
    total = F(0)
    power = x
    for k in range(terms):
        total += (-1 if k & 1 else 1) * power / (2 * k + 1)
        power *= x * x
    error = abs(power) / (2 * terms + 1)
    return total - error, total + error


def cos_point_interval(x: F, terms: int = 60):
    term = F(1)
    total = F(1)
    for k in range(1, terms):
        term *= -x * x / ((2 * k - 1) * (2 * k))
        total += term
    next_term = abs(term * x * x / ((2 * terms - 1) * (2 * terms)))
    return total - next_term, total + next_term


def poly_add(*polys):
    out = [F(0)] * max(map(len, polys))
    for poly in polys:
        for j, value in enumerate(poly):
            out[j] += value
    return out


def poly_scale(poly, value):
    return [value * item for item in poly]


def poly_mul(left, right):
    out = [F(0)] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            out[i + j] += x * y
    return out


def reconstruct_tail():
    epsilon = F(81, 1024)
    kappa = F(34, 81)
    lam = kappa * kappa
    m0, j0, h0 = F(33, 400), F(285, 2704), F(1077, 17576)
    avec = [2 * m0]
    bvec = [2 * (j0 + F(63, 160) * m0), 3 * m0 / kappa]
    cvec = [
        2 * (h0 + F(63, 80) * j0 + F(9, 8) * m0),
        2 * ((3 * j0 + 10 * m0) / kappa - F(9, 4) * m0 / kappa**2 + F(63, 80) * F(3, 2) * m0 / kappa),
        F(9, 2) * m0 / kappa**2,
    ]
    first0 = poly_scale(poly_mul(avec, avec), 1 / (2 * epsilon))
    first1 = poly_add(
        poly_scale(poly_mul(avec, bvec), 1 / epsilon),
        poly_scale(poly_mul(avec, avec), F(1, 3) / (2 * epsilon**2)),
    )
    first2 = poly_add(
        poly_scale(poly_add(poly_mul(bvec, bvec), poly_mul(avec, cvec)), 1 / epsilon),
        poly_scale(poly_mul(avec, bvec), F(2, 3) / epsilon**2),
        poly_scale(poly_mul(avec, avec), F(1, 9) / epsilon**3 + F(2, 3) / epsilon**2),
    )
    polynomial = poly_add(
        first2,
        poly_mul([F(4), F(1)], first1),
        poly_mul([F(9), F(9)], first0),
    )
    expected = [
        F(342449808326286961, 15178486401000000),
        F(154889893499, 5135349375),
        F(1809918, 180625),
    ]
    assert polynomial == expected
    a0, a1, a2 = polynomial
    r = 9
    tail = (lam**r / 2) * (
        a2 * (F(r * r, 1 - lam) + 2 * r * lam / (1 - lam) ** 2 + lam * (1 + lam) / (1 - lam) ** 3)
        + a1 * (F(r, 1 - lam) + lam / (1 - lam) ** 2)
        + a0 / (1 - lam)
    )
    return polynomial, tail


def parse_rows(data: bytes):
    rows = {}
    for raw in data.decode("utf-8").splitlines():
        if not raw or raw.startswith("#"):
            continue
        fields = raw.split()
        assert len(fields) == 11
        node = int(fields[0])
        assert node not in rows
        values = [hx(value) for value in fields[1:9]]
        assert values[0] <= values[1]
        assert values[2] <= 1 <= values[3]
        assert values[4] <= 0 <= values[5]
        assert values[6] <= 0 <= values[7]
        assert int(fields[10]) == 4**9
        rows[node] = {
            "curvature": (values[0], values[1]),
            "normalization": values[2:],
            "seconds": fields[9],
            "leaves": int(fields[10]),
        }
    assert set(rows) == set(range(128))
    return rows


def dct_gate(rows, cosines, tail):
    m_exact = sum(
        (F(4, 3) ** n * F(144, 25) * (3 * n**3 + 4 * n**2) for n in (20, 18)),
        F(0),
    ) / 2
    assert m_exact == F(318159082659774464, 9685512225)
    assert m_exact < 40_000_000
    interpolation = F(240_000_000, 3**32)
    assert interpolation == F(80_000_000, 617673396283947)
    cells = []
    for cell in range(4):
        coefficients = []
        for degree in range(32):
            accumulator = (F(0), F(0))
            for j in range(32):
                index = (degree * (2 * j + 1)) % 128
                if index > 64:
                    index = 128 - index
                accumulator = iadd(accumulator, imul(rows[32 * cell + j]["curvature"], cosines[index]))
            coefficients.append(iscale(accumulator, F(1, 32) if degree == 0 else F(1, 16)))
        polynomial_upper = coefficients[0][1] + sum(max(abs(a), abs(b)) for a, b in coefficients[1:])
        true_upper = polynomial_upper + interpolation + tail
        assert true_upper < -F(1, 3000)
        cells.append({
            "cell": [str(F(2 + cell, 4)), str(F(3 + cell, 4))],
            "polynomial_upper": str(polynomial_upper),
            "true_upper": str(true_upper),
            "true_upper_decimal": float(true_upper),
            "coefficient_count": len(coefficients),
        })
    return m_exact, interpolation, cells


def verify_inputs(inputs):
    assert inputs["N"] == 32 and inputs["r"] == 9 and inputs["rho"] == 3
    pi_a = atan_interval(F(1, 5), 140)
    pi_b = atan_interval(F(1, 239), 60)
    pi_interval = 16 * pi_a[0] - 4 * pi_b[1], 16 * pi_a[1] - 4 * pi_b[0]
    generated_cos = [tuple(hx(value) for value in pair) for pair in inputs["cos_pi_j_over_64"]]
    assert len(generated_cos) == 65
    for j, enclosure in enumerate(generated_cos):
        if j == 0:
            assert enclosure == (F(1), F(1))
            continue
        if j == 64:
            # The endpoint is the defining identity cos(pi)=-1.  Do not apply
            # monotonicity to a pi enclosure whose upper end is above pi.
            assert enclosure == (F(-1), F(-1))
            continue
        xlo = pi_interval[0] * j / 64
        xhi = pi_interval[1] * j / 64
        lo = cos_point_interval(xhi)[0]
        hi = cos_point_interval(xlo)[1]
        assert enclosure[0] <= lo <= hi <= enclosure[1]
    nodes = inputs["nodes"]
    assert len(nodes) == 128
    for node_id, node in enumerate(nodes):
        assert node["id"] == node_id and node["cell"] == node_id // 32 and node["j"] == node_id % 32
        center = F(5 + 2 * node["cell"], 8)
        cosine = generated_cos[2 * node["j"] + 1]
        tlo, thi = hx(node["t_lo"]), hx(node["t_hi"])
        assert tlo <= center + cosine[0] / 8 <= center + cosine[1] / 8 <= thi
        assert F(2 + node["cell"], 4) < tlo <= thi < F(3 + node["cell"], 4)
    x = F(1, 3)
    log2_mid = 2 * sum((x ** (2 * j + 1) / (2 * j + 1) for j in range(100)), F(0))
    log2_tail = 2 * x**201 / (201 * (1 - x * x))
    loglo, loghi = (hx(value) for value in inputs["log2_hex"])
    assert loglo < log2_mid and log2_mid + log2_tail < loghi
    assert 2 * F(1, 4) ** 33 / (33 * (1 - F(1, 16))) < F(1, 2**68)
    return generated_cos, pi_interval


def static_kernel_checks():
    source = (CERT / "certify_nodes.cpp").read_text(encoding="utf-8")
    checks = {
        "no_library_transcendentals": all(token not in source for token in ("std::log(", "std::sin(", "std::cos(")),
        "rounding_mode_checked": "std::fegetround()!=FE_TONEAREST" in source,
        "each_interval_arithmetic_padded": all(token in source for token in ("dn(a.l+b.l)", "up(a.h+b.h)", "dn(1.0/a.h)", "up(1.0/a.l)")),
        "second_taylor_product_rule": "a.v*b.h+a.d*b.d+a.h*b.v" in source,
        "inverse_second_taylor_rule": "square(a.d)*r2*r-a.h*r2" in source,
        "current_four_events": "for(int a:{-1,1})for(int b:{-1,1})" in source,
        "future_word_count_checked": "a.leaves!=262144" in source,
        "normalization_jets_checked": "normalization jets not enclosed" in source,
        "per_original_coordinate_cancellation_documented": "factor 1/2 per original coordinate cancels the factor 2" in source,
        "atanh_tail_pad_present": "I(-0x1p-68,0x1p-68)" in source,
        "thread_ceiling_four": "threads>4" in source,
    }
    assert all(checks.values())
    return checks


def main():
    started = time.perf_counter()
    blobs = {name: git_blob(CERT / name) for name in EXPECTED_BLOBS}
    assert blobs == EXPECTED_BLOBS
    inputs = json.loads((CERT / "certificate_inputs.json").read_text(encoding="utf-8"))
    cosines, pi_interval = verify_inputs(inputs)
    parts = [(CERT / f"node_output.part{i}.tsv").read_bytes() for i in range(4)]
    saved = b"".join(parts)
    assert len(saved) == 25414
    rows = parse_rows(saved)
    polynomial, tail = reconstruct_tail()
    assert tail < F(115, 1_000_000)
    m_exact, interpolation, cells = dct_gate(rows, cosines, tail)
    summary = json.loads((CERT / "certificate_summary.json").read_text(encoding="utf-8"))
    assert summary["nodes"] == 128
    assert summary["complete_future_words_per_node"] == 4**9
    assert summary["complete_current_future_atoms_per_node"] == 4**10
    assert F(summary["tail_E9_upper"]) == F(115, 1_000_000)
    assert F(summary["chebyshev_error"]) == interpolation
    for item, audited in zip(summary["cells"], cells):
        displayed = F(item["true_curvature_upper"])
        assert F(audited["true_upper"]) <= displayed < -F(1, 3000)
    record = {
        "schema": "pr136-s2-independent-saved-finite-audit-v1",
        "status": "SAVED_FINITE_EVIDENCE_PASS_FRESH_REPRODUCTION_BLOCKED",
        "frozen_head": "39098dac760cea2d27f2955bed31f80c87913810",
        "blob_binding": blobs,
        "input_verification": {
            "nodes": len(inputs["nodes"]),
            "cosine_enclosures": len(cosines),
            "pi_interval": [str(value) for value in pi_interval],
            "log2_enclosed": True,
            "chebyshev_nodes_enclosed": True,
        },
        "saved_output": {
            "part_bytes": [len(value) for value in parts],
            "concatenated_bytes": len(saved),
            "unique_ids": len(rows),
            "future_words_each": 4**9,
            "current_future_atoms_each": 4**10,
            "normalization_jets_all_enclose": True,
        },
        "tail": {
            "polynomial_coefficients_a0_a1_a2": [str(value) for value in polynomial],
            "E9": str(tail),
            "E9_decimal": float(tail),
            "E9_lt_115e_minus_6": tail < F(115, 1_000_000),
        },
        "continuum": {
            "M_exact": str(m_exact),
            "M_lt_40000000": m_exact < 40_000_000,
            "interpolation_error": str(interpolation),
            "cells": cells,
        },
        "static_kernel_checks": static_kernel_checks(),
        "fresh_reproduction": {
            "status": "BLOCKED_COMPILER_MISSING",
            "required": "g++ -O3 -std=c++17 -ffp-contract=off -fno-fast-math -fopenmp",
            "probes": ["where.exe g++", "where.exe clang++", "where.exe c++", "where.exe cl.exe"],
        },
        "elapsed_seconds": time.perf_counter() - started,
    }
    output = ROOT / "independent_saved_audit.json"
    output.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": record["status"], "output": str(output), "elapsed_seconds": record["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
