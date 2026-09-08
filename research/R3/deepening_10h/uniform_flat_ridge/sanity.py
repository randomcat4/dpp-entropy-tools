"""Standard-library exact sanity checks for D10-U; not the proof."""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations


def add(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    size = max(len(left), len(right))
    result = [Fraction(0) for _ in range(size)]
    for index, value in enumerate(left):
        result[index] += value
    for index, value in enumerate(right):
        result[index] += value
    return result


def multiply(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    result = [Fraction(0) for _ in range(len(left) + len(right) - 1)]
    for i, left_value in enumerate(left):
        for j, right_value in enumerate(right):
            result[i + j] += left_value * right_value
    return result


def permutation_sign(permutation: tuple[int, ...]) -> int:
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def determinant_polynomial(matrix: list[list[list[Fraction]]]) -> list[Fraction]:
    n = len(matrix)
    result = [Fraction(0)]
    for permutation in permutations(range(n)):
        term = [Fraction(permutation_sign(permutation))]
        for row, column in enumerate(permutation):
            term = multiply(term, matrix[row][column])
        result = add(result, term)
    return result


def event_polynomial(direction: list[list[Fraction]], mask: int) -> list[Fraction]:
    n = len(direction)
    signs = [1 if (mask >> i) & 1 else -1 for i in range(n)]
    matrix: list[list[list[Fraction]]] = []
    for i in range(n):
        row = []
        for j in range(n):
            constant = Fraction(1 if i == j else 0)
            linear = 2 * signs[i] * direction[i][j]
            row.append([constant, linear])
        matrix.append(row)
    polynomial = determinant_polynomial(matrix)
    return [coefficient / (2**n) for coefficient in polynomial]


def main() -> None:
    direction = [
        [Fraction(0), Fraction(1, 3), Fraction(-2, 5), Fraction(0)],
        [Fraction(1, 3), Fraction(0), Fraction(1, 7), Fraction(2, 9)],
        [Fraction(-2, 5), Fraction(1, 7), Fraction(0), Fraction(-1, 4)],
        [Fraction(0), Fraction(2, 9), Fraction(-1, 4), Fraction(0)],
    ]
    atoms = [event_polynomial(direction, mask) for mask in range(16)]
    coefficient_sums = [sum(atom[degree] for atom in atoms) for degree in range(5)]
    assert coefficient_sums == [Fraction(1), Fraction(0), Fraction(0), Fraction(0), Fraction(0)]
    second_relative = [atom[2] * 16 for atom in atoms]
    kl_quartic = sum(value * value for value in second_relative) / 32
    expected = 8 * sum(
        direction[i][j] ** 4 for i in range(4) for j in range(i + 1, 4)
    )
    assert kl_quartic == expected
    print({"status": "PASS", "events": 16, "quartic_coefficient": str(expected)})


if __name__ == "__main__":
    main()
