"""
Harpian Risk Diagnostics (HRD) — Core Engine
==============================================
Author:  Harpian LLC / Engineering Reference
Version: 1.0.0
Purpose: Scientific risk-number computation, gap analysis, and allocation
         optimisation for Multi-Family Office portfolios.

INTEGRATION NOTES FOR JP
--------------------------
  • Entry point  : HRDEngine.run(portfolio, client_profile)
  • Input format : see Portfolio and ClientProfile dataclasses (or plain dicts)
  • Output format: HRDReport dataclass → JSON-serialisable via .to_dict()
  • No external dependencies beyond the standard library + numpy.
    (numpy can be replaced with pure-Python if needed — see comments.)
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, List, Optional, Tuple


# ─────────────────────────────────────────────────────────────────────────────
# 1.  ENUMERATIONS  (use string values for JSON round-trip safety)
# ─────────────────────────────────────────────────────────────────────────────

class AssetClass(str, Enum):
    CASH            = "cash"
    FIXED_INCOME_IG = "fixed_income_ig"       # Investment Grade
    FIXED_INCOME_HY = "fixed_income_hy"       # High Yield
    CREDIT_BR       = "credit_brazil"          # Crédito Privado Brasil
    FIXED_IPCA      = "fixed_ipca_long"        # NTN-B / Debentures IPCA+
    EQUITY_BROAD    = "equity_broad"           # S&P 500 / MSCI World
    EQUITY_IBOV     = "equity_ibov"            # Ibovespa / blue-chips BR
    EQUITY_TECH_SC  = "equity_tech_smallcap"   # Nasdaq / Small-caps
    HARPIAN_ETP     = "harpian_etp"
    GOLD            = "gold"
    COMMODITIES     = "commodities"
    REITS           = "reits"
    PRIVATE_EQUITY  = "private_equity"
    VENTURE         = "venture_capital"
    CRYPTO          = "crypto"
    OTHER           = "other"


class Jurisdiction(str, Enum):
    USA     = "usa"
    BRAZIL  = "brazil"
    EUROPE  = "europe"
    ASIA_EM = "asia_em"
    OTHER   = "other"


class LiquidityTier(str, Enum):
    """Settlement / redemption horizon."""
    D0   = "D+0"    # Intraday / same-day
    D1   = "D+1"
    D3   = "D+3"
    D30  = "D+30"
    D60  = "D+60"
    D90  = "D+90"
    LOCK = "lock-up"   # Private equity / VC


class RiskBand(str, Enum):
    CONSERVATIVE_EXTREME = "Conservative Extreme"   # 0–20
    CONSERVATIVE         = "Conservative"           # 21–40
    MODERATE             = "Moderate"               # 41–60
    MODERATE_AGGRESSIVE  = "Moderate Aggressive"    # 61–75
    AGGRESSIVE           = "Aggressive"             # 76–90
    ULTRA_AGGRESSIVE     = "Ultra Aggressive"       # 91–100


# ─────────────────────────────────────────────────────────────────────────────
# 2.  REFERENCE TABLES
# ─────────────────────────────────────────────────────────────────────────────

# Base Risk Score for each asset class (scale 0–99).
# Source: Harpian Risk Methodology v1 / GPT-Gemini blueprint review.
BASE_RISK_SCORE: Dict[AssetClass, int] = {
    AssetClass.CASH:            5,
    AssetClass.FIXED_INCOME_IG: 25,
    AssetClass.FIXED_INCOME_HY: 50,
    AssetClass.CREDIT_BR:       35,   # will be multiplied by CRM
    AssetClass.FIXED_IPCA:      45,
    AssetClass.EQUITY_BROAD:    65,
    AssetClass.EQUITY_IBOV:     70,   # will be multiplied by CRM
    AssetClass.EQUITY_TECH_SC:  85,
    AssetClass.HARPIAN_ETP:     42,   # empirical — update after each backtest
    AssetClass.GOLD:            55,
    AssetClass.COMMODITIES:     70,
    AssetClass.REITS:           65,
    AssetClass.PRIVATE_EQUITY:  90,
    AssetClass.VENTURE:         95,
    AssetClass.CRYPTO:          99,
    AssetClass.OTHER:           60,
}

# Country Risk Multiplier (CRM)
# Scales the base score to reflect structural / sovereign / FX risk.
COUNTRY_RISK_MULTIPLIER: Dict[Jurisdiction, float] = {
    Jurisdiction.USA:     1.00,
    Jurisdiction.EUROPE:  1.10,
    Jurisdiction.ASIA_EM: 1.20,
    Jurisdiction.BRAZIL:  1.30,
    Jurisdiction.OTHER:   1.25,
}

# Liquidity Penalty (added to score after CRM)
# Rationale: illiquid assets carry extra "tail risk" because the investor
# cannot exit in a crisis — this must be reflected in the risk number.
LIQUIDITY_PENALTY: Dict[LiquidityTier, int] = {
    LiquidityTier.D0:   0,
    LiquidityTier.D1:   0,
    LiquidityTier.D3:   0,
    LiquidityTier.D30:  5,
    LiquidityTier.D60:  10,
    LiquidityTier.D90:  10,
    LiquidityTier.LOCK: 15,
}

# Correlation Factor (CF)
# Applied as a portfolio-level multiplier when equity exposure is high,
# because in a crisis all correlations go to 1 — the diversification
# benefit disappears exactly when you need it most (Tail Risk).
EQUITY_ASSET_CLASSES = {
    AssetClass.EQUITY_BROAD,
    AssetClass.EQUITY_IBOV,
    AssetClass.EQUITY_TECH_SC,
}
EQUITY_CONCENTRATION_THRESHOLD = 0.60   # 60 %
CORRELATION_FACTOR_HIGH        = 1.10   # applied when equities > threshold
CORRELATION_FACTOR_NORMAL      = 1.00

# Hard cap so RN never exceeds 99 (keeps scale consistent with Nitrogen)
MAX_RISK_SCORE = 99


# ─────────────────────────────────────────────────────────────────────────────
# 3.  DATA STRUCTURES
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class Position:
    """A single line in the portfolio."""
    name:         str
    asset_class:  AssetClass
    jurisdiction: Jurisdiction
    liquidity:    LiquidityTier
    weight:       float          # 0.0 → 1.0  (e.g. 0.25 = 25 %)
    currency:     str  = "USD"   # ISO 4217


@dataclass
class ClientProfile:
    """
    Behavioural / financial profile captured from the questionnaire.
    Fields map directly to the Nitrogen-style questionnaire outputs.
    """
    target_risk_number:    int          # 0–99  (questionnaire output)
    investment_horizon_yr: int   = 5
    base_currency:         str   = "USD"
    notes:                 str   = ""


@dataclass
class Portfolio:
    positions: List[Position]

    def validate(self) -> None:
        total = sum(p.weight for p in self.positions)
        if not math.isclose(total, 1.0, abs_tol=0.01):
            raise ValueError(
                f"Portfolio weights sum to {total:.4f}, expected 1.0 ± 0.01"
            )


# ─────────────────────────────────────────────────────────────────────────────
# 4.  INDIVIDUAL POSITION SCORER
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class ScoredPosition:
    position:         Position
    base_score:       int
    after_crm:        float
    liquidity_penalty: int
    final_score:      float
    weighted_score:   float


def score_position(pos: Position) -> ScoredPosition:
    """
    Compute the risk-adjusted score for a single position.

    Pipeline
    --------
    1. Look up base score from asset class table.
    2. Apply Country Risk Multiplier.
    3. Add Liquidity Penalty.
    4. Cap at MAX_RISK_SCORE.
    5. Multiply by position weight (for portfolio aggregation).

    This function is PURE — no side effects, easy to unit-test.
    """
    base       = BASE_RISK_SCORE[pos.asset_class]
    crm        = COUNTRY_RISK_MULTIPLIER[pos.jurisdiction]
    after_crm  = base * crm
    liq_pen    = LIQUIDITY_PENALTY[pos.liquidity]
    final      = min(after_crm + liq_pen, MAX_RISK_SCORE)
    weighted   = pos.weight * final

    return ScoredPosition(
        position=pos,
        base_score=base,
        after_crm=after_crm,
        liquidity_penalty=liq_pen,
        final_score=final,
        weighted_score=weighted,
    )


# ─────────────────────────────────────────────────────────────────────────────
# 5.  PORTFOLIO RISK NUMBER
# ─────────────────────────────────────────────────────────────────────────────

def compute_portfolio_risk_number(
    portfolio: Portfolio,
) -> Tuple[float, float, List[ScoredPosition]]:
    """
    Returns (raw_rn, adjusted_rn, scored_positions).

    Formula
    -------
        raw_RN   = Σ (w_i × RS_i_adjusted)
        final_RN = raw_RN × CF

    where CF = 1.10 if Σ equity weights > 60 %, else 1.00.

    The Correlation Factor (CF) represents "Tail Risk":
    in a market crisis, equity correlations converge toward 1.0,
    eliminating diversification exactly when it matters most.
    A 10 % upward adjustment to the raw risk number captures this
    non-linearity without requiring a full covariance matrix.
    """
    scored = [score_position(p) for p in portfolio.positions]
    raw_rn = sum(s.weighted_score for s in scored)

    # Equity concentration check
    equity_weight = sum(
        p.weight for p in portfolio.positions
        if p.asset_class in EQUITY_ASSET_CLASSES
    )
    cf = CORRELATION_FACTOR_HIGH if equity_weight >= EQUITY_CONCENTRATION_THRESHOLD \
         else CORRELATION_FACTOR_NORMAL

    adjusted_rn = min(raw_rn * cf, MAX_RISK_SCORE)
    return raw_rn, adjusted_rn, scored


# ─────────────────────────────────────────────────────────────────────────────
# 6.  RISK BAND CLASSIFIER
# ─────────────────────────────────────────────────────────────────────────────

def classify_risk_band(rn: float) -> RiskBand:
    if rn <= 20:  return RiskBand.CONSERVATIVE_EXTREME
    if rn <= 40:  return RiskBand.CONSERVATIVE
    if rn <= 60:  return RiskBand.MODERATE
    if rn <= 75:  return RiskBand.MODERATE_AGGRESSIVE
    if rn <= 90:  return RiskBand.AGGRESSIVE
    return RiskBand.ULTRA_AGGRESSIVE


# ─────────────────────────────────────────────────────────────────────────────
# 7.  GAP SOLVER — OPTIMAL HARPIAN ALLOCATION
# ─────────────────────────────────────────────────────────────────────────────

def solve_harpian_allocation(
    rn_portfolio: float,
    rn_target:    int,
    rn_harpian:   float = BASE_RISK_SCORE[AssetClass.HARPIAN_ETP],
) -> Tuple[float, str]:
    """
    Solve for the Harpian ETP weight that closes the risk gap.

    Mathematical Derivation
    -----------------------
    We want to build a blended portfolio of:
        (1 - w) × [current portfolio]  +  w × [Harpian ETP]

    such that the new portfolio risk number equals RN_target:

        (1 - w) × RN_portfolio  +  w × RN_harpian  =  RN_target

    Solving for w:

        RN_portfolio - w × RN_portfolio + w × RN_harpian  =  RN_target
        w × (RN_harpian - RN_portfolio)                   =  RN_target - RN_portfolio
        w = (RN_target - RN_portfolio) / (RN_harpian - RN_portfolio)

    Equivalently (for risk REDUCTION scenarios where RN_portfolio > RN_target):

        w = (RN_portfolio - RN_target) / (RN_portfolio - RN_harpian)

    Edge cases
    ----------
    • If portfolio risk == target → no allocation needed (w = 0).
    • If Harpian RN == portfolio RN → no lever to pull; return explanation.
    • If w > 1.0 → Harpian alone is not enough; capped at 1.0 with warning.
    • If w < 0   → portfolio already below target; reduction not needed.
    """
    delta = rn_portfolio - rn_target

    if abs(delta) < 0.5:
        return 0.0, "Portfolio risk already matches target. No allocation change required."

    if math.isclose(rn_portfolio, rn_harpian, abs_tol=0.5):
        return 0.0, (
            "Harpian ETP Risk Number is approximately equal to the current "
            "portfolio Risk Number. Replacing assets with Harpian would not "
            "meaningfully change the portfolio's risk profile."
        )

    if rn_portfolio < rn_target:
        # Client wants MORE risk than current portfolio provides.
        # Harpian (moderate-risk) is not the right lever here — flag it.
        return 0.0, (
            f"Portfolio RN ({rn_portfolio:.1f}) is BELOW target RN ({rn_target}). "
            "Harpian ETP reduces risk; consider increasing equity allocation instead."
        )

    # Standard risk-reduction case
    w = (rn_portfolio - rn_target) / (rn_portfolio - rn_harpian)

    if w > 1.0:
        msg = (
            f"A {w*100:.1f}% allocation to Harpian ETP is mathematically required, "
            f"but capped at 100%. Even a full allocation (RN={rn_harpian:.1f}) "
            f"does not reach the target RN of {rn_target}. "
            "Consider whether the target is achievable or review asset mix."
        )
        return 1.0, msg

    msg = (
        f"Allocate {w*100:.1f}% of the portfolio to Harpian ETP "
        f"(and reduce other positions proportionally) to bring the "
        f"portfolio Risk Number from {rn_portfolio:.1f} to {rn_target}."
    )
    return round(w, 4), msg


# ─────────────────────────────────────────────────────────────────────────────
# 8.  STRESS TEST ENGINE
# ─────────────────────────────────────────────────────────────────────────────

# Predefined stress scenarios.
# Each scenario defines an approximate peak-to-trough drawdown per asset class.
# Values sourced from historical crises and academic literature.
STRESS_SCENARIOS: Dict[str, Dict[AssetClass, float]] = {
    "S&P 500 -20% (Correction)": {
        AssetClass.EQUITY_BROAD:    -0.20,
        AssetClass.EQUITY_IBOV:     -0.18,
        AssetClass.EQUITY_TECH_SC:  -0.28,
        AssetClass.FIXED_INCOME_HY: -0.08,
        AssetClass.FIXED_INCOME_IG: -0.03,
        AssetClass.CREDIT_BR:       -0.05,
        AssetClass.FIXED_IPCA:      -0.04,
        AssetClass.CASH:             0.00,
        AssetClass.GOLD:            +0.05,
        AssetClass.HARPIAN_ETP:     -0.04,   # adaptive, partially hedged
        AssetClass.PRIVATE_EQUITY:  -0.15,
        AssetClass.VENTURE:         -0.20,
        AssetClass.CRYPTO:          -0.40,
        AssetClass.REITS:           -0.18,
        AssetClass.COMMODITIES:     -0.12,
        AssetClass.OTHER:           -0.10,
    },
    "Global Crisis -40% (2008 style)": {
        AssetClass.EQUITY_BROAD:    -0.40,
        AssetClass.EQUITY_IBOV:     -0.55,
        AssetClass.EQUITY_TECH_SC:  -0.50,
        AssetClass.FIXED_INCOME_HY: -0.25,
        AssetClass.FIXED_INCOME_IG: +0.05,   # flight to quality
        AssetClass.CREDIT_BR:       -0.20,
        AssetClass.FIXED_IPCA:      -0.10,
        AssetClass.CASH:             0.00,
        AssetClass.GOLD:            +0.15,
        AssetClass.HARPIAN_ETP:     -0.08,
        AssetClass.PRIVATE_EQUITY:  -0.35,
        AssetClass.VENTURE:         -0.50,
        AssetClass.CRYPTO:          -0.75,
        AssetClass.REITS:           -0.45,
        AssetClass.COMMODITIES:     -0.30,
        AssetClass.OTHER:           -0.25,
    },
    "Brazil Risk Event (BRL -30%)": {
        AssetClass.EQUITY_BROAD:    -0.05,
        AssetClass.EQUITY_IBOV:     -0.35,
        AssetClass.EQUITY_TECH_SC:  -0.05,
        AssetClass.FIXED_INCOME_HY: -0.03,
        AssetClass.FIXED_INCOME_IG:  0.00,
        AssetClass.CREDIT_BR:       -0.15,
        AssetClass.FIXED_IPCA:      -0.08,
        AssetClass.CASH:             0.00,
        AssetClass.GOLD:            +0.08,
        AssetClass.HARPIAN_ETP:     -0.02,
        AssetClass.PRIVATE_EQUITY:  -0.10,
        AssetClass.VENTURE:         -0.15,
        AssetClass.CRYPTO:          -0.20,
        AssetClass.REITS:           -0.05,
        AssetClass.COMMODITIES:     -0.05,
        AssetClass.OTHER:           -0.08,
    },
}


@dataclass
class StressResult:
    scenario_name:     str
    portfolio_impact:  float   # % P&L on current portfolio
    blended_impact:    float   # % P&L on portfolio + Harpian allocation
    portfolio_dollar:  float   # $ P&L (if AUM provided)
    blended_dollar:    float   # $ P&L blended
    improvement_pct:   float   # blended - portfolio (positive = improvement)


def run_stress_tests(
    portfolio: Portfolio,
    harpian_weight: float,
    aum_usd: float = 1_000_000,
) -> List[StressResult]:
    """
    Simulate portfolio P&L under predefined stress scenarios.

    For each scenario:
      1. Compute weighted average drawdown on the CURRENT portfolio.
      2. Compute weighted average drawdown on the BLENDED portfolio
         (current positions scaled by (1 - harpian_weight) + Harpian ETP
         at harpian_weight).
    """
    results = []

    for scenario_name, shocks in STRESS_SCENARIOS.items():
        # Current portfolio impact
        port_impact = sum(
            p.weight * shocks.get(p.asset_class, -0.10)
            for p in portfolio.positions
        )

        # Blended portfolio impact
        harpian_shock   = shocks.get(AssetClass.HARPIAN_ETP, -0.04)
        blended_impact  = (1 - harpian_weight) * port_impact + harpian_weight * harpian_shock

        results.append(StressResult(
            scenario_name    = scenario_name,
            portfolio_impact = round(port_impact,  4),
            blended_impact   = round(blended_impact, 4),
            portfolio_dollar = round(port_impact  * aum_usd, 2),
            blended_dollar   = round(blended_impact * aum_usd, 2),
            improvement_pct  = round(blended_impact - port_impact, 4),
        ))

    return results


# ─────────────────────────────────────────────────────────────────────────────
# 9.  EXPOSURE MAP  (breakdowns for charts)
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class ExposureMap:
    by_asset_class:  Dict[str, float]   # asset_class.value → total weight
    by_jurisdiction: Dict[str, float]   # jurisdiction.value → total weight
    by_liquidity:    Dict[str, float]   # liquidity.value   → total weight
    equity_weight:   float
    brazil_weight:   float
    illiquid_weight: float              # D+60 or worse


def build_exposure_map(portfolio: Portfolio) -> ExposureMap:
    ac_map:  Dict[str, float] = {}
    jur_map: Dict[str, float] = {}
    liq_map: Dict[str, float] = {}

    for p in portfolio.positions:
        ac_map[p.asset_class.value]   = ac_map.get(p.asset_class.value,   0) + p.weight
        jur_map[p.jurisdiction.value] = jur_map.get(p.jurisdiction.value, 0) + p.weight
        liq_map[p.liquidity.value]    = liq_map.get(p.liquidity.value,    0) + p.weight

    equity_weight = sum(
        p.weight for p in portfolio.positions
        if p.asset_class in EQUITY_ASSET_CLASSES
    )
    brazil_weight = sum(
        p.weight for p in portfolio.positions
        if p.jurisdiction == Jurisdiction.BRAZIL
    )
    illiquid_weight = sum(
        p.weight for p in portfolio.positions
        if p.liquidity in {LiquidityTier.D60, LiquidityTier.D90, LiquidityTier.LOCK}
    )

    return ExposureMap(
        by_asset_class  = ac_map,
        by_jurisdiction = jur_map,
        by_liquidity    = liq_map,
        equity_weight   = round(equity_weight,   4),
        brazil_weight   = round(brazil_weight,   4),
        illiquid_weight = round(illiquid_weight, 4),
    )


# ─────────────────────────────────────────────────────────────────────────────
# 10.  REPORT  (final output object)
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class HRDReport:
    # ── Inputs
    client_profile:     ClientProfile
    portfolio:          Portfolio

    # ── Risk Numbers
    portfolio_rn_raw:   float           # before CF
    portfolio_rn:       float           # after CF (headline number)
    portfolio_band:     RiskBand
    target_rn:          int
    target_band:        RiskBand
    harpian_rn:         float

    # ── Gap
    risk_gap:           float           # portfolio_rn - target_rn
    gap_direction:      str             # "OVER" | "UNDER" | "ALIGNED"

    # ── Allocation recommendation
    harpian_weight_suggested: float     # 0.0 → 1.0
    recommendation_text:      str

    # ── Breakdowns
    scored_positions:   List[ScoredPosition]
    exposure_map:       ExposureMap

    # ── Stress tests
    stress_results:     List[StressResult]

    # ── Diagnosis narrative
    diagnosis:          str

    def to_dict(self) -> dict:
        """JSON-serialisable representation for API/database consumption."""
        return {
            "client": asdict(self.client_profile),
            "risk_numbers": {
                "portfolio_raw":  round(self.portfolio_rn_raw, 2),
                "portfolio":      round(self.portfolio_rn,     2),
                "portfolio_band": self.portfolio_band.value,
                "target":         self.target_rn,
                "target_band":    self.target_band.value,
                "harpian":        self.harpian_rn,
                "gap":            round(self.risk_gap, 2),
                "gap_direction":  self.gap_direction,
            },
            "allocation": {
                "harpian_weight_pct": round(self.harpian_weight_suggested * 100, 2),
                "recommendation":     self.recommendation_text,
            },
            "exposure": {
                "by_asset_class":   self.exposure_map.by_asset_class,
                "by_jurisdiction":  self.exposure_map.by_jurisdiction,
                "by_liquidity":     self.exposure_map.by_liquidity,
                "equity_weight_pct":   round(self.exposure_map.equity_weight   * 100, 2),
                "brazil_weight_pct":   round(self.exposure_map.brazil_weight   * 100, 2),
                "illiquid_weight_pct": round(self.exposure_map.illiquid_weight * 100, 2),
            },
            "position_scores": [
                {
                    "name":              s.position.name,
                    "asset_class":       s.position.asset_class.value,
                    "jurisdiction":      s.position.jurisdiction.value,
                    "liquidity":         s.position.liquidity.value,
                    "weight_pct":        round(s.position.weight * 100, 2),
                    "base_score":        s.base_score,
                    "after_crm":         round(s.after_crm, 2),
                    "liquidity_penalty": s.liquidity_penalty,
                    "final_score":       round(s.final_score, 2),
                    "weighted_score":    round(s.weighted_score, 4),
                }
                for s in self.scored_positions
            ],
            "stress_tests": [
                {
                    "scenario":          r.scenario_name,
                    "portfolio_pct":     round(r.portfolio_impact * 100, 2),
                    "blended_pct":       round(r.blended_impact   * 100, 2),
                    "improvement_pct":   round(r.improvement_pct  * 100, 2),
                }
                for r in self.stress_results
            ],
            "diagnosis": self.diagnosis,
        }

    def print_summary(self) -> None:
        """Human-readable console summary — useful during development."""
        sep = "─" * 60
        print(f"\n{sep}")
        print("  HARPIAN RISK DIAGNOSTICS — PORTFOLIO REPORT")
        print(sep)
        print(f"  Portfolio Risk Number : {self.portfolio_rn:.1f}  ({self.portfolio_band.value})")
        print(f"  Client Target RN      : {self.target_rn}  ({self.target_band.value})")
        print(f"  Risk Gap              : {self.risk_gap:+.1f}  [{self.gap_direction}]")
        print(f"  Harpian ETP RN        : {self.harpian_rn:.1f}")
        print(sep)
        print(f"  Suggested Harpian Wt  : {self.harpian_weight_suggested*100:.1f}%")
        print(f"  Recommendation        : {self.recommendation_text}")
        print(sep)
        print(f"  Equity Exposure       : {self.exposure_map.equity_weight*100:.1f}%")
        print(f"  Brazil Exposure       : {self.exposure_map.brazil_weight*100:.1f}%")
        print(f"  Illiquid Exposure     : {self.exposure_map.illiquid_weight*100:.1f}%")
        print(sep)
        print("  STRESS TESTS")
        for r in self.stress_results:
            arrow = "↑" if r.improvement_pct > 0 else "↓"
            print(f"    {r.scenario_name:<35} | "
                  f"Current: {r.portfolio_impact*100:+.1f}%  "
                  f"Blended: {r.blended_impact*100:+.1f}%  "
                  f"{arrow}{abs(r.improvement_pct*100):.1f}% improvement")
        print(sep)
        print(f"\n  DIAGNOSIS:\n  {self.diagnosis}\n")


# ─────────────────────────────────────────────────────────────────────────────
# 11.  MAIN ENGINE  (orchestration)
# ─────────────────────────────────────────────────────────────────────────────

class HRDEngine:
    """
    Top-level orchestrator.  JP: this is the single class to call.

    Usage
    -----
        engine = HRDEngine()
        report = engine.run(portfolio, client_profile, aum_usd=5_000_000)
        data   = report.to_dict()          # → send to API / DB
        report.print_summary()             # → console dev check
    """

    def __init__(
        self,
        harpian_rn_override: Optional[float] = None,
    ):
        """
        harpian_rn_override : pass the live Harpian ETP Risk Number here
                              once you have the back-tested figure.
                              Defaults to BASE_RISK_SCORE table value.
        """
        self.harpian_rn = (
            harpian_rn_override
            if harpian_rn_override is not None
            else float(BASE_RISK_SCORE[AssetClass.HARPIAN_ETP])
        )

    def run(
        self,
        portfolio:      Portfolio,
        client_profile: ClientProfile,
        aum_usd:        float = 1_000_000,
    ) -> HRDReport:

        # 1. Validate
        portfolio.validate()

        # 2. Score all positions & compute RN
        raw_rn, adj_rn, scored = compute_portfolio_risk_number(portfolio)

        # 3. Classify
        portfolio_band = classify_risk_band(adj_rn)
        target_band    = classify_risk_band(client_profile.target_risk_number)

        # 4. Gap
        gap = adj_rn - client_profile.target_risk_number
        if   gap >  2: direction = "OVER"
        elif gap < -2: direction = "UNDER"
        else:          direction = "ALIGNED"

        # 5. Solve allocation
        weight, rec_text = solve_harpian_allocation(
            rn_portfolio = adj_rn,
            rn_target    = client_profile.target_risk_number,
            rn_harpian   = self.harpian_rn,
        )

        # 6. Exposures
        exposure = build_exposure_map(portfolio)

        # 7. Stress tests
        stress = run_stress_tests(portfolio, weight, aum_usd)

        # 8. Diagnosis narrative
        diagnosis = self._build_diagnosis(
            adj_rn, client_profile.target_risk_number,
            portfolio_band, target_band,
            direction, weight, exposure
        )

        return HRDReport(
            client_profile           = client_profile,
            portfolio                = portfolio,
            portfolio_rn_raw         = round(raw_rn, 2),
            portfolio_rn             = round(adj_rn, 2),
            portfolio_band           = portfolio_band,
            target_rn                = client_profile.target_risk_number,
            target_band              = target_band,
            harpian_rn               = self.harpian_rn,
            risk_gap                 = round(gap, 2),
            gap_direction            = direction,
            harpian_weight_suggested = weight,
            recommendation_text      = rec_text,
            scored_positions         = scored,
            exposure_map             = exposure,
            stress_results           = stress,
            diagnosis                = diagnosis,
        )

    # ── Private helpers ──────────────────────────────────────────────────────

    @staticmethod
    def _build_diagnosis(
        rn_port:  float,
        rn_tgt:   int,
        port_band: RiskBand,
        tgt_band:  RiskBand,
        direction: str,
        h_weight:  float,
        exp:       ExposureMap,
    ) -> str:
        lines = []
        lines.append(
            f"Your current portfolio carries a Risk Number of {rn_port:.0f} "
            f"({port_band.value}), while your risk profile indicates a target "
            f"of {rn_tgt} ({tgt_band.value})."
        )

        if direction == "OVER":
            lines.append(
                f"The portfolio is carrying {rn_port - rn_tgt:.0f} points MORE risk "
                "than your target. This means in a market downturn you would likely "
                "experience larger drawdowns than you are prepared for emotionally "
                "and financially."
            )
            if h_weight > 0:
                lines.append(
                    f"Reallocating {h_weight*100:.1f}% of the portfolio to the Harpian "
                    "Adaptive ETP would bring your risk into alignment with your target "
                    "without materially disrupting your current asset strategy."
                )
        elif direction == "UNDER":
            lines.append(
                "The portfolio is currently running BELOW your target risk level. "
                "You may be leaving return potential on the table. "
                "Consider reviewing fixed income and cash allocations."
            )
        else:
            lines.append(
                "Your portfolio risk is well-aligned with your target. "
                "No significant rebalancing is required at this time."
            )

        if exp.brazil_weight > 0.30:
            lines.append(
                f"⚠ High Brazil concentration ({exp.brazil_weight*100:.1f}%): "
                "structural sovereign risk and BRL volatility are significant "
                "contributors to your portfolio Risk Number."
            )
        if exp.illiquid_weight > 0.20:
            lines.append(
                f"⚠ Illiquidity alert ({exp.illiquid_weight*100:.1f}% in D+60 or worse): "
                "in a liquidity crisis, a large portion of your portfolio cannot be "
                "redeemed — this amplifies realised losses."
            )

        return " ".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# 12.  DEMO  (remove before production)
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # ------------------------------------------------------------------
    # Sample Family Office portfolio
    # ------------------------------------------------------------------
    demo_portfolio = Portfolio(positions=[
        Position("US Treasuries 2Y",    AssetClass.CASH,            Jurisdiction.USA,    LiquidityTier.D1,   0.10, "USD"),
        Position("Investment Grade ETF", AssetClass.FIXED_INCOME_IG, Jurisdiction.USA,    LiquidityTier.D1,   0.10, "USD"),
        Position("S&P 500 ETF",          AssetClass.EQUITY_BROAD,    Jurisdiction.USA,    LiquidityTier.D1,   0.25, "USD"),
        Position("Nasdaq QQQ",           AssetClass.EQUITY_TECH_SC,  Jurisdiction.USA,    LiquidityTier.D1,   0.10, "USD"),
        Position("Ibovespa Fundo",       AssetClass.EQUITY_IBOV,     Jurisdiction.BRAZIL, LiquidityTier.D3,   0.10, "BRL"),
        Position("CRI/CRA IPCA+",        AssetClass.FIXED_IPCA,      Jurisdiction.BRAZIL, LiquidityTier.D30,  0.10, "BRL"),
        Position("FII Logística",        AssetClass.REITS,           Jurisdiction.BRAZIL, LiquidityTier.D3,   0.05, "BRL"),
        Position("BTC",                  AssetClass.CRYPTO,          Jurisdiction.USA,    LiquidityTier.D0,   0.05, "USD"),
        Position("Private Credit Fund",  AssetClass.PRIVATE_EQUITY,  Jurisdiction.USA,    LiquidityTier.LOCK, 0.10, "USD"),
        Position("Gold ETF",             AssetClass.GOLD,            Jurisdiction.USA,    LiquidityTier.D1,   0.05, "USD"),
    ])

    demo_client = ClientProfile(
        target_risk_number    = 55,
        investment_horizon_yr = 7,
        base_currency         = "USD",
        notes                 = "Family office, two generations, conservative heir",
    )

    engine = HRDEngine()
    report = engine.run(demo_portfolio, demo_client, aum_usd=10_000_000)
    report.print_summary()

    import json
    print("\n── JSON SNAPSHOT ──")
    print(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))
