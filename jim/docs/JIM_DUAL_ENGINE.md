# JIM Dual Engine Specification
## OUTPUT 1 (INTERNAL_ANALYSIS) + OUTPUT 2 (CLIENT_READY_MESSAGE)

**Version:** 2.0 | **Classification:** Confidential — Internal Use Only  
**Part of:** JIM Architecture v2

---

## Core Concept

Every JIM query produces two structurally distinct outputs processed in parallel after the Response Orchestrator stage. These outputs serve different audiences and carry different content, format, and regulatory treatment.

```
Single Query → DECISION ENGINE → OUTPUT 1: INTERNAL_ANALYSIS
             → ADVISOR COMM. ENGINE → OUTPUT 2: CLIENT_READY_MESSAGE
```

---

## OUTPUT 1 — INTERNAL_ANALYSIS

### Purpose

Full institutional-grade analysis for the licensed advisor, compliance officer, or authorized system user. This output contains the complete reasoning chain — including adversarial scenarios, model limitations, and counter-theses — that supports but never replaces the advisor's professional judgment.

### Audience

- Financial Advisors (FA_LITE, FA_PRO)
- MFO / FO Institutional
- Compliance Admin
- System Auditor

**Never shown to clients.**

### Structure

Output 1 follows a fixed 8-block structure. Each block is labeled and separated. Not all blocks are present in every response — the Response Orchestrator selects applicable blocks based on `intent_id` and `response_level`.

---

#### BLOCK 1 — DIAGNOSTIC

**Present in:** All intents (except ACTION_REQUEST — mandatory response only)  
**Purpose:** Factual state of the indicator or portfolio metric being queried  
**Format:** Direct statements of measured values, no forward-looking language

```
[DIAGNOSTIC]
Risk Number: 72 | Target: 60 | Gap: +12
Alignment Score: 48 — Below threshold (50)
AlphaDroid Signal: Defensive (as of 2026-04-28)
StormGuard: INACTIVE — Regime: Growth
```

**Rules:**
- All values must come from `context_payload` (CAE-assembled data)
- No interpretation of what values "mean" for the client's future
- If data missing: flag with `[DATA_UNAVAILABLE]` and apply DISC-011

---

#### BLOCK 2 — CAUSE

**Present in:** PORTFOLIO_ALIGNMENT, RISK_NUMBER delta, QUANTITATIVE_METRICS anomaly  
**Purpose:** Technical explanation of why the measured state exists  
**Format:** Factor attribution, plain analytical language

```
[CAUSE]
Alignment Score below threshold driven by:
- Fixed Income allocation 38% vs. mandate max 25% (+13% excess)
- Risk Number above target by 12 points following March rebalance
- Duration gap: portfolio 7.2Y vs. mandate 4.5Y
```

**Rules:**
- Must be factual attribution only — not prescriptive
- May reference mandate parameters
- May not suggest what to do about the cause

---

#### BLOCK 3 — SIMULATION

**Present in:** INT-015, INT-016, INT-020 — and any query triggering HRD Engine output  
**Purpose:** Present hypothetical scenario output from HRD Engine  
**Format:** Before/After comparison table, labeled as hypothetical

```
[SIMULATION]
HRD Engine — Hypothetical Scenario (Not a recommendation)

Scenario: +10% allocation to HPC22, -10% HPC11

                    Before          After (Hypothetical)
Risk Number:         72              68
Alignment Score:     48              61
Sharpe (3Y):        0.81            0.87
Max Drawdown:       -18.3%          -16.1%
CAGR (3Y):          7.2%            7.6%

[DISC-002 applies to all values in this block]
```

**Rules:**
- DISC-002 must appear before the table, not after
- Must attribute to "HRD Engine — Hypothetical Scenario"
- Must include both Before and After columns
- Must not characterize the After column as "better" or "recommended"

---

#### BLOCK 4 — RISK

**Present in:** SIMULATION responses, PORTFOLIO_ALIGNMENT, STRESS_TESTING  
**Purpose:** Quantified risk metrics for the current or simulated state  
**Format:** Structured metric table

```
[RISK]
Measured Risk Metrics (Current Portfolio):
- Volatility (1Y): 14.2%
- Max Drawdown (3Y): -18.3%
- Beta vs. S&P 500: 0.91
- VaR 95% (Monthly): -4.1%
- Correlation to benchmark: 0.87
```

**Rules:**
- All metrics must be sourced from `context_payload`
- Historical period must be stated for every metric
- DISC-001 applies to all historical risk metrics

---

#### BLOCK 5 — ADVERSE_SCENARIO

**Present in:** L3/L4 responses, SIMULATION, STRESS_TESTING — Adversarial Engine activation  
**Purpose:** Model the scenario in which the strategy or allocation fails  
**Format:** Named scenario with quantified impact

```
[ADVERSE_SCENARIO]
Adversarial Engine — Adverse Case Analysis

Scenario: HPC22 allocation underperforms in Rising Rate Environment

Conditions tested:
- 10Y Treasury yield: +150bps over 12 months
- Credit spread widening: +80bps (IG universe)
- Equity correction: -15% (S&P 500)

Projected portfolio impact (hypothetical):
- Risk Number: 72 → 79 (pro-cyclical increase)
- Alignment Score: 48 → 39 (further misalignment)
- CAGR (12M simulated): -3.2%
- Max Drawdown (simulated): -22.1%

[DISC-002, DISC-009 apply to all values in this block]
```

**Rules:**
- Must be explicitly labeled "Adversarial Engine" and "Adverse Case"
- Must not imply this scenario is certain or probable
- DISC-009 required for all stress test scenarios
- Cannot be the only scenario presented — must accompany a base case [SIMULATION] block

---

#### BLOCK 6 — COUNTER_THESIS

**Present in:** L4 (Adversarial level) only — when strategy has alternative interpretation  
**Purpose:** Present the strongest analytical argument against the implied direction  
**Format:** Structured argument, no judgment

```
[COUNTER_THESIS]
Alternative interpretation of current portfolio state:

The measured misalignment (Alignment Score: 48) may reflect:
1. Deliberate defensive positioning by the advisor, not drift
2. Short-term mandate divergence within tolerance parameters
3. Recent client risk event not captured in current Risk Number

Arguments for maintaining current allocation:
- AlphaDroid in Defensive mode supports lower-risk positioning
- StormGuard inactive but Growth/Defensive boundary within 8%
- Fixed income overweight partially hedged by duration reduction

[This block presents an alternative analytical view — not a recommendation]
```

**Rules:**
- Must open with explicit label: "Alternative interpretation"
- Must close with explicit non-recommendation statement
- Cannot be omitted at L4 when simulation results are directionally strong
- Regulatory basis: balanced presentation requirement (FINRA Rule 2210)

---

#### BLOCK 7 — MODEL_LIMITATION

**Present in:** SIMULATION, STRESS_TESTING, ADVERSARIAL_ENGINE outputs  
**Purpose:** Disclose assumptions and model dependencies  
**Format:** Bulleted limitation list

```
[MODEL_LIMITATION]
HRD Engine Model Assumptions — Material Limitations:

- CAGR projections use trailing 3Y data; past performance does not predict future results
- Correlation coefficients assume historical co-movement — may not hold under stress
- Risk Number calculated on current allocation — does not reflect intra-period rebalancing
- Stress scenarios use parametric VaR — tail events may exceed modeled distributions
- AlphaDroid signal is regime-based; transition periods carry elevated model uncertainty
- All values in USD — currency exposure not reflected for non-USD-denominated positions

[DISC-001, DISC-002 reinforce model limitation disclosures]
```

**Rules:**
- Always present in SIMULATION and STRESS_TESTING responses
- Must be specific to the model being used — not generic disclaimers
- Cannot be placed after the simulation table — must appear alongside or before

---

#### BLOCK 8 — NEUTRAL_CONCLUSION

**Present in:** All L2+ responses  
**Purpose:** Summary statement that synthesizes the diagnostic without prescribing action  
**Format:** 2–4 sentences, analytical close

```
[NEUTRAL_CONCLUSION]
The current portfolio shows a measured Risk Number of 72 against a client target of 60,
with an Alignment Score of 48, below the 50-point threshold. The HRD Engine simulation
indicates that a hypothetical reallocation scenario reduces the measured gap. Adverse
scenario analysis shows material sensitivity to a rising rate environment. The investment
decision resides with the licensed advisor within the formal suitability process.
```

**Rules:**
- Must not recommend action
- Must reference the formal suitability process
- Must not use: "should", "recommend", "ideal", "best", "you should"
- Must use: "measured", "simulated", "hypothetical", "the data shows", "the diagnostic indicates"

---

## OUTPUT 2 — CLIENT_READY_MESSAGE

### Purpose

A maximum 5-line plain-language message that the advisor may copy-paste or paraphrase into client communications. Derived from Output 1 — never generated independently.

### Audience

- End clients (via advisor forwarding)
- Advisor assistants drafting client communications

### Rules — Non-Negotiable

1. **Maximum 5 lines** — no exceptions
2. **No financial jargon** — Risk Number becomes "portfolio risk level", Sharpe becomes omitted or "risk-adjusted return"
3. **No recommendations** — no "you should", "we recommend", "the best option"
4. **No simulation numbers** — unless explicitly requested, and if included must carry "(hypothetical, not a guarantee)"
5. **Neutral tone** — no alarm, no optimism, no reassurance beyond factual state
6. **Plain language** — readable at 8th-grade level

### Structure

```
[CLIENT_READY_MESSAGE]
Line 1: Current portfolio status (1 sentence)
Line 2: Key metric state (1 sentence)
Line 3: Any relevant alert or flag (1 sentence, if applicable)
Line 4: What the advisor will review or discuss (1 sentence)
Line 5: Standard regulatory close (fixed — from template library)
```

### Example — Portfolio Misalignment Query

**Output 1 → INTERNAL_ANALYSIS (advisor sees):**
> [DIAGNOSTIC] Risk Number: 72, Target: 60, Gap: +12. Alignment Score: 48, threshold 50.
> [CAUSE] Fixed income overweight driving misalignment...
> [SIMULATION] HRD Engine: hypothetical reallocation reduces gap to 4...
> [NEUTRAL_CONCLUSION] Decision resides with licensed advisor...

**Output 2 → CLIENT_READY_MESSAGE (client sees):**
```
[CLIENT_READY_MESSAGE]
Your portfolio is currently positioned slightly above your agreed risk level.
Our monitoring system has flagged a gap between your current allocation and your target profile.
Your advisor has been notified and will review your portfolio.
You can expect a call or message from your advisor to discuss any potential adjustments.
All decisions regarding your portfolio are made by your advisor in accordance with your investment objectives.
```

---

### Template Mapping

The Advisor Communication Engine selects from pre-approved templates in `config/response_templates.json`. Templates are indexed by:
- `intent_category`
- `alert_level` (none / informational / flagged / critical)
- `client_language` (EN / PT)

Custom messages are not permitted — advisors choose from approved templates.

---

## Dual Engine — Activation Matrix

| Intent Category | Output 1 | Output 2 | Adversarial |
|----------------|----------|----------|-------------|
| RISK_NUMBER | Full | Yes | No |
| QUANTITATIVE_METRICS | Full | Yes | No |
| STORMGUARD | Full | Yes | No |
| ALPHADROID | Full | Yes | No |
| PORTFOLIO_ALIGNMENT | Full | Yes | L3+ |
| SIMULATION_ENGINE | Full | Yes | Always |
| DAILY_DASHBOARD | Summary | Yes | No |
| HIDDEN_RISK | Full | Yes | L3+ |
| STRESS_TESTING | Full | Yes | Always |
| COMPLIANCE_SUITABILITY | Compliance only | No | No |
| FO_INSTITUTIONAL | Full | Internal only | L4 |
| UX_NAVIGATION | Navigation | No | No |
| ACTION_REQUEST | Mandatory response only | No | No |

---

*Part of JIM Architecture v2 | See also: JIM_RESPONSE_ENGINE.md | JIM_ADVERSARIAL_ENGINE.md | JIM_ADVISOR_COMMUNICATION.md*
