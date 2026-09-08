# Technical report — scarce-copy quantum phase recognition

## 1. Task

The Track 2 problem asks for quantum-phase recognition when the input is itself a many-body quantum state and only a bounded number of copies are available at inference. The target labels are FM, XY, NEEL, and an UNKNOWN rejection outcome for states incompatible with the protected problem family. The low-copy region is the central research regime, so the study reports 4, 8, and 16 copies as the scored window and 32/64 as required crossover points.

## 2. V9.2 lineage and deployed runtime

The V9.2 notebook was designed to fix a train/inference mismatch discovered in V9. It trains candidate heads on the same finite-shot feature estimator used at inference. Three candidates were compared: a one-parameter Bell ablation, a three-parameter generalized Bell circuit, and a six-parameter QCNN-inspired local circuit. The M2 QCNN candidate led the public low-copy research comparison with weighted F1 0.950374.

That public win did not automatically trigger deployment. The notebook required protected near-critical and OOD evidence before replacing the incumbent. Those promotion gates were incomplete in the executed notebook, so the deployment winner remained the exact incumbent runtime.

The resulting V9.2 submission is therefore a one-parameter Bell-QML model. It alternates periodic nearest-neighbour matchings, applies CNOT plus a shared `RY(theta)` with `theta=-pi/2`, and decodes the measured pair outcomes into XX, YY, and ZZ estimators. A transparent FM rule is applied first, then a one-class XXZ compatibility test, followed by a shallow one-dimensional XXZ prototype composite-likelihood head for XY versus NEEL.

## 3. V12 few-data study

V12 starts from a measured limitation of the public data rather than assuming 48 rows represent 48 independent examples. The 48 N=16 states lie on a smooth one-dimensional Hamiltonian sweep and exhibit strong fidelity redundancy. The fidelity Gram matrix has effective rank about 3.16 and neighboring XY/NEEL states have mean fidelity around 0.998. This makes ordinary random row splitting optimistic.

V12 therefore performs nested state-level selection, a boundary-proxy split, a fidelity-gap split, and hierarchical state+seed uncertainty. It compares direct-state M2 QCNN, minimal QRNN, shared TTN, projected QSVM, and a low-copy shadow-kernel SVM. The QRNN is intentionally reduced to one shared recurrent parameter.

In the uploaded quick-mode run, QRNN_MINIMAL_1P has the highest primary weighted low-copy F1 at 0.940228, followed by M2 QCNN at 0.933592. The bootstrap margin between them is small and its 95% interval crosses zero. More importantly, M2 wins both the boundary-proxy and fidelity-gap stress tests. The executed V12 promotion matrix therefore does not establish a robust replacement and keeps the validated incumbent.

## 4. Quantum/classical comparison

Both notebooks retain matched classical baselines because a public phase score by itself does not establish a quantum advantage. V12 compares against Z-only logistic regression, X/Z logistic regression, and RBF-SVM. The public differences are small and highly split-dependent. This repository therefore reports comparative measurements without claiming a general quantum advantage.

## 5. Resource scaling

Both deployed packages use a trainable quantum parameter count independent of system size. V9.2 reuses one Bell angle across all matched bonds. V12 reuses one recurrent angle across the entire chain. At N=16, V12's resource table estimates 15 one-qubit and 30 two-qubit gates per QRNN copy, compared with 48 one-qubit and 16 two-qubit gates for the six-parameter M2 brickwork candidate. The trade-off is therefore recurrent depth versus local parallelism rather than parameter count alone.

## 6. OOD, criticality, and transfer

The public dataset contains no true near-critical examples. V12's uploaded run records near-critical, independent OOD, and empirical size-transfer evidence as UNVERIFIED. The runtime packages do include one-class UNKNOWN logic, but this repository does not convert absent validation into a scientific claim.

## 7. Reproducibility and integrity

The exact executed notebooks are included. Compact CSVs reproduce the headline tables from their outputs. SHA-256 manifests cover both runtime packages. A static validation script checks package structure and rejects common organizer-private filenames. The original uploaded archives are retained separately for provenance; the V9.2 GitHub-ready package corrects a directory-layout mismatch without modifying the runtime code/model/prototype bytes.

## 8. Final status

- **V9.2 runtime:** validated incumbent Bell-QML, one shared parameter.
- **V12 runtime:** minimal QRNN, one shared parameter; experimental public research winner.
- **Deployment decision supported by uploaded V12 artifact:** keep the validated incumbent.

This distinction is intentional: research ranking, stress robustness, and deployment readiness are separate questions.
