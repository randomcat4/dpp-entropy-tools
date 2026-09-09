# Frozen statement v1 — B0

Proof agents must not modify, add or reinterpret assumptions.

Let K=[[x,a,b],[a,y,c],[b,c,z]] be any real symmetric matrix with 0<K<I whose graph of nonzero off-diagonal entries is connected. The six coordinates and bases are (x,y,z,a,b,c) and (E11,E22,E33,E12+E21,E13+E31,E23+E32). All directions are real symmetric and paths are affine in K. Logs are natural.

For each S subset of {1,2,3}, pS=sum(T superset S)(-1)^(|T|-|S|) det K_T; pS>0. Define Fij=sum_S dpS[Ei]dpS[Ej]/pS. Write ell12=log(p0 p12/(p1 p2)), with cyclic counterparts, Lambda=log(p123 p1 p2 p3/(p0 p12 p13 p23)), and N=-diag(ell23,ell13,ell12)-Lambda K. The required connected-domain positivity N>0 is to be rebuilt, or explicitly treated as an external premise where used. Put d=det N, eta_i=tr(N^-1 Ei), Gij=tr(N^-1 Ei N^-1 Ej), Z=sum_S 1/pS, g=grad Lambda, v=g/sqrt Z, Fpair=F-vv^T, M=Fpair+dG. Reconstruct Fpair=J^T Cov(X1,X2,X3,X1X2,X1X3,X2X3)^-1 J, M>0, and B=-Hess H=F+dG-d eta eta^T before relying on them.

Set alpha=eta^T M^-1 eta and beta=v^T M^-1 eta. The target is:

    for every such K, beta(K)=0 implies d(K) alpha(K)<=1.

The actual optimizer is D_M with coordinate vector M^-1 eta/alpha. An arbitrary direction with Lambda'[D]=0 is not an admissible substitute. Approximate beta zeros cannot discard the rank-one correction in the full Hessian. Zero edges are allowed under graph connectivity; no division by a,b,c is licensed on those strata. Realizability is inherited from the six entries, with T=2abc and T^2=4a^2b^2c^2 and their full affine jets.

Success means a universal proof, or a certified exact beta-zero violation together with its strict K-affine entropy chord. Partial subdomain statements must list additional assumptions and remaining parameters. Finite probes, numeric near-zeros, and equivalent reformulations are not a solution. This statement makes no claim about n>=4, the stationary entropy-rate problem, or novelty.
