# Validation protocol

## 1. Repository validation

Run:

```bash
python scripts/validate_repo.py
```

This checks:

- required repository files
- Python syntax of both `submission.py` files
- JSON model/manifest structure
- SHA-256 manifests
- V9.2 artifact layout
- absence of common organizer-private files

## 2. Participant-side public validation

Use the participant kit only. The helper script accepts an explicit kit path and submission directory:

```bash
python validation/participant_validation.py \
  --kit /path/to/AQH_64_Copy_Professional_Solution \
  --submission submissions/V12
```

The script performs static compile/import checks when possible and invokes participant `verify_submission.py` / `self_score.py` when present.

A public self-score is an engineering diagnostic, not a hidden-set estimate.

## 3. Organizer audit boundary

Organizer-private tests must remain outside this public repository. Hidden evaluation may be performed separately after model freeze, but its hidden dataset, answer key, per-state predictions, and secret harness artifacts must not be committed.

## 4. Promotion rule

A public winner is not automatically a deployment winner. V9.2 and V12 both preserve this distinction in their own outputs.
