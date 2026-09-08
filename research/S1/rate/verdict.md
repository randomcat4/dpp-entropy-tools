# Verdict

Status: `CORRECT` for the audit of the route-owner strict n=8 certificate; `INCOMPLETE` only for this directory's own floating-point `r=16` witness as a standalone certificate.

Mathematical route status:

- The finite-suffix upper/lower entropy-rate bounds are proved.
- For strictly positive finite-degree symbols, the Lyons--Steif extreme all-one boundary kernel differs from the ordinary future Toeplitz kernel only in the leading `m by m` corner.  The same holds for `1-f`.
- Therefore each finite suffix length `r` gives effective true entropy-rate bounds.

Benchmark status:

- The supplied benchmark has exact uniform margin `3/50`.
- At `r=16`, the positive counterexample gate is negative:

```text
L_+(16) - U_0(16) = -2.6124196211729789e-05.
```

- The negative exclusion gate is also negative:

```text
U_+(16) - L_0(16) = -2.6124194808629930e-05.
```

The route-owner n=8 rational/interval certificate supplies that outward arithmetic and gives:

```text
-2.6204849038956574e-05
<= (h(f_-)+h(f_+))/2 - h(f_0)
<= -2.6051480851662238e-05.
```

I audited the probability, perturbation, entropy-rate and log-interval chain in `author_certificate_audit.md` and found no critical gaps.  The result excludes only this fixed pair; it does not solve the global conjecture.
