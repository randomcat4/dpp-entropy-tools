# Frozen exact obstruction: conditional acceleration can be positive, v1

Version date: 2026-09-08. This is a counterexample to a proposed proof shortcut,
not a counterexample to entropy concavity. Premises must not be changed.

Let

    K = [[1/4, 1/10, 1/10],
         [1/10, 3/4, 1/1000],
         [1/10, 1/1000, 1/2]],
    A=K[{1,2}], b=(1/10,1/1000)^T, c=1/2, w=(0,1)^T,
    C_1=A-bb^T/c, C_0=A+bb^T/(1-c).

Let f denote the full-event two-point DPP Shannon entropy with natural logs.
Claims:

1. K is a connected triangle satisfying 0<K<I, and both C_0,C_1 are strict
   two-point contractions.
2. The exact real number

       R = 2 (Df(C_0)[ww^T] - Df(C_1)[ww^T])

   is strictly positive.
3. Along K(t)=[[A,b+tw],[(b+tw)^T,c]], R is the conditional-kernel
   acceleration contribution in the entropy chain rule at t=0. Its sign
   refutes the blanket assertion that this contribution is always nonpositive.

The remaining weighted conditional-Hessian terms are not included in R.
Neither this statement nor a certificate for R claims that the total entropy
Hessian or a finite chord gap is positive. Strict feasibility and the sign
must be proved by exact rational arithmetic and rigorous logarithm bounds,
not a floating diagnostic. No novelty claim.
