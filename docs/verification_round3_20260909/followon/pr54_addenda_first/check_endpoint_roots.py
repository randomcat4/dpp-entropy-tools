from fractions import Fraction as F


def matmul(A, B):
    return [
        [sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))]
        for i in range(len(A))
    ]


def transpose(A):
    return [list(row) for row in zip(*A)]


def eye(n):
    return [[F(1 if i == j else 0) for j in range(n)] for i in range(n)]


def sub(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def inv(A):
    n = len(A)
    aug = [list(A[i]) + eye(n)[i] for i in range(n)]
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if aug[row][col] != 0:
                pivot = row
                break
        if pivot is None:
            raise ValueError("singular matrix")
        if pivot != col:
            aug[col], aug[pivot] = aug[pivot], aug[col]
        p = aug[col][col]
        aug[col] = [x / p for x in aug[col]]
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            if factor:
                aug[row] = [aug[row][j] - factor * aug[col][j] for j in range(2 * n)]
    return [row[n:] for row in aug]


def trace(A):
    return sum(A[i][i] for i in range(len(A)))


def endpoint_stats(A, C, B):
    S = matmul(inv(C), matmul(matmul(transpose(B), inv(A)), B))
    tr = trace(S)
    disc = 2 * trace(matmul(S, S)) - tr * tr
    return tr, disc


def fmt(x):
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


A = [
    [F(1, 2), F(1, 20), F(1, 30)],
    [F(1, 20), F(2, 5), F(1, 25)],
    [F(1, 30), F(1, 25), F(3, 5)],
]
C = [
    [F(2, 5), -F(1, 30), F(1, 40)],
    [-F(1, 30), F(1, 2), F(1, 35)],
    [F(1, 40), F(1, 35), F(11, 20)],
]
U = [
    [F(1, 100), F(1, 100)],
    [F(2, 100), F(1, 100)],
    [F(3, 100), F(1, 100)],
]
V = [
    [F(1), F(0)],
    [F(1), F(1)],
    [F(1), F(2)],
]
B = matmul(U, transpose(V))
I = eye(3)

tr_K, disc_K = endpoint_stats(A, C, B)
tr_IK, disc_IK = endpoint_stats(sub(I, A), sub(I, C), B)

expected_disc_K = F(3710825577769541084161, 4104054745543938939062500)
expected_disc_IK = F(16227278265011862790681, 6214062013120963640250000)

rho_K_upper = F(1, 25)
rho_IK_lower = F(1, 20)
rhs_K = 2 * rho_K_upper - tr_K
sep_K = rhs_K * rhs_K - disc_K
rhs_IK = 2 * rho_IK_lower - tr_IK
sep_IK = disc_IK - rhs_IK * rhs_IK

checks = {
    "Delta_K_matches_output": disc_K == expected_disc_K,
    "Delta_IK_matches_output": disc_IK == expected_disc_IK,
    "Delta_K_positive": disc_K > 0,
    "Delta_IK_positive": disc_IK > 0,
    "rho_K_upper_rhs_positive": rhs_K > 0,
    "rho_K_less_than_1_over_25_square_gap_positive": sep_K > 0,
    "rho_IK_lower_rhs_positive": rhs_IK > 0,
    "rho_IK_greater_than_1_over_20_square_gap_positive": sep_IK > 0,
}

print("independent exact rational endpoint-root check")
print(f"tr_K = {fmt(tr_K)}")
print(f"Delta_K = {fmt(disc_K)}")
print(f"2*(1/25)-tr_K = {fmt(rhs_K)}")
print(f"[2*(1/25)-tr_K]^2 - Delta_K = {fmt(sep_K)}")
print(f"tr_IK = {fmt(tr_IK)}")
print(f"Delta_IK = {fmt(disc_IK)}")
print(f"2*(1/20)-tr_IK = {fmt(rhs_IK)}")
print(f"Delta_IK - [2*(1/20)-tr_IK]^2 = {fmt(sep_IK)}")
for name, ok in checks.items():
    print(f"{name}: {'PASS' if ok else 'FAIL'}")
if not all(checks.values()):
    raise SystemExit(1)
