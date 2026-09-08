# Rank-one missing Fisher information and four strict boundary strips

AUTHOR PROOF CANDIDATES; not self-certified. Global Delta_T>0 is INCOMPLETE.

## 1. Notation and two logarithms

Put b=beta, c=alpha when useful, and define

U=alpha+2 beta-3 alpha beta,
V=2 alpha+beta-3 alpha beta.

Both are positive throughout the strict square. The per-subset exact atoms
are p0=(1-alpha)(1-beta)^2, p1=(1-beta)U/3, p2=beta V/3,
p3=alpha beta^2, with multiplicities (1,3,3,1).

Define two exact log ratios

ell=log[3(1-alpha) beta V/U^2],
Lambda=log[alpha(1-beta)U^3/((1-alpha)beta V^3)],
n_alpha=-ell-alpha Lambda,
n_beta=-ell-beta Lambda.                                   (1)

These n's are the two eigenvalues of the reviewed U8 cofactor matrix N:
the alpha eigenline has n_alpha and the repeated beta eigenspace has n_beta.
Connectedness, alpha!=beta, makes both strictly positive. In particular
their positivity is available without any unresolved triangle determinant
claim.

Grouping the exact atom second derivatives gives the invariant Hessian

C_aa=F_aa,
C_ab=F_ab+2(ell+beta Lambda)=F_ab-2n_beta,
C_bb=F_bb+2(ell+alpha Lambda)=F_bb-2n_alpha.                 (2)

Here a,b subscripts on C and F mean alpha,beta, not the offdiagonal entry
a=(alpha-beta)/3. Formula (2) uses only TWO log ratios, rather than four
separately cancelling log atoms. It is an identity, not yet a positivity
argument.

## 2. The invariant Fisher matrix is diagonal minus one rank-one matrix

Let X~Bernoulli(alpha) and Z~Binomial(2,beta) be independent and N0=X+Z.
The observed count of the exchangeable DPP has this exact law, by its
probability-generating determinant. Conditional on the count, the observed
subset is uniform, independently of the parameters. Hence its invariant
Fisher information equals that of N0.

Set u=1/[alpha(1-alpha)] and v=1/[beta(1-beta)]. The complete-data scores
are u(X-alpha) and v(Z-2beta), with Fisher diag(u,2v). Given N0, we have
Z=N0-X, so the conditional score covariance is
Var(X|N0)(u,-v)(u,-v)^T. The conditional-expectation score identity and the
law of total covariance therefore prove exactly

F=diag(u,2v)-kappa (u,-v)(u,-v)^T,                         (3)
kappa=E Var(X|N0)
 =2 alpha(1-alpha)beta(1-beta)[(1-beta)/U+beta/V].            (4)

For completeness, only counts one and two contribute. Their two latent
weights are alpha(1-beta)^2 and 2(1-alpha)beta(1-beta), and
2alpha beta(1-beta) and (1-alpha)beta^2, respectively. Summing AB/(A+B)
for these two pairs gives (4). This proves the missing-information formula
without an appeal to a numerical inverse or an unidentified general theorem.

The entire remaining scalar condition is thus the explicit inequality

[u-kappa u^2][2v-kappa v^2-2n_alpha]
                   -[kappa uv-2n_beta]^2 > 0.              (5)

The first factor u-kappa u^2=F_aa is strictly positive: the derivative of
p0 with respect to alpha is nonzero. Consequently (5) is equivalent to
full Sym(3) Hessian strictness by the reviewed U10f standard-block theorem.
It is not a weaker sufficient test. At alpha=beta it equals zero; that
ridge is excluded. The rational latent variance alone does not establish
the needed coupling with the two logarithms n_alpha,n_beta.

## 3. A genuine new theorem candidate: four uniform boundary strips

For each fixed 0<r<1/2 there exists epsilon_r>0 such that B_K>0 on ALL
Sym(3) for every point in any of the four regions

```text
beta in [r,1-r], 0<alpha<epsilon_r;
beta in [r,1-r], 0<1-alpha<epsilon_r;
alpha in [r,1-r], 0<beta<epsilon_r;
alpha in [r,1-r], 0<1-beta<epsilon_r.
```

Choose epsilon_r<r/2, so these regions are automatically connected and
avoid alpha=beta. The proof is the uniform asymptotic computation below,
not a finite sequence approaching the boundary. Epsilon_r is existential;
no effective numerical width is claimed.

### 3.1 alpha decreases to zero, beta in a compact interior interval

The atom p3=alpha beta^2 alone vanishes, to first order. The other three
layer probabilities tend to

((1-beta)^2, 2beta(1-beta)/3, beta^2/3),

and are uniformly positive on the chosen compact beta interval. Direct
exact-event differentiation consequently gives uniformly

C_aa=beta^2/alpha+O_r(1),
C_ab=2beta log(alpha)+O_r(1),
C_bb=L(beta)+O_r(alpha |log alpha|),                        (6)
L(beta)=2/[beta(1-beta)]-2log(4/3)>0.

To check L independently, the limiting entropy is exactly
2h(beta)-2beta(1-beta)log2+(2beta-beta^2)log3. Its negative second
derivative is L. Its lower bound is at least 8-2log(4/3)>0.
The singular contributions in (6) can also be read directly from p3:
its Fisher C_aa term is beta^2/alpha, its mixed log term is
2beta log(alpha beta^2), and its C_bb log term is
2alpha log(alpha beta^2). Every remaining term extends smoothly.

It follows uniformly that

alpha Delta_T -> beta^2 L(beta)>0.                         (7)

For example the determinant remainder before multiplication by alpha is
O_r(1+|log alpha|^2); alpha times this remainder vanishes uniformly. The
limiting function has a strictly positive minimum over [r,1-r]. This
proves the first strip without estimating a small eigenvalue by subtraction.

### 3.2 beta decreases to zero, alpha in a compact interior interval

Here p0->1-alpha and p1->alpha/3 remain positive, whereas

p2=(2alpha/3)beta+O_r(beta^2), p3=alpha beta^2.

The vanishing orders are one and two, respectively. The exact derivatives
give uniformly

C_aa=1/[alpha(1-alpha)]+O_r(beta),
C_ab=2log beta+O_r(1),
C_bb=2alpha/beta+2(1-alpha)log beta+O_r(1).                 (8)

The leading C_bb pole comes from the three p2 atoms. The coefficient of
log beta is 2(1-3alpha) from their second derivatives plus 4alpha from
p3, totaling 2(1-alpha). In C_ab these terms contribute
(2-6beta)log beta+4beta log beta=2log beta+o(1).
The pure Fisher C_aa extends smoothly to the stated positive Bernoulli
limit. Therefore

beta Delta_T -> 2/(1-alpha)>0                              (9)

uniformly on the compact alpha interval. The error in Delta_T is at worst
O_r(1+|log beta|^2), so the normalized error vanishes uniformly. This proves
the third strip.

### 3.3 Complemented edges and uniform quantifiers

Complementation sends (alpha,beta) to (1-alpha,1-beta) and leaves C, under
the common coordinate sign change, congruent to itself. Thus it preserves
Delta_T. The other two normalized limits are

(1-alpha)Delta_T -> (1-beta)^2 L(beta),
(1-beta)Delta_T -> 2/alpha.                                (10)

All atom polynomials not explicitly vanishing in (6)/(8) stay bounded
below on the indicated compact transverse intervals. Their rational
derivatives and logarithms therefore have uniform remainder bounds.
The displayed powers times logarithms vanish uniformly in the small
parameter. Taking the minimum of the four resulting positive widths,
and of r/2, gives the stated common epsilon_r. The already-positive U10f
four-dimensional standard block then transfers the invariant sign to
the FULL Hessian at every point of those strips. No uniform eigenvalue
lower bound for the standard block at a boundary is required.

The four corners are NOT included in this theorem: r is fixed. Letting
r tend to zero simultaneously would require new two-scale estimates.

## 4. Diagonal ridge, compact middle, and invalid shortcuts

The reviewed U10f theorem already proves a punctured diagonal neighborhood
uniformly for x in compact subsets of (0,1). This unit does not rebrand that
result as new. Its Taylor coefficient is compatible with (5). The new
boundary strips and that old ridge neighborhood do not exhaust the square:
corner approaches and a separated compact middle remain without a global
analytic bound here. Positivity of a continuous function on a finite net
does not provide the missing compact-middle proof.

More explicitly, on alpha=x+2a,beta=x-a the reviewed local expansion gives
Delta_T/(alpha-beta)^2 -> 2/[3x^3(1-x)^3]. The factor is obtained from
det C=(1/9)det B_(x,a) and (alpha-beta)^2=9a^2; neither coordinate system
is being silently treated as orthonormal.

There is no alpha<->beta entropy symmetry. These rates have different
multiplicities (one and two). The exact rational comparison
(alpha,beta)=(1/5,2/5) versus (2/5,1/5) has different entropies; the script
proves inequality by clearing denominators in their prime-log coefficient
vectors, without trusting a floating difference. A coordinate swap may
relabel the domain, but it does not preserve the formula or justify
discarding half of it.

For this witness, exactly
125[H(1/5,2/5)-H(2/5,1/5)]
=226log2-71log3+28log7-38log19 != 0.
After exponentiating, nonzero prime exponents prove non-equality by unique
factorization. The numerical difference, about 0.169973, is only an
illustration of that exact obstruction.

Another tempting shortcut would bound the mixed entry by assuming
2n_beta<=F_ab, or assume C_ab>=0. Equation (8) disproves it on an entire
strict boundary approach: C_ab=2log beta+O(1)->-infinity for fixed interior
alpha. Nevertheless Delta_T stays positive by (9). Thus an entrywise
sign argument is the wrong target; the positive C_bb pole compensates for
the squared logarithmic mixed term.

Likewise complete-data Fisher positivity and the rank-one identity (3)
alone do not control the acceleration subtraction in (2). No proof that
arbitrary positive matrices with that rank-one pattern satisfy (5) is
being asserted. The remaining inequality must exploit the exact rational
kappa and the DPP log ratios jointly.

## 5. Review priorities and exact unresolved gate

The most fragile steps are the latent-score signs in (3), the factor two
on beta's complete Fisher information, the C_ab versus C_bb placement of
n_beta/n_alpha, and the log coefficients and uniform errors in (6)/(8).
All four edges are obtained by complement, not by swapping alpha and beta.

The global target remains EXACTLY (5)>0 over the entire strict square off
the diagonal. New boundary theorem candidates settle only the quantified
strips in section 3. The script provides exact algebra and bounded numerical
sanity, not an independent certificate of a universal inequality.
