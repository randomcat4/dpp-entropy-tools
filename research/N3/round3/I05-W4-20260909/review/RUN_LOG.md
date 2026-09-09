# Review run log

Date: 2026-09-09.  Platform recorded by the programs:

```text
Python 3.13.5
SymPy 1.14.0
NumPy 2.3.5
mpmath 1.3.0
Linux-6.18.35-x86_64-with-glibc2.41
```

## 1. Freeze and manifest

```sh
sha256sum I05-W4-20260909_result.zip
# b408d1e8faa8bd99e2df33e03dc00548ff42c4e22ef3e814838049820000c308

cd submission
sha256sum -c MANIFEST.sha256
```

Result: every listed file `OK`.

## 2. Submitted programs, fresh rerun

```sh
cd submission
python3 code/verify_exact.py > /tmp/i05_verify_exact_fresh.txt
python3 code/replay_explorations.py > /tmp/i05_replay_fresh.json
cmp outputs/verify_exact.txt /tmp/i05_verify_exact_fresh.txt
cmp outputs/explorations.json /tmp/i05_replay_fresh.json
```

Both comparisons were byte-identical.  Output hashes:

```text
88bcea90f027587a9e23f5222e71ef22d6bfda029496a67a4f05d8a9d752bcd0  /tmp/i05_verify_exact_fresh.txt
4e10b5f65c348c6e6658fe1202501aa7d493df81d770139450c7840b03882827  /tmp/i05_replay_fresh.json
```

## 3. Independent verifier

The reviewer-owned program does not import submission modules.

```sh
cd review
python3 independent_verify.py \
  --seed 20260909 \
  --random-centers 3000 \
  --output independent_verify_output.json \
  > /tmp/i05_independent_verify_stdout.txt
```

Observed runtime in the review environment:

```text
elapsed=0:19.75
maxrss_kb=131956
```

Final source and output hashes:

```text
02cb42c069fcf8b78cd441c4dcc2880d1dd909f90bc1af4230df7570e484c3b2  independent_verify.py
7f0067e77b25000c209d313430273769c937d92b7afd8a4b1fdd476dc1c7fc9d  independent_verify_output.json
```

The program's `status` field is `PASS`.  It checks symbolic state identities,
exact proof constants, 3,036 complete six-dimensional Hessian matrices, and
four additional 110-digit boundary probes.

## 4. Failed float-only precursor and resolution

Before adding precision control, the same direct Mobius construction reported

```text
min normalized gap = -3.6865570387886781
x=(0.9997675225046964, 0.9999514128199806, 0.9983286741372697)
e=(0.0035340391227428047, 0, 0.173080689635704)
```

At that center, ordinary double precision reconstructed the rare `000` event as

```text
1.831368390270427e-11
```

whereas the stable product-density expression gave

```text
1.8313537435089712e-11.
```

The relative error was about `7.998e-6`, large enough to corrupt a curvature
entry whose theorem weight was about `1.818e-11`.  A separate 100-digit direct
principal-minor/Mobius calculation gave

```text
suspect h13 curvature / theorem weight = 6.18472441530648...
minimum normalized gap = 0.29999999017376038...
```

The final verifier retains determinant/Mobius evaluation but automatically
repeats suspicious centers at 90 digits.  Thus the resolution does not assume
the submitted density formula to decide the sign.

## 5. Interpretation

Program reruns and finite stress tests are execution evidence only.  The
mathematical verdict is based on the separate analytic audit in
`INDEPENDENT_REVIEW.md`; novelty remains unchecked.
