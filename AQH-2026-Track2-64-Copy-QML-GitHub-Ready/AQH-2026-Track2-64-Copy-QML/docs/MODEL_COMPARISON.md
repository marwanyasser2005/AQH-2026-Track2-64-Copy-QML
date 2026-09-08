# Model comparison

## Deployment packages

| Property | V9.2 | V12 |
|---|---|---|
| Runtime family | Bell-QML incumbent | Minimal QRNN |
| Shared quantum parameters | 1 | 1 |
| Frozen angle | `-pi/2` | `-pi/4` |
| Spatial pattern | Alternating PBC matchings | Forward/reverse recurrent sweep |
| Runtime features | decoded `XX/YY/ZZ` + pair counts | 12D parity-aggregated bitstring statistics |
| Known-phase head | 1D XXZ prototype composite likelihood | budget-specific standardized linear classifier |
| UNKNOWN handling | physical one-class XXZ compatibility gate | Mahalanobis one-class gate |
| Parameter count grows with N | No | No |
| Package status | validated incumbent | experimental public winner, not promoted |

## V9.2 research notebook

The V9.2 notebook compared three new shot-consistent candidates. The reported low-copy weighted scores are:

| Candidate | Weighted F1 (4/8/16) | Params |
|---|---:|---:|
| M2 QCNN local | 0.950374 | 6 |
| M0 Bell ablation | 0.935204 | 1 |
| M1 generalized Bell | 0.924527 | 3 |

M2 was the **preliminary public research winner**, but promotion evidence for protected near-critical states and OOD was incomplete. The notebook explicitly retained the exact incumbent for deployment.

## V12 public quick-mode ranking

| Rank | Model | Weighted low-copy F1 |
|---:|---|---:|
| 1 | QRNN_MINIMAL_1P | 0.940228 |
| 2 | M2_QCNN_LOCAL_6P | 0.933592 |
| 3 | PROJECTED_QSVM | 0.922569 |
| 4 | LOW_COPY_SHADOW_KERNEL_SVM | 0.901754 |
| 5 | SHARED_TTN_6P | 0.756554 |

The QRNN advantage over M2 on the primary split is small. The state+seed bootstrap reported mean margin `+0.007414` with 95% CI `[-0.052278, +0.071104]`; this does not establish separation.

## Stress-split interpretation

Using the official scored weights over 4/8/16, the M2 QCNN is stronger on both harder public stress protocols:

- boundary-proxy: M2 approximately 0.864 vs QRNN approximately 0.838
- fidelity-gap: M2 approximately 0.920 vs QRNN approximately 0.874

Therefore V12's own deployment decision remains `KEEP_VALIDATED_INCUMBENT`.

## Classical comparison

The V12 notebook includes Z-only logistic regression, X/Z logistic regression, and RBF-SVM baselines. Public differences are small enough that this repository does not claim a general quantum advantage.
