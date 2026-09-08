"""Function snapshot read before concurrent author revision.

Source file SHA256 at read/replay:
e691fb766e5a3a41357205e3656e07bed308f2a27f9b6c884df9f6f91446da9d
This preserves the audited algorithm, not the entire original source file.
"""
import numpy as np

def max_quadratic_on_simplex(M: np.ndarray):
    best_val = -float("inf")
    best_v = None
    candidates = []
    for mask in range(1, 1 << 3):
        idx = [i for i in range(3) if (mask >> i) & 1]
        if len(idx) == 1:
            v = np.zeros(3)
            v[idx[0]] = 1.0
            candidates.append(v)
            continue
        A = M[np.ix_(idx, idx)]
        ones = np.ones(len(idx))
        try:
            w = np.linalg.solve(A, ones)
            denom = float(np.sum(w))
            if abs(denom) > 1e-13:
                loc = w / denom
                if np.all(loc >= -1e-10):
                    v = np.zeros(3)
                    v[idx] = np.maximum(loc, 0.0)
                    s = float(np.sum(v))
                    if s > 0.0:
                        candidates.append(v / s)
        except np.linalg.LinAlgError:
            pass
        if len(idx) == 2:
            i, j = idx
            a = M[i, i] - 2.0 * M[i, j] + M[j, j]
            b = 2.0 * (M[i, j] - M[j, j])
            if a < -1e-14:
                t = -b / (2.0 * a)
                if -1e-10 <= t <= 1.0 + 1e-10:
                    t = min(1.0, max(0.0, t))
                    v = np.zeros(3)
                    v[i] = t
                    v[j] = 1.0 - t
                    candidates.append(v)
    for v in candidates:
        val = float(v @ M @ v)
        if val > best_val:
            best_val = val
            best_v = v.copy()
    return best_val, best_v
