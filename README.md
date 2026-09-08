# AQH 2026 Track 2: The 64-Copy Problem

<div align="center">

### Quantum Machine Learning from Scarce Quantum Data

**Direct-state quantum phase classification under strict copy-metered inference**

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![PennyLane](https://img.shields.io/badge/PennyLane-QML-00C7B7)
![Task](https://img.shields.io/badge/Task-Quantum%20Phase%20Classification-6C5CE7)
![Copy Budget](https://img.shields.io/badge/Max%20Copies-64-FF8C42)
![Status](https://img.shields.io/badge/Repository-Research%20%2B%20Submission-2EA44F)

**FM • XY • NEEL • UNKNOWN**

</div>

---

## Overview

This repository contains the research, experiments, validation artifacts, and frozen submission packages developed for **Alexandria Quantum Hackathon 2026, Track 2: The 64-Copy Problem**.

The challenge is to classify unknown many-body quantum states while respecting a strict physical resource constraint:

> **Each measurement consumes one copy of the unknown state, with a maximum budget of 64 copies per state.**

The system must classify each state as:

- **FM**: Ferromagnetic phase
- **XY**: Gapless XY phase
- **NEEL**: Antiferromagnetic Néel phase
- **UNKNOWN**: Out-of-distribution state outside the target XXZ family

The project focuses on **copy-efficient direct-state QML**, where trainable quantum circuits operate on the unknown quantum state through the official copy-metered oracle.

---

## Problem Statement

The physical system is a one-dimensional spin-1/2 XXZ chain.

For the XXZ family, the phase is controlled by the anisotropy parameter `Delta`:

| Region | Phase |
|---|---|
| `Delta < -1` | FM |
| `-1 < Delta < +1` | XY |
| `Delta > +1` | NEEL |
| Outside target XXZ family | UNKNOWN |

The model must also work under:

- scarce copies
- destructive measurement
- near-critical states
- measurement noise
- unseen system sizes
- out-of-distribution impostors
- constant trainable quantum parameter count with respect to system size

---

## Official Inference Interface

Both frozen runtime packages expose the same competition entry point:

```python
classify(oracle, state_ids)
```

Conceptually:

```text
Unknown quantum state
        |
        v
CopyOracle
        |
        v
Copy-metered quantum measurements
        |
        v
Quantum feature extraction
        |
        v
Finite-shot aggregation
        |
        v
Phase classification + OOD rejection
        |
        v
FM / XY / NEEL / UNKNOWN
```

The official copy budgets considered throughout the work are:

```text
4 / 8 / 16 / 32 / 64 copies per state
```

The low-copy research objective emphasizes the most resource-starved region:

```text
0.40 * F1@4 + 0.35 * F1@8 + 0.25 * F1@16
```

---

## Repository Highlights

This repository preserves two major submission generations:

| Version | Architecture | Quantum Parameters | Role |
|---|---|---:|---|
| **V9.2** | Validated incumbent runtime / Bell-QML lineage | N-independent | Deployment reference |
| **V12** | `QRNN_MINIMAL_1P` | **1 shared parameter** | Latest public research candidate |

The research notebooks also compare:

- `M2_QCNN_LOCAL_6P`
- `QRNN_MINIMAL_1P`
- `SHARED_TTN_6P`
- `SHARED_MERA_8P`
- `PROJECTED_QSVM`
- `LOW_COPY_SHADOW_KERNEL_SVM`
- classical physics baselines
- classical linear baselines
- RBF-SVM baselines

---

## Main Quantum Architectures

### M2 QCNN Local 6P

`M2_QCNN_LOCAL_6P` is a QCNN-inspired direct-state quantum feature extractor using alternating nearest-neighbor local blocks.

For one parity pass:

```text
RY(theta1) on qubit a
        |
RY(theta2) on qubit b
        |
CNOT(a -> b)
        |
RZ(theta3) on qubit b
```

For the complementary pass:

```text
RY(theta4) on qubit a
        |
CNOT(b -> a)
        |
RX(theta5) on qubit b
        |
RZ(theta6) on qubit a
```

Key properties:

- 6 shared trainable quantum parameters
- parameter count independent of system size
- alternating nearest-neighbor processing
- direct operation on the unknown state
- finite-shot bitstring readout
- shot-consistent feature extraction

For each parity, six statistics are extracted:

1. pair control mean
2. pair target mean
3. pair product mean
4. global magnetization
5. staggered magnetization
6. nearest-neighbor correlation

Two parity views produce a **12-dimensional feature vector**.

---

### QRNN Minimal 1P

`QRNN_MINIMAL_1P` is the strongest V12 public research candidate.

It uses a sequential recurrent sweep across neighboring qubits with only **one shared trainable parameter**.

Recurrent cell:

```text
RY(theta) on qubit a
        |
CNOT(a -> b)
        |
CNOT(b -> a)
```

The selected V12 public parameter was approximately:

```text
theta = -pi / 4
```

Recurrent views:

```text
Parity 0:
q0 -> q1 -> q2 -> q3 -> ... -> qN-1

Parity 1:
qN-1 -> qN-2 -> ... -> q1 -> q0
```

Key properties:

- 1 shared trainable quantum parameter
- parameter count independent of N
- direct-state architecture
- O(N) recurrent sweep depth
- bidirectional parity views
- finite-shot feature aggregation
- budget-specific classical phase head
- one-class XXZ compatibility gate

---

## End-to-End QML Pipeline

```text
                Unknown N-qubit state
                         |
                         v
                    CopyOracle
                         |
                         v
             Copy-budget scheduler
                         |
            +------------+------------+
            |                         |
            v                         v
      QCNN local blocks          QRNN recurrent sweep
            |                         |
            +------------+------------+
                         |
                         v
                 Measured bitstrings
                         |
                         v
              Shot-consistent features
                         |
             +-----------+-----------+
             |                       |
             v                       v
      Known-phase classifier     XXZ OOD gate
             |                       |
             v                       v
        FM / XY / NEEL            UNKNOWN
```

---

## Dataset

The public training dataset contains:

```text
48 labeled XXZ quantum states
N = 16 qubits
3 known phases
```

Class distribution:

| Phase | Number of states |
|---|---:|
| FM | 14 |
| XY | 20 |
| NEEL | 14 |
| **Total** | **48** |

Each N=16 statevector has:

```text
2^16 = 65,536 complex amplitudes
```

The public phase ranges are separated from the exact transition points, so smooth public validation can overestimate true near-critical generalization.

---

## Dataset Geometry Audit

A major finding of the V12 study is that the public dataset is highly redundant in quantum-state geometry.

Approximate diagnostics:

```text
State-Gram effective rank      ~ 2.70
Fidelity-Gram effective rank   ~ 3.16
```

Additional observations:

- FM states are almost physically identical across the public range
- adjacent XY states have very high fidelity
- adjacent NEEL states have very high fidelity
- validation points are often extremely close to training states in fidelity space

This motivated stronger validation beyond ordinary train/validation interpolation.

---

## Validation Strategy

The V12 research pipeline introduced multiple validation views.

### Primary split

Used for standard model ranking.

### Boundary Proxy

Places greater emphasis on states closer to difficult phase boundaries.

### Fidelity Gap

Reduces validation examples that are nearly identical to training examples in quantum-state geometry.

### Hierarchical bootstrap

Used to compare models while respecting the fact that repeated finite-shot episodes are not independent physical states.

---

## V12 Public Research Ranking

Weighted low-copy objective:

```text
0.40 * F1@4 + 0.35 * F1@8 + 0.25 * F1@16
```

| Rank | Model | Weighted Low-Copy Macro-F1 |
|---:|---|---:|
| 1 | **QRNN_MINIMAL_1P** | **~0.9402** |
| 2 | `M2_QCNN_LOCAL_6P` | ~0.9336 |
| 3 | `PROJECTED_QSVM` | ~0.9226 |
| 4 | `LOW_COPY_SHADOW_KERNEL_SVM` | ~0.9018 |
| 5 | `SHARED_TTN_6P` | ~0.7566 |

The ranking alone was **not** used as sufficient evidence for deployment promotion.

---

## Stress-Test Results

| Model | Primary | Boundary Proxy | Fidelity Gap |
|---|---:|---:|---:|
| **QRNN_MINIMAL_1P** | **0.940** | 0.838 | 0.874 |
| **M2_QCNN_LOCAL_6P** | 0.934 | **0.864** | **0.920** |
| PROJECTED_QSVM | 0.923 | 0.855 | 0.879 |
| LOW_COPY_SHADOW_KERNEL_SVM | 0.902 | 0.759 | 0.727 |
| SHARED_TTN_6P | 0.757 | 0.742 | 0.687 |

### Interpretation

The QRNN performs best on the smooth primary public split.

The M2 QCNN is stronger under the harder boundary and fidelity-gap stress tests.

This is one of the key reasons the research winner was not automatically promoted to deployment.

---

## Statistical Comparison

Approximate paired result:

```text
QRNN - M2 weighted low-copy margin ~ +0.0074
95% CI ~ [-0.052, +0.071]
```

The interval crosses zero.

Therefore:

> **The public evidence does not establish that QRNN is statistically superior to M2 QCNN.**

This repository intentionally distinguishes:

```text
highest public score
```

from:

```text
statistically established superiority
```

---

## Classical Baselines

### Z-Physics

A physics-informed baseline using Z-basis measurements and compact physical observables.

```text
Unknown state
    |
    v
Z-basis measurements
    |
    v
Magnetization + longitudinal correlations
    |
    v
Physics-based phase decision
```

### X/Z-Linear

A two-basis classical baseline that splits the copy budget between X and Z measurement views and performs a linear phase decision.

```text
                 Unknown state
                      |
          +-----------+-----------+
          |                       |
          v                       v
       Z shots                 X shots
          |                       |
          v                       v
      Z features               X features
          +-----------+-----------+
                      |
                      v
               Linear classifier
                      |
                      v
               FM / XY / NEEL
```

---

## V6 Classical Baseline Results

Macro-F1 under the same copy budgets:

| Model | 4 Copies | 8 Copies | 16 Copies | 32 Copies | 64 Copies |
|---|---:|---:|---:|---:|---:|
| **Z-Physics** | **0.933** | **0.993** | **1.000** | **0.993** | **1.000** |
| **X/Z-Linear** | **0.874** | **0.924** | **0.952** | **0.965** | **1.000** |
| Primary QML, V6 | 0.812 | 0.834 | 0.928 | 0.967 | 0.983 |

### Scientific conclusion

The V6 evidence does **not** establish a quantum advantage.

The strongest classical physics baseline remained extremely competitive and outperformed the V6 QML model across the tested budgets.

The correct conclusion is:

> **QML is competitive under scarce-copy constraints, but the current evidence does not justify claiming a robust quantum advantage over the strongest matched-budget classical baseline.**

---

## Resource Accounting

| Model | Trainable Quantum Params | Depth Scaling | Unknown-State Access |
|---|---:|---|---|
| `M2_QCNN_LOCAL_6P` | 6 | O(1) ideal brickwork | Direct learned circuit |
| `QRNN_MINIMAL_1P` | **1** | O(N) | Direct learned circuit |
| `SHARED_TTN_6P` | 6 | O(log N) tree levels | Direct learned circuit |
| PROJECTED_QSVM | 0 | O(1) local basis rotations | X/Z measurements |
| SHADOW_KERNEL_SVM | 0 | O(1) local basis rotations | X/Y/Z measurements |

The parameter counts of the direct-state learned architectures remain independent of system size.

---

## OOD / UNKNOWN Handling

UNKNOWN is **not** treated as a fourth XXZ phase.

```text
Measured state features
        |
        v
XXZ compatibility score
        |
   +----+----+
   |         |
compatible  incompatible
   |         |
   v         v
FM/XY/NEEL UNKNOWN
```

OOD evidence is treated separately from ordinary phase accuracy.

---

## What We Learned

1. **More parameters are not automatically better.**  
   The one-parameter QRNN remained highly competitive with larger quantum circuits.

2. **Public interpolation can be misleading.**  
   The 48-state public dataset has strong state-level redundancy.

3. **Stress tests matter.**  
   The primary public winner changed when harder generalization splits were used.

4. **Statistical significance matters.**  
   A higher mean score is not enough when uncertainty intervals overlap.

5. **Classical baselines matter.**  
   Physics-informed classical methods are extremely strong in this task.

6. **Copy efficiency is a first-class metric.**  
   A model should be judged on performance across the full copy curve, not only at 64 copies.

---

## Research Grounding

Representative research directions used in the project include:

- few-data quantum machine learning
- QCNN generalization
- quantum phase recognition
- quantum-kernel concentration
- projected quantum kernels
- randomized measurements and classical shadows
- tensor-network quantum classifiers
- recurrent and shared-parameter QML architectures

Representative references:

1. Caro et al., *Generalization in quantum machine learning from few training data*, Nature Communications, 2022.
2. Gil-Fuster et al., Nature Communications, 2024, on QNN memorization and generalization.
3. Thanasilp et al., Nature Communications, 2024, on quantum-kernel concentration.
4. Huang et al., Nature Communications, 2021, on projected quantum kernels and quantum-data learning.
5. Lazzarin, Galli and Prati, Physics Letters A, 2022, on TTN/MERA quantum phase classification.
6. Liu et al., Physical Review Letters, 2023, on QCNN-based quantum phase recognition.
7. Srikumar, Hill and Hollenberg, Quantum Machine Intelligence, 2024, on quantum random forests.

---

## Repository Structure

```text
AQH-2026-Track2-64-Copy-QML/
|
|-- README.md
|-- CHANGELOG.md
|-- REPO_SETUP.md
|-- REPOSITORY_MANIFEST.json
|-- SHA256SUMS_REPOSITORY.txt
|
|-- submissions/
|   |-- V9_2/
|   `-- V12/
|
|-- notebooks/
|   |-- V9_2/
|   `-- V12/
|
|-- results/
|   |-- V9_2/
|   `-- V12/
|
|-- docs/
|   |-- ARCHITECTURE.md
|   |-- MODEL_COMPARISON.md
|   |-- METHODOLOGY.md
|   |-- DATASET_AUDIT.md
|   |-- VALIDATION_PROTOCOL.md
|   |-- COMPETITION_COMPLIANCE.md
|   |-- REPRODUCIBILITY.md
|   |-- SECURITY_AND_DATA_BOUNDARIES.md
|   `-- TECHNICAL_REPORT.md
|
|-- validation/
|   `-- participant_validation.py
|
|-- scripts/
|   |-- validate_repo.py
|   |-- build_release_archives.py
|   |-- publish_to_github.ps1
|   `-- publish_to_github.sh
|
|-- releases/
|
`-- .github/
    `-- workflows/
        `-- ci.yml
```

---

## Reproducibility

Install the research environment:

```bash
pip install -r requirements-research.txt
```

For runtime-only dependencies:

```bash
pip install -r requirements-runtime.txt
```

Run the repository validation:

```bash
python scripts/validate_repo.py
```

Participant-side validation:

```bash
python validation/participant_validation.py   --kit /path/to/AQH_64_Copy_Professional_Solution   --submission submissions/V12
```

---

## Security and Hidden-Set Boundary

Organizer-private evaluation material is intentionally excluded from this public repository.

Never commit:

```text
hidden_test.npz
answer_key.csv
organizer-only evaluation folders
hidden predictions
hidden confusion matrices
private commitment credentials
```

Hidden evaluation must not participate in:

- architecture search
- hyperparameter tuning
- model selection
- threshold tuning
- feature selection

The hidden set is reserved for final organizer-side audit only.

---

## Deployment Philosophy

This project intentionally separates:

```text
Public research winner
        !=
Statistically proven winner
        !=
Validated deployment winner
```

The V12 public study identified:

```text
PUBLIC_RESEARCH_WINNER = QRNN_MINIMAL_1P
```

but the evidence did not justify replacing the validated incumbent.

Therefore the deployment decision remained:

```text
KEEP_VALIDATED_INCUMBENT
```

This is a deliberate evidence-based decision.

---

## Judging Criteria Alignment

| Judging Criterion | Evidence in This Repository |
|---|---|
| Creativity of Quantum Computing | Direct-state QCNN and minimal QRNN architectures |
| Time Management | Time-boxed model branches and promotion gates |
| Continuous Judge Interaction | Requirement-driven validation and compliance checks |
| Team Work | Shared research, implementation, validation, documentation, and presentation workflow |
| Clear Problem-Solution Flow | Copy-metered input to quantum circuit to finite-shot inference to final phase |
| Research | Literature-grounded architecture and validation methodology |
| Presentation Skills | Architecture diagrams, copy curves, stress tests, confusion matrices, and concise technical reporting |

---

## Team

- **Menna Mohamed**
- **Sara Mosbah**
- **Sarah ElShinnawy**
- **Ahmed Alaa**
- **Marwan Abdelghaffar**

---

## Final Takeaway

The central question is not:

> Which model achieves the highest single score?

The more meaningful question is:

> **Which model extracts the most reliable phase information from the fewest physical copies while remaining robust, interpretable, scalable, and scientifically defensible?**

This repository shows that compact quantum architectures can remain highly competitive under severe copy constraints.

At the same time, the experiments demonstrate that:

- classical physics baselines are extremely strong
- public interpolation can overestimate generalization
- stress testing changes model rankings
- statistical uncertainty must be reported
- quantum advantage should never be claimed without sufficient evidence

<div align="center">

## QNova

### Small Copies. Strong Evidence. Responsible Quantum Learning.

**AQH 2026 • Track 2 • The 64-Copy Problem**

</div>
