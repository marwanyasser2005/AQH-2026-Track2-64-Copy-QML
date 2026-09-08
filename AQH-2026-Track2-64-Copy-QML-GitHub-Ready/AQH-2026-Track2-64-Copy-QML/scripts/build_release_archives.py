from pathlib import Path
import zipfile, hashlib
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'releases'; OUT.mkdir(exist_ok=True)

def build(name,base,rels):
    dst=OUT/name
    if dst.exists(): dst.unlink()
    with zipfile.ZipFile(dst,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for rel in rels: z.write(base/rel,arcname=rel.as_posix())
    print(dst)

build('AQH_Track2_FINAL_SUBMISSION_V9_2_GITHUB_READY.zip',ROOT/'submissions/V9_2',[
    Path('submission.py'),Path('artifacts/model_config.json'),Path('artifacts/xxz_bell_prototypes.npz'),Path('SHA256SUMS.txt'),Path('README.md')])
build('AQH_Track2_V12_FINAL_SUBMISSION_GITHUB_READY.zip',ROOT/'submissions/V12',[
    Path('submission.py'),Path('model_config.json'),Path('SUBMISSION_MANIFEST.json'),Path('README.txt'),Path('SHA256SUMS.txt'),Path('README.md')])
