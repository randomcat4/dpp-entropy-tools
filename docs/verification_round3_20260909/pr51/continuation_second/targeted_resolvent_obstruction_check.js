// Independent tiny exact-rational check for PR51 continuation.md §6.1.
//
// Public-ready preservation of the checker actually executed during the
// pr51_continuation_second review. This script reconstructs the two-bit
// marginals and the p_ij1 atoms from inclusion-exclusion, then evaluates
// Phi'' for the displayed auxiliary conditional-resolvent obstruction.
//
// It intentionally does not import author code, private Drive artifacts, or
// the issue #52 multivariate M input.

class Q {
  constructor(n, d = 1n) {
    if (d === 0n) throw new Error("zero denominator");
    if (d < 0n) {
      n = -n;
      d = -d;
    }
    const g = Q.gcd(n < 0n ? -n : n, d);
    this.n = n / g;
    this.d = d / g;
  }

  static gcd(a, b) {
    while (b) {
      const t = a % b;
      a = b;
      b = t;
    }
    return a || 1n;
  }

  static of(o) {
    return o instanceof Q ? o : new Q(BigInt(o), 1n);
  }

  add(o) {
    o = Q.of(o);
    return new Q(this.n * o.d + o.n * this.d, this.d * o.d);
  }

  sub(o) {
    o = Q.of(o);
    return new Q(this.n * o.d - o.n * this.d, this.d * o.d);
  }

  mul(o) {
    o = Q.of(o);
    return new Q(this.n * o.n, this.d * o.d);
  }

  div(o) {
    o = Q.of(o);
    return new Q(this.n * o.d, this.d * o.n);
  }

  neg() {
    return new Q(-this.n, this.d);
  }

  cmp(o) {
    o = Q.of(o);
    const v = this.n * o.d - o.n * this.d;
    return v < 0n ? -1 : v > 0n ? 1 : 0;
  }

  toString() {
    return this.d === 1n ? `${this.n}` : `${this.n}/${this.d}`;
  }
}

const q = (n, d = 1n) => new Q(BigInt(n), BigInt(d));
const zero = q(0);
const one = q(1);

function p(c0, c1 = zero, c2 = zero) {
  return [Q.of(c0), Q.of(c1), Q.of(c2)];
}

function padd(a, b) {
  return [a[0].add(b[0]), a[1].add(b[1]), a[2].add(b[2])];
}

function psub(a, b) {
  return [a[0].sub(b[0]), a[1].sub(b[1]), a[2].sub(b[2])];
}

function pmul(a, b) {
  return [
    a[0].mul(b[0]),
    a[0].mul(b[1]).add(a[1].mul(b[0])),
    a[0].mul(b[2]).add(a[1].mul(b[1])).add(a[2].mul(b[0])),
  ];
}

function pscale(a, s) {
  s = Q.of(s);
  return [a[0].mul(s), a[1].mul(s), a[2].mul(s)];
}

function psq(a) {
  return pmul(a, a);
}

function det3(x, a, b, y, c, z) {
  return padd(
    padd(pmul(pmul(x, y), z), pscale(pmul(pmul(a, b), c), q(2))),
    padd(
      padd(pscale(pmul(x, psq(c)), q(-1)), pscale(pmul(y, psq(b)), q(-1))),
      pscale(pmul(z, psq(a)), q(-1)),
    ),
  );
}

function secondP2OverR(P, R) {
  const P0 = P[0];
  const P1 = P[1];
  const P2 = P[2].mul(2);
  const R0 = R[0];
  const R1 = R[1];
  const R2 = R[2].mul(2);
  const shifted = P1.sub(P0.mul(R1).div(R0));
  const term1 = q(2).mul(shifted).mul(shifted).div(R0);
  const term2 = q(2).mul(P0).mul(P2).div(R0);
  const term3 = P0.mul(P0).mul(R2).div(R0.mul(R0)).neg();
  return term1.add(term2).add(term3);
}

const x = p(q(23, 25));
const a = p(q(0), q(-1));
const b = p(q(1, 5), q(-4, 5));
const y = p(q(2, 5), q(1, 3));
const c = p(q(8, 25), q(1, 20));
const z = p(q(3, 10), q(-2, 15));

const q12 = psub(pmul(x, y), psq(a));
const q13 = psub(pmul(x, z), psq(b));
const q23 = psub(pmul(y, z), psq(c));
const q123 = det3(x, a, b, y, c, z);

const P00 = padd(psub(psub(p(one), x), y), q12);
const P10 = psub(x, q12);
const P01 = psub(y, q12);
const P11 = q12;

const R00 = padd(psub(psub(z, q13), q23), q123);
const R10 = psub(q13, q123);
const R01 = psub(q23, q123);
const R11 = q123;

const terms = [
  [P00, R00],
  [P10, R10],
  [P01, R01],
  [P11, R11],
].map(([P, R]) => secondP2OverR(P, R));

const phiSecond = terms.reduce((acc, t) => acc.add(t), zero);
const qK = q(3, 10).sub(q(1, 25).div(q(23, 25))).sub(q(64, 625).div(q(2, 5)));
const qIminusK = q(7, 10).sub(q(1, 25).div(q(2, 25))).sub(q(64, 625).div(q(3, 5)));
const expected = new Q(-53670727895896612562246875n, 14117659525214393686902n);

console.log("Phi_second", phiSecond.toString());
console.log("Phi_second_float", Number(phiSecond.n) / Number(phiSecond.d));
console.log("Phi_negative", phiSecond.cmp(zero) < 0);
console.log("K_schur_q", qK.toString(), "positive", qK.cmp(zero) > 0);
console.log("IminusK_schur", qIminusK.toString(), "positive", qIminusK.cmp(zero) > 0);
console.log("matches_expected", phiSecond.cmp(expected) === 0);
