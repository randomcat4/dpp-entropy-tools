# Resolution of `cat5779/rl01#126`: exact three-input flow consistency gap

## Status

**PROVED for the frozen subproblem in [cat5779/rl01#126](https://github.com/cat5779/rl01/pull/126).**

This note records a self-contained resolution of the bounded three-coordinate DPP transport problem that was left as an unreviewed candidate in the earlier selector archive.

For every
[
0<etale rac1{10},
]
with
[
P=rac13mathbf1mathbf1^{mathsf T},qquad
K_0=rac12I+rac{eta}{21}
egin{pmatrix}
-11&13&-2\
13&-2&-11\
-2&-11&13
end{pmatrix},
]
and (K_a=sigma^aK_0sigma^{-a}), (sigma=(123)), the full positive birth-flow fibers (mathcal F_a) satisfy

[
oxed{
inf_{finmathcal F_a, ginmathcal F_b}|f-g|_1
=rac{48eta}{21}qquad(a
e b),
}
]

and

[
oxed{
inf_{f_ainmathcal F_a}
max_{a<b}|f_a-f_b|_1
=rac{52eta}{21}.
}
]

Hence the exact incompatibility ratio is

[
oxed{rac{52}{48}=rac{13}{12}}.
]

This proves the finite three-input gluing obstruction claimed as a candidate in the previous continuation packet. It does **not** prove or disprove the unrestricted dimension-free selector problem.

## Provenance

Frozen source:

- [cat5779/rl01#126](https://github.com/cat5779/rl01/pull/126)
- frozen head: `428c693273332743e9618fce9856384a6eb9b9e5`
- task file: `research/flow3exact01/TASK.md`

The earlier appearance of the (13/12) value was explicitly marked unreviewed. The derivation below reconstructs the result from the displayed matrices and does not inherit that verdict.

## 1. Spectrum and the common projector

Write
[
t=rac{eta}{21},qquad
A=
egin{pmatrix}
-11&13&-2\
13&-2&-11\
-2&-11&13
end{pmatrix}.
]

Direct multiplication gives

[
Amathbf1=0,qquad
A^2=441(I-P),qquad
operatorname{tr}A=0.
]

Thus the eigenvalues of (A) are (0,pm21), and therefore

[
operatorname{spec}(K_a)
=
left{rac12-eta,rac12,rac12+etaight}
subseteq
left[rac25,rac35ight].
]

Permutation conjugation fixes (P), so

[
K_aP=PK_a=rac12P.
]

A terminology point matters here: the three kernels are not mutually commuting for (eta>0); what is required and used is that every (K_a) commutes with the same rank-one projector (P).

## 2. Exact atoms and divergences

Let
[
a=(-11,-2,13),qquad
q=rac14-eta^2,qquad
h=rac1{12}+eta^2.
]

For (i=1,2,3) and (ar i={1,2,3}setminus{i}), exact expansion of
[
p_K(S)=(-1)^{|S^c|}det(K-D_{S^c})
]
gives

[
p_0(arnothing)=p_0(E)=rac q2,
]

[
p_0({i})
=
rac18+rac{a_it}{2}+rac{eta^2}{6},
qquad
p_0(ar i)
=
rac18-rac{a_it}{2}+rac{eta^2}{6}.
]

Differentiating in the direction (P) gives

[
b_0(arnothing)=-q,qquad b_0(E)=q,
]

[
b_0({i})=-h-a_it,qquad
b_0(ar i)=h-a_it.
]

The other two inputs are cyclic relabelings:
[
p_a=R^ap_0,qquad b_a=R^ab_0.
]

## 3. The full fibers really are covered

The task allows arbitrary flows in the full positive fibers, not just a preferred coupling.

For any nonnegative upward flow (f) with (Df=b_a), the empty and full vertices force total bottom and top mass
[
sum_i f(arnothing,i)
=
sum_i f(ar i,i)
=
q.
]

The singleton equations then bound every singleton outgoing mass by
[
rac13+13tlerac{83}{210}.
]

Meanwhile every exact atom satisfies, uniformly on (0<etale1/10),
[
p_a(S)gerac{79}{840}.
]

Hence
[
5p_a(S)-f_{m out}(S)
ge
rac{79}{168}-rac{83}{210}
=
rac3{40}>0.
]

So the stated capacity inequalities are automatic throughout the interval once nonnegativity and the divergence equations hold.

Also, using the vertex potential (|S|), whose gradient is (1) on every upward edge,
[
sum_e f_e
=
sum_S |S|,b_a(S)
=
1.
]

Therefore
[
oxed{mathcal F_a={fge0:Df=b_a}}
]
for this frozen family.

That point is what makes the lower bounds below genuine full-fiber statements.

## 4. Pairwise optimum: (48eta/21)

Set
[
s=rac1{12}-rac{eta^2}{3},
qquad
r=rac1{12}+rac{eta^2}{3}.
]

Give all six outer edges mass (s). Order the six middle edges as
[
1	o12,;
2	o12,;
2	o23,;
3	o23,;
3	o13,;
1	o13.
]

A feasible flow (F_0) has middle masses
[
r+t(-8,-5,3,8,5,-3).
]

Let (F_a=R^aF_0). Define the middle six-cycle circulation
[
C=(1,-1,1,-1,1,-1),
qquad DC=0.
]

For the pair ((0,1)), take
[
G_1=F_1+2tC.
]

Then
[
(F_0-G_1)_{m mid}
=
t(-15,0,9,15,0,-9),
]
so
[
|F_0-G_1|_1=48t.
]

All displayed masses are positive on the full interval; for example
[
r-8tgerac{19}{420}>0.
]

For the lower bound, use the potential
[
phi(arnothing)=phi(E)=0,
]
[
igl(phi(1),phi(2),phi(3)igr)
=
igl(phi(23),phi(13),phi(12)igr)
=
left(rac12,-rac12,-rac12ight).
]

Its edge gradient has absolute value at most (1). Therefore every
(finmathcal F_0), (ginmathcal F_1) obeys

[
|f-g|_1
ge
langlephi,b_0-b_1angle
=
48t.
]

The upper and lower bounds agree:
[
oxed{
inf_{finmathcal F_0,ginmathcal F_1}|f-g|_1
=
48t
=
rac{48eta}{21}.
}
]

Cyclic relabeling gives the same answer for every distinct pair.

## 5. Simultaneous optimum: (52eta/21)

The cyclic triple
[
(F_0,F_1,F_2)
]
is feasible, and direct subtraction gives
[
|F_a-F_b|_1=52t
qquad(a
e b).
]

So the simultaneous optimum is at most (52t).

For the exact lower bound, define
[
psi_0(arnothing)=psi_0(E)=rac23,
]
[
(psi_0(1),psi_0(2),psi_0(3))=(1,1,0),
]
[
(psi_0(12),psi_0(23),psi_0(13))=(0,1,1),
]
and let
[
psi_a=R^apsi_0.
]

On each edge (e), the three gradients
[
w_a(e)=D^{mathsf T}psi_a(e)
]
sum to zero and have total positive mass at most (1). Hence for any three real edge values (v_0,v_1,v_2),
[
sum_a w_a v_a
le
max_a v_a-min_a v_a
=
rac12sum_{a<b}|v_a-v_b|.
]

Applying this edge by edge to arbitrary feasible
((f_0,f_1,f_2)) yields
[
rac12sum_{a<b}|f_a-f_b|_1
ge
sum_alanglepsi_a,b_aangle.
]

A direct substitution of the exact divergences gives
[
langlepsi_0,b_0angle=26t,
]
and cyclic symmetry gives the same value for all (a). Therefore
[
sum_{a<b}|f_a-f_b|_1
ge
156t,
]
so
[
max_{a<b}|f_a-f_b|_1
ge
52t.
]

Together with the explicit cyclic triple,
[
oxed{
inf_{f_ainmathcal F_a}
max_{a<b}|f_a-f_b|_1
=
52t
=
rac{52eta}{21}.
}
]

Importantly, this lower bound applies directly to arbitrary feasible triples. No equivariance assumption is imposed on the competitors.

## 6. Why the three pairwise optima cannot glue

The pairwise dual certificate has a rigid equality case. For the pair ((0,1)), every pairwise-optimal difference is forced to be
[
d_{01}
=
t(-15,0,9,15,0,-9)
]
on the middle six-cycle, with zero outer-edge difference.

The other two pairwise-optimal differences are its cyclic rotations
[
Rd_{01},qquad R^2d_{01}.
]

But
[
d_{01}+Rd_{01}+R^2d_{01}
=
-6tC

e0.
]

Actual differences of three vectors must telescope:
[
(f_0-f_1)+(f_1-f_2)+(f_2-f_0)=0.
]

So the three independently pairwise-optimal choices cannot all come from a single triple. The optimal simultaneous solution repairs exactly this cycle-closing defect, raising the worst distance from (48t) to (52t).

This is the concrete meaning of the factor
[
rac{52}{48}=rac{13}{12}.
]

## 7. Scope

What is proved here:

- the two frozen formulas in `cat5779/rl01#126`;
- explicit attaining flows;
- interval-wide nonnegativity and capacity checks;
- exact full-fiber pairwise dual certificates;
- an exact simultaneous/cyclic dual certificate;
- a direct explanation of the (13/12) incompatibility.

What is **not** proved here:

- no dimension-free lower-bound divergence;
- no disproof of a universal finite-consistency selector;
- no resolution of the unrestricted problem in `cat5779/rl01#123`;
- no novelty claim.

Per the repository research protocol, this should be treated as a proof candidate in a draft PR until independently reviewed. It is appropriate to update the status of the frozen #126 subtask after review, but not the status of the parent unrestricted theorem.
