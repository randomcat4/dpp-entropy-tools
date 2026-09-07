"""Local probability/derivative/stratum checks; no SciPy dependency."""
import json
from pathlib import Path
import platform
import numerics as nu
import numpy as np

def main():
    root=Path(__file__).resolve().parent
    rng=np.random.default_rng(20260908201)
    tests=[]
    calls=0
    for n in range(1,11):
        q,_=np.linalg.qr(rng.normal(size=(n,n)))
        k=(q*rng.uniform(.15,.85,size=n))@q.T
        h,diagnostics=nu.hessian(k);calls+=1
        coeff=rng.normal(size=len(h));coeff/=np.linalg.norm(coeff)
        v=np.einsum("a,aij->ij",coeff,nu.layout(n)[3])
        analytic=float(coeff@h@coeff)
        alternate=nu.signed_directional(k,v)
        p,p1,p2=(nu.mobius(z,n) for z in nu.inclusion_derivatives(k))
        cp,cp1,cp2=(nu.mobius(z,n) for z in nu.inclusion_derivatives(np.eye(n)-k))
        gradient=-(1+np.log(p))@p1
        cgradient=-(1+np.log(cp))@cp1
        gradient_flip_error=float(np.max(abs(gradient+cgradient)))
        assert np.max(abs(p-cp[::-1]))<2e-12
        assert np.max(abs(p1+cp1[::-1]))<2e-11
        assert np.max(abs(p2-cp2[::-1]))<2e-10
        assert gradient_flip_error<2e-9
        assert abs(nu.entropy(k)-nu.entropy(np.eye(n)-k))<2e-11
        steps=(1e-3,3e-4,1e-4)
        fd=[(nu.entropy(k+t*v)-2*nu.entropy(k)+nu.entropy(k-t*v))/t**2 for t in steps]
        assert abs(analytic-alternate)<2e-9,(n,analytic,alternate)
        assert min(abs(z-analytic) for z in fd)<3e-5,(n,analytic,fd)
        tests.append(dict(n=n,analytic=analytic,alternate=alternate,finite_difference=fd,steps=steps,
                          gradient_flip_error=gradient_flip_error,**diagnostics))
    strata=[]
    for n in (3,5,8,10):
        for band in range(4):
            for complement in (0,1):
                x=nu.initial_x(20260908201,n,band,complement,0)
                value,k,v,diag=nu.evaluate(x,n,band,complement);calls+=1
                alt=nu.signed_directional(k,v)
                assert abs(alt-value)<2e-7,(n,band,value,alt)
                chords=nu.chord(k,v)
                strata.append(dict(n=n,band=band,complement=complement,alternate=alt,chords=chords,**diag))
    # Full diagonal Hessian, including every mixed coordinate.
    k=np.diag([.2,.45,.7])
    h,_=nu.hessian(k);calls+=1
    expected=np.zeros_like(h)
    for a,e in enumerate(nu.layout(3)[3]):
        if np.count_nonzero(e)==1:
            j=np.flatnonzero(e.diagonal())[0]
            expected[a,a]=-1/(k[j,j]*(1-k[j,j]))
    assert np.max(abs(h-expected))<1e-12
    report=dict(status="PASS",seed=20260908201,primary_hessian_calls=calls,
                python=platform.python_version(),numpy=np.__version__,threads=1,
                directional_tests=tests,stratum_tests=strata,diagonal_hessian_error=float(np.max(abs(h-expected))))
    (root/"selftest_result.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(dict(status="PASS",primary_hessian_calls=calls,
        max_alternate_error=max(abs(r["analytic"]-r["alternate"]) for r in tests),stratum_cases=len(strata))),flush=True)

if __name__=="__main__":
    main()
