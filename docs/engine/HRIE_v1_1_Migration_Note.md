# HRIE v1.1 Hardening Pass — Migration Note

**GOLDEN_MIGRATION: RN_MODEL_V2**

| Field | Value |
| --- | --- |
| From version | 1.0.0 |
| To version | 1.1.0 |
| Migration type | Non-backward-compatible (RN values change) |
| Approval required | COO + CIO |
| Date | April 2026 |

---

## Summary of Changes

Five hardening adjustments transform the engine from a correct quantitative calculator into an institutional-grade, regime-aware, capital-preservation-first risk system.

---

## 1. Risk Number Model — Pure Downside (BREAKING)

**What changed:**

The expected return was removed from the core Risk Number computation.

```
v1.0:  Downside_95_6m = max(0, Z × σ_d × √0.5 − E[r]_6m)
v1.1:  Downside_95_6m = Z × σ_d × √0.5
```

**Why:**

Expected return is forward-looking and model-dependent. Different estimation methods (historical CAGR, analyst consensus, factor model) produce different expected returns for the same asset, causing the same observed downside deviation to yield different Risk Numbers. This violates the principle that RN should be an objective, observable measure of downside risk.

Additionally, the `max(0, ...)` clamp meant that high-return assets could show RN ≈ 1 despite exhibiting substantial drawdowns — this is mathematically correct under the old formula but institutionally dangerous.

**Impact on outputs:**

RN_base will increase for assets with positive expected returns. The magnitude depends on the asset's expected return relative to its downside deviation. Typical impacts:

| Asset type | Typical v1.0 RN | Expected v1.1 RN | Delta |
| --- | --- | --- | --- |
| Tesouro Selic | 1-2 | 2-3 | +1 |
| CDB 110% CDI | 1 | 1-2 | 0-1 |
| FII Logística | 42-48 | 48-52 | +4-6 |
| Ibovespa | 68-75 | 75-78 | +3-5 |
| Small Caps | 82-88 | 85-88 | +2-3 |

Low-volatility, high-return assets are affected most. High-volatility assets are minimally affected because downside deviation already dominated the formula.

**Backward compatibility:**

`risk_number_base` and `risk_number_adjusted` remain in the API schema. Their *values* change, but their *type, range, and semantics* are preserved. Expected return remains in all output metrics (Sharpe, Sortino, Calmar).

A config flag `RN_INCLUDE_EXPECTED_RETURN` can be set to `True` for temporary parallel computation during validation. It is set to `False` in production.

---

## 2. RAF Non-Linear Sigmoid (NON-BREAKING)

**What changed:**

RAF aggregation uses a sigmoid transformation instead of linear scaling.

```
v1.0:  RAF = 1 + 9 × raw_score
v1.1:  RAF = 1 + 9 × normalized_sigmoid(k × (raw_score − 0.5))
       where k = 5.0 (configurable)
```

**Why:**

Linear scaling treats all regime transitions equally. In reality, the transition from "normal" to "elevated" risk (raw_score 0.3→0.5) is gradual and predictable, while the transition from "elevated" to "rupture" (raw_score 0.7→0.9) is exponential and catastrophic. The sigmoid captures this asymmetry.

**Impact on outputs:**

| Raw score range | v1.0 RAF | v1.1 RAF | Effect |
| --- | --- | --- | --- |
| 0.0 – 0.25 | 1.0 – 3.25 | 1.0 – 2.5 | Dampened (fewer false positives) |
| 0.25 – 0.5 | 3.25 – 5.5 | 2.5 – 5.5 | Similar |
| 0.5 – 0.75 | 5.5 – 7.75 | 5.5 – 8.0 | Slightly amplified |
| 0.75 – 1.0 | 7.75 – 10.0 | 8.0 – 10.0 | Accelerated toward maximum |

The output range [1, 10] is preserved. Monotonicity is preserved. The midpoint (raw=0.5) produces approximately the same RAF under both models.

**Backward compatibility:**

Full. `risk_acceleration_factor` in the API schema is unchanged.

---

## 3. Multi-Horizon Correlation Blending (NON-BREAKING)

**What changed:**

Normal correlation is now a weighted blend of three windows instead of a single 252d window.

```
v1.0:  Corr_normal = corr_252d
v1.1:  Corr_normal = 0.2×corr_21d + 0.3×corr_63d + 0.5×corr_252d
```

Stress blending formula unchanged: `Corr_dynamic = (1-γ)×Corr_normal + γ×Corr_stress`.

**Why:**

A single 252d window lags regime transitions by 3-6 months. During the March 2020 COVID crash, the 252d correlation between IBOV and IFIX showed moderate levels — the stress had already occurred but the window hadn't rotated yet. The 21d component captures recent shifts while the 252d component provides structural anchoring.

NaN handling: if a shorter window has NaN (insufficient data), the remaining windows are renormalized. If all windows are NaN, the engine assumes independence (ρ=0).

**Impact on outputs:**

Portfolio-level RN may change slightly due to the updated correlation matrix. The direction is unpredictable — recent correlation shifts could increase or decrease the blended value. PSD projection is applied after blending, so the output matrix is always valid.

**Backward compatibility:**

Full. Correlation values in the API schema are unchanged in type and semantics.

---

## 4. Proxy Penalty System (ADDITIVE)

**What changed:**

New step in the RN pipeline: proxy-based computation receives a conservative RN uplift.

```
Proxy depth 0 → +0 RN
Proxy depth 1 → +3 RN
Proxy depth 2 → +6 RN
Proxy depth ≥3 → +10 RN

RN_after_proxy = min(99, RN_adjusted + proxy_penalty)
```

**Why:**

Proxy-derived risk metrics systematically underestimate idiosyncratic risk. A fund mapped to IDA-Geral inherits the diversified index's volatility, which is lower than any single debênture. The penalty conservatively compensates for this model risk.

**Impact on outputs:**

Assets with direct data: no change. Assets using proxies: RN increases by 3-10 points depending on proxy chain depth.

**Backward compatibility:**

`risk_number_adjusted` still reflects the RAF-adjusted value (pre-proxy, pre-confidence). The proxy penalty only affects the internal `risk_number_final` used for alignment decisions. API schema unchanged.

---

## 5. Confidence-Aware Risk Adjustment (ADDITIVE)

**What changed:**

Confidence score now multiplicatively adjusts the final Risk Number.

```
HIGH     → ×1.00
MEDIUM   → ×1.05
LOW      → ×1.10
VERY_LOW → ×1.20

RN_final = min(99, RN_after_proxy × confidence_multiplier)
```

**Why:**

A Risk Number computed from 1 year of monthly proxy data and a Risk Number computed from 5 years of daily direct data should NOT carry the same weight in alignment decisions. The multiplier operationalizes the "fail conservative when uncertain" principle that was previously only informational.

**Impact on outputs:**

High-confidence assets: no change. Low-confidence assets: RN increases by 5-20%.

**Backward compatibility:**

Full. `confidence_score` in the API schema remains a string enum. The multiplier is applied internally to produce `risk_number_final`, which is a new internal field not exposed in the external API.

---

## Pipeline Order (v1.1)

```
Step 1: Downside_95_6m = Z × σ_d × √0.5           (pure)
Step 2: RN_base = interpolate(Downside, anchors)    (unchanged)
Step 3: RAF = 1 + 9 × sigmoid(k×(raw−0.5))         (non-linear)
Step 4: RN_adjusted = RN_base × (1+λ×(RAF−1)/9)    (unchanged)
Step 5: RN_after_proxy = RN_adjusted + penalty      (new)
Step 6: RN_final = RN_after_proxy × conf_mult       (new)
```

Audit log captures all intermediate values with version stamps.

---

## Files Changed

| File | Change type |
| --- | --- |
| `config.py` | Updated — new constants, version bumps |
| `risk_number/computer.py` | Updated — removed expected return from downside |
| `raf/aggregator.py` | Updated — sigmoid transformation |
| `raf/adjuster.py` | Updated — trace additions (formula unchanged) |
| `risk_number/proxy_penalty.py` | **New** — proxy penalty system |
| `risk_number/confidence_adjuster.py` | **New** — confidence adjustment |
| `risk_number/pipeline.py` | **New** — orchestrates 6-step pipeline |
| `correlation/dynamic.py` | Updated — multi-horizon blending |
| `tests/test_v1_1_hardening.py` | **New** — 55 tests covering all changes |

---

## Golden Vector Migration

All existing golden vectors must be regenerated under the new RN model. The migration commit must carry the flag:

```
GOLDEN_MIGRATION: RN_MODEL_V2
```

The CI pipeline will reject PRs that change golden outputs without this flag.

---

## Rollback Procedure

If the hardening pass must be rolled back:

1. Set `RN_INCLUDE_EXPECTED_RETURN = True` in config.
2. Set `RAF_TRANSFORMATION_MODE = RAFTransformationMode.LINEAR`.
3. Set `PROXY_PENALTY_TABLE = {0: 0, 1: 0, 2: 0}` and `PROXY_PENALTY_MAX = 0`.
4. Set `CONFIDENCE_MULTIPLIER = {"high": 1.0, "medium": 1.0, "low": 1.0, "very_low": 1.0}`.
5. Regenerate golden vectors with flag `GOLDEN_MIGRATION: ROLLBACK_TO_V1`.

All changes are config-driven. No code changes required for rollback.

---

## Sign-Off

| Role | Name | Sign-off |
| --- | --- | --- |
| COO | João Daniel | ☐ |
| CEO / PM | Diogo Scelza | ☐ |
| CIO | Johnny Zighelboim | ☐ |
| CTO | João Pedro Panizzutti | ☐ |
