# JIM Adversarial Engine
## Specification — Adverse Scenario, Counter-Thesis, Model Limitation

**Version:** 2.0 | **Classification:** Confidential — Internal Use Only  
**New in:** JIM Architecture v2

---

## Purpose

The Adversarial Engine (AE) is a mandatory processing module that activates on simulation, risk, and alignment queries at institutional response levels (L3/L4). Its function is to ensure balanced analytical presentation by automatically generating:

1. **ADVERSE_SCENARIO** — quantified impact when the analyzed strategy fails
2. **COUNTER_THESIS** — strongest alternative analytical interpretation of the data
3. **MODEL_LIMITATION** — specific model assumptions and dependency disclosures

The Adversarial Engine exists to prevent JIM from producing outputs that appear directionally promotional, even when no explicit recommendation is made. A simulation showing "improved Risk Number" without a corresponding adverse scenario would be one-sided — which is a FINRA Rule 2210 violation.

---

## Activation Rules

### Automatic Activation

| Condition | AE Activates |
|-----------|-------------|
| `response_level = L3` AND intent in [SIMULATION, PORTFOLIO_ALIGNMENT, HIDDEN_RISK, STRESS_TESTING] | Yes — ADVERSE_SCENARIO + MODEL_LIMITATION |
| `response_level = L4` | Yes — ALL THREE blocks (ADVERSE_SCENARIO + COUNTER_THESIS + MODEL_LIMITATION) |
| `intent_id = INT-015` (Hypothetical Allocation) | Always — regardless of level |
| `intent_id = INT-016` (Stress Test) | Always — regardless of level |
| `intent_id = INT-020` (Rate Shock / Scenario) | Always — regardless of level |

### No Activation

| Condition | AE Does Not Activate |
|-----------|---------------------|
| `response_level = L1` | Client messaging — never adversarial |
| `response_level = L2` | Advisor standard — no adversarial |
| `intent_category = UX_NAVIGATION` | Navigation queries only |
| `intent_category = ACTION_REQUEST` | Mandatory response only — no engine output |
| `intent_category = DAILY_DASHBOARD` | Status summary only |

---

## Block 1 — ADVERSE_SCENARIO

### When Required

Every SIMULATION or STRESS_TESTING response at L3/L4. Must accompany the [SIMULATION] block — cannot be omitted if [SIMULATION] is present.

### Construction Rules

1. **Named scenario** — give the adverse scenario a descriptive name (e.g., "Rising Rate Environment", "Credit Spread Widening", "Equity Drawdown — 2008 Pattern")
2. **Quantified conditions** — state the macro parameters used (e.g., "10Y yield +150bps", "S&P 500 -20%")
3. **Quantified portfolio impact** — show impact on same metrics as the base simulation (Risk Number, Alignment Score, CAGR, Max Drawdown)
4. **Source attribution** — must state "Adversarial Engine — Adverse Case Analysis" and "HRD Engine — Stress Scenario"
5. **DISC-009** — mandatory for all adverse scenario outputs
6. **No probability claims** — never state "this is likely" or "this is unlikely"

### Standard Adverse Scenarios Library

The Adversarial Engine selects from a library of pre-defined scenarios, supplemented by scenario parameters from the user query context:

| Scenario ID | Name | Conditions |
|-------------|------|-----------|
| ADV-001 | Rising Rate Environment | 10Y +150bps / Credit +80bps |
| ADV-002 | Deep Equity Drawdown | Equity -25% / VIX >40 |
| ADV-003 | Credit Event | IG spread +120bps / HY spread +300bps |
| ADV-004 | Stagflation | CPI +6% / GDP -1.5% / Rate hike cycle |
| ADV-005 | Liquidity Shock | Bid-ask spread +300% / Volume collapse |
| ADV-006 | Currency Shock | USD +15% vs. EM basket |
| ADV-007 | Emerging Market Contagion | EM equity -30% / EM FX -20% |
| ADV-008 | 2008 Pattern | Equity -40% / Credit freeze / VaR breach cascade |
| ADV-009 | 2020 COVID Pattern | Equity -34% in 33 days / Recovery within 6 months |
| ADV-010 | Rate Reversal | Yield curve inversion / Recession signal |

### Format Template

```
[ADVERSE_SCENARIO]
Adversarial Engine — Adverse Case Analysis
HRD Engine — Stress Scenario: {SCENARIO_NAME}

Conditions tested:
- {Macro parameter 1}
- {Macro parameter 2}
- {Macro parameter 3}

Portfolio impact (hypothetical):
- Risk Number: {before} → {after_adverse}
- Alignment Score: {before} → {after_adverse}
- CAGR (scenario period): {value}%
- Max Drawdown (simulated): {value}%
- {Additional relevant metric}

[DISC-002, DISC-009 apply to all values in this block]
Note: This scenario does not represent a forecast or prediction.
```

---

## Block 2 — COUNTER_THESIS

### When Required

L4 response level only. Mandatory when [SIMULATION] or [PORTFOLIO_ALIGNMENT] blocks show a directionally clear result (either confirming or contradicting the current allocation).

### Purpose

The counter-thesis presents the strongest analytical argument that the implied direction of the data may be incomplete, misinterpreted, or subject to alternative valid interpretations. This is not skepticism for its own sake — it is required analytical balance.

### Construction Rules

1. **Open with explicit label:** "Alternative interpretation of current data:"
2. **Present 2–4 specific arguments** — each must be analytically grounded
3. **Do not editorialize** — present arguments neutrally, never advocate for the counter position
4. **Close with explicit disclaimer:** "This block presents an alternative analytical view, not a recommendation."
5. No regulatory disclaimers beyond the closing statement required at this block (CGE handles disclaimer injection at pipeline level)

### Common Counter-Thesis Scenarios

**When simulation shows Risk Number improvement:**
- Defensive mandate argues that higher risk was intentional positioning, not drift
- Recent market regime shift may make the "improved" state inappropriate by next quarter
- Rebalancing transaction costs may offset measured metric improvement

**When Alignment Score is below 50:**
- Misalignment may reflect a known and documented advisor override
- Short-term misalignment within a rebalancing cycle — not yet a compliance event
- Client risk event (unreported) may justify divergence from mandate

**When AlphaDroid is in Risk-On:**
- AlphaDroid is a momentum/regime signal, not a forward-looking predictor
- Signal lag may mean current reading reflects last week's regime, not today's
- Client-specific factors may override systematic signal for this portfolio

### Format Template

```
[COUNTER_THESIS]
Alternative interpretation of current data:

1. {Argument 1 — factual, specific, grounded}
2. {Argument 2 — factual, specific, grounded}
3. {Argument 3 if applicable}

Arguments for alternative allocation view:
- {Specific analytical point}
- {Specific analytical point}

[This block presents an alternative analytical view — not a recommendation]
[Investment decisions reside with the licensed advisor in the formal suitability process]
```

---

## Block 3 — MODEL_LIMITATION

### When Required

All SIMULATION and STRESS_TESTING responses at L2+. Must accompany any response that references HRD Engine output, AlphaDroid signals, or StormGuard data.

### Construction Rules

1. **Model-specific** — limitation disclosures must name the specific model (HRD Engine, AlphaDroid, StormGuard, Risk Number)
2. **Not generic** — "past performance does not guarantee results" alone is insufficient; specific model dependencies must be named
3. **Quantified where possible** — e.g., "model trained on data from 2003–2025; pre-2003 regimes not represented"
4. **No minimization** — limitations must be stated clearly, not buried in qualifications

### Standard Limitation Sets by Model

**HRD Engine:**
- Uses trailing-period data; historical correlation may not hold under stress
- CAGR projections based on arithmetic mean; geometric return may differ under volatility drag
- Does not account for tax consequences, withdrawal sequencing, or illiquidity
- Parametric VaR may underestimate tail risk in non-normal distributions
- All values in USD unless stated; currency exposure of non-USD positions not reflected

**Risk Number:**
- Calculated on current allocation snapshot; does not reflect intra-period drift
- Based on Riskalyze methodology; third-party model dependency
- Does not capture client behavioral response to drawdown (behavioral risk not modeled)
- Single composite score — two portfolios with same Risk Number may have materially different risk profiles

**AlphaDroid:**
- Momentum/regime classification — not a predictive signal
- Signal reflects trailing data; regime transitions carry elevated uncertainty
- Regime labels (Aggressive/Moderate/Defensive) are relative classifications, not absolute risk levels
- Model does not incorporate idiosyncratic or company-specific risk for equity positions

**StormGuard:**
- Rule-based system — may not capture novel macro regimes not present in training history
- INACTIVE status does not mean "safe" — it means trigger conditions not currently met
- Trigger thresholds are fixed parameters; market structure changes may affect sensitivity

### Format Template

```
[MODEL_LIMITATION]
{Model Name} — Material Assumptions and Limitations:

- {Limitation 1 — specific}
- {Limitation 2 — specific}
- {Limitation 3 — specific}
- {Additional as applicable}

[DISC-001, DISC-002 reinforce model limitation disclosures where applicable]
```

---

## Adversarial Engine — Output Integration

The AE blocks are integrated into Output 1 (INTERNAL_ANALYSIS) by the Response Orchestrator. They do not appear in Output 2 (CLIENT_READY_MESSAGE) directly, but the ACE may reference that "adverse scenarios were reviewed" in plain language.

### Example Integration

Output 1 (advisor sees):
```
[SIMULATION] ... HRD Engine base case ...
[ADVERSE_SCENARIO] ... Rising rate adverse case ...
[COUNTER_THESIS] ... Alternative interpretation ...
[MODEL_LIMITATION] ... HRD Engine assumptions ...
```

Output 2 (client-ready):
```
Your portfolio has been analyzed including scenarios where market conditions change unfavorably.
Your advisor has reviewed the full analysis and adverse scenario projections.
A detailed review will be shared with you at your next scheduled consultation.
All data is based on historical simulation and is not a guarantee of future results.
Your advisor will make any portfolio decisions within your agreed investment guidelines.
```

---

## Regulatory Basis

| Requirement | Regulatory Source |
|-------------|-----------------|
| Balanced presentation | FINRA Rule 2210(d)(1) |
| Material risk disclosure | SEC Marketing Rule 206(4)-1 |
| No selective performance | FINRA Rule 2210(d)(1)(A) |
| Stress scenario labeling | SEC Marketing Rule, FINRA 2210 |
| Model assumption disclosure | SEC Marketing Rule 206(4)-1(a)(1)(vii) |

---

*New in JIM Architecture v2 | See also: JIM_DUAL_ENGINE.md | JIM_RESPONSE_ENGINE.md | JIM_COMPLIANCE_RULES_v2.md*
