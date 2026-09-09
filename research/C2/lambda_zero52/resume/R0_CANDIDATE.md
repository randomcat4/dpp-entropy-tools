# r=0 sign certificate candidate

STATUS: CANDIDATE, awaiting fresh nonauthor review. This is only the entire
r=0 subfamily, not the full four-parameter assertion.

Let P be the residual numerator factor in
`outputs/r0/report.json`, fourth principal determinant. Exact elimination of
the saved Rstar gives

```text
det Rstar = (1-mu^2)^2 (1-nu^2)^2 P(mu,nu,u) / (2 J^5),
J=1-u^4.
```

The factors outside P are strictly positive for |mu|,|nu|<1 and 0<u<1.
P has separate degrees (4,4,16). Put

```text
mu=(X-1)/(X+1), nu=(Y-1)/(Y+1), u=U/(1+U).
Q=(1+X)^4(1+Y)^4(1+U)^16 P(mu,nu,u).
```

This substitution bijects the domain with X,Y,U>0 and has a strictly positive
clearing multiplier. `coefficient_outputs/r0_coefficient_table.json` records
the exact nonzero coefficients of Q: 389 positive integer entries, minimum
192, maximum 99220032, with no negative nonzero entry. The checker applies the
binomial expansions one variable at a time using integer arithmetic. Hence,
subject to independent checking of the recorded identities and table, Q>0 and
P>0 throughout the open r=0 domain.

The determinant would therefore never vanish. That domain is connected, the
matrix is symmetric and continuous, and the independently reviewed positive
seed (mu,nu,u)=(0,0,1/2) lies inside it. Inertia continuation would give
Rstar>0 throughout this three-parameter domain; the reviewed Schur reduction
would then give M>0 for r=0 and all six fixed direction coordinates.

The full-r attempt has 6415 positive and 146 negative nonzero transformed
coefficients. It is not a certificate, and mixed coefficients do not show a
negative value. No full-r sign or entropy counterexample is claimed.
