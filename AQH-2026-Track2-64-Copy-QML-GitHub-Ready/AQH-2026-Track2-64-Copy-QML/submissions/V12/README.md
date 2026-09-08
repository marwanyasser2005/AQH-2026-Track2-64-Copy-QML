# V12 submission — experimental minimal QRNN

**Architecture:** `QRNN_MINIMAL_1P`

**Status from uploaded manifest:** `EXPERIMENTAL_DIRECT_PUBLIC_WINNER_NOT_PROMOTED`

**Deployment decision from uploaded manifest:** `KEEP_VALIDATED_INCUMBENT`

The V12 package is preserved as a separate research candidate, not mislabeled as the promoted competition winner.

## Quantum cell

For each adjacent recurrent step:

```text
RY(theta) on a
CNOT(a -> b)
CNOT(b -> a)
```

with one shared `theta = -pi/4`. Forward and reverse sweeps alternate by parity. Full bitstrings are aggregated into 12 shot-consistent features and passed to a budget-specific linear head plus one-class XXZ compatibility gate.
