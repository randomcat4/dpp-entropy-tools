#!/usr/bin/env python3
"""Complete-configuration finite-DPP derivatives for n <= 6.

The event formula is

    p_S(K) = (-1)^|S^c| det(K - diag(1_{S^c})).

For K(t)=K+tA, determinant jets give p, p' and p'' analytically.  Every
2^n event is retained; this module never substitutes spectral entropy for
configuration Shannon entropy.
"""
from __future__ import annotations

import itertools
import math
from dataclasses import dataclass

import numpy as np


@dataclass
class HessianResult:
    hessian: float
    fisher: float
    acceleration: float
    min_probability: float
    sum_p: float
    sum_p1: float
    sum_p2: float
    max_imaginary_residual: float


def complete_event_jets(K: np.ndarray, A: np.ndarray):
    K = np.asarray(K, dtype=np.complex128)
    A = np.asarray(A, dtype=np.complex128)
    n = K.shape[0]
    if K.shape != (n, n) or A.shape != (n, n):
        raise ValueError("K and A must be square matrices of the same size")
    rows = []
    max_imag = 0.0
    for mask in range(1 << n):
        complement = [i for i in range(n) if not (mask & (1 << i))]
        M = K.copy()
        M[complement, complement] -= 1.0
        sign = -1.0 if len(complement) % 2 else 1.0
        det = np.linalg.det(M)
        X = np.linalg.solve(M, A)
        tr = np.trace(X)
        second_factor = tr * tr - np.trace(X @ X)
        values = (sign * det, sign * det * tr, sign * det * second_factor)
        max_imag = max(max_imag, *(abs(complex(x).imag) for x in values))
        rows.append(tuple(float(complex(x).real) for x in values))
    return rows, max_imag


def complete_shannon_hessian(K: np.ndarray, A: np.ndarray) -> HessianResult:
    rows, max_imag = complete_event_jets(K, A)
    p = np.array([x[0] for x in rows])
    p1 = np.array([x[1] for x in rows])
    p2 = np.array([x[2] for x in rows])
    if np.min(p) <= 0:
        raise ArithmeticError(f"nonpositive event probability {np.min(p)}")
    fisher = -float(np.sum(p1 * p1 / p))
    acceleration = -float(np.sum(p2 * np.log(p)))
    return HessianResult(
        hessian=fisher + acceleration,
        fisher=fisher,
        acceleration=acceleration,
        min_probability=float(np.min(p)),
        sum_p=float(np.sum(p)),
        sum_p1=float(np.sum(p1)),
        sum_p2=float(np.sum(p2)),
        max_imaginary_residual=max_imag,
    )


def hermitian_toeplitz_projection(M: np.ndarray) -> np.ndarray:
    """Frobenius orthogonal projection onto Hermitian Toeplitz matrices."""
    M = np.asarray(M, dtype=np.complex128)
    M = (M + M.conj().T) / 2.0
    n = M.shape[0]
    lags: dict[int, complex] = {0: complex(np.trace(M).real / n)}
    for k in range(1, n):
        # Convention: T[i,j] = c[i-j].
        value = complex(np.mean(np.diag(M, k=-k)))
        lags[k] = value
        lags[-k] = value.conjugate()
    return np.array([[lags[i - j] for j in range(n)] for i in range(n)])


def toeplitz_from_coefficients(c0: float, coefficients: np.ndarray, n: int) -> np.ndarray:
    """T_n(f), where f(x)=c0+2 Re sum c_k exp(2 pi i k x)."""
    coefficients = np.asarray(coefficients, dtype=np.complex128)
    lags = {0: complex(c0)}
    for k, value in enumerate(coefficients, start=1):
        lags[k] = complex(value)
        lags[-k] = complex(value).conjugate()
    return np.array([[lags.get(i - j, 0.0) for j in range(n)] for i in range(n)])


def coefficients_from_toeplitz(T: np.ndarray):
    T = hermitian_toeplitz_projection(T)
    n = len(T)
    return float(T[0, 0].real), np.array([T[k, 0] for k in range(1, n)])


def symbol_values(c0: float, coefficients: np.ndarray, x: np.ndarray) -> np.ndarray:
    out = np.full_like(x, c0, dtype=float)
    for k, value in enumerate(coefficients, start=1):
        out += 2.0 * np.real(value * np.exp(2j * np.pi * k * x))
    return out


def lipschitz_symbol_certificate(
    c0: float, coefficients: np.ndarray, grid_size: int = 65536
):
    """Conservative whole-circle bounds from grid values and sup |f'|."""
    x = np.arange(grid_size, dtype=float) / grid_size
    values = symbol_values(c0, coefficients, x)
    derivative_bound = 4.0 * math.pi * sum(
        k * abs(value) for k, value in enumerate(coefficients, start=1)
    )
    remainder = derivative_bound / (2.0 * grid_size)
    return {
        "grid_size": grid_size,
        "grid_min": float(np.min(values)),
        "grid_max": float(np.max(values)),
        "derivative_bound": float(derivative_bound),
        "remainder": float(remainder),
        "certified_lower": float(np.min(values) - remainder),
        "certified_upper": float(np.max(values) + remainder),
    }


def hermitian_coordinates(M: np.ndarray) -> np.ndarray:
    """Real orthonormal coordinates for Hermitian matrices."""
    M = np.asarray(M, dtype=np.complex128)
    n = len(M)
    out = [float(M[i, i].real) for i in range(n)]
    root2 = math.sqrt(2.0)
    for k in range(1, n):
        for i in range(n - k):
            z = M[i + k, i]
            out.extend((root2 * z.real, root2 * z.imag))
    return np.array(out)


def assert_toeplitz_projection(M: np.ndarray, T: np.ndarray, atol: float = 2e-12):
    n = len(M)
    assert np.linalg.norm(T - T.conj().T) <= atol
    for i, j, p, q in itertools.product(range(n), repeat=4):
        if i - j == p - q:
            assert abs(T[i, j] - T[p, q]) <= atol
    residual = hermitian_coordinates(M - T)
    # Test orthogonality against an orthonormal spanning set numerically.
    tests = [np.eye(n, dtype=np.complex128)]
    for k in range(1, n):
        R = np.zeros((n, n), dtype=np.complex128)
        I = np.zeros((n, n), dtype=np.complex128)
        for i in range(n - k):
            R[i + k, i] = R[i, i + k] = 1.0
            I[i + k, i] = 1j
            I[i, i + k] = -1j
        tests.extend((R, I))
    for X in tests:
        inner = np.trace((M - T).conj().T @ X)
        assert abs(inner) <= 50 * atol
    return float(np.linalg.norm(residual))
