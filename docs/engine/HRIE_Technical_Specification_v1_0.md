# HARPIAN RISK INTELLIGENCE ENGINE (HRIE)

**Technical Specification v1.0**

Independent Asset-Level and Portfolio-Level Risk Computation Engine
Companion module to the HRD Engine — Operates with or without AlphaDroid

| Field | Value |
| --- | --- |
| Document version | 1.0.0 |
| Date | April 2026 |
| Prepared for | JP (CTO / Lead Developer), Johnny Zighelboim (CIO) |
| Owner | João Daniel (COO), Diogo Scelza (CEO) |
| Classification | Confidential — Internal Use Only |
| Companion documents | HRD Expansion Technical Specification v1.1, HRIS Conceptual Framework v2 |
| Implementation target | Python 3.11+ backend service, REST + internal SDK |

---

## Table of Contents

1. Executive Summary
2. Scope and Architectural Position
3. System Architecture
4. Module and Repository Structure
5. Domain Model — Canonical Types
6. Data Ingestion Layer
7. Asset Classification Subsystem
8. Statistical Computation Layer
9. Risk Number Computation
10. Risk Acceleration Factor (RAF) Computation
11. Correlation Engine
12. Portfolio Aggregation Layer
13. Confidence Scoring and Provenance
14. Stress Scenarios and Alert Logic
15. Output Contracts (JSON Schemas)
16. Public API and Python SDK
17. Integration Contracts (AlphaDroid, HRD Engine, Terminal)
18. Testing Strategy
19. Performance and Operational Requirements
20. Implementation Roadmap
21. Appendix A — Brazilian Asset Universe Reference Tables
22. Appendix B — Mathematical Definitions Glossary
23. Appendix C — Pseudocode for Critical Algorithms

---

## 1. Executive Summary

### 1.1 Purpose

The Harpian Risk Intelligence Engine (HRIE) is a proprietary, asset-class-agnostic risk computation engine that produces **canonical Harpian risk metrics** — Risk Number (RN), Risk Acceleration Factor (RAF), and the full downside/correlation/drawdown surface — for any asset or portfolio, independently of AlphaDroid availability.

It is the layer that allows Harpian to analyze **real client portfolios as they exist today**, including the Brazilian universe (FIIs, CDBs, LCIs/LCAs, debêntures, multimercados, previdência, COEs, crédito privado, and structured products) which is largely outside the AlphaDroid asset universe.

### 1.2 Why It Must Exist

AlphaDroid is the primary source of return, volatility, and signal data for the Core 11 and Core 22 proprietary strategies. It is, however, optimized for U.S.-listed and globally-traded instruments. The HRD Engine — which orchestrates the four-pillar alignment diagnostic (`RN_appetite`, `RN_capacity`, `RN_requirement`, `RN_portfolio`) — requires `RN_portfolio` to be computed for **any** portfolio a Family Office uploads. Without HRIE:

- The HRD Engine cannot diagnose client portfolios that contain Brazilian local-market assets.
- The platform depends on a single external data source for risk interpretation.
- Stress correlations, regime-conditional behavior, and liquidity penalties are not consistently modeled across the asset universe.

HRIE closes this gap. It functions as **fallback, complement, and independent verifier** of AlphaDroid for risk computation purposes.

### 1.3 Design Principles

| Principle | Implication |
| --- | --- |
| **Downside before volatility** | RN is anchored on `Downside_95_6m`, not on standard deviation. |
| **Regime over snapshot** | Risk metrics carry a base value and a stress-adjusted value (RAF). |
| **Provenance is mandatory** | Every output carries `data_source`, `confidence_score`, and proxy chain. |
| **Compatibility with AlphaDroid** | When AlphaDroid data exists and is fresher, HRIE defers to it but still emits a parallel verification. |
| **Auditability** | Every recommendation is reproducible. The engine is deterministic given the same inputs. |
| **Performance ceilings** | Asset-level computation < 50ms; portfolio-level < 500ms for n ≤ 100 assets. |

### 1.4 Theoretical Foundation

HRIE operationalizes the **Temporal Portfolio Theory (TPT)** quantitative apparatus into deployable code:

- **Boyer-Gibson-Loretan (1999)** — conditional correlation under stress, drives the dynamic correlation blending.
- **GARCH(1,1)** — volatility clustering, drives the volatility acceleration component of RAF.
- **Hidden Markov Models (HMM)** — regime detection, optional layer feeding `regime_instability`.
- **Kalman Filters** — recursive trend estimation under heteroscedastic noise.
- **CVaR / CDaR (Uryasev)** — tail-risk and drawdown-conditional measures used in portfolio aggregation.
- **Milevsky-Robinson Ruin Factor** — optional Destination Risk overlay.

The engine does not implement all of these on day one. The roadmap in §20 distinguishes the v1.0 surface from the v1.1 / v1.2 academic layers.

---

## 2. Scope and Architectural Position

### 2.1 In Scope (v1.0)

- Asset-level risk metrics: returns, volatility, downside deviation, drawdowns, recovery time, Sharpe, Sortino, Calmar, VaR, CVaR.
- Asset-level RN_base and RAF.
- Asset-level RN_adjusted (RAF-penalized).
- Pairwise correlations: rolling, stress-conditional, dynamic blend.
- Portfolio-level aggregation: weighted RN, dynamic covariance, RN_portfolio_adjusted.
- Confidence scoring and proxy chain provenance.
- Alert generation against client commitments and capacity.
- JSON output contracts and REST + Python SDK exposure.

### 2.2 Out of Scope (v1.0 — deferred to v1.1+)

- HMM regime classification (initially fed externally as a flag).
- LPPL (Log-Periodic Power Law) bubble detector.
- Kalman filter trend estimation.
- Live integration with Bloomberg, Economatica, or CVM streaming feeds (v1.0 uses periodic snapshots).
- Prepayment / convexity modeling for credit instruments beyond duration approximations.
- Cross-currency hedge cost decomposition (BRL-hedged asset RN treats hedging cost as a yield haircut, not a stochastic factor).

### 2.3 Boundary with AlphaDroid

```
                ┌─────────────────────────────────────────┐
                │           AlphaDroid (external)         │
                │  Strategy signals, Core 11 / Core 22    │
                │  daily NAV, internal volatility model   │
                └────────────────────┬────────────────────┘
                                     │ snapshot pull
                                     ▼
       ┌─────────────────────────────────────────────────────┐
       │                   HRIE  (this spec)                 │
       │ ┌────────┐  ┌────────────┐  ┌────────────┐          │
       │ │Ingest  │→ │Classify    │→ │ Compute RN │ → output │
       │ └────────┘  └────────────┘  └────────────┘          │
       │      ▲             ▲              ▲                 │
       │      │             │              │                 │
       │  Brazil feeds  Asset Master   RAF + Corr            │
       └──────┬──────────────────────────────┬───────────────┘
              │                              │
              ▼                              ▼
       Market data sources           HRD Engine consumes
       (B3, ANBIMA, CVM,             RN_portfolio +
        Yahoo, Morningstar)          RAF for alignment
```

**Rule of precedence:**

1. If AlphaDroid carries the asset and the data is < 2 trading days stale → AlphaDroid is primary.
2. If AlphaDroid lacks the asset, or data is stale → HRIE is primary.
3. HRIE always produces an independent shadow computation when AlphaDroid is primary, used for audit reconciliation.

### 2.4 Boundary with HRD Engine

The HRD Engine is the **diagnostic and alignment layer**. It computes `RN_appetite`, `RN_capacity`, `RN_requirement`, and orchestrates Reality Check, parser, and UI. HRIE is a **pure computation service** consumed by HRD via:

- `HRIE.compute_asset_risk(asset_input) → AssetRiskOutput`
- `HRIE.compute_portfolio_risk(portfolio_input) → PortfolioRiskOutput`

HRD does not call HRIE internals. HRIE does not know about clients, objectives, or behavioral profiles. The contract is uni-directional and stateless (apart from caching).

---

## 3. System Architecture

### 3.1 Layered Architecture

HRIE is a six-layer pipeline. Each layer has a single responsibility and is independently testable.

| Layer | Responsibility | Stateless? |
| --- | --- | --- |
| L1 — Ingestion | Resolve identifiers, pull price/return history, normalize calendars. | Cache-backed |
| L2 — Classification | Map asset to taxonomy, attach default RAF and proxy chain. | Yes |
| L3 — Statistics | Compute returns, volatility, downside, drawdown, recovery. | Yes |
| L4 — Risk Pricing | Compute `RN_base`, RAF components, `RN_adjusted`. | Yes |
| L5 — Correlation | Compute pairwise rolling, stress, and dynamic correlations. | Yes |
| L6 — Aggregation | Portfolio downside, dynamic covariance, `RN_portfolio_adjusted`, alerts. | Yes |

Statelessness means: given the same `(asset_id, as_of_date, params_hash)`, every layer returns byte-identical output. This is enforced in tests (§18).

### 3.2 Data Flow

```
Asset Input ──▶ L1 Ingest ──▶ L2 Classify ──▶ L3 Statistics ──▶ L4 Risk Pricing
                                                                     │
                                                                     ▼
Portfolio ──▶ (loop assets) ──▶ L5 Correlation ──▶ L6 Aggregation ──▶ Output
```

### 3.3 Deployment Topology

- **Service**: `harpian-hrie` — FastAPI process, Uvicorn workers.
- **Cache**: Redis for asset-level computed metrics (TTL = 1 trading day).
- **Persistence**: PostgreSQL for asset master, proxy registry, golden vectors, audit log.
- **Storage**: S3-compatible bucket for historical price tapes (Parquet partitioned by `asset_class/year`).
- **Dependencies**: NumPy, SciPy, pandas, pyarrow, Pydantic v2. **No** machine-learning libraries in v1.0 — the engine must remain auditable.

---

## 4. Module and Repository Structure

```
harpian/
├── hrie/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py              # FastAPI routes
│   │   └── schemas.py             # Pydantic request/response models
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── resolver.py            # Identifier resolution
│   │   ├── providers/
│   │   │   ├── alphadroid.py
│   │   │   ├── b3.py
│   │   │   ├── anbima.py
│   │   │   ├── yahoo.py
│   │   │   └── manual.py          # Manual override input
│   │   └── normalizer.py          # Calendar + currency normalization
│   ├── classification/
│   │   ├── __init__.py
│   │   ├── taxonomy.py            # AssetClass enum, definitions
│   │   ├── classifier.py          # Asset → AssetClass routing
│   │   ├── proxy_registry.py      # Proxy index lookup
│   │   └── raf_defaults.py        # Default RAF by class
│   ├── statistics/
│   │   ├── __init__.py
│   │   ├── returns.py
│   │   ├── volatility.py
│   │   ├── downside.py
│   │   ├── drawdown.py
│   │   └── ratios.py              # Sharpe, Sortino, Calmar, VaR, CVaR
│   ├── risk_number/
│   │   ├── __init__.py
│   │   ├── anchors.py             # RN anchor table
│   │   ├── computer.py            # downside → RN_base
│   │   └── interpolator.py
│   ├── raf/
│   │   ├── __init__.py
│   │   ├── components.py          # 5 sub-scores
│   │   ├── aggregator.py          # weighted RAF_raw → RAF
│   │   └── adjuster.py            # RN_base → RN_adjusted
│   ├── correlation/
│   │   ├── __init__.py
│   │   ├── rolling.py
│   │   ├── stress.py
│   │   └── dynamic.py             # Blending engine
│   ├── portfolio/
│   │   ├── __init__.py
│   │   ├── covariance.py
│   │   ├── aggregator.py
│   │   └── contributors.py        # Risk attribution
│   ├── scoring/
│   │   ├── __init__.py
│   │   └── confidence.py
│   ├── alerts/
│   │   ├── __init__.py
│   │   └── rules.py
│   ├── contracts/
│   │   ├── __init__.py
│   │   ├── inputs.py              # Pydantic input models
│   │   ├── outputs.py             # Pydantic output models
│   │   └── errors.py
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── hrd_adapter.py         # HRIE ↔ HRD Engine bridge
│   │   └── alphadroid_adapter.py
│   ├── persistence/
│   │   ├── __init__.py
│   │   ├── asset_master.py
│   │   ├── cache.py
│   │   └── audit_log.py
│   └── config.py
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── golden_vectors/
│   └── property/
└── pyproject.toml
```

---

## 5. Domain Model — Canonical Types

All public types live in `harpian.hrie.contracts`. They are Pydantic v2 models for API surfaces and `@dataclass(frozen=True)` for internal computation.

### 5.1 Asset Identity

```python
from enum import Enum
from typing import Optional, List
from decimal import Decimal
from datetime import date
from pydantic import BaseModel, Field


class AssetIdentifier(BaseModel):
    """All known identifiers for an asset. At least one required."""

    isin: Optional[str] = None
    cusip: Optional[str] = None
    ticker: Optional[str] = None
    sedol: Optional[str] = None
    cnpj: Optional[str] = None              # Brazilian fund identifier
    anbima_code: Optional[str] = None
    cetip_code: Optional[str] = None        # Fixed income BR
    internal_id: Optional[str] = None       # Manual override
    raw_name: str                           # Always required

    def primary_key(self) -> str:
        for k in (self.isin, self.cnpj, self.cetip_code,
                  self.anbima_code, self.ticker, self.cusip,
                  self.sedol, self.internal_id):
            if k:
                return k
        return self.raw_name.lower().strip()
```

### 5.2 Asset Class Taxonomy

```python
class AssetClass(str, Enum):
    CASH                          = "cash"
    FIXED_INCOME_POST_FIXED       = "fixed_income_post_fixed"
    FIXED_INCOME_INFLATION_LINKED = "fixed_income_inflation_linked"
    FIXED_INCOME_PRE_FIXED        = "fixed_income_pre_fixed"
    PRIVATE_CREDIT                = "private_credit"
    REAL_ESTATE_FUND_PAPER        = "real_estate_fund_paper"
    REAL_ESTATE_FUND_BRICK        = "real_estate_fund_brick"
    EQUITY_INDEX                  = "equity_index"
    EQUITY_SECTOR                 = "equity_sector"
    EQUITY_FACTOR                 = "equity_factor"
    SMALL_CAPS                    = "small_caps"
    MULTIMARKET_MACRO             = "multimarket_macro"
    MULTIMARKET_QUANT             = "multimarket_quant"
    PENSION_FUND                  = "pension_fund"
    INTERNATIONAL_EQUITY          = "international_equity"
    GOLD                          = "gold"
    STRUCTURED_PRODUCT            = "structured_product"
    ALTERNATIVE                   = "alternative"
    CRYPTO                        = "crypto"
    UNKNOWN                       = "unknown"
```

### 5.3 Market Data Bundle

```python
class MarketDataFrequency(str, Enum):
    DAILY     = "daily"
    WEEKLY    = "weekly"
    MONTHLY   = "monthly"
    QUARTERLY = "quarterly"
    ANNUAL    = "annual"


class MarketDataBundle(BaseModel):
    """Normalized historical data for a single asset."""

    asset_id: str
    frequency: MarketDataFrequency
    currency: str = "BRL"
    as_of: date
    prices: List[Decimal]           # NAV / close price series
    dates: List[date]               # Aligned with prices
    dividend_or_coupon: Optional[List[Decimal]] = None
    benchmark_returns: Optional[List[Decimal]] = None
    source: str                     # "alphadroid" | "b3" | "anbima" | ...
    proxy_chain: List[str] = Field(default_factory=list)
```

### 5.4 Asset Risk Output

```python
class DataSource(str, Enum):
    ALPHADROID  = "alphadroid"
    MARKET_DATA = "market_data"
    PROXY       = "proxy"
    PEER_GROUP  = "peer_group"
    DEFAULT     = "asset_class_default"
    MANUAL      = "manual"


class ConfidenceLevel(str, Enum):
    HIGH      = "high"
    MEDIUM    = "medium"
    LOW       = "low"
    VERY_LOW  = "very_low"


class AssetRiskOutput(BaseModel):
    asset_id: str
    asset_name: str
    asset_class: AssetClass
    currency: str
    as_of: date

    # Returns
    annualized_return: float
    expected_return_annual: float

    # Volatility / downside
    annualized_volatility: float
    downside_deviation: float

    # Drawdown
    max_drawdown: float
    average_drawdown: float
    recovery_time_days: int
    rolling_drawdown_max_252d: float

    # Ratios
    sharpe_ratio: float
    sortino_ratio: float
    calmar_ratio: float
    var_95_6m: float
    cvar_95_6m: float

    # Correlations to canonical references
    correlation_to_ibov: float
    correlation_to_cdi: float
    correlation_to_sp500: float
    correlation_to_usdbrl: float

    # Risk pricing
    risk_number_base: int          # 1..99
    risk_acceleration_factor: float  # 1..10
    risk_number_adjusted: int      # 1..99

    # RAF decomposition
    raf_volatility_acceleration: float
    raf_correlation_expansion: float
    raf_liquidity_stress: float
    raf_macro_sensitivity: float
    raf_drawdown_convexity: float

    # Provenance
    data_source: DataSource
    proxy_chain: List[str]
    confidence_score: ConfidenceLevel
    data_points_used: int
    history_years: float
```

### 5.5 Portfolio Input and Output

```python
class PortfolioPosition(BaseModel):
    asset: AssetIdentifier
    weight: float                  # 0..1, must sum to 1.0 ± 0.02
    market_value: Optional[Decimal] = None
    currency: str = "BRL"


class PortfolioInput(BaseModel):
    portfolio_id: str
    positions: List[PortfolioPosition]
    base_currency: str = "BRL"
    as_of: date
    benchmark: str = "CDI"


class PortfolioRiskOutput(BaseModel):
    portfolio_id: str
    as_of: date

    portfolio_return_expected: float
    portfolio_volatility: float
    portfolio_downside_deviation: float
    portfolio_max_drawdown_estimated: float

    portfolio_risk_number_base: int
    portfolio_raf: float
    portfolio_risk_number_adjusted: int

    dominant_risk_contributors: List["RiskContribution"]
    correlation_clusters: List["CorrelationCluster"]
    stress_scenario_results: dict   # see §14
    alerts: List["Alert"]
    confidence_score: ConfidenceLevel

    asset_breakdown: List[AssetRiskOutput]
```

---

## 6. Data Ingestion Layer

### 6.1 Source Hierarchy

The ingestion resolver must traverse sources in this strict order, recording every fallback in the proxy chain:

| Priority | Source | Coverage | Latency target |
| --- | --- | --- | --- |
| 1 | AlphaDroid snapshot | U.S./global listed instruments | < 24h stale |
| 2 | B3 / market data feed | Brazilian listed equities, FIIs, ETFs | EOD |
| 3 | ANBIMA | Indices, fund performance | T+1 |
| 4 | CVM | Fund holdings, regulatory returns | Monthly |
| 5 | Yahoo / Morningstar / Economatica | Backup for international | EOD |
| 6 | Proxy index | When asset unmatched | Variable |
| 7 | Peer group average | When proxy index missing | Variable |
| 8 | Asset-class default assumptions | Last resort before manual | N/A |
| 9 | Manual Harpian classification | Operator override | N/A |

### 6.2 Ingestion Contract

```python
class IngestionRequest(BaseModel):
    identifier: AssetIdentifier
    history_years_required: float = 3.0
    frequency_preferred: MarketDataFrequency = MarketDataFrequency.DAILY


class IngestionResult(BaseModel):
    bundle: Optional[MarketDataBundle]
    actual_source: DataSource
    proxy_chain: List[str]
    history_years_actual: float
    warnings: List[str]
```

### 6.3 Calendar and Currency Normalization

- All dates are normalized to **B3 trading calendar** when the asset is BRL-quoted.
- Dual-currency assets (e.g., S&P 500 in BRL) require synthetic series: USD price × USD/BRL FX rate, with explicit FX rolldown handling.
- Missing data points: forward-fill is **prohibited**; the engine flags gaps > 5 trading days and lowers `confidence_score`.
- Frequency downsampling is allowed (daily → monthly), upsampling is not.

### 6.4 Brazilian-Specific Identifier Resolution

For each Brazilian asset class, the resolver must attempt a specific identifier strategy:

| Asset class | Primary identifier | Secondary | Tertiary |
| --- | --- | --- | --- |
| FII | Ticker (e.g., `KNRI11`) | CNPJ | Anbima code |
| CDB | Issuer + maturity + index | CETIP | — |
| Debênture | CETIP / B3 ticker | CNPJ issuer | — |
| Fundo (multimercado, previdência) | CNPJ | Anbima code | — |
| Tesouro | Anbima code (e.g., `LFT 030328`) | — | — |
| ETF BR | Ticker (`IVVB11`) | CNPJ | — |

If primary fails, the resolver downgrades to secondary and records `proxy_chain.append("identifier:secondary")`.

---

## 7. Asset Classification Subsystem

### 7.1 Classification Routing

The classifier is a deterministic rule engine. There is **no ML classifier in v1.0** — the goal is auditability. Routing rules in priority order:

1. **Identifier prefix rules** (e.g., FII tickers ending in `11`, fund names containing "Previdência").
2. **CNPJ → ANBIMA category** lookup for Brazilian funds.
3. **Issuer + instrument type** for fixed income.
4. **Heuristic name matching** with a controlled vocabulary.
5. **Operator override** (manual tagging in the asset master).
6. Fallback: `AssetClass.UNKNOWN` (will fail closed in §13 confidence scoring).

### 7.2 Default RAF by Asset Class

Defaults inherit from the Brazilian quantitative analysis (Appendix A). They are used **only** when bottom-up RAF computation is infeasible (e.g., insufficient history). When history exists, the bottom-up RAF (§10) overrides the default; the default then serves as a sanity bound.

```python
DEFAULT_RAF: dict[AssetClass, float] = {
    AssetClass.CASH:                          1.0,
    AssetClass.FIXED_INCOME_POST_FIXED:       1.0,
    AssetClass.FIXED_INCOME_INFLATION_LINKED: 4.5,
    AssetClass.FIXED_INCOME_PRE_FIXED:        4.0,
    AssetClass.PRIVATE_CREDIT:                3.0,
    AssetClass.REAL_ESTATE_FUND_PAPER:        2.5,
    AssetClass.REAL_ESTATE_FUND_BRICK:        6.0,
    AssetClass.EQUITY_INDEX:                  7.0,
    AssetClass.EQUITY_SECTOR:                 6.5,
    AssetClass.EQUITY_FACTOR:                 4.5,
    AssetClass.SMALL_CAPS:                    9.0,
    AssetClass.MULTIMARKET_MACRO:             5.0,
    AssetClass.MULTIMARKET_QUANT:             6.0,
    AssetClass.PENSION_FUND:                  4.0,
    AssetClass.INTERNATIONAL_EQUITY:          5.5,
    AssetClass.GOLD:                          3.0,
    AssetClass.STRUCTURED_PRODUCT:            2.5,
    AssetClass.ALTERNATIVE:                   7.0,
    AssetClass.CRYPTO:                       10.0,
    AssetClass.UNKNOWN:                       7.0,  # fail-conservative
}
```

### 7.3 Proxy Registry

For each asset class, the registry defines the canonical proxy index used when the asset itself lacks history. Maintained as a versioned database table:

| Asset class | Proxy index (BRL) | Min history req. |
| --- | --- | --- |
| FIXED_INCOME_POST_FIXED | CDI | 3y |
| FIXED_INCOME_INFLATION_LINKED (long) | IMA-B | 5y |
| FIXED_INCOME_INFLATION_LINKED (short) | IMA-B 5 | 3y |
| PRIVATE_CREDIT | IDA-Geral | 3y |
| REAL_ESTATE_FUND_PAPER | IFIX Papel proxy | 3y |
| REAL_ESTATE_FUND_BRICK | IFIX | 5y |
| EQUITY_INDEX | IBOV | 10y |
| EQUITY_FACTOR (low vol) | CAPE11 | 3y |
| EQUITY_FACTOR (dividend) | NDIV11 / IDIV | 3y |
| SMALL_CAPS | SMLL | 5y |
| INTERNATIONAL_EQUITY (US) | IVVB11 | 5y |
| GOLD | GOLD11 / OZ1D | 5y |
| MULTIMARKET_MACRO | IHFA | 5y |
| PENSION_FUND | Fund-class median | 3y |

When a proxy is used, `proxy_chain.append(f"proxy:{index_name}")` and `confidence_score` is degraded (§13).

---

## 8. Statistical Computation Layer

### 8.1 Returns

```python
def simple_return(p_t: float, p_t_minus_1: float) -> float:
    return (p_t / p_t_minus_1) - 1.0

def log_return(p_t: float, p_t_minus_1: float) -> float:
    return math.log(p_t / p_t_minus_1)

def cagr(p_start: float, p_end: float, years: float) -> float:
    return (p_end / p_start) ** (1.0 / years) - 1.0
```

Returns are computed on **total-return series** (NAV + reinvested distributions for funds; price + dividend for equities). For instruments without dividend data (most BR funds), the engine uses the published quotation series and flags the limitation.

### 8.2 Volatility

Annualization factor depends on frequency:

| Frequency | √(periods/yr) |
| --- | --- |
| Daily | √252 |
| Weekly | √52 |
| Monthly | √12 |
| Quarterly | √4 |
| Annual | 1 |

```python
def annualized_volatility(returns: np.ndarray, freq: MarketDataFrequency) -> float:
    factor = {
        MarketDataFrequency.DAILY:     math.sqrt(252),
        MarketDataFrequency.WEEKLY:    math.sqrt(52),
        MarketDataFrequency.MONTHLY:   math.sqrt(12),
        MarketDataFrequency.QUARTERLY: math.sqrt(4),
        MarketDataFrequency.ANNUAL:    1.0,
    }[freq]
    return float(np.std(returns, ddof=1) * factor)
```

### 8.3 Downside Deviation

`MAR` (Minimum Acceptable Return) defaults to **CDI** for BR portfolios, **3-month Treasury** for USD portfolios. Configurable per call.

```python
def downside_deviation(returns: np.ndarray, mar: float, freq: MarketDataFrequency) -> float:
    excess = returns - mar
    downside = np.minimum(excess, 0.0)
    factor = annualization_factor(freq)
    return float(math.sqrt(np.mean(downside ** 2)) * math.sqrt(factor))
```

### 8.4 Drawdown

```python
def drawdown_series(prices: np.ndarray) -> np.ndarray:
    running_max = np.maximum.accumulate(prices)
    return (prices / running_max) - 1.0

def max_drawdown(prices: np.ndarray) -> float:
    return float(np.min(drawdown_series(prices)))

def recovery_time_days(prices: np.ndarray, dates: list[date]) -> int:
    dd = drawdown_series(prices)
    trough_idx = int(np.argmin(dd))
    pre_trough_peak = prices[:trough_idx + 1].max()
    post = prices[trough_idx:]
    recovered_idx = np.argmax(post >= pre_trough_peak)
    if recovered_idx == 0 and post[0] < pre_trough_peak:
        return -1   # Not yet recovered
    return (dates[trough_idx + int(recovered_idx)] - dates[trough_idx]).days
```

### 8.5 Ratios

```python
def sharpe(ret_ann: float, vol_ann: float, rf: float) -> float:
    return (ret_ann - rf) / vol_ann if vol_ann > 0 else 0.0

def sortino(ret_ann: float, downside_dev: float, mar: float) -> float:
    return (ret_ann - mar) / downside_dev if downside_dev > 0 else 0.0

def calmar(ret_ann: float, max_dd: float) -> float:
    return ret_ann / abs(max_dd) if max_dd < 0 else 0.0
```

### 8.6 VaR and CVaR (6-month, 95%)

Historical method (preferred when ≥ 5y of data):

```python
def var_95_6m(returns_6m_overlapping: np.ndarray) -> float:
    return float(np.percentile(returns_6m_overlapping, 5))

def cvar_95_6m(returns_6m_overlapping: np.ndarray) -> float:
    threshold = var_95_6m(returns_6m_overlapping)
    tail = returns_6m_overlapping[returns_6m_overlapping <= threshold]
    return float(tail.mean()) if len(tail) > 0 else threshold
```

Parametric fallback (Cornish-Fisher with skewness and kurtosis adjustment) when history is < 5y. The chosen method is recorded in the output payload.

---

## 9. Risk Number Computation

### 9.1 Definition

The Risk Number (RN) is an integer in `[1, 99]` representing the **expected 6-month downside at 95% confidence**, mapped through a calibrated anchor table.

### 9.2 Downside Estimate

```
Downside_95_6m = max( 0, Z_95 × downside_deviation × √0.5 − expected_return_6m )

where:
  Z_95              = 1.645
  downside_dev      = annualized downside deviation (§8.3)
  expected_return   = annualized expected return
  expected_return_6m = expected_return / 2
```

The `max(0, ...)` clamp prevents negative downside estimates when expected return dominates.

### 9.3 Anchor Table

```python
RN_ANCHORS: list[tuple[float, int]] = [
    (0.02,  22),   # 2.00%  → RN 22
    (0.05,  32),   # 5.00%  → RN 32
    (0.07,  42),   # 7.00%  → RN 42
    (0.12,  62),   # 12.00% → RN 62
    (0.18,  82),   # 18.00% → RN 82
    (0.2742, 91),  # 27.42% → RN 91
]
```

Below 2% downside the engine extrapolates linearly to `(0.0, 1)`. Above 27.42% it caps at `RN = 99`.

### 9.4 Linear Interpolation

```python
def map_downside_to_rn(downside: float) -> int:
    if downside <= 0:
        return 1
    if downside >= RN_ANCHORS[-1][0]:
        return 99
    for i in range(1, len(RN_ANCHORS)):
        d_lo, rn_lo = RN_ANCHORS[i-1]
        d_hi, rn_hi = RN_ANCHORS[i]
        if downside <= d_hi:
            ratio = (downside - d_lo) / (d_hi - d_lo)
            rn = rn_lo + ratio * (rn_hi - rn_lo)
            return int(max(1, min(99, round(rn))))
    return 99
```

### 9.5 Reproducibility Constraint

Every call must store `(downside_input, anchor_table_version, output_rn)` in the audit log. Anchor changes require a versioned migration; no silent recalibration.

---

## 10. Risk Acceleration Factor (RAF) Computation

### 10.1 Definition

The RAF is a float in `[1, 10]` capturing how rapidly an asset's risk profile expands under regime stress. It is **not** a measure of current risk — it is a measure of regime sensitivity.

### 10.2 Component Model

```
RAF_raw = β1·VolAccel + β2·CorrExpansion + β3·LiquidityStress + β4·MacroSensitivity + β5·DrawdownConvexity

Default weights (v1.0):
  β1 = 0.30  (Volatility Acceleration)
  β2 = 0.25  (Correlation Expansion)
  β3 = 0.20  (Liquidity Stress)
  β4 = 0.10  (Macro Sensitivity)
  β5 = 0.15  (Drawdown Convexity)
```

The weights live in `harpian.hrie.config` and are versioned. Re-weighting is a controlled change.

### 10.3 Component Definitions

**Volatility Acceleration**

```
VolAccel = vol_21d_realized / vol_252d_realized
clamped to [0.5, 4.0], then normalized:
  VolAccel_norm = clip( (VolAccel - 0.5) / 3.5, 0, 1 )
```

**Correlation Expansion**

```
CorrExpansion = ρ_stress − ρ_normal

where:
  ρ_stress = mean pairwise correlation against the asset's class index
              computed on days where IBOV (or equivalent) return < 10th percentile
  ρ_normal = mean pairwise correlation on remaining days
clamped to [0, 1] (negative values floored to 0)
```

**Liquidity Stress**

For listed assets:

```
LiquidityStress = z_score(bid_ask_spread_21d)
                + z_score(volume_drop_21d_vs_252d)
normalized to [0, 1] via logistic squash
```

For fund vehicles (no order book):

```
LiquidityStress_fund = 0.4·redemption_period_score
                    + 0.3·asset_liquidity_score
                    + 0.3·concentration_score

redemption_period_score:
  D+0       → 0.0
  D+1..3    → 0.2
  D+4..30   → 0.6
  D+30+     → 0.9
  closed-end → 1.0
```

**Macro Sensitivity**

```
MacroSensitivity = beta_to_selic_change + beta_to_usdbrl_change
clamped to [0, 1]
```

Computed via regression of asset returns on Selic and USD/BRL daily changes over a 504-day window.

**Drawdown Convexity**

```
DrawdownConvexity = recent_dd_speed / historical_dd_speed
where:
  recent_dd_speed       = |drawdown_21d| / 21
  historical_dd_speed   = mean( |dd_window_i| / duration_i )

clamped and normalized to [0, 1]
```

### 10.4 Aggregation

```python
def compute_raf(components: RAFComponents) -> float:
    raw = (0.30 * components.vol_accel
         + 0.25 * components.corr_expansion
         + 0.20 * components.liquidity_stress
         + 0.10 * components.macro_sensitivity
         + 0.15 * components.drawdown_convexity)
    raf = 1.0 + 9.0 * raw   # raw is in [0, 1] → raf in [1, 10]
    return round(max(1.0, min(10.0, raf)), 2)
```

### 10.5 RN Adjustment

```
RN_adjusted = min(99, RN_base × (1 + λ × ((RAF − 1) / 9)))

λ = 0.35  (default systemic penalty intensity)
```

Rationale: at RAF = 10 the upward shift is 35%; at RAF = 1 there is no shift. The cap at 99 prevents overflow.

### 10.6 Sanity Bounds vs Default

If the bottom-up RAF deviates from the asset-class default by more than ±3.0 points, the engine emits a warning `raf_outlier` and lowers confidence. The bottom-up value is still used — outliers are surfaced, not suppressed.

---

## 11. Correlation Engine

### 11.1 Rolling Correlations

Computed in four windows: 21d, 63d, 126d, 252d. The portfolio aggregator (§12) defaults to 252d for stability and 63d as the secondary signal.

```python
def rolling_correlation(returns_a, returns_b, window: int) -> np.ndarray:
    return pd.Series(returns_a).rolling(window).corr(pd.Series(returns_b)).values
```

### 11.2 Stress Correlations

Stress correlation is computed only on days where the **systemic benchmark** (configurable; default IBOV for BRL portfolios, S&P 500 for USD) returned below its 10th percentile over the lookback window.

```python
def stress_correlation(returns_a, returns_b, benchmark_returns, lookback: int = 1260) -> float:
    threshold = np.percentile(benchmark_returns[-lookback:], 10)
    mask = benchmark_returns >= threshold       # invert: keep only stress days
    mask = ~mask
    if mask.sum() < 30:
        return float("nan")  # insufficient stress observations
    return float(np.corrcoef(returns_a[mask], returns_b[mask])[0, 1])
```

### 11.3 Dynamic Correlation Blending

The correlation matrix used in portfolio aggregation is a **weighted blend** between normal and stress matrices, where the weight is a function of the portfolio-level RAF:

```
γ = portfolio_systemic_RAF / 10
Σ_dynamic = (1 − γ) · Σ_normal + γ · Σ_stress
```

This formalizes the Boyer-Loretan insight: as systemic risk accelerates, the effective correlation matrix migrates toward the stress regime — diversification benefits decay continuously rather than collapsing discretely.

### 11.4 Positive Semi-Definiteness

Blended matrices are not guaranteed PSD. The engine applies **nearest-PSD projection** (Higham, 2002):

```python
from scipy.linalg import eigh

def nearest_psd(matrix: np.ndarray) -> np.ndarray:
    sym = (matrix + matrix.T) / 2
    eigvals, eigvecs = eigh(sym)
    eigvals_clipped = np.clip(eigvals, 0, None)
    return eigvecs @ np.diag(eigvals_clipped) @ eigvecs.T
```

---

## 12. Portfolio Aggregation Layer

### 12.1 Inputs

```python
class PortfolioAggregationInput(BaseModel):
    weights: list[float]
    asset_outputs: list[AssetRiskOutput]
    correlation_matrix_normal: np.ndarray
    correlation_matrix_stress: np.ndarray
    portfolio_systemic_raf: float
```

`portfolio_systemic_raf` is the weighted average of asset RAFs plus a systemic overlay (§12.5).

### 12.2 Dynamic Covariance

```
D_vol = diag(σ_1, σ_2, ..., σ_n)         # asset annualized volatilities
Σ_dynamic = D_vol · Corr_dynamic · D_vol   (then nearest-PSD)
```

### 12.3 Portfolio Volatility

```
σ_portfolio = √(w^T · Σ_dynamic · w)
```

### 12.4 Portfolio Downside

A naive aggregation of individual downsides understates diversification. The engine uses a **weighted downside deviation** with the same dynamic covariance:

```python
def portfolio_downside_deviation(weights, asset_downsides, sigma_dynamic) -> float:
    # Downside volatility scaling using semivariance pseudo-matrix
    D_dd = np.diag(asset_downsides)
    # Use the same correlation structure as full covariance
    # since asymmetric correlation under stress is captured in sigma_dynamic
    semivar_matrix = D_dd @ sigma_dynamic_normalized @ D_dd
    return float(math.sqrt(weights.T @ semivar_matrix @ weights))
```

`sigma_dynamic_normalized` is `sigma_dynamic` divided element-wise by `D_vol @ D_vol.T` so the off-diagonals stay in correlation form.

### 12.5 Portfolio RAF

```
RAF_portfolio = Σ(w_i · RAF_i) + systemic_overlay

systemic_overlay logic:
  - If concentration HHI > 0.30: +0.5
  - If foreign currency exposure > 40%: +0.3
  - If correlation cluster > 0.85 between top-3 weights: +0.5
  - Otherwise: 0.0
```

Concentration HHI = Σ(w_i²). The overlay caps `RAF_portfolio` at 10.

### 12.6 Portfolio Risk Number

```
Downside_portfolio = Z_95 · σ_downside_portfolio · √0.5 − expected_return_portfolio_6m

RN_portfolio_base = map_downside_to_rn(Downside_portfolio)
RN_portfolio_adjusted = min(99, RN_portfolio_base × (1 + λ × ((RAF_portfolio − 1) / 9)))
```

### 12.7 Risk Contribution

```python
class RiskContribution(BaseModel):
    asset_id: str
    weight: float
    marginal_contribution_to_vol: float
    contribution_pct: float           # share of total portfolio variance
    raf: float
    flag: Optional[str]               # "concentration", "correlation_cluster", etc.
```

Marginal contribution:

```
MCR_i = (Σ · w)_i / σ_p
contribution_i = w_i · MCR_i / σ_p     (sums to 1.0)
```

### 12.8 Correlation Clusters

The engine performs hierarchical clustering on the dynamic correlation matrix (single-linkage, distance = 1 − |ρ|) and reports clusters with mean intra-cluster correlation > 0.7. Clusters are surfaced as risk contributors.

---

## 13. Confidence Scoring and Provenance

### 13.1 Confidence Score Formula

```python
def confidence_score(
    history_years: float,
    frequency: MarketDataFrequency,
    proxy_chain_depth: int,
    liquidity_quality: float,
    data_source: DataSource,
) -> ConfidenceLevel:
    base = 0.0

    # History
    if history_years >= 5:    base += 0.40
    elif history_years >= 3:  base += 0.30
    elif history_years >= 1:  base += 0.15
    else:                     base += 0.05

    # Frequency
    if frequency == MarketDataFrequency.DAILY:    base += 0.25
    elif frequency == MarketDataFrequency.WEEKLY: base += 0.18
    elif frequency == MarketDataFrequency.MONTHLY: base += 0.12
    else:                                          base += 0.05

    # Proxy depth penalty
    base -= 0.05 * proxy_chain_depth

    # Liquidity quality (0..1)
    base += 0.20 * liquidity_quality

    # Source
    if data_source in (DataSource.ALPHADROID, DataSource.MARKET_DATA):
        base += 0.15
    elif data_source == DataSource.PROXY:
        base += 0.05
    else:
        base += 0.0

    base = max(0.0, min(1.0, base))

    if base >= 0.80: return ConfidenceLevel.HIGH
    if base >= 0.55: return ConfidenceLevel.MEDIUM
    if base >= 0.30: return ConfidenceLevel.LOW
    return ConfidenceLevel.VERY_LOW
```

### 13.2 Provenance Record

Every `AssetRiskOutput` carries a fully traceable provenance record. Audit log entries include:

- Asset identifier resolution path
- Each source attempted and its outcome
- Anchor table version
- RAF weights version
- Computation timestamp and engine version

The audit log is append-only and cryptographically hashed (chain hash per asset_id) for institutional defensibility.

### 13.3 Effect on Output

`VERY_LOW` confidence triggers an automatic alert (§14) and prevents the asset from being used as a primary signal in HRD Engine alignment decisions. The HRD layer can still display the metric but must mark it visually.

---

## 14. Stress Scenarios and Alert Logic

### 14.1 Built-in Stress Scenarios

```python
STRESS_SCENARIOS = {
    "br_fiscal_crisis": {
        "shocks": {
            "ibov":   -0.30,
            "imab":   -0.18,
            "ifix":   -0.25,
            "usdbrl": +0.20,
        },
        "correlation_overlay": "stress",
    },
    "global_recession": {
        "shocks": {"sp500": -0.35, "ibov": -0.25, "gold": +0.15, "usdbrl": +0.15},
        "correlation_overlay": "stress",
    },
    "rate_shock_up": {
        "shocks": {"imab": -0.15, "fii_brick": -0.18, "equity": -0.10},
        "correlation_overlay": "normal",
    },
    "br_political_event": {
        "shocks": {"ibov": -0.20, "usdbrl": +0.12, "imab": -0.10},
        "correlation_overlay": "stress",
    },
}
```

For each scenario the portfolio is repriced and an `EstimatedDrawdown` is reported alongside the base RN. v1.0 uses linear shock propagation; non-linear repricing (Greeks for COEs) is deferred to v1.1.

### 14.2 Alert Rules

```python
def evaluate_alerts(asset_or_portfolio: AssetRiskOutput | PortfolioRiskOutput,
                   client_context: Optional[ClientContext]) -> list[Alert]:
    alerts = []

    if asset_or_portfolio.risk_number_adjusted - asset_or_portfolio.risk_number_base > 15:
        alerts.append(Alert("risk_acceleration_detected", severity="medium"))

    if asset_or_portfolio.risk_acceleration_factor >= 8.0:
        alerts.append(Alert("regime_rupture_risk", severity="high"))

    if hasattr(asset_or_portfolio, "stress_scenario_results"):
        worst_dd = min(
            r["estimated_drawdown"]
            for r in asset_or_portfolio.stress_scenario_results.values()
        )
        if client_context and abs(worst_dd) > client_context.behavioral_tolerance:
            alerts.append(Alert("portfolio_exceeds_behavioral_tolerance", severity="high"))

    if client_context:
        if client_context.rn_requirement > client_context.rn_capacity:
            alerts.append(Alert("destination_risk_mismatch", severity="critical"))
        if asset_or_portfolio.risk_number_adjusted > client_context.target_rn:
            alerts.append(Alert("portfolio_misaligned_with_client_rn", severity="high"))

    return alerts
```

### 14.3 Alert Schema

```python
class Alert(BaseModel):
    code: str
    severity: Literal["info", "low", "medium", "high", "critical"]
    message: str
    detail: dict
    triggered_at: datetime
```

---

## 15. Output Contracts (JSON Schemas)

### 15.1 Asset-Level Output (canonical)

```json
{
  "asset_id": "PATL11",
  "asset_name": "Pátria Logística FII",
  "asset_class": "real_estate_fund_brick",
  "currency": "BRL",
  "as_of": "2026-04-25",
  "annualized_return": 0.4878,
  "expected_return_annual": 0.18,
  "annualized_volatility": 0.124,
  "downside_deviation": 0.078,
  "max_drawdown": -0.145,
  "average_drawdown": -0.034,
  "recovery_time_days": 142,
  "rolling_drawdown_max_252d": -0.108,
  "sharpe_ratio": 1.92,
  "sortino_ratio": 2.85,
  "calmar_ratio": 3.36,
  "var_95_6m": -0.082,
  "cvar_95_6m": -0.114,
  "correlation_to_ibov": 0.45,
  "correlation_to_cdi": -0.08,
  "correlation_to_sp500": 0.12,
  "correlation_to_usdbrl": -0.18,
  "risk_number_base": 48,
  "risk_acceleration_factor": 5.2,
  "risk_number_adjusted": 56,
  "raf_volatility_acceleration": 0.62,
  "raf_correlation_expansion": 0.41,
  "raf_liquidity_stress": 0.30,
  "raf_macro_sensitivity": 0.55,
  "raf_drawdown_convexity": 0.48,
  "data_source": "market_data",
  "proxy_chain": [],
  "confidence_score": "high",
  "data_points_used": 1260,
  "history_years": 5.0
}
```

### 15.2 Portfolio-Level Output

```json
{
  "portfolio_id": "FO_CARTEIRA_001",
  "as_of": "2026-04-25",
  "portfolio_return_expected": 0.142,
  "portfolio_volatility": 0.088,
  "portfolio_downside_deviation": 0.054,
  "portfolio_max_drawdown_estimated": -0.118,
  "portfolio_risk_number_base": 42,
  "portfolio_raf": 5.4,
  "portfolio_risk_number_adjusted": 50,
  "dominant_risk_contributors": [
    {"asset_id": "SMAL11", "weight": 0.18, "contribution_pct": 0.34, "raf": 9.0,
     "flag": "concentration"}
  ],
  "correlation_clusters": [
    {"members": ["KNRI11", "HSML11", "PATL11"], "mean_correlation": 0.78}
  ],
  "stress_scenario_results": {
    "br_fiscal_crisis": {"estimated_drawdown": -0.215, "rn_under_stress": 78},
    "global_recession":  {"estimated_drawdown": -0.158, "rn_under_stress": 68}
  },
  "alerts": [
    {"code": "regime_rupture_risk", "severity": "high",
     "message": "Portfolio RAF 5.4 ; one constituent at RAF 9.0"}
  ],
  "confidence_score": "medium",
  "asset_breakdown": ["...AssetRiskOutput[]..."]
}
```

---

## 16. Public API and Python SDK

### 16.1 REST Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/hrie/v1/asset/risk` | Compute risk for a single asset |
| POST | `/hrie/v1/portfolio/risk` | Compute risk for a portfolio |
| POST | `/hrie/v1/portfolio/stress` | Run stress scenarios on a portfolio |
| GET | `/hrie/v1/asset/{id}/provenance` | Return provenance trace |
| GET | `/hrie/v1/health` | Health probe |
| GET | `/hrie/v1/version` | Engine + anchor + RAF weight versions |

### 16.2 Python SDK

```python
from harpian.hrie import HRIEClient

client = HRIEClient(base_url="http://hrie.internal", api_key=...)

# Single asset
output = client.compute_asset_risk(
    identifier=AssetIdentifier(ticker="PATL11", raw_name="Pátria Logística FII"),
    as_of=date.today(),
)

# Portfolio
portfolio_output = client.compute_portfolio_risk(
    portfolio=PortfolioInput(
        portfolio_id="demo",
        positions=[
            PortfolioPosition(asset=..., weight=0.30),
            PortfolioPosition(asset=..., weight=0.40),
            PortfolioPosition(asset=..., weight=0.30),
        ],
        as_of=date.today(),
    ),
)
```

### 16.3 Idempotency

Every POST accepts an `Idempotency-Key` header. The engine caches the response for 24h keyed on `(idempotency_key, request_hash)`.

### 16.4 Error Surface

```python
class HRIEError(Exception): ...
class InsufficientHistoryError(HRIEError): ...
class IdentifierUnresolvedError(HRIEError): ...
class StaleDataError(HRIEError): ...
class ProxyChainExhaustedError(HRIEError): ...
```

REST errors follow RFC 7807 (`application/problem+json`).

---

## 17. Integration Contracts

### 17.1 HRIE ↔ AlphaDroid Bridge

```python
class AlphaDroidAdapter:
    def has_asset(self, identifier: AssetIdentifier) -> bool: ...
    def get_market_data(self, identifier: AssetIdentifier) -> MarketDataBundle: ...
    def get_alphadroid_native_metrics(self, identifier: AssetIdentifier) -> dict: ...
    def is_fresh(self, identifier: AssetIdentifier, max_staleness_days: int = 2) -> bool: ...
```

When AlphaDroid is primary, HRIE still computes its own metrics in shadow mode and persists divergences to the audit log. Divergences > 10% on `RN_base` trigger a reconciliation alert to ops.

### 17.2 HRIE ↔ HRD Engine Bridge

```python
class HRIEAdapter:
    """Used by HRD Engine to obtain RN_portfolio."""

    def __init__(self, client: HRIEClient): ...

    def get_portfolio_risk_number(self, portfolio: hrd.Portfolio) -> int:
        """Returns RN_portfolio_adjusted for HRD alignment."""
        hrie_input = self._translate(portfolio)
        out = self.client.compute_portfolio_risk(hrie_input)
        return out.portfolio_risk_number_adjusted

    def get_full_risk_breakdown(self, portfolio: hrd.Portfolio) -> PortfolioRiskOutput:
        """Returns full breakdown for the diagnostic dashboard."""
        ...
```

The translation layer maps HRD's `Position` (which carries `weight`, `asset_class`, but not necessarily a Brazilian-friendly identifier) to HRIE's `AssetIdentifier`.

### 17.3 HRIE ↔ Harpian Terminal

The Terminal calls HRIE through HRD; it does not call HRIE directly. This preserves the principle that HRIE is a pure computation service and HRD is the orchestration layer.

---

## 18. Testing Strategy

### 18.1 Unit Tests

Per-module coverage target: **90%**. Each layer (L1–L6) has isolated tests with fixture-based inputs.

### 18.2 Golden Vector Tests

A versioned set of `(input, expected_output)` pairs lives in `tests/golden_vectors/`. Each vector is a curated real-world example:

- `IVVB11_5y.json` — international equity ETF in BRL
- `PATL11_3y.json` — FII tijolo logística
- `tesouro_selic.json` — pure post-fixed
- `multimercado_macro_xpm_30.json` — multimarket macro fund
- `previdência_brz_target_2040.json` — pension target-date
- `family_office_balanced_50_30_20.json` — composite portfolio

Golden vectors are regenerated only via a controlled migration commit signed by both COO and CIO. CI fails on any drift.

### 18.3 Property-Based Tests

Using `hypothesis`:

- RN is monotonic in downside.
- RAF is bounded in [1, 10] for any valid input.
- Portfolio RN ≤ max(asset RNs) only when correlations are sufficiently low (specific bound).
- Nearest-PSD projection is idempotent.
- `compute_portfolio_risk` is permutation-invariant in position order.

### 18.4 Regression Tests

The HRIE shadow-computation against AlphaDroid (when both have data) generates a daily reconciliation report. Sustained divergence > 5% over 5 trading days flags a regression and blocks deploys.

### 18.5 Performance Tests

- 100-asset portfolio risk computation: P95 < 500ms.
- Single asset risk: P95 < 50ms (cache hit) / < 200ms (cache miss).
- Cold start: < 3s (asset master + proxy registry load).

---

## 19. Performance and Operational Requirements

| Requirement | Target |
| --- | --- |
| Asset-level computation latency (P95) | < 50ms cached, < 200ms cold |
| Portfolio-level (n ≤ 100) latency (P95) | < 500ms |
| Portfolio-level (n ≤ 500) latency (P95) | < 2s |
| Cache hit ratio (production) | > 80% |
| Availability | 99.5% (institutional-grade) |
| Audit log retention | 7 years (regulatory floor) |
| Recompute on anchor/RAF version bump | Backfill within 48h |
| Memory ceiling per worker | 1 GB |
| Cold start time | < 3s |

Engine version is exposed via `/health` and embedded in every output payload.

---

## 20. Implementation Roadmap

### v1.0 — Production-ready core (Target: 8 weeks)

| Week | Deliverable |
| --- | --- |
| 1 | Domain model, contracts, taxonomy, repo skeleton |
| 2 | Ingestion layer (manual + AlphaDroid + B3) |
| 3 | Statistics layer (returns, vol, downside, drawdown) |
| 4 | RN computer + anchors + interpolation |
| 5 | RAF components + aggregator + adjustment |
| 6 | Correlation engine + portfolio aggregation |
| 7 | Confidence + alerts + JSON outputs + REST API |
| 8 | Golden vectors + integration tests + HRD adapter |

### v1.1 — Academic depth layer (Target: +6 weeks)

- HMM regime classifier (feeding `regime_instability` input to RAF).
- LPPL bubble detector → systemic overlay component.
- Kalman filter trend estimation as an alternative volatility-acceleration input.
- Cornish-Fisher VaR for short-history fallback.
- Non-linear repricing for structured products (Greeks).

### v1.2 — Streaming and intraday

- Live streaming feeds (Bloomberg, Economatica).
- Intraday RAF refresh.
- Real-time alert webhook to HRD Engine.
- Family Office multi-client batch endpoint.

---

## 21. Appendix A — Brazilian Asset Universe Reference Tables

### A.1 RN / RAF Reference (2025-2026 calibration)

| Asset class proxy | Annual vol | Max DD | RN (base) | RAF | Correlation IBOV |
| --- | --- | --- | --- | --- | --- |
| Tesouro Selic | 0.25% | 0.0% | 2 | 1 | -0.12 |
| CDB 110% CDI | 0.15% | 0.0% | 1 | 1 | -0.15 |
| LCI 85% CDI | 0.10% | 0.0% | 1 | 1 | -0.10 |
| Tesouro IPCA+ 2035 | 8.20% | -12.4% | 32 | 5 | 0.35 |
| IDA-Geral (debêntures) | 4.20% | -2.3% | 20 | 3 | 0.18 |
| FII Papel (high grade) | 5.90% | -8.0% | 25 | 2 | 0.22 |
| FII Logística (PATL11) | 12.40% | -14.5% | 48 | 5 | 0.45 |
| FII Shopping (HSML11) | 15.50% | -18.2% | 55 | 6 | 0.52 |
| FII Lajes Corporativas | 18.20% | -24.0% | 62 | 8 | 0.58 |
| Ibovespa (IBOV) | 18.50% | -45.0% | 75 | 7 | 1.00 |
| Smart Dividend (NDIV11) | 14.20% | -22.0% | 62 | 5 | 0.85 |
| Low Volatility (CAPE11) | 11.00% | -15.8% | 52 | 4 | 0.72 |
| Small Caps (SMLL) | 24.00% | -55.0% | 88 | 9 | 0.88 |
| Multimercado Macro Cons. | 6.50% | -7.5% | 35 | 4 | 0.28 |
| Multimercado Macro Agres. | 10.50% | -15.0% | 48 | 6 | 0.45 |
| Ouro (OZ1D) | 19.77% | -25.0% | 72 | 3 | -0.25 |
| S&P 500 BRL (IVVB11) | 21.00% | -32.0% | 78 | 5 | 0.32 |
| Nasdaq BRL (QQQ-BRL) | 28.50% | -38.0% | 85 | 6 | 0.38 |
| COE Capital Protected | 2.10% | 0.0% | 15 | 2 | 0.10 |

These values seed the asset master and serve as sanity bounds. Bottom-up computation overrides them when sufficient history exists.

### A.2 Risk Number Anchor Table (canonical)

| Downside_95_6m | RN | Profile |
| --- | --- | --- |
| 2.00% | 22 | Renda Fixa High Grade / Pós-fixado |
| 5.00% | 32 | Conservador / Crédito Privado Curto |
| 7.00% | 42 | Moderado / Multimercados Macro (Core 11 = 42) |
| 12.00% | 62 | Crescimento / FIIs de Tijolo (Core 22 = 58 ≈ this band) |
| 18.00% | 82 | Agressivo / Ações Blue Chips |
| 27.42% | 91 | Especulativo / Small Caps e Alavancados |

---

## 22. Appendix B — Mathematical Definitions Glossary

| Symbol | Definition |
| --- | --- |
| `r_t` | Simple return at time t |
| `σ` | Annualized volatility |
| `σ_d` | Annualized downside deviation |
| `MAR` | Minimum Acceptable Return (default = CDI for BRL) |
| `Z_95` | Standard normal critical value at 95% (= 1.645) |
| `Downside_95_6m` | `max(0, Z_95 · σ_d · √0.5 − E[r]_6m)` |
| `RN` | Risk Number, integer in [1, 99] |
| `RAF` | Risk Acceleration Factor, float in [1, 10] |
| `λ` | Systemic penalty intensity (default 0.35) |
| `ρ_normal` | Mean correlation in non-stress regime |
| `ρ_stress` | Mean correlation in stress regime |
| `γ` | Stress-blend weight = portfolio_systemic_RAF / 10 |
| `Σ_dynamic` | Dynamic covariance matrix |
| `MCR_i` | Marginal contribution to risk of asset i |
| `HHI` | Herfindahl-Hirschman concentration index = Σ w_i² |
| `CDaR` | Conditional Drawdown at Risk |

---

## 23. Appendix C — Pseudocode for Critical Algorithms

### C.1 Asset-Level Computation Top-Level

```
function compute_asset_risk(identifier, as_of):
    # L1 — Ingestion
    ingestion_result = ingest(identifier, history_years=5, freq=DAILY)
    if ingestion_result.bundle is None:
        raise IdentifierUnresolvedError

    # L2 — Classification
    asset_class = classify(identifier, ingestion_result.bundle)
    default_raf = DEFAULT_RAF[asset_class]

    # L3 — Statistics
    returns = compute_returns(ingestion_result.bundle.prices)
    vol = annualized_volatility(returns, freq=DAILY)
    dd = downside_deviation(returns, mar=cdi_rate(), freq=DAILY)
    drawdown_metrics = compute_drawdowns(ingestion_result.bundle.prices)
    ratios = compute_ratios(returns, vol, dd, drawdown_metrics, rf=cdi_rate())
    var_cvar = compute_var_cvar_6m(returns)

    # L4 — Risk pricing
    expected_return = estimate_expected_return(returns, asset_class)
    downside_estimate = max(0, Z_95 * dd * sqrt(0.5) - expected_return / 2)
    rn_base = map_downside_to_rn(downside_estimate)

    raf_components = compute_raf_components(returns, ingestion_result.bundle, asset_class)
    raf = compute_raf(raf_components)

    # Sanity check
    if abs(raf - default_raf) > 3.0:
        emit_warning("raf_outlier")

    rn_adjusted = min(99, rn_base * (1 + 0.35 * (raf - 1) / 9))

    # L5 — Correlations to canonical references (precomputed)
    correlations = compute_canonical_correlations(returns)

    # Confidence
    conf = confidence_score(
        history_years=ingestion_result.history_years_actual,
        frequency=ingestion_result.bundle.frequency,
        proxy_chain_depth=len(ingestion_result.proxy_chain),
        liquidity_quality=estimate_liquidity_quality(asset_class, ingestion_result.bundle),
        data_source=ingestion_result.actual_source,
    )

    return AssetRiskOutput(...)
```

### C.2 Portfolio-Level Computation Top-Level

```
function compute_portfolio_risk(portfolio):
    # 1. Compute per-asset (parallel)
    asset_outputs = parallel_map(compute_asset_risk, portfolio.positions)

    # 2. Build covariance components
    weights = [pos.weight for pos in portfolio.positions]
    vols = [a.annualized_volatility for a in asset_outputs]
    downsides = [a.downside_deviation for a in asset_outputs]

    # 3. Correlation matrices
    Σ_normal_corr = build_correlation_matrix(asset_outputs, mode="normal")
    Σ_stress_corr = build_correlation_matrix(asset_outputs, mode="stress")

    # 4. Portfolio RAF
    raf_weighted = sum(w_i * a.risk_acceleration_factor for w_i, a in zip(weights, asset_outputs))
    overlay = systemic_overlay(weights, asset_outputs)
    raf_portfolio = min(10, raf_weighted + overlay)

    # 5. Dynamic correlation
    γ = raf_portfolio / 10
    Σ_dynamic_corr = (1 - γ) * Σ_normal_corr + γ * Σ_stress_corr
    Σ_dynamic_corr = nearest_psd(Σ_dynamic_corr)

    # 6. Dynamic covariance
    D_vol = diag(vols)
    Σ_dynamic = D_vol @ Σ_dynamic_corr @ D_vol

    # 7. Portfolio metrics
    σ_p = sqrt(weights.T @ Σ_dynamic @ weights)
    σ_d_p = portfolio_downside_deviation(weights, downsides, Σ_dynamic_corr)
    expected_return_p = sum(w_i * a.expected_return_annual for w_i, a in zip(weights, asset_outputs))

    downside_p_6m = max(0, Z_95 * σ_d_p * sqrt(0.5) - expected_return_p / 2)
    rn_base_p = map_downside_to_rn(downside_p_6m)
    rn_adjusted_p = min(99, rn_base_p * (1 + 0.35 * (raf_portfolio - 1) / 9))

    # 8. Risk attribution
    contributors = compute_risk_contributions(weights, Σ_dynamic, asset_outputs)
    clusters = hierarchical_correlation_clusters(Σ_dynamic_corr, asset_outputs)

    # 9. Stress scenarios
    stress_results = run_stress_scenarios(portfolio, asset_outputs, Σ_dynamic_corr)

    # 10. Alerts
    alerts = evaluate_alerts(...)

    return PortfolioRiskOutput(...)
```

---

## End of Specification v1.0

**Sign-off**

| Role | Name | Sign-off |
| --- | --- | --- |
| COO | João Daniel | ☐ |
| CEO / PM | Diogo Scelza | ☐ |
| CIO | Johnny Zighelboim | ☐ |
| CTO | João Pedro Panizzutti (JP) | ☐ |
| Strategic Advisor | Scott Juds | ☐ |

Any change to the RN anchor table, RAF component weights, λ, or stress correlation methodology is a **versioned migration** and requires sign-off from CIO + COO at minimum.
