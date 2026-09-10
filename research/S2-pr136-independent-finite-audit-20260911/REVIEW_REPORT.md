# PR136 independent finite-evidence review

Status: **INCOMPLETE**.

The public saved finite package is internally reproducible and passes both the
frozen exact checker and a separately written exact-Fraction audit. The
mandatory independent fresh 128-node production was not run because this host
has no C++ compiler. Therefore this review does not award
`INDEPENDENT_FINITE_PASS` to PR136.

## What passed

The eight certificate files reproduce the exact Git blob identities listed by
PR136. Independent input reconstruction used longer rational Machin/atan and
cosine Taylor tails than the frozen generator. It verifies all 65 cosine
enclosures, both binary64 bounds for log(2), all 128 first-kind Chebyshev node
intervals, their IDs/cells, and the four closed-cell interiors.

Concatenating the four saved parts in numeric part order produces exactly
25,414 bytes and 128 unique IDs `0..127`. Every row has 11 fields,
`leaves=262144=4^9`, ordered curvature endpoints, and normalization Taylor
jets enclosing `1,0,0`. The C++ leaf explicitly loops over four current events,
so the enumerated entropy sum has `4^10=1,048,576` current/future atoms per
node.

The unchanged frozen checker runs successfully on that saved concatenation.
Because Python's `resource` module is unavailable on Windows, the runner
injects only a zero-valued `ru_maxrss` telemetry object. No formula, constant,
input, output, or success predicate is changed.

The independent Fraction implementation reconstructs, rather than copies,

```text
a0 = 342449808326286961/15178486401000000
a1 = 154889893499/5135349375
a2 = 1809918/180625
```

and obtains

```text
E9 = 589387328229019964285617091244680106481903343765504
     /5143466080331011979778316775380842071512247021978203125
   = 0.0001145895236838209... < 115/1000000.
```

It also verifies

```text
M = 318159082659774464/9685512225 < 40000000,
Echeb = 80000000/617673396283947,
```

the DCT-I alias index `degree*(2*j+1) mod 128`, coefficient scalings `1/32`
and `1/16`, and the triangle sup-norm bound. The resulting exact four-cell
upper bounds agree with the full frozen audit; their decimals are

```text
[1/2,3/4]  -0.0003746944028546811...
[3/4,1]    -0.0010306469749631383...
[1,5/4]    -0.0019577212125145367...
[5/4,3/2]  -0.0031712104741915452...
```

Each is strictly below `-1/3000`, and each is below the upward-rounded short
fraction published in `certificate_summary.json`.

## Static outward-kernel audit

The source requires IEEE binary64 and round-to-nearest. With the published
flags, every elementary `+`, `-`, `*`, and reciprocal endpoint is padded by one
adjacent binary64 value; exact power-of-two log scaling does not add rounding.
The `up`/`dn` bit steps have the correct direction for both signs and expand a
rounded zero to both smallest subnormals. Division rejects zero-crossing
denominators.

The logarithm implementation rescales into the declared atanh range, uses 16
odd terms, and adds the independently verified symmetric `2^-68` remainder;
the generated log(2) hex endpoints enclose an independent 100-term rational
atanh sum and tail. The generator's 40-term cosine remainder and outward
binary64 conversion are covered by a separate 60-term exact check.

For Taylor jets, multiplication uses
`a.v*b.h+a.d*b.d+a.h*b.v`, and the inverse second coefficient is correct.
At the leaf, `p.h*b0+p.d*b1+p.v*b2` retains probability-law acceleration and
the cross term. Since `J.h` is the `dt^2` coefficient, conversion to a second
derivative contributes two while entropy per original coordinate contributes
one half; the cancellation in the source is correct.

## Preserved publication failures

The PR commit history explicitly records the node 59 and node 97 added-zero
normalization transcription repairs and the temporary node 48 curvature digit
error. The intermediate node 48 line would reverse its curvature interval and
is rejected by the frozen checker; the final line restores ordered endpoints.
These are publication-text faults, not evidence that the first uploads passed.

The disclosed `ndef p_scale` failure is necessarily a parse-time SyntaxError
before arithmetic. The invalid historical checker file and original terminal
log are not among the eight public blobs, so this review can classify its
mathematical effect as nil on the frozen successful source but cannot
independently authenticate that private historical log. Likewise, the final
public blob binding is exact, while the author's asserted byte comparison to
unpublished original local files cannot be independently repeated here.

## Blocking gap

The authorized success gate required compiling the frozen source with

```text
g++ -O3 -std=c++17 -ffp-contract=off -fno-fast-math -fopenmp
```

and producing a new 128-node output. This host has no `g++`, `clang++`, `c++`,
or MSVC compiler on the command surface. Installing one was explicitly
forbidden. No new output exists, so there is no fresh-result checker run and no
saved-versus-fresh enclosure comparison. This exact gap prevents finite PASS.

