"""Exact symbolic identities for the n=2 entropy Hessian; not a sign proof."""
import os
for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[key] = "1"

import json
from pathlib import Path
import sympy as s

root = Path(__file__).resolve().parent
a, b, c, L = s.symbols("a b c L", real=True)
u = c*c
p = s.Matrix([(1-a)*(1-b)-u, a*(1-b)+u, (1-a)*b+u, a*b-u])
J = p.jacobian([a, b, c])*s.diag(1, 1, 1/s.sqrt(2))
F = J.T*s.diag(*[1/z for z in p])*J
P = s.prod(p)
A = a*(1-a)
B = b*(1-b)
alpha = 1-2*a
beta = 1-2*b
C = A*B-u*alpha*beta-u*u
G = s.Matrix([
    [A, -u, c*alpha/s.sqrt(2)],
    [-u, B, c*beta/s.sqrt(2)],
    [c*alpha/s.sqrt(2), c*beta/s.sqrt(2), C/(2*u)],
])
R = s.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, -1]])

assert (F*G-s.eye(3)).applyfunc(lambda z: s.simplify(s.factor(z))) == s.zeros(3)
assert s.factor(G.det()-P/(2*u)) == 0
T = G*R
minor_sum = sum(T.extract(ids, ids).det() for ids in ((0, 1), (0, 2), (1, 2)))
assert s.factor(minor_sum) == 0
expected = 1+(2*u+C/(2*u))*L-P/(2*u)*L**3
assert s.factor((s.eye(3)-L*T).det()-expected) == 0
assert s.factor(p[1]*p[2]-p[0]*p[3]-u) == 0

report = {
    "status": "EXACT_IDENTITIES_CHECKED",
    "sympy": s.__version__,
    "exit_code": 0,
    "identities": [
        "F G = I",
        "det G = P/(2u)",
        "sum principal order-two minors of G R = 0",
        "det(F-LR) = [2u+(C+4u^2)L-P L^3]/P",
        "p10*p01-p00*p11=u",
    ],
    "note": "Exact equalities only; the sign proof is in proofs/n2_concavity.md.",
}
(root/"symbolic_identities.json").write_text(json.dumps(report, indent=2)+"\n")
print(json.dumps(report))

