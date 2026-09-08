# Competition compliance map

| Requirement | Repository implementation |
|---|---|
| At most 64 copies/state | Both runtime submissions meter calls through `CopyOracle` and support max budget 64 |
| Scored window 4/8/16 | Results tables and research ranking use weighted 4/8/16 objective |
| Report 32/64 | Both research notebooks report 4/8/16/32/64 |
| QML circuit acts on unknown state | V9.2 Bell-QML and V12 QRNN both apply trainable/frozen shared quantum operations through `ops_fn` |
| Parameter count independent of N | V9.2: 1 shared angle; V12: 1 shared recurrent angle |
| Classical baselines | V9.2: Z-only + X/Z; V12: Z-only, X/Z, RBF-SVM |
| Noise analysis | Research notebooks contain hooks/analysis; V12 quick uploaded run did not complete matched noise promotion evidence |
| Near-critical analysis | Public data lacks near-critical points; V12 uploaded run marks evidence UNVERIFIED |
| OOD/UNKNOWN | Both runtime packages contain one-class rejection; V12 uploaded run marks independent OOD development evidence UNVERIFIED |
| Size transfer | Parameterization is N-independent; empirical V12 uploaded run marks size-transfer evidence UNVERIFIED |
| Hidden-data isolation | Hidden organizer data are excluded from this repository and were not used for public model selection according to notebook manifests |

This document reports what the uploaded artifacts support. It does not upgrade an `UNVERIFIED` gate to `PASS`.
