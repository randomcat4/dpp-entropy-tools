# Authoritative notation correction for `moment_response_entropy.md`

Status: **STATIC/MATHEMATICAL CLARIFICATION; part of the author proof.**

In Section 2 of `moment_response_entropy.md`, the return sequence was typeset once as `\nu_n` and subsequently as `u_n`. There is only one sequence. To avoid confusing it with the invariant measure `\nu_s`, the authoritative notation is

\[
r_n:=\mathbf P_0(S_n=0),\qquad n\ge0.
\]

Accordingly, equations (2.7)--(2.9) and every later occurrence of `u_n` in that file are to be read as follows:

\[
r_0=1,
\qquad
r_n=\sum_{k=1}^n f_k r_{n-k},
\tag{C.1}
\]

\[
\sum_{n\ge0}r_n=\frac1{1-\theta}<\infty,
\tag{C.2}
\]

and

\[
\operatorname{osc}(\mathcal L_s^nF)
\le\sum_{k=0}^n\operatorname{var}_k(F)r_{n-k}.
\tag{C.3}
\]

All proofs and nonnegative sum exchanges use this single defective-renewal sequence. No statement, estimate, threshold, or entropy conclusion changes. In particular, the symbols retain their separate roles:

- `\nu_s`: stationary DPP future law at parameter `s`;
- `r_n`: return probability of the BFG auxiliary age chain at time `n`;
- `f_n`: defective first-positive-return law;
- `\theta=\sum_{n\ge1}f_n<1`.

Independent review should treat (C.1)--(C.3) as the authoritative notation.