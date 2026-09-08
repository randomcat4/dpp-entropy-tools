# D10-U10g lambda-zero connected subfamily fresh audit

STATUS: CORRECT_SCOPED_MINIMAL_REPLAY.

No hard error was found in the checked structural identities or in the explicit
`Kstar` ball certificate.  The global connected `Lambda=0` theorem is still
`INCOMPLETE`, exactly as the author states.

This is a time-boxed freeze after an interrupted longer audit.  I stopped
expanding scope and wrote only the minimal independent replay
`fresh_min_check.py`, its JSON output, and this verdict.  I did not import or
call author `sanity.py` or any U8/U10 gate/search module.

## Frozen input hashes

The replay re-hashed the frozen files:

| file | sha256 |
|---|---|
| `frozen_problem.md` | `23ef7719d08a45da72acd1ee92473724f0625d3799a6e308b0698116185fa176` |
| `derivation.md` | `f0dc43ffd3c90240dcc1ae87fd708e6483d084539d7bf5d7ec3d247fe7381b80` |
| `proof_or_blocker.md` | `5040629574676dcd0af9f4c867651134cf88953ddd0455bc53e85137fcc6d43b` |
| `verdict.md` | `8a78d4e78e39781eceebf4bea38d4be96cfb4e071ae4e2c6779f118e239313e0` |
| `run_log.md` | `0d509e28ad1658ff17022cf7e0123e92535aea8ebed43dbdb80a96588c8827d6` |
| `sanity.py` | `0472bb41b49c0625cd5ae543b854857ca9742b76c7359c5742a823eed8f615ba` |
| `sanity.json` | `44919f4c04807385060c1d27277f9397652b24f64c863e1e4d301a826a1196e0` |

## Checks completed

1. `Lambda=0` and Cauchy `L` parameterization  
   Lines `derivation.md:7-48` are algebraically sound in this review.  The
   exact-event `L`-ensemble semantics are correct; `exp Lambda=1` reduces to
   `det R=(1-A^2)(1-B^2)(1-C^2)`; the resulting quadratic gives the two
   `sech(alpha+gamma)` / `sech(alpha-gamma)` branches; the zero-offdiagonal
   case is disconnected; and positive weighted Cauchy matrices give the
   converse.  I did not mechanize this as a CAS proof, but no missing branch was
   found.

2. Fisher external-field identity  
   Lines `derivation.md:52-78` pass.  The general exponential-tilt argument
   gives `F(D_h,E)=sum_i h_i E_ii`.  The minimal replay checked the matrix
   identity

   ```text
   F [C; U] = [I; 0]
   ```

   exactly over `Fraction` at `Kstar`, covering all `18/18` entries.

3. Retained three-by-three gate  
   Lines `derivation.md:84-117` pass algebraic inspection.  The block equations
   from `F[C;U]=[I;0]` give

   ```text
   Fxz=-C^(-1)U^T R,
   Fxx=C^(-1)+C^(-1)U^T R U C^(-1),
   ```

   and Schur elimination of `Bzz=R+Z` gives the retained gate

   ```text
   T=C-CJC+U^T (R^(-1)+Z^(-1))^(-1) U.
   ```

   The noncommuting parallel-sum identity is used in its valid form.  This is
   an equivalence/gate, not a proof of global positivity.

4. Explicit `Kstar` certificate  
   Lines `proof_or_blocker.md:8-32` pass the independent replay.  For

   ```text
   Kstar = [[1/2,3/10,0],[3/10,1/2,3/10],[0,3/10,1/2]]
   ```

   exact atoms are

   ```text
   p_empty=7/200,
   p_1=1/8, p_2=43/200, p_3=1/8,
   p_12=1/8, p_13=43/200, p_23=1/8,
   p_123=7/200.
   ```

   Their sum is exactly `1`, the `Lambda` ratio is exactly `1`, and

   ```text
   Lstar=(1/7)[[25,30,18],[30,43,30],[18,30,25]]
   ```

   is exactly `Kstar(I-Kstar)^(-1)`.  A direct 90-digit Decimal reconstruction
   of the full six-coordinate exact-event Hessian gives Frobenius-generalized
   eigenvalues beginning with

   ```text
   lambda_min = 1.977991365669662...
   ```

   so the claimed conservative base bound `Bstar >= (1/3)||D||_F^2` has a
   large margin.

5. Radius and third-derivative constants  
   Lines `proof_or_blocker.md:34-71` pass the rational arithmetic check:

   ```text
   L_H = 35781360/49,
   epsilon = 49/214688160,
   L_H * epsilon = 1/6.
   ```

   Also `epsilon < 1/40`, `epsilon < q/6`, and
   `q-3epsilon > q/2` for `q=7/200`.  The core lower-bound arithmetic in
   line `29` checks as

   ```text
   48(1-u)u/(6-u)^2 = 130032/326041 > 1/3
   ```

   at `u=324/625`.  The ordered-column derivative constants in lines `43-45`
   are loose but valid.

6. Three-parameter external-field box  
   Lines `proof_or_blocker.md:76-94` are correct conditional on the ball
   certificate above.  External fields preserve `Lambda=0`; the derivative
   formula gives

   ```text
   ||dK_sh/ds||_F <= ||diag h||_F < 2||h||_infinity,
   ```

   so `||h||_infinity <= epsilon/2` puts the whole box inside the certified
   Frobenius ball.  Therefore the box is full-`Sym(3)` positive, not merely
   tangent-positive.  I did not separately replay all eight box corners in this
   minimal freeze.

7. Fisher-only blocker wording  
   Lines `derivation.md:126-147` and `verdict.md:27-31` are scoped correctly.
   The replay gives, for `r=1-2^-16`,

   ```text
   delta V = 2.6456024962624092683...
   (2/3)delta V = 1.7637349975082728455... > 5/4.
   ```

   This refutes only the Fisher-only/proxy sufficient criterion.  It is not a
   `rho>1` witness and not an entropy nonconcavity counterexample.

## Not completed in this minimal freeze

- I did not rerun the author's full `15/15` sanity ledger or all `270` reported
  exact field identities.
- I did not mechanize the Cauchy classification as a formal symbolic proof.
- I did not independently replay the eight external-field box corners; the box
  conclusion was checked through the analytic ball inclusion.
- I did not prove positivity on the entire connected `Lambda=0` submanifold.

## Command

From repo root:

```text
C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe research\R3\deepening_10h\dense_hessian\n3_global_full_hessian\lambda_zero_subfamily\verifications\fresh_min_check.py
```

Exit code: `0`.

