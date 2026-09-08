# Methodology

## Resource discipline

Every inference circuit execution consumes one copy of the unknown quantum state. The repository reports the required copy curve at 4, 8, 16, 32, and 64 copies and emphasizes the low-copy scored window 4/8/16.

## Shot consistency

A central V9.2 correction is that model fitting and finite-copy inference use the same shot-level estimator. This avoids fitting a classifier to exact expectation-value features and then evaluating it on a different nonlinear finite-shot feature distribution.

## Public model selection

- Organizer hidden data are not used to choose architecture, quantum parameters, thresholds, or heads.
- V9.2 uses public finite-copy Monte Carlo episodes for candidate comparison.
- V12 uses nested state-level search and a held-out outer validation split.
- V12 adds boundary-proxy and fidelity-gap stress splits to reduce the false confidence created by near-duplicate neighboring states.

## UNKNOWN semantics

`UNKNOWN` means incompatible with the protected XXZ problem family. It is not a fourth XXZ phase, and legitimate near-critical XXZ states should remain known-domain.

## Statistical discipline

The V12 quick run uses only three report seeds and therefore is not treated as final promotion evidence. Hierarchical resampling is performed at physical-state and seed level rather than treating repeated shot episodes as independent states.

## Kernel models

Projected QSVM and low-copy shadow-kernel models are research comparators. Their auxiliary quantum-runtime assumptions are not silently treated as equivalent to a direct circuit acting on the unknown state.
