# A2 audit addendum: execution record and partial formal coverage

Publication note: machine-local paths are normalized to placeholders; original execution records remain in the isolated route archive. Mathematical content, code and numeric output are unchanged.

This addendum records execution details from the prior v2 bounded checks and a
read-only local-formal coverage check. It does not revise
`final_v2_review.md` or `final_v3_review.md`, and it does not add any new
mathematical conclusion.

## 1. Failed attempt to run the submitted sympy tool

Purpose: extract the `moving_frame_check.py` blob from v2 commit
`ab4d57cdbdc782fd033178795da9873db01bf7be` into the audit directory and try
to run `--mode smoke` and `--mode certify` with the bundled Python runtime.

Tool record: `functions.exec_command`, chunk id `2acee6`.

Command: PowerShell invoked
`<bundled-python> -c <script>`.

PID: `UNAVAILABLE`. The process id was not printed by the command or exposed in
the captured tool result.

Exit code: `1`.

The temporary extracted script was later removed from the audit directory.

Captured output:

```text
source_sha256 38b82d9df1b8efb6b9b7d33018d21169ef0591c508c5dcddea765c6d99046b8a
mode smoke exit 1

Traceback (most recent call last):
  File "<audit-dir>/tmp_moving_frame_check_ab4d57.py", line 20, in <module>
    import sympy as sp
ModuleNotFoundError: No module named 'sympy'
```

This failed run was not used as mathematical evidence.

## 2. Standard-library rational 4x4 cross-check

Purpose: independently reconstruct the v2 rational family at finitely many
rational chords using only Python standard-library exact rational arithmetic;
check the actual arithmetic midpoint, all principal minors of `K` and `I-K`,
the full inclusion-exclusion event law, and high-precision Decimal entropy
differences. This was a finite cross-check only, not a general proof.

Tool record: `functions.exec_command`, chunk id `c89371`.

Command: PowerShell invoked
`<bundled-python> -c <script>`.

PID: `UNAVAILABLE`. The process id was not printed by the command or exposed in
the captured tool result.

Exit code: `0`.

Code executed:

```python
from fractions import Fraction as F
from decimal import Decimal, getcontext
from itertools import combinations
getcontext().prec = 80

def matmul(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]

def transpose(A):
    return [list(row) for row in zip(*A)]

def eye(n):
    return [[F(int(i==j),1) for j in range(n)] for i in range(n)]

def add(A,B):
    return [[A[i][j]+B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def scale(c,A):
    return [[c*x for x in row] for row in A]

def submatrix(A, ids):
    return [[A[i][j] for j in ids] for i in ids]

def det(A):
    n=len(A)
    if n==0: return F(1)
    M=[row[:] for row in A]
    sign=1
    prev=F(1)
    for k in range(n-1):
        piv=None
        for i in range(k,n):
            if M[i][k]!=0:
                piv=i; break
        if piv is None: return F(0)
        if piv!=k:
            M[k],M[piv]=M[piv],M[k]
            sign*=-1
        pivot=M[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                M[i][j]=(M[i][j]*pivot-M[i][k]*M[k][j])/prev
        prev=pivot
        for i in range(k+1,n):
            M[i][k]=F(0)
    return sign*M[n-1][n-1]

def kernel(t,x,sigma):
    c=(1-t*t)/(1+t*t)
    s=2*t/(1+t*t)
    Q=eye(4)
    Q[1][1]=c; Q[1][2]=-s; Q[2][1]=s; Q[2][2]=c
    A=matmul(Q, [[F(1),F(0)],[F(1),F(0)],[F(0),F(1)],[F(0),F(1)]])
    AAT=matmul(A,transpose(A))
    X=[[F(0),x],[x,F(0)]]
    AXAT=matmul(matmul(A,X),transpose(A))
    return add(add(scale(t,eye(4)), scale((1-2*t)/2,AAT)), scale(sigma*t/2,AXAT))

def principal_minors(K):
    out={}
    for mask in range(16):
        ids=[i for i in range(4) if mask>>i & 1]
        out[mask]=det(submatrix(K,ids))
    return out

def full_law(K):
    minors=principal_minors(K)
    masses={}
    for mask in range(16):
        total=F(0)
        for other,val in minors.items():
            if other & mask == mask:
                total += ((-1)**((other^mask).bit_count()))*val
        masses[mask]=total
    return masses,minors

def dec(q):
    return Decimal(q.numerator)/Decimal(q.denominator)

def entropy(law):
    total=Decimal(0)
    for p in law.values():
        if p:
            dp=dec(p)
            total -= dp*dp.ln()
    return total

def check(t,x):
    Ks={sig: kernel(t,x,sig) for sig in (-1,0,1)}
    assert Ks[0] == [[(Ks[-1][i][j]+Ks[1][i][j])/2 for j in range(4)] for i in range(4)]
    rows=[]
    for sig,K in Ks.items():
        law,minors=full_law(K)
        comp=full_law([[F(int(i==j),1)-K[i][j] for j in range(4)] for i in range(4)])[1]
        assert sum(law.values()) == 1
        assert min(law.values()) > 0
        assert all(v>0 for m,v in minors.items() if m)
        assert all(v>0 for m,v in comp.items() if m)
        rows.append((sig, min(law.values())))
    laws={sig: full_law(Ks[sig])[0] for sig in (-1,0,1)}
    delta=(entropy(laws[-1])+entropy(laws[1]))/2-entropy(laws[0])
    return rows, delta

for t,x in [(F(1,8),F(1,2)),(F(1,16),F(1,4)),(F(1,64),F(1,4)),(F(1,16),F(1,2)),(F(1,64),F(1,2)),(F(1,16),F(3,4)),(F(1,64),F(3,4))]:
    rows,delta=check(t,x)
    print(f"t={t} x={x} min_masses={rows} delta={delta}")
```

Captured output:

```text
t=1/8 x=1/2 min_masses=[(-1, Fraction(147, 16384)), (0, Fraction(49, 4096)), (1, Fraction(147, 16384))] delta=-0.0043945921343792580363964661094879463943096797605634919432654805920572092242852
t=1/16 x=1/4 min_masses=[(-1, Fraction(3375, 1048576)), (0, Fraction(225, 65536)), (1, Fraction(3375, 1048576))] delta=-0.0001463794411047078916266295366277748662672997930927380390374869950682059477069
t=1/64 x=1/4 min_masses=[(-1, Fraction(59535, 268435456)), (0, Fraction(3969, 16777216)), (1, Fraction(59535, 268435456))] delta=-0.0000027376794559304041794146761052015364784048535961555885973686394278306328736
t=1/16 x=1/2 min_masses=[(-1, Fraction(675, 262144)), (0, Fraction(225, 65536)), (1, Fraction(675, 262144))] delta=-0.0006813454475789014968429735248109602767702152740198740533181369800671094469113
t=1/64 x=1/2 min_masses=[(-1, Fraction(11907, 67108864)), (0, Fraction(3969, 16777216)), (1, Fraction(11907, 67108864))] delta=-0.0000173144918184946666556567715178311673699587148462511542084785252364617074428
t=1/16 x=3/4 min_masses=[(-1, Fraction(1575, 1048576)), (0, Fraction(225, 65536)), (1, Fraction(1575, 1048576))] delta=-0.0019792800154265563350677092860269520057293926210217913835948876126638532025731
t=1/64 x=3/4 min_masses=[(-1, Fraction(27783, 268435456)), (0, Fraction(3969, 16777216)), (1, Fraction(27783, 268435456))] delta=-0.0000688116944653320208515023451012136186445351295115673861813616188959418319137
```

## 3. Read-only partial formal coverage check

Commit: `50e22cf21b5ced0fdb8d034cc9039f7816ad89f4`

Path read: `research/A2/formal/FrameAlgebra.lean`

SHA256 of blob content:
`2504581656433f9d32a245b70c695a1281966164ed665083b14ee72f42db0f6a`

Read command: PowerShell invoked
`<bundled-python> -c <git cat-file/hash script>`.

PID: `UNAVAILABLE`. The process id was not printed by the command or exposed in
the captured tool result.

Read exit code: `0`.

The Lean file defines 0-based integer matrices:

```lean
def A : M4 := fun i j => match i.val, j.val with
  | 0, 1 | 1, 0 | 2, 3 | 3, 2 => 1
  | _, _ => 0

def B : M4 := fun i j => match i.val, j.val with
  | 0, 2 | 2, 0 => 1
  | 1, 3 | 3, 1 => -1
  | _, _ => 0
```

These definitions match the v2 proof matrices under 0-based indexing:

```text
A =
[[0,1,0,0],
 [1,0,0,0],
 [0,0,0,1],
 [0,0,1,0]]

B =
[[0,0,1,0],
 [0,0,0,-1],
 [1,0,0,0],
 [0,-1,0,0]]
```

The Lean statements present in this file cover only the fixed integer algebra
used in the v2 commutator obstruction:

- `A_squared`: `A^2=I`
- `B_squared`: `B^2=I`
- `anticommutes`: `AB=-BA`
- `product_nonzero`: `(AB)_{0,3}=-1`
- `noncommutes`: `AB≠BA`

This is partial local coverage only. It does not formalize entropy, the
exact-event DPP law, feasibility, asymptotic expansions, uniform remainders,
or the v2/v3 natural-language theorems. I did not run Lean and did not read
`README` or `build.log` in this addendum.

