# Packaging audit

## V9.2 uploaded ZIP layout issue

The uploaded V9.2 archive contains these four files at ZIP root:

```text
SHA256SUMS.txt
model_config.json
submission.py
xxz_bell_prototypes.npz
```

However the uploaded `submission.py` explicitly loads:

```text
artifacts/model_config.json
artifacts/xxz_bell_prototypes.npz
```

The original notebook's archive-integrity check verified file presence and hashes but did not detect this relative-path mismatch.

### Repository correction

The GitHub-ready V9.2 directory changes **only the directory layout**:

```text
submissions/V9_2/
├── submission.py
└── artifacts/
    ├── model_config.json
    └── xxz_bell_prototypes.npz
```

The three runtime artifact byte streams are unchanged. Their SHA-256 values remain identical to the uploaded archive. A new layout-aware `SHA256SUMS.txt` is generated, while `SHA256SUMS.original.txt` preserves the uploaded manifest.

The untouched original ZIP is retained under `releases/original_uploads/` for provenance.

## V12

V12's submission reads `model_config.json` from the same directory as `submission.py`, matching the uploaded flat archive layout. No layout correction was necessary.
