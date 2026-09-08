# V9.2 submission — validated incumbent

**Runtime architecture:** alternating nearest-neighbour Bell-QML incumbent (`V8.1-final-frozen`).

This is the actual deployed runtime selected by the executed V9.2 notebook. The research notebook's preliminary M2 QCNN winner was not promoted because protected near-critical + OOD promotion evidence was incomplete.

## Files

```text
submission.py
artifacts/model_config.json
artifacts/xxz_bell_prototypes.npz
SHA256SUMS.txt
```

The `artifacts/` layout is required by `submission.py` and corrects the flat uploaded ZIP packaging without modifying the runtime file bytes.

## Quantum model

- shared `theta = -pi/2`
- one trainable/frozen quantum parameter
- alternating periodic nearest-neighbour Bell-QML matching
- decoded XX, YY, ZZ pair observables
- FM physical gate + one-class UNKNOWN gate + XXZ prototype head
