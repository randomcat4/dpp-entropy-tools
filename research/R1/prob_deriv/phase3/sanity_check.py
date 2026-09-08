"""Exact-rational bookkeeping checks for the block-composition theorem."""

from fractions import Fraction as F
import json
import math
from pathlib import Path


def det(a):
    if not a:
        return F(1)
    m = [row[:] for row in a]
    out = F(1)
    for j in range(len(m)):
        pivot = next((i for i in range(j, len(m)) if m[i][j]), None)
        if pivot is None:
            return F(0)
        if pivot != j:
            m[j], m[pivot] = m[pivot], m[j]
            out = -out
        value = m[j][j]
        out *= value
        for i in range(j + 1, len(m)):
            scale = m[i][j] / value
            for k in range(j, len(m)):
                m[i][k] -= scale * m[j][k]
    return out


def submatrix(k, indices):
    return [[k[i][j] for j in indices] for i in indices]


def indices(mask, n):
    return [i for i in range(n) if mask >> i & 1]


def event_probs(k):
    n = len(k)
    minors = [det(submatrix(k, indices(mask, n))) for mask in range(1 << n)]
    full = (1 << n) - 1
    probs = []
    for event in range(1 << n):
        complement = full ^ event
        subset = complement
        total = F(0)
        while True:
            total += (-1 if subset.bit_count() & 1 else 1) * minors[event | subset]
            if subset == 0:
                break
            subset = (subset - 1) & complement
        probs.append(total)
    return probs


def add(k, v, sign):
    return [[k[i][j] + sign * v[i][j] for j in range(len(k))] for i in range(len(k))]


def strict_contraction(k):
    n = len(k)
    eye_minus = [[(F(1) if i == j else F(0)) - k[i][j] for j in range(n)] for i in range(n)]
    return all(det(submatrix(m, range(size))) > 0 for m in (k, eye_minus) for size in range(1, n + 1))


def entropy(probs):
    assert all(p > 0 for p in probs)
    return -sum(float(p) * math.log(float(p)) for p in probs)


def project(mask, block):
    return sum(((mask >> original) & 1) << pos for pos, original in enumerate(block))


def marginal(probs, n, block):
    out = [F(0) for _ in range(1 << len(block))]
    for mask in range(1 << n):
        out[project(mask, block)] += probs[mask]
    return out


def check(name, k0, v, blocks):
    n = len(k0)
    km, kp = add(k0, v, -1), add(k0, v, 1)
    assert all(strict_contraction(k) for k in (k0, km, kp))
    p0, pm, pp = map(event_probs, (k0, km, kp))
    assert all(sum(p) == 1 and min(p) > 0 for p in (p0, pm, pp))
    block_p0 = [event_probs(submatrix(k0, block)) for block in blocks]
    factorizes = all(
        p0[mask] == math.prod(bp[project(mask, block)] for bp, block in zip(block_p0, blocks))
        for mask in range(1 << n)
    )
    marginals_match = all(
        marginal(probs, n, block) == event_probs(submatrix(kernel, block))
        for probs, kernel in ((pm, km), (pp, kp))
        for block in blocks
    )
    block_gaps = []
    for block in blocks:
        q0 = event_probs(submatrix(k0, block))
        qm = event_probs(submatrix(km, block))
        qp = event_probs(submatrix(kp, block))
        block_gaps.append((entropy(qm) + entropy(qp)) / 2 - entropy(q0))
    gap = (entropy(pm) + entropy(pp)) / 2 - entropy(p0)
    owners = {i: owner for owner, block in enumerate(blocks) for i in block}
    cross = [(i, j, v[i][j]) for i in range(n) for j in range(i + 1, n) if owners[i] != owners[j] and v[i][j]]
    return {
        "name": name,
        "strict_feasibility_exact": True,
        "probability_sums": [str(sum(p)) for p in (p0, pm, pp)],
        "minimum_probabilities": [str(min(p)) for p in (p0, pm, pp)],
        "center_factorizes_exact": factorizes,
        "block_marginals_match_exact": marginals_match,
        "cross_entries": [[i, j, str(x)] for i, j, x in cross],
        "first_cross_pair_gap": str(-cross[0][2] ** 2) if cross else None,
        "delta": gap,
        "sum_block_deltas": sum(block_gaps),
        "sum_block_minus_global": sum(block_gaps) - gap,
    }


def main():
    k4 = [
        [F(2, 5), F(1, 30), F(0), F(0)],
        [F(1, 30), F(1, 3), F(0), F(0)],
        [F(0), F(0), F(1, 4), F(1, 40)],
        [F(0), F(0), F(1, 40), F(3, 5)],
    ]
    v4_cross = [
        [F(1, 80), F(1, 50), F(1, 100), F(0)],
        [F(1, 50), F(-1, 70), F(0), F(-1, 110)],
        [F(1, 100), F(0), F(1, 90), F(-1, 60)],
        [F(0), F(-1, 110), F(-1, 60), F(-1, 100)],
    ]
    v4_block = [[v4_cross[i][j] if (i < 2) == (j < 2) else F(0) for j in range(4)] for i in range(4)]
    k5 = [
        [F(1, 3), F(1, 25), F(0), F(0), F(0)],
        [F(1, 25), F(2, 5), F(0), F(0), F(0)],
        [F(0), F(0), F(1, 2), F(0), F(0)],
        [F(0), F(0), F(0), F(1, 4), F(1, 35)],
        [F(0), F(0), F(0), F(1, 35), F(3, 5)],
    ]
    v5 = [
        [F(1, 90), F(-1, 70), F(1, 120), F(0), F(1, 140)],
        [F(-1, 70), F(-1, 100), F(0), F(-1, 130), F(0)],
        [F(1, 120), F(0), F(1, 80), F(1, 150), F(0)],
        [F(0), F(-1, 130), F(1, 150), F(-1, 110), F(1, 90)],
        [F(1, 140), F(0), F(0), F(1, 90), F(1, 100)],
    ]
    data = {
        "description": "Exact-rational full-event checks for P3-02 block composition",
        "cases": [
            check("n4_cross_2plus2", k4, v4_cross, [[0, 1], [2, 3]]),
            check("n4_no_cross_equality_2plus2", k4, v4_block, [[0, 1], [2, 3]]),
            check("n5_cross_2plus1plus2", k5, v5, [[0, 1], [2], [3, 4]]),
        ],
    }
    path = Path(__file__).with_name("sanity_checks.json")
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(data))


if __name__ == "__main__":
    main()
