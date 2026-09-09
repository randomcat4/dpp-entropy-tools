# F2 scope, frozen before execution

This unit implements the principal investigator's frozen theorem v2 only
after the independent rational check of the proposed five-point frame.

There are 24 centers: three fixed rational 5x3 isometries times eight declared
nonisotropic spectra. Let a=(1,2,3,4,5); use U=H(a)H(b)[:,0:3] with
b=(2,-1,3,-2,1), (2,-1,4,-2,1), (3,-1,3,-2,1). Every triple minor is checked
exactly nonzero, and the triple weights sum exactly to one. A change of b
starts a new fixed face; it never enters a tested chord.

The spectra are moderate (1/8,1/2,7/8), sparse (1/10000,1/500,1/20),
dense (19/20,499/500,9999/10000), one-zero (1/10000,1/3,4/5),
two-zero (1/10000,1/1000,3/4), one-one (1/5,2/3,9999/10000),
split-extreme (1/10000,1/2,9999/10000), and clustered (49/100,1/2,51/100).
Each is conjugated by two rational Householder rotations selected with seed
202609090529. No scalar-center thinning control is used.

At every center, compute the full six-dimensional Hessian from the 26
events of cardinality at most three; the other six events and jets are
structural zero and are never divided by. At 60 digits, retain all event
jets, Fisher, acceleration and Hessian matrices. Freeze two rationalized
directions: maximal full-Hessian eigenvector and maximal acceleration
eigenvector. Each is tested at three fixed-U A-affine rational steps.

For each direction save the exact determinant jets d,d',d'', c=H(q),
geometry c*d'', top Fisher (d')^2/d, base acceleration -d''log(d),
the resulting top-layer total and the three separate lower-cardinality
contributions. This decomposition is checked against the direct 26-event
computation rather than used as its implementation.

Positive curvature or finite gap must be frozen immediately and sent for
independent checking. Non-hits require diagnosis of whether geometry is
negative, top-layer Fisher covers it, or lower layers provide compensation.
No further sample expansion follows automatically.
