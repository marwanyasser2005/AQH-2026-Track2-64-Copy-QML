from pathlib import Path
import ast, json, hashlib, sys

ROOT = Path(__file__).resolve().parents[1]
errors=[]

def sha256(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''): h.update(c)
    return h.hexdigest()

def check(cond,msg):
    if not cond: errors.append(msg)

required=[
    'README.md',
    'submissions/V9_2/submission.py',
    'submissions/V9_2/artifacts/model_config.json',
    'submissions/V9_2/artifacts/xxz_bell_prototypes.npz',
    'submissions/V12/submission.py',
    'submissions/V12/model_config.json',
    'submissions/V12/SUBMISSION_MANIFEST.json',
    'notebooks/V9_2/AQH_Track2_FINAL_V9_2.ipynb',
    'notebooks/V12/AQH_Track2_FINAL_V12.ipynb',
]
for r in required: check((ROOT/r).exists(),f'Missing required file: {r}')

# Syntax only: no PennyLane import required.
for r in ['submissions/V9_2/submission.py','submissions/V12/submission.py']:
    p=ROOT/r
    if p.exists():
        try: ast.parse(p.read_text(encoding='utf-8'),filename=str(p))
        except Exception as e: errors.append(f'Syntax failure {r}: {e}')

# Config semantics.
try:
    v9=json.loads((ROOT/'submissions/V9_2/artifacts/model_config.json').read_text())
    check(v9.get('qml',{}).get('trainable_parameter_count')==1,'V9.2 expected one quantum parameter')
    check(v9.get('qml',{}).get('size_independent') is True,'V9.2 size_independent must be true')
except Exception as e: errors.append(f'V9.2 config error: {e}')
try:
    v12=json.loads((ROOT/'submissions/V12/model_config.json').read_text())
    check(v12.get('architecture')=='QRNN_MINIMAL_1P','V12 architecture mismatch')
    check(v12.get('parameter_count')==1,'V12 parameter count mismatch')
    check(v12.get('parameter_count_depends_on_N') is False,'V12 parameter scaling mismatch')
    check(set(map(int,v12.get('allowed_budgets',[])))=={4,8,16,32,64},'V12 budget set mismatch')
except Exception as e: errors.append(f'V12 config error: {e}')

# SHA manifests.
for sub in ['V9_2','V12']:
    base=ROOT/'submissions'/sub
    man=base/'SHA256SUMS.txt'
    if not man.exists(): errors.append(f'Missing SHA manifest: {man}')
    else:
        for line in man.read_text().splitlines():
            if not line.strip(): continue
            digest,rel=line.split(None,1); rel=rel.strip()
            p=base/rel
            check(p.exists(),f'SHA target missing: {sub}/{rel}')
            if p.exists(): check(sha256(p)==digest,f'SHA mismatch: {sub}/{rel}')

# Public-repo firewall: check filenames, not harmless documentation strings.
for p in ROOT.rglob('*'):
    if not p.is_file(): continue
    name=p.name.lower()
    if name in {'hidden_test.npz','answer_key.csv','commitment_password.txt'}:
        errors.append(f'Private artifact present: {p.relative_to(ROOT)}')

if errors:
    print('REPOSITORY VALIDATION: FAIL')
    for e in errors: print(' -',e)
    sys.exit(1)
print('REPOSITORY VALIDATION: PASS')
print('Required files, syntax, model invariants, SHA manifests, and private-file firewall all passed.')
