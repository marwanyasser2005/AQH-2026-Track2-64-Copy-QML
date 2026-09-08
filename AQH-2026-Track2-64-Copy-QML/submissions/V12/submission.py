from pathlib import Path
import json, numpy as np
import pennylane as qml
HERE=Path(__file__).resolve().parent
MODEL=json.loads((HERE/'model_config.json').read_text(encoding='utf-8'))
ARCH=MODEL['architecture']; PARAMS=np.asarray(MODEL['params'],float); BUDGETS=[4,8,16,32,64]

def pair_starts(n,parity):
    s=list(range(int(parity),int(n)-1,2))
    if int(n)%2==0 and int(parity)==1: s.append(int(n)-1)
    return s

def m2_ops(parity):
    p=PARAMS
    def ops(wires):
        n=len(wires)
        for a in pair_starts(n,parity):
            b=(a+1)%n; qml.RY(float(p[0]),wires=a); qml.RY(float(p[1]),wires=b); qml.CNOT(wires=[a,b]); qml.RZ(float(p[2]),wires=b)
        for a in pair_starts(n,1-int(parity)):
            b=(a+1)%n; qml.RY(float(p[3]),wires=a); qml.CNOT(wires=[b,a]); qml.RX(float(p[4]),wires=b); qml.RZ(float(p[5]),wires=a)
    return ops

def qrnn_ops(parity):
    theta=float(PARAMS[0])
    def cell(a,b): qml.RY(theta,wires=a); qml.CNOT(wires=[a,b]); qml.CNOT(wires=[b,a])
    def ops(wires):
        n=len(wires)
        if int(parity)==0:
            for a in range(n-1): cell(a,a+1)
        else:
            for a in range(n-1,0,-1): cell(a,a-1)
    return ops

def ttn_block(a,b,p):
    qml.RY(float(p[0]),wires=a); qml.RY(float(p[1]),wires=b); qml.IsingXX(float(p[2]),wires=[a,b]); qml.IsingZZ(float(p[3]),wires=[a,b]); qml.CNOT(wires=[a,b]); qml.RY(float(p[4]),wires=b); qml.RZ(float(p[5]),wires=b)

def ttn_ops(parity):
    p=PARAMS
    def ops(wires):
        active=list(wires)
        if int(parity)==1: active=active[1:]+active[:1]
        while len(active)>1:
            nxt=[]; i=0
            while i+1<len(active):
                a,b=active[i],active[i+1]; ttn_block(a,b,p); nxt.append(b); i+=2
            if i<len(active): nxt.append(active[i])
            active=nxt
    return ops

def mera_dis(a,b,p): qml.IsingXX(float(p[0]),wires=[a,b]); qml.IsingYY(float(p[1]),wires=[a,b]); qml.RZ(float(p[2]),wires=a); qml.RZ(float(p[3]),wires=b)
def mera_pool(a,b,p): qml.CNOT(wires=[a,b]); qml.RY(float(p[4]),wires=b); qml.IsingZZ(float(p[5]),wires=[a,b]); qml.RX(float(p[6]),wires=a); qml.RZ(float(p[7]),wires=b)
def mera_ops(parity):
    p=PARAMS
    def ops(wires):
        active=list(wires)
        if int(parity)==1: active=active[1:]+active[:1]
        while len(active)>1:
            for i in range(1,len(active)-1,2): mera_dis(active[i],active[i+1],p)
            nxt=[]; i=0
            while i+1<len(active):
                a,b=active[i],active[i+1]; mera_pool(a,b,p); nxt.append(b); i+=2
            if i<len(active): nxt.append(active[i])
            active=nxt
    return ops

def ops_builder(parity):
    if ARCH=='M2_QCNN_LOCAL_6P': return m2_ops(parity)
    if ARCH=='QRNN_MINIMAL_1P': return qrnn_ops(parity)
    if ARCH=='SHARED_TTN_6P': return ttn_ops(parity)
    if ARCH=='SHARED_MERA_8P': return mera_ops(parity)
    raise ValueError(ARCH)

def shot_feature(bits,parity):
    bits=np.asarray(bits,int).reshape(-1); n=len(bits); z=1.-2.*bits; c=[];t=[];pr=[]
    for a in pair_starts(n,parity):
        b=(a+1)%n; c.append(z[a]); t.append(z[b]); pr.append(z[a]*z[b])
    return np.asarray([np.mean(c) if c else 0.,np.mean(t) if t else 0.,np.mean(pr) if pr else 0.,np.mean(z),np.mean(((-1.)**np.arange(n))*z),np.mean(z*np.roll(z,-1))],float)

def aggregate(shots):
    d={0:[],1:[]}
    for p,b in shots: d[int(p)].append(shot_feature(b,int(p)))
    return np.concatenate([np.mean(d[p],axis=0) if d[p] else np.zeros(6) for p in [0,1]])

def linear_predict(x,cfg):
    mean=np.asarray(cfg['scaler_mean'],float); scale=np.asarray(cfg['scaler_scale'],float); scale=np.where(np.abs(scale)<1e-12,1.,scale); z=(np.asarray(x,float)-mean)/scale
    coef=np.asarray(cfg['coef'],float); inter=np.asarray(cfg['intercept'],float); classes=np.asarray(cfg['classes'],str); return str(classes[int(np.argmax(coef@z+inter))])

def compatible(x,cfg):
    d=np.asarray(x,float)-np.asarray(cfg['mu'],float); return bool(float(d@np.asarray(cfg['inv'],float)@d)<=float(cfg['threshold']))

def choose_budget(n):
    valid=[b for b in BUDGETS if b<=int(n)]; return max(valid) if valid else max(0,int(n))

def classify(oracle,state_ids):
    out={}
    for sid in state_ids:
        sid=str(sid); available=int(getattr(oracle,'copy_budget',64))
        if hasattr(oracle,'remaining'): available=min(available,int(oracle.remaining(sid)))
        target=choose_budget(available); shots=[]
        for shot_id in range(target):
            if hasattr(oracle,'remaining') and oracle.remaining(sid)<=0: break
            parity=shot_id%2
            try: bits=oracle.measure(sid,ops_fn=ops_builder(parity))
            except Exception as exc:
                if exc.__class__.__name__=='CopyBudgetExceeded': break
                raise
            shots.append((parity,np.asarray(bits,np.int8)))
        if not shots: out[sid]='UNKNOWN'; continue
        feat=aggregate(shots); b=choose_budget(len(shots)); trained=sorted(int(k) for k in MODEL['budgets']); use=b if str(b) in MODEL['budgets'] else min(trained,key=lambda x:abs(x-b)); cfg=MODEL['budgets'][str(use)]
        pred=linear_predict(feat,cfg['phase_head']); out[sid]=pred if compatible(feat,cfg['oneclass']) else 'UNKNOWN'
    return out
