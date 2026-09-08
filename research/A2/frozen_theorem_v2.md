# Frozen candidate family v2: rational physical rotation

Frozen by A2 on 2026-09-08. This specializes v1 to an explicit candidate;
it does not modify the finite entropy question. Authors cannot vary the
assumptions below without a new frozen version.

## Objects

Let U0 have columns (1,1,0,0)^T/sqrt(2) and (0,0,1,1)^T/sqrt(2).
For 0<t<1/2 let c=(1-t^2)/(1+t^2), s=2t/(1+t^2). Let Q(t) be identity
on coordinates 1 and 4 and have block [[c,-s],[s,c]] on coordinates 2,3.
Set U(t)=Q(t)U0 and P(t)=U(t)U(t)^T. Fix x with 0<x<1 and set
X=[[0,x],[x,0]]. For sigma in {-1,+1}, define

    M(t)=t I4+(1-2t)P(t),
    K_sigma(t)=M(t)+sigma t U(t)XU(t)^T,
    K_0(t)=(K_-(t)+K_+(t))/2=M(t).

Use the complete exact-event law, natural logarithms and Delta from v1.
All physical observation coordinates are held fixed as t varies.

## Frozen claims to decide

1. For every t in (0,1/2) all three kernels are strict real positive
   contractions and K_0 is the actual arithmetic midpoint.
2. On no interval (0,t0) can this entire path be represented directly by
   the R2 fixed-data two-term mixed family or unequal scalar-slack family,
   even after one fixed orthogonal representation and a common scalar
   reparameterization tending to zero. The necessary invariant to check is
   commutativity of every pair of midpoint matrices.
3. For every fixed x in (0,1), determine the first nonzero asymptotic term
   of Delta(t,x), with a remainder uniform for x in every compact subinterval
   of (0,1), and decide its sign. All 16 events must be included, including
   events absent in the limiting projection.

## Success and non-claims

A complete family claim needs a self-contained proof and independent review.
Finite rational evaluations supply cross-checks, not the family proof.
There is no claim about x tending to zero or one with t; those regimes
require their own freeze and remainder analysis. A changing high-space
column gauge is not counted as a physical mechanism. No global concavity or
novelty claim is made.
