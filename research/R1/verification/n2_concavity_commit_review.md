CORRECT

# Commit-bound non-author review: `n=2` concavity

The reviewer read only fixed Git objects, not working-tree proof files.

## Object binding

- Commit: `603300c06059518961766c724377c3b9d1198fc5`.
- Tree: `9c1a4db5462dddaf4a3b7cc37c010927254cbda4`.
- Parent: `c61686734aa442b520baaa97dc98b318c76176fc`.
- Frozen theorem blob: `cc247289014ba6874387da87543667e0e01616c3`.
- Proof blob: `7d652eae8d745d2289713db82b590d0c41c04bc7`.
- Symbolic-check blob: `4b29bc795ca7ce1927e2369517535d097c9a0e33`.
- Symbolic-result blob: `1d5ebfe7b140c6673a28787061bdae580110c0b4`.

All objects were read with `git show <commit>:<path>`.  The reviewer did not
author the proof.

## Verdict

The proof establishes

```text
[H(K_-)+H(K_+)]/2-H(K_0) <= 0
```

for every strictly feasible real symmetric `2 x 2` DPP chord.  No critical
gap or counterexample was found.

## Checks performed

1. The four complete events obtained by Mobius inversion are
   `A=1-a-b+d`, `B=a-d`, `C=b-d`, `D=d`, where `d=ab-c^2`; the identity
   `BC-AD=c^2` is correct.  Principal minors are not misused as complete
   events.
2. For `V=[[u,w],[w,v]]`, the event acceleration is
   `2 det(V)(1,-1,-1,1)`.  Hence `H''=-F+2qL`; the factor two and all signs
   are correct.
3. For `c!=0`, the change to `(u,v,alpha)` is invertible.  The displayed
   Fisher matrix `G`, determinant form `Q`, and
   `det(G-sQ)=[16r+4sE-s^3P]/(16rP)` agree algebraically under
   `A+B+C+D=1`.  The exact symbolic record gives the equivalent identity in
   scaled Frobenius coordinates.
4. The bounds `sqrt(P)L<=r` and `E>4r^2` are valid.  They show the determinant
   stays positive for the full path `0<=s<=2L`, not only at its endpoint.
   Inertia therefore remains positive definite from `G` to `G-2LQ`.
5. At `c=0`, `L=0` and the undivided formula gives `H''=-F<=0`; no singular
   coordinate is used there.
6. The strict feasible domain is convex and the entropy is `C^2`, so the
   local Hessian result integrates to the frozen global midpoint inequality.
   The additional strictness claim for every nonzero chord is also correct.

The theorem, proof, symbolic identities, boundary handling, and
local-to-global step are mutually consistent.

