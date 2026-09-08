"""80-digit eventwise diagnosis of one frozen S3 gain maximizer; no search."""
import os,json,hashlib,time
from pathlib import Path
import mpmath as mp
mp.mp.dps=80
root=Path(__file__).parent;rec=json.loads((root/'batch3'/'best_gain.json').read_text());start=time.time()
K=mp.matrix([[mp.mpf(float(x)) for x in row] for row in rec['K']]);basis=[]
for i,j in ((0,2),(1,2),(0,3),(1,3)):
    E=mp.matrix(4);E[i,j]=E[j,i]=1;basis.append(E)
def tr(M):return sum(M[i,i] for i in range(M.rows))
def arr(M):return [[str(M[i,j]) for j in range(M.cols)] for i in range(M.rows)]
def eig(M):return [str(x) for x in mp.eigsy(M,eigvals_only=True)]
def block_report(M):return {'matrix':arr(M),'spectrum':eig(M),'block33':arr(M[:2,:2]),'block33_spectrum':eig(M[:2,:2]),'block44':arr(M[2:,2:]),'block44_spectrum':eig(M[2:,2:]),'cross_block':arr(M[:2,2:])}
events=[];F=mp.matrix(4);A=mp.matrix(4)
for s in range(16):
    M=K.copy()
    for i in range(4):M[i,i]-=1-((s>>i)&1)
    p=(-1)**(4-s.bit_count())*mp.det(M);X=[M**-1*E for E in basis];g=mp.matrix([p*tr(Y) for Y in X]);Fi=g*g.T/p;Ai=mp.matrix(4)
    for i in range(4):
        for j in range(4):Ai[i,j]=-mp.log(p)*(g[i]*g[j]/p-p*tr(X[i]*X[j]))
    F+=Fi;A+=Ai;events.append({'S':s,'sites':[i for i in range(4) if (s>>i)&1],'p':p,'gradient':g,'fisher_positive':Fi,'acceleration':Ai})
B=F-A
most_rare=min(events,key=lambda e:e['p']);strongest=max(events,key=lambda e:tr(e['fisher_positive']))
e3,Q3=mp.eigsy(B[:2,:2]);e4,Q4=mp.eigsy(B[2:,2:]);q3=Q3[:,1];q4=Q4[:,1]
Fs=most_rare['fisher_positive'];As=most_rare['acceleration']
fraction3=(q3.T*Fs[:2,:2]*q3)[0]/e3[1];fraction4=(q4.T*Fs[2:,2:]*q4)[0]/e4[1]
payload=[]
for e in events:
    payload.append({'S':e['S'],'sites':e['sites'],'p':str(e['p']),'gradient_actual_entries':[str(x) for x in e['gradient']],'negative_fisher_Hessian_contribution':arr(-e['fisher_positive']),'acceleration_Hessian_contribution':arr(e['acceleration']),'fisher_positive_trace':str(tr(e['fisher_positive']))})
report={'status':'AUTHOR_MECHANISM_DIAGNOSTIC_NOT_CERTIFICATE','pid':os.getpid(),'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'frozen_best_sha256':hashlib.sha256((root/'batch3'/'best_gain.json').read_bytes()).hexdigest(),'index':rec['index'],'precision':80,'mpmath':mp.__version__,'event_evaluations':16,'restricted_Hessian_calls':1,'rare_event_S':most_rare['S'],'largest_Fisher_trace_event_S':strongest['S'],'rare_event_probability':str(most_rare['p']),'total_Fisher_trace':str(tr(F)),'rare_event_Fisher_trace':str(tr(Fs)),'stiff_block33_mode_Fisher_fraction':str(fraction3),'stiff_block44_mode_Fisher_fraction':str(fraction4),'negative_Hessian':block_report(B),'remaining_negative_Hessian_after_removing_rare_Fisher_only':block_report(B-Fs),'remaining_negative_Hessian_after_removing_entire_rare_event':block_report(B-Fs+As),'events':payload,'elapsed_seconds':time.time()-start,'exit_code':0}
(root/'batch3'/'best_event_diagnostic.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k not in ('events','negative_Hessian','remaining_negative_Hessian_after_removing_rare_Fisher_only','remaining_negative_Hessian_after_removing_entire_rare_event')}),flush=True)
