# Fresh non-author audit of D10-U10k

## Verdict

`CORRECT`, scoped to strict exchangeable kernels with
\(\alpha,\beta\in(0,1)\) and \(\alpha\ne\beta\).

Two independent reconstructions were performed.  One started from the
reviewed Fisher/missing-information identity.  The other rebuilt

\[
H=-\{p_0\log p_0+3p_1\log p_1+3p_2\log p_2+p_3\log p_3\}
\]

directly from the four per-subset atoms and differentiated before making
the odds substitution.  Both obtained

\[
\det C=
\frac{\sum_{k=0}^4c_k(t)q^k}
{qt(1+q)^2(t+2)(2t+1)}
\]

with the same five coefficients as [proof.md](../proof.md).

## Checks that passed

- The multiplicities \((1,3,3,1)\), Hessian sign, and factor of two in the
  repeated \(\beta\) Fisher information were rebuilt from the atoms.
- The odds map was used only to substitute into the already-computed
  \((\alpha,\beta)\) Hessian; no invalid Hessian coordinate transformation
  was made.
- The positive denominator and the coefficients \(c_0,c_2,c_3,c_4\) agree
  exactly.  Complementation gives \(c_1\) and the self-reciprocity of
  \(c_2\), with \(d,e\) explicitly interchanged under \(t\mapsto1/t\).
- The small-\(t\) proof does not use the false global bound
  \(d<\log(4/3)\).  The unbounded logarithm is controlled by
  \(\log(1+z)\le\sqrt z\), giving the explicit positive lower bound
  \(c_3/2>179/384\).
- The \(c_2\) split for \(t>1\) was checked term by term.  A second audit
  also closed it independently after reciprocal reduction to \(0<t<1\),
  obtaining a positive multiple of \((t-1)^2\).
- The exact formula for \(C_{\alpha\alpha}\) is positive, so determinant
  positivity implies positive definiteness of the invariant block.
- At \(t=1\), all five coefficients vanish and \(\det C=0\).  This is the
  excluded diagonal \(\alpha=\beta\), not a failure of strictness on the
  connected domain.

## Corrections made during review

An early draft incorrectly treated \(d\) as bounded when \(t\downarrow0\).
The reviewer rejected that step.  Equations (23)--(24) of the final proof
replace it with a valid uniform estimate.  The final text also states the
domain of \(d\le\log(4/3)\), the interchange of \(d,e\) under complement,
and the exclusion of \(t=1\) wherever strict positivity is claimed.

No finite sampling is used to certify the theorem.
The separate [sanity replay](../run_log.md) checks seven frozen rational
points, including a near-diagonal scale, against direct event differentiation.
