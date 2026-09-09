import json
import sys
from fractions import Fraction as F
from pathlib import Path
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)
p = Path(r"C:/game/gameproject/showa100/math/i05-seven-fronts-20260909/runs/C2/verification2/hessian_review/local_smoke_run/run_20260909T065954Z_pid9692/certificate.json")
d = json.loads(p.read_text())
b = d["accepted_boxes"][0]
S = [[F(x) for x in row] for row in b["negative_hessian_preconditioner_S"]]
def det(A):
    A=[row[:] for row in A]; n=len(A); s=F(1); prev=F(1)
    for k in range(n-1):
        if A[k][k]==0:
            for r in range(k+1,n):
                if A[r][k]: A[k],A[r]=A[r],A[k]; s=-s; break
            else: return F(0)
        piv=A[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                A[i][j]=(A[i][j]*piv-A[i][k]*A[k][j])/prev
        prev=piv
    return s*A[-1][-1]
rows=b["preconditioned_gershgorin_rows_exact"]
mins=[F(r["margin"]) for r in rows]
print("status", d["status"], "accepted", d["centers_accepted"], "/", d["centers_requested"])
print("box", b["center"], b["radius"], "min_probability_lower", b["min_probability"]["lower"])
print("detS_nonzero", det(S) != 0)
print("detS", det(S))
print("min_exact_margin", min(mins))
print("positive_rows", all(m > 0 for m in mins))
print("zero_events", len(d["zero_events"]))
