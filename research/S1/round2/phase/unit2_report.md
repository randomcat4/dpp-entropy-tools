# Round 2 phase unit 2: spectral-factor boundary geometry

Status: **INCOMPLETE** for the frozen entropy-rate problem. Six exact spectral-factor centers were frozen, then 12 full finite Hessians were executed. No positive eigenvalue was found numerically. This unit is substantively different from the first: every center fails the former coefficient l1 margin, and four symbols actually attain their prescribed small lower bound. No family theorem or rate sign is inferred.

## Exact objects and their geometry

For z=exp(2*pi*i*x), define

    f(x)=epsilon+(1-2epsilon)|P(z)|^2/L^2.

The centers were committed before execution in `84588292ab2ab374fd058b9adf9801b6b0fed29e`. With P coefficients in increasing order:

|ID|P coefficients|epsilon|L|unit-circle geometry|
|---|---|---:|---:|---|
|S3_control|(4,1,i,1)|1/100|7|constant 4 dominates remaining modulus sum 3|
|S3_root1|(1,-1+i,2-i,-2)|1/1000|27/4|(1-z)(1+i*z+2*z^2)|
|S3_root2|(1,-1+2i,1-i,-1-i)|1/100|25/4|(1-z)(1+2i*z+(1+i)z^2)|
|S4_control|(5,1,i,1,i)|1/100|9|constant 5 dominates remaining modulus sum 4|
|S4_root1|(1,-1+i,1-i,0,-1)|1/1000|5|(1-z)(1+i*z+z^2+z^3)|
|S4_root2|(1,i,-1-i,1+i,-1-i)|1/100|13/2|(1-z)(1+(1+i)z+(1+i)z^3)|

The radius lists bounding the coefficient moduli are respectively

    (4,1,1,1), (1,3/2,9/4,2), (1,9/4,3/2,3/2),
    (5,1,1,1,1), (1,3/2,3/2,0,1), (1,1,3/2,3/2,3/2).

Each listed rational radius has square at least the squared Gaussian integer modulus, and the radii sum to L. Thus |P|<=L on the unit circle, proving **epsilon<=f<=1-epsilon**. All four root factors have P(1)=0 and so attain exactly f(0)=epsilon. The two controls have |P|>=1 by the reverse triangle inequality and no unit-circle roots; their proved symbol lower bounds are 3/100 and 179/8100 respectively. The common two-sided margins epsilon remain valid for every center and are not claimed optimal for the controls.

Writing f=p+sum(a_k cos(2*pi*k*x)+b_k sin(2*pi*k*x)), the exact coefficients are:

```text
S3_control:
  p=39/100
  a=(4/25,1/25,4/25)
  b=(0,-4/25,0)
S3_root1:
  p=12823/48600
  a=(-31936/91125,15968/91125,-7984/91125)
  b=(7984/91125,-3992/91125,0)
S3_root2:
  p=3261/12500
  a=(-3136/15625,0,-784/15625)
  b=(784/15625,-1568/15625,784/15625)
S4_control:
  p=2923/8100
  a=(49/405,98/2025,49/405,0)
  b=(-49/2025,-49/405,-49/2025,-49/405)
S4_root1:
  p=6013/25000
  a=(-1497/6250,0,499/6250,-499/6250)
  b=(-499/6250,499/3125,-499/6250,0)
S4_root2:
  p=661/3380
  a=(-196/845,392/4225,0,-196/4225)
  b=(-392/4225,392/4225,-392/4225,196/4225)
```

These follow by the exact Gaussian-integer autocorrelation r_k=sum_j P_(j+k) conjugate(P_j). With s=(1-2epsilon)/L^2, one has p=epsilon+s*r_0, a_k=2s Re(r_k), b_k=-2s Im(r_k). Both this calculation and all modulus inequalities were checked with rational arithmetic by the invoked script. That exact arithmetic does not certify the subsequent floating Hessian signs.

The unscaled cycle invariants r_1^2 conjugate(r_2) are, in the same order,

    16-64i, 272+68i, 16-30i, 98-100i, 12+16i, 82+2i.

The actual invariants are these numbers times s^3>0. Their nonzero imaginary parts exclude any translation or diagonal gauge making the center real. Within each degree all means differ, so these centers are not translation/conjugation repetitions. They also differ in mean from the previous unit's centers of the same degree. Degree is fixed and the top harmonic is nonzero.

The old bound min(p,1-p)-sum(|a_k|+|b_k|) equals, respectively,

    -13/100, -350567/729000, -11919/62500,
    -1781/8100, -11951/25000, -1691/3380.

All are negative. These centers were therefore genuinely outside the previous triangle-constrained coefficient ball; they were not rejected on that inappropriate test. Their feasibility comes from spectral factorization.

## Safe general affine directions

For any rational direction d=(d_p,d_a,d_b), set S=|d_p|+sum(|d_a|+|d_b|). If S>0, choose any rational 0<tau<=epsilon/(2S). Then for every |t|<=tau,

    epsilon/2 <= f_0+t*g <= 1-epsilon/2.

For S=0 the chord is constant. This is a uniform scalar-symbol bound covering all windows. It uses the spectral margin epsilon, not the negative old triangle margin. A floating Euclidean-unit eigenvector in dimension d=2m+1 has l1 norm at most sqrt(d); the conservative bound tau=epsilon/(2d) is safe for an exact vector with coordinate magnitudes at most 1. Any rationalization used for a later candidate must recompute its actual S. No such finite candidate was promoted here.

The directions span the full 7- or 9-dimensional coefficient space. Centers need not have a real first Fourier coefficient; the same universal translation tangent and second-derivative identity from `unit1_report.md` still apply.

## Full Hessian findings

All 12 n=6,8 Hessians were negative numerically. At n=8:

|Center|top Q|F on top Q|A on top Q|top A|F on top A|
|---|---:|---:|---:|---:|---:|
|S3_control|-0.324047412|0.0105448917|-0.313502520|4.65946147|38.4548391|
|S3_root1|-0.511494931|0.139263927|-0.372231004|21.5194803|73.5768625|
|S3_root2|-0.138545300|0.0279301771|-0.110615123|5.85003977|48.1482035|
|S4_control|-0.156026758|0.00859682864|-0.147429930|3.49829293|38.2652627|
|S4_root1|-0.165089067|0.0271129070|-0.137976160|12.8437409|59.7926405|
|S4_root2|-0.168207603|0.0367911986|-0.131416404|15.0902804|72.7667128|

Both full F and A matrices, their spectra, gradients, eigenvectors and gauge diagnostics are retained in `spectral_results.json`. The root geometry can make positive acceleration substantially larger (e.g. 21.51948), but Fisher cost on that direction is still larger (73.57686). The best full-Hessian directions all have negative acceleration already. Thus the two mechanisms of failure remain distinct, as in the first unit.

The mixed cosine-sine block maximum ranged from 0.110004 to 2.515405 across the 12 evaluations, confirming that the old even-center restriction is not still suppressing every mixed term. The maximum residuals were: probability mass 8.88178e-16, first mass derivative 1.14492e-15, second mass derivative 7.50458e-15, imaginary part 2.55481e-14, and the translation second-derivative identity 2.63678e-16. These are consistency observations, not numerical error certification.

## Stop and scope

This child has now evaluated **18 distinct predeclared centers and 36 full Hessians** in round 2, with 5760 event determinant/inverse evaluations. The main instance's separate B1 has **1 center and 2 Hessians** and is not included in these files or the child's denominator. Combined, these give 19 centers and 38 Hessians only if the main B1 execution is separately confirmed. No n=10 run, unreported adaptive center or additional endpoint entropy computation occurred here.

Two substantively different center constructions return to the same missing mechanism: positive acceleration directions have excessive Fisher cost, while observed low-cost directions have negative acceleration. No coupling inequality explaining this over a family was obtained, and no concrete direction defeats it. Consequently the task stops at **STOPPED_SUBSTANTIVE / INCOMPLETE** without larger windows or further centers. A finite point check cannot establish an all-symbol theorem; no rate limit sign, uniform curvature inequality or novelty claim follows. All three-symbol rate obligations remain with the main route and are not replaced by these Hessians.
