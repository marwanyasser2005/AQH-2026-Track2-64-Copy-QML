# Public dataset audit

The executed V12 notebook analyzes 48 XXZ ground states at `N=16` with class counts:

- FM: 14
- XY: 20
- NEEL: 14

The public set is a smooth one-dimensional sweep in anisotropy and leaves a deliberate gap around the phase boundaries near `Delta = +/-1`.

## Physical redundancy

V12 reports:

- state-Gram effective rank: **2.70195**
- fidelity-Gram effective rank: **3.15660**
- FM within-class fidelity: effectively **1.0**
- adjacent XY fidelity mean: **0.998178**
- adjacent NEEL fidelity mean: **0.998005**

The key implication is that 48 rows do not represent 48 statistically independent physical regimes. The public set is low-dimensional and strongly correlated along the Hamiltonian sweep.

This is why V12 adds state-level nested selection, a boundary-proxy split, a fidelity-gap split, and hierarchical state+seed uncertainty rather than treating shot episodes as independent physical examples.

The repository does not infer hidden near-critical performance from this public geometry.
