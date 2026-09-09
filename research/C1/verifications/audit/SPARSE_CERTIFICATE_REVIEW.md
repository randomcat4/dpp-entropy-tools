# C1 non-author audit: rational sparse finite-epsilon certificate

STATUS: CORRECT

Scope: this review covers only the finite-epsilon rational certificate in `runs/C1/children/mechanism/outputs/sparse_rational_certificate.json` and the two frozen scripts `runs/C1/children/mechanism/scripts/sparse_rational_certificate.py` and `runs/C1/children/mechanism/scripts/mechanism_probe.py`. It does not certify the B0 global theorem and does not certify the unit-normalized sparse family used in the main asymptotic proof.

## Frozen sources checked

- `sparse_rational_certificate.py` SHA256 `5EF212FAFA0CE3B8F9F5C13768B8AEA9BC59C1077BB8D2B669E0C561599F74E8`, matching the certificate's recorded source hash.
- `mechanism_probe.py` SHA256 `13191B5147F5E1F14132BA5A2C54A71FDE097F71FEB575B418AF3DFC21F07236`, matching the certificate's recorded helper hash.
- Original certificate JSON SHA256 `5EF28BA676AF0DA0BC35AFD0A5572F9E5CFD15565B7853AF3CC9FB95743F72FA`.

The certificate family is explicitly the finite rational variant

\[
K(q)=\varepsilon I+\frac{7}{10}u(q)u(q)^T,\qquad
u(q)=\left(\frac35,\frac45,q\sqrt\varepsilon\right),\qquad
\varepsilon=10^{-8}.
\]

This is not the unit-normalized family with `u1^2=2/5`, `u2^2=3/5`, `u3^2=κ ε`. The certificate itself states the finite-epsilon distinction at `sparse_rational_certificate.py:427-428`; I treat that distinction as part of the proven scope.

## Independent rerun

I copied the two mechanism scripts into my own audit directory and reran the certificate on the server with `/opt/venv/bin/python`, one thread, no GPU. The successful reproducing run used an explicit `--cert-steps 60`:

- certificate rerun PID: `165603`
- exit code: `0`
- rerun output: `runs/C1/children/audit/mechanism_rerun/outputs/sparse_rational_certificate.cert60.json`
- rerun output SHA256: `DD347FA71CF2B1028740A65B1748897A169E2C8CE9F47A1CEB898EF147A4E6D2`
- reproduced status: `CERTIFIED_RATIONAL_SPARSE_ROOT_DALPHA_LT_ONE`
- reproduced bracket:
  - left `4418854248579277079/2305843009213693952`
  - right `8837708497158554159/4611686018427387904`
  - width `1/4611686018427387904 = 2^-62`

A default rerun with the script's present default `--cert-steps 24` did not reproduce the certificate; it failed at the whole-bracket probability positivity assertion in `interval_quantities` (`sparse_rational_certificate.py:274-277`). This is not a mathematical gap in the certified JSON, because the JSON bracket and the explicit 60-step rerun are consistent, but it is a reproducibility caveat: any public provenance should record the 60-step setting or record the certified bracket directly.

## Whole-bracket interval checks

I audited the rerun certificate by reading its rational interval endpoints, not just the Boolean status. The interval construction is in `sparse_rational_certificate.py:235-240`; the event probabilities and first derivatives use determinant cofactors with the symmetric off-diagonal factor at `sparse_rational_certificate.py:243-253`; the Fisher/N/Htilde quantities are assembled at `sparse_rational_certificate.py:274-320`.

The following exact interval implications hold on the entire certified q-bracket:

- `K(q)` is positive definite and `I-K(q)` is positive definite. This follows from the rank-one form and the script's exact bound at `sparse_rational_certificate.py:323-333`: `ε>0`, `q>0`, and the recomputed upper eigenvalue is `<1`.
- All eight atom probabilities stay positive. The certified whole-bracket lower bound for `min_p` is approximately `7.0000003569e-17`.
- `N` is positive definite on the whole bracket: the interval lower bounds for the leading minors are positive, with `N00≈1.68938956796`, leading 2x2 minor `≈1.53030383762`, and `detN≈27.23946978415` from the certificate intervals.
- The interval solve for `Htilde=dM` is valid over the bracket: all elimination pivots exclude zero and the residual intervals contain zero.
- The endpoint signs are strict: left `β√Z>0`, right `β√Z<0`. The certified endpoint intervals are approximately `+4.674079896578e-22` and `-2.493935158521e-21`.
- The whole bracket has `dα<1`; the certified interval is approximately `[0.925605324011963372275912789435720081, 0.925806704946127239064572716414179284]`.

These checks prove an exact beta zero inside the displayed rational finite-epsilon family by continuity, and at that zero the optimizer direction has `dα<1`.

## Independent high-precision formula reconstruction

I wrote `runs/C1/children/audit/sparse_certificate_audit.py` and ran it independently of `mechanism_probe.evaluate`. It reconstructs the eight probabilities, derivative rows, `Fpair`, `N`, `M`, `alpha`, `beta`, `D_M`, and the entropy second derivative from the displayed K family. Server run:

- audit PID: `165764`
- exit code: `0`
- output: `runs/C1/children/audit/sparse_certificate_audit.remote.json`
- output SHA256: `43B5B73691DE43EDF5A9D727C4A797C65EFF5EBE894569013E87A5C9E93D4CD0`
- result: `AUDIT_PASS`
- environment: Python `3.12.3`, mpmath `1.3.0`, thread variables set to one thread and GPU hidden.

Representative high-precision cross-checks from the certified bracket:

- left endpoint: `β√Z = 4.6740798965779922e-22 > 0`, `dα = 0.92570601274138076038744138014786522527048794204895`;
- midpoint: `β√Z = -1.0132635844314964e-21`, `dα = 0.92570601274138076038744137966101664313696984093366`;
- right endpoint: `β√Z = -2.4939351585207919e-21 < 0`, `dα = 0.9257060127413807603874413791741680610034517397887`.

At the midpoint, the independently reconstructed real `D_M=M^{-1}η/α` is approximately

\[
(0.2439226433102662,
0.4336401292365760,
9.674099846862683\cdot 10^{-10},
0.3252299645300764,
1.4589419787243505\cdot 10^{-5},
1.9452548811192780\cdot 10^{-5}).
\]

The two reconstructions of `h` agree: solving with `M` and solving with `Htilde=dM` differ by at most `4.76e-118`. The normalization residual is `η(D_M)-1≈1.94e-121`. The midpoint is not asserted to be the exact beta root, so `Λ'(D_M)≈-2.98e-20` is only a near-zero consistency check, not the root proof.

For the exact beta zero supplied by IVT, `β=0`; with `dα<1`, `d>0`, and `α=dα/d>0`, the identity

\[
B(D_M,D_M)=\frac1α+\left(\frac βα\right)^2-d
\]

gives `B(D_M,D_M)>0`, hence the entropy second derivative in that direction is negative. The midpoint numerical check gives `B(D_M,D_M)≈2.1861463502126951` and `H''≈-2.1861463502126951`, consistent with the certificate's intended sign.

## Review conclusion

The finite-epsilon rational certificate is correct within its stated scope. It rigorously certifies a beta-zero q in the displayed bracket for `K=εI+(7/10)uu^T`, with positive event probabilities, positive definite `K`, positive definite `I-K`, positive definite `N`, invertible `M`, `dα<1`, and the expected negative entropy second derivative along the true optimized direction at the beta zero.

No critical mathematical gap was found in this finite certificate. The only material caveat is provenance/reproducibility: the checked certificate corresponds to the `2^-62` bracket, reproduced with `--cert-steps 60`; the script's current default `--cert-steps 24` does not by itself reproduce the stored certificate.
