from pathlib import Path
import argparse, subprocess, sys, ast, json, shutil, tempfile

ap=argparse.ArgumentParser(description='Public participant-side submission validator; never uses organizer hidden data.')
ap.add_argument('--kit',type=Path,required=True)
ap.add_argument('--submission',type=Path,required=True)
args=ap.parse_args()
kit=args.kit.resolve(); sub=args.submission.resolve(); sp=sub/'submission.py'
if not sp.exists(): raise SystemExit(f'Missing {sp}')
for r in ['oracle.py','evaluate.py','self_score.py','xxz_public_train.npz']:
    if not (kit/r).exists(): raise SystemExit(f'Participant kit missing {r}')
ast.parse(sp.read_text(encoding='utf-8'))
print('Static submission syntax: PASS')
for private in ['hidden_test.npz','answer_key.csv','COMMITMENT_PASSWORD.txt']:
    if (sub/private).exists(): raise SystemExit(f'Private artifact found in submission: {private}')
verify=kit/'verify_submission.py'
if verify.exists():
    p=subprocess.run([sys.executable,str(verify),str(sp)],cwd=kit,text=True)
    print('verify_submission return code:',p.returncode)
print('\nRunning participant self_score.py ...')
p=subprocess.run([sys.executable,str(kit/'self_score.py'),str(sp)],cwd=kit,text=True)
print('self_score return code:',p.returncode)
if p.returncode: raise SystemExit(p.returncode)
print('PARTICIPANT-SIDE PUBLIC VALIDATION: PASS')
print('Note: this is not evidence of hidden-set performance.')
