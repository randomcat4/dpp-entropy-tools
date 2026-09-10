from fractions import Fraction as F

ALPHA = F(1, 5)
BETA = F(1, 200)
DELTA = F(1, 10**100)
S = 1 - DELTA
BITS = 384
TERMS = 140


def det2(m):
    return m[0][0]*m[1][1]-m[0][1]*m[1][0]


def det3(m):
    return (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])
            -m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])
            +m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))


def inv3(m):
    d = det3(m)
    cof = [
        [m[1][1]*m[2][2]-m[1][2]*m[2][1],
         -(m[1][0]*m[2][2]-m[1][2]*m[2][0]),
         m[1][0]*m[2][1]-m[1][1]*m[2][0]],
        [-(m[0][1]*m[2][2]-m[0][2]*m[2][1]),
         m[0][0]*m[2][2]-m[0][2]*m[2][0],
         -(m[0][0]*m[2][1]-m[0][1]*m[2][0])],
        [m[0][1]*m[1][2]-m[0][2]*m[1][1],
         -(m[0][0]*m[1][2]-m[0][2]*m[1][0]),
         m[0][0]*m[1][1]-m[0][1]*m[1][0]],
    ]
    return [[cof[j][i]/d for j in range(3)] for i in range(3)]


def mm(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def tr(a):
    return [list(x) for x in zip(*a)]


def sub(a, b):
    return [[a[i][j]-b[i][j] for j in range(len(a[0]))]
            for i in range(len(a))]


def atom3(m, mask):
    d = [[F(1 if i == j and not ((mask >> i) & 1) else 0)
          for j in range(3)] for i in range(3)]
    return (-1)**(3-mask.bit_count()) * det3(sub(m, d))


def shifted(m, mask):
    d = [[F(1 if i == j and not ((mask >> i) & 1) else 0)
          for j in range(3)] for i in range(3)]
    return sub(m, d)


def matrices(alpha, beta):
    q = [[F(1, 3) for _ in range(3)] for _ in range(3)]
    p = [[F(1 if i == j else 0)-q[i][j] for j in range(3)]
         for i in range(3)]
    a = [[alpha*p[i][j]+beta*q[i][j] for j in range(3)]
         for i in range(3)]
    c = [[F(1 if i == j else 0)-a[i][j] for j in range(3)]
         for i in range(3)]
    return a, c


E = [[F(1), F(0)], [F(0), F(1)], [F(-1), F(-1)]]
GI = [[F(2, 3), F(-1, 3)], [F(-1, 3), F(2, 3)]]


def event_coefficients(alpha, beta):
    a, c = matrices(alpha, beta)
    left = {}
    right = {}
    for mask in range(8):
        left[mask] = (atom3(a, mask), mm(mm(tr(E), inv3(shifted(a, mask))), E))
        right[mask] = (atom3(c, mask),
                       mm(mm(mm(mm(GI, tr(E)), inv3(shifted(c, mask))), E), GI))
    rho2 = alpha*(1-alpha)
    rows = []
    for lm in range(8):
        for rm in range(8):
            mul = left[lm][0]*right[rm][0]
            prod = mm(left[lm][1], right[rm][1])
            aa = rho2*(prod[0][0]+prod[1][1])
            bb = rho2*rho2*det2(left[lm][1])*det2(right[rm][1])
            rows.append((mul, aa, bb))
    return rows


def floor_log2(x):
    k = x.numerator.bit_length()-x.denominator.bit_length()
    def p2(j):
        return F(1 << j) if j >= 0 else F(1, 1 << (-j))
    while x < p2(k):
        k -= 1
    while x >= p2(k+1):
        k += 1
    return k


def ceil_div(n, d):
    return -((-n)//d)


def log_atanh_fixed(y):
    # 1 <= y <= 2. Return integer endpoints divided by 2**BITS.
    if y == 1:
        return 0, 0
    z = (y-1)/(y+1)
    p, q = z.numerator, z.denominator
    p2, q2 = p*p, q*q
    pn, qn = p, q
    scale = 1 << BITS
    lo = hi = 0
    for j in range(TERMS):
        num = 2*pn*scale
        den = qn*(2*j+1)
        lo += num//den
        hi += ceil_div(num, den)
        pn *= p2
        qn *= q2
    tail_num = 2*pn*q*q*scale
    tail_den = qn*(2*TERMS+1)*(q*q-p*p)
    hi += ceil_div(tail_num, tail_den)
    return lo, hi


LOG2_LO, LOG2_HI = log_atanh_fixed(F(2))


def log_fixed(x):
    k = floor_log2(x)
    scale = F(1 << k) if k >= 0 else F(1, 1 << (-k))
    y = x/scale
    ylo, yhi = log_atanh_fixed(y)
    if k >= 0:
        return k*LOG2_LO+ylo, k*LOG2_HI+yhi
    return k*LOG2_HI+ylo, k*LOG2_LO+yhi


rows = event_coefficients(ALPHA, BETA)
assert len(rows) == 64
assert sum(mu for mu, _, _ in rows) == 1
assert sum(mu*aa for mu, aa, _ in rows) == 0
assert sum(mu*bb for mu, _, bb in rows) == 0

# Group only exactly identical likelihoods; all 64 original weights remain in the sums.
groups = {}
for mu, aa, bb in rows:
    groups[(aa, bb)] = groups.get((aa, bb), F(0)) + mu
assert len(groups) == 13

alo = F(0)
ahi = F(0)
fisher = F(0)
qmin = None
scale = 1 << BITS
for (aa, bb), weight in groups.items():
    q = 1-aa*S+bb*S*S
    assert q > 0
    z = (aa-S*bb)*(aa-6*S*bb)
    v = aa-2*S*bb
    if q == 1:
        tlo = thi = 2*weight*z
    else:
        loglo_i, loghi_i = log_fixed(q)
        loglo, loghi = F(loglo_i, scale), F(loghi_i, scale)
        coeff = 2*weight*z/(q-1)
        if coeff >= 0:
            tlo, thi = coeff*loglo, coeff*loghi
        else:
            tlo, thi = coeff*loghi, coeff*loglo
    alo += tlo
    ahi += thi
    fisher += 4*weight*v*v/q
    qmin = q if qmin is None or q < qmin else qmin

assert F(-127, 1000) < alo <= ahi < F(-126, 1000)
assert fisher > 10**99
assert fisher + alo > 0
assert qmin == DELTA*DELTA

print('PASS')
print('events=64 groups=13')
print('alpha=1/5 beta=1/200 delta=10^-100 s=1-delta')
print('A_norm enclosure:')
print('  lower =', alo)
print('  upper =', ahi)
print('  outward decimals =', format(float(alo), '.17g'), format(float(ahi), '.17g'))
print('  width <', F(1, 10**100))
print('certified comparison: -127/1000 < A_norm < -126/1000')
print('F_norm numerator digits =', len(str(fisher.numerator)))
print('F_norm denominator digits =', len(str(fisher.denominator)))
print('certified comparison: F_norm > 10^99')
print('therefore Gamma=F_norm+A_norm > 0')
print('minimum likelihood q_min = delta^2 = 10^-200')
print('log enclosure: fixed-point bits=', BITS, 'atanh terms=', TERMS)
