# Reproducibility

## Exact artifacts

The repository includes exact copies of the two uploaded executed notebooks and original submission archives under `releases/original_uploads/`.

## Environment

Portable minimum dependencies are in `requirements-runtime.txt` and `requirements-research.txt`. The V9.2 executed environment reported:

- Python 3.12.13
- NumPy 2.0.2
- pandas 2.3.3
- Matplotlib 3.10.0
- PennyLane 0.45.1
- scikit-learn 1.6.1
- SciPy 1.16.3

## Rebuilding release ZIPs

```bash
python scripts/build_release_archives.py
```

## Verifying repository integrity

```bash
python scripts/validate_repo.py
```
