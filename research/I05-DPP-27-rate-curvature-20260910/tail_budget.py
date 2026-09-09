from fractions import Fraction

rho = Fraction(49, 64)
C0 = Fraction(1033420800, 1263214441)
M2 = Fraction(256, 15)
M3 = Fraction(57344, 225)
M4 = Fraction(27656192, 3375)
U1 = Fraction(9, 8)
U2 = Fraction(37, 8)

A0 = M2 / 2
A1 = 8 * M2 + (M3 * U1) / 2
A2 = 192 * M2 + 16 * M3 * U1 + (M4 * U1 * U1 + M3 * U2) / 2
q = rho ** 4


def er2_prefactor(r: int) -> Fraction:
    # e_r^2 = C0^2 rho^(4r-12) = C0^2 rho^(-12) q^r.
    poly = A2 + 4 * (r + 1) * A1 + (4 * (r + 1) ** 2 + 4 * (r + 1)) * A0
    return poly * C0 * C0 * rho ** (-12)


def tail(R: int) -> Fraction:
    # Write er2_prefactor(r) = c2 r^2 + c1 r + c0 and sum exactly.
    vals = [er2_prefactor(r) for r in (0, 1, 2)]
    c0 = vals[0]
    c2 = (vals[2] - 2 * vals[1] + vals[0]) / 2
    c1 = vals[1] - c0 - c2

    s0 = q ** R / (1 - q)
    s1 = q ** R * (Fraction(R, 1) / (1 - q) + q / (1 - q) ** 2)
    s2 = q ** R * (
        Fraction(R * R, 1) / (1 - q)
        + Fraction(2 * R, 1) * q / (1 - q) ** 2
        + q * (1 + q) / (1 - q) ** 3
    )
    return c2 * s2 + c1 * s1 + c0 * s0


if __name__ == "__main__":
    print("A0", A0)
    print("A1", A1)
    print("A2", A2)
    for R in range(18, 25):
        T = tail(R)
        print(R, T, format(float(T), ".17g"))

    # Frozen acceptance-relevant thresholds. These are tail-only statements,
    # not curvature certificates because the finite conditional curvature
    # still needs an outward interval enclosure on every parameter cell.
    assert tail(20) > Fraction(1, 2500)
    assert tail(21) < Fraction(1, 2500)
    assert tail(21) > Fraction(1, 5000)
    assert tail(22) < Fraction(1, 10000)
    print("PASS")
