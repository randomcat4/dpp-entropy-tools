# Same-task continuation: explicit boundary response and physical consequences

Status: AUTHOR_PROOF / PENDING_INDEPENDENT_REVIEW. This note follows the publication of the whole-interval author result. No new DPP enumeration is used.

## 1. The previously qualitative boundary constant is now explicit

Let H_(2m)(t) be the complete entropy of m two-site cells, h_j(t)=(1/2)H(Y_0|Y_1,...,Y_j), and h(t) the true rate per original site. The chain rule gives exactly

    Psi_m(t):=H_(2m)(t)-2m h(t)
             =2 sum_(j=0)^(m-1) [h_j(t)-h(t)].              (1)

This is the same boundary excess as the Poisson telescoping formula, without a choice of corrector normalization.

Use the C2 tail of ENTROPY_KL_C2_TAIL.md. Write lambda=(34/81)^2 and P(j)=a2*j^2+a1*j+a0 with the three exact coefficients printed there. Since |h_j''-h''|<=E_j=(1/2)sum_(k>=j)lambda^k P(k), nonnegative summation yields

    sup_(m>=1,t in [1/2,3/2]) |Psi_m''(t)|
       <=sum_(k>=0)(k+1)lambda^k P(k)
       =61058907361461622425512049/975025993225062025000000
       <63.                                                (2)

This is a genuine all-volume second-PARAMETER-response bound. It comes from differentiated complete KL identities and complete Fisher/acceleration estimates, not from differentiating a value inequality or invoking a generic C3 spectral gap.

For verification let

    S0=1/(1-lambda), S1=lambda/(1-lambda)^2,
    S2=lambda(1+lambda)/(1-lambda)^3,
    S3=lambda(1+4lambda+lambda^2)/(1-lambda)^4.

Then the middle expression in (2) is a2(S3+S2)+a1(S2+S1)+a0(S1+S0), an exact rational expression.

The same proof for first derivatives uses the quantities F0 and F1(k) of the KL note and sqrt(3(k+1))<=(k+4)/2. It gives

    sup_(m,t)|Psi_m'(t)|
       <=sum_(k>=0)(k+1)lambda^k [F1(k)+(k+4)F0/2]
       =108500876203250223/33356756332656250.                (3)

In the squared parameter s=t^2/256, retaining its acceleration,

    partial_s^2 Psi_m=(16384/t^2)Psi_m''-(16384/t^3)Psi_m'.

Thus on J=[1/1024,9/1024] a concrete constant for the old PR115 boundary question is

    sup_(m,s in J)|partial_s^2 Psi_m|
      <=69019566760677589014731867136/15234781144141594140625
      <4531000.                                            (4)

This s-constant is NOT claimed sharp or small enough to use the old n=6/7/8 margins. The successful interval proof uses the exponentially small conditional-memory tail instead. Equations (2)-(4) replace the unsupported generic-spectral-gap phrasing of the earlier qualitative checkpoint with an explicit proof.

## 2. The entropy-specific response combination that is actually signed

For s=t^2/256, t>0, deleting odd-even couplings leaves K_0 and preserves each parity marginal. For every finite window this makes its parity mutual information equal to H(K_0)-H(K_t). Dividing by the number of original sites gives the relative-entropy rate

    D(s)=h(0)-h(t(s)).

The exact physical derivative is

    h_tt=-(1/128)[D'(s)+2s D''(s)].                         (5)

Therefore the author whole-interval theorem in RESULT.md yields

    D'(s)+2s D''(s) >16/375
    for every s in [1/1024,9/1024].                         (6)

This is a quantitative control of the combined response including acceleration. It does NOT prove D''>=0 or D'>=0 separately. No inference from a value bound D>=0 is made on an interval disconnected from zero.

## 3. Exact sign gauge and the negative parameter interval

Let U be diagonal with U_jj=(-1)^j. The original coordinate kernel satisfies

    K_(-t)=U K_t U.

For any finite complete event, U commutes with its vacancy diagonal matrix, so

    det(K_(-t)-I_vac)=det(U(K_t-I_vac)U)=det(K_t-I_vac).

Thus EVERY complete event has the same probability at t and -t, in the original observation coordinates; this is not a spectral rotation of the observations. Hence h(-t)=h(t), and RESULT.md also gives

    h_tt(t)<-1/3000 whenever 1/2<=|t|<=3/2.                (7)

No statement about the intervening gap |t|<1/2 is inferred from (7).

## 4. Strong Jensen margin on each connected component

If t0,t1 belong to the same one of [1/2,3/2] and [-3/2,-1/2], and 0<=alpha<=1, integration of (7) gives

    h((1-alpha)t0+alpha t1)
      >=(1-alpha)h(t0)+alpha h(t1)
          +alpha(1-alpha)(t1-t0)^2/6000.                   (8)

For distinct endpoints and 0<alpha<1 the inequality is strict. This does not compare a chord passing through the unproved gap.

The calculations in (2)-(4) are new tiny exact-rational geometric sums, not another finite-window or node computation. All new claims here remain author results pending independent review.
