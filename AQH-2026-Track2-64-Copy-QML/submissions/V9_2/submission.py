"""AQH 2026 Track 2 — V8 organizer-grounded reference submission.

Architecture
------------
1. Shared-parameter Bell-QML measurement on alternating nearest-neighbour bonds.
2. One frozen trainable quantum angle theta=-pi/2 (parameter count independent of N).
3. Each pair outcome yields simultaneous estimators of XX, YY, ZZ.
4. FM and UNKNOWN are handled by transparent one-class physical gates.
5. XY vs NEEL uses a shallow 1-D XXZ prototype likelihood head, derived from
   development XXZ states only; no hidden IDs, answer key, or hidden statevectors.

Runtime contract:
    classify(oracle, state_ids) -> {state_id: label}
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import numpy as np

VALID = {"FM", "XY", "NEEL", "UNKNOWN"}
BASE = Path(__file__).resolve().parent

_DEFAULT = {
    "theta": -math.pi / 2.0,
    "fm_zz_threshold": 0.45,
    "unknown_transverse_threshold": -0.20,
}


def _load_config():
    p = BASE / "artifacts" / "model_config.json"
    out = dict(_DEFAULT)
    if p.exists():
        try:
            cfg = json.loads(p.read_text(encoding="utf-8"))
            out.update(cfg.get("runtime", cfg))
        except Exception:
            pass
    return out


CFG = _load_config()
THETA = float(CFG["theta"])
FM_ZZ_THRESHOLD = float(CFG["fm_zz_threshold"])
UNKNOWN_T_THRESHOLD = float(CFG["unknown_transverse_threshold"])


def _load_prototypes():
    p = BASE / "artifacts" / "xxz_bell_prototypes.npz"
    if not p.exists():
        return None, None
    d = np.load(p)
    delta = np.asarray(d["delta"], dtype=float)
    probs = np.asarray(d["probs"], dtype=float)
    probs = np.clip(probs, 1e-12, 1.0)
    probs /= probs.sum(axis=1, keepdims=True)
    return delta, np.log(probs)


PROTO_DELTA, PROTO_LOGP = _load_prototypes()


def _matching(n: int, parity: int) -> List[Tuple[int, int]]:
    if n % 2:
        raise ValueError("V8 reference circuit expects an even number of qubits.")
    if parity == 0:
        return [(i, i + 1) for i in range(0, n, 2)]
    return [(i, (i + 1) % n) for i in range(1, n, 2)]


def _ops_for_matching(pairs: List[Tuple[int, int]]):
    def ops_fn(wires):
        import pennylane as qml
        for a, b in pairs:
            qml.CNOT(wires=[a, b])
            qml.RY(THETA, wires=a)
    return ops_fn


def _measure_state(oracle, sid: str):
    n = int(getattr(oracle, "n", 16))
    budget = int(oracle.remaining(sid))
    # category order: (XX,ZZ)=(+,+),(+,-),(-,+),(-,-)
    counts = np.zeros(4, dtype=np.int64)
    xx_sum = yy_sum = zz_sum = 0.0
    pair_count = 0

    for shot in range(budget):
        parity = shot & 1
        pairs = _matching(n, parity)
        bits = np.asarray(
            oracle.measure(sid, ops_fn=_ops_for_matching(pairs)), dtype=np.int8
        ).reshape(-1)
        if bits.size != n:
            raise RuntimeError(f"Expected {n} output bits, got {bits.size}")
        eig = 1.0 - 2.0 * bits.astype(float)

        for a, b in pairs:
            x = float(eig[a])      # XX eigenvalue at theta=-pi/2
            z = float(eig[b])      # ZZ eigenvalue
            y = float(-x * z)      # YY because XX*ZZ = -YY
            xx_sum += x
            yy_sum += y
            zz_sum += z
            pair_count += 1
            if x > 0 and z > 0:
                counts[0] += 1
            elif x > 0 and z < 0:
                counts[1] += 1
            elif x < 0 and z > 0:
                counts[2] += 1
            else:
                counts[3] += 1

    if pair_count == 0:
        return {"counts": counts, "xx": 0.0, "yy": 0.0, "zz": 0.0,
                "transverse": 0.0, "anisotropy": 0.0, "budget": 0}

    xx = xx_sum / pair_count
    yy = yy_sum / pair_count
    zz = zz_sum / pair_count
    transverse = 0.5 * (xx + yy)
    return {
        "counts": counts,
        "xx": float(xx),
        "yy": float(yy),
        "zz": float(zz),
        "transverse": float(transverse),
        "anisotropy": float(zz - transverse),
        "budget": budget,
    }


def _phase_from_prototype(counts: np.ndarray, anisotropy: float) -> str:
    # Fallback remains the exact XXZ anisotropy sign rule if the artifact is absent.
    if PROTO_DELTA is None or PROTO_LOGP is None:
        return "XY" if anisotropy >= 0.0 else "NEEL"

    # Pseudo-likelihood over the one-dimensional XXZ development manifold.
    # Correlations between disjoint bonds make this a shallow composite likelihood,
    # not a claim of independent pair samples. Its role is only to stabilize the
    # finite-copy boundary estimate around Delta=+1.
    ll = PROTO_LOGP @ np.asarray(counts, dtype=float)
    delta_hat = float(PROTO_DELTA[int(np.argmax(ll))])
    return "XY" if delta_hat < 1.0 else "NEEL"


def _decide(f) -> str:
    zz = float(f["zz"])
    t = float(f["transverse"])

    # FM exemption must happen before OOD rejection because true FM has weak
    # transverse correlation but an unmistakable ZZ≈+1 signature.
    if zz > FM_ZZ_THRESHOLD:
        return "FM"

    # UNKNOWN is not a learned external family. It is rejection from the locked
    # XXZ manifold. Non-FM XXZ has strong negative transverse correlation,
    # whereas the organizer's interleaved Hubbard impostors have weak local
    # transverse spin correlation in this measurement.
    if t > UNKNOWN_T_THRESHOLD:
        return "UNKNOWN"

    return _phase_from_prototype(f["counts"], float(f["anisotropy"]))


def classify(oracle, state_ids: Iterable[str]) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for sid in state_ids:
        sid = str(sid)
        pred = _decide(_measure_state(oracle, sid))
        out[sid] = pred if pred in VALID else "UNKNOWN"
    return out
