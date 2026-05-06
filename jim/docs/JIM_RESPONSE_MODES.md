# JIM Response Modes
## Mode Specifications, Format Rules & Examples

**Version:** 1.0 | **Classification:** Confidential — Internal Use Only

---

## Mode Selection Logic

Response mode is selected automatically based on:
1. Intent category and subcategory
2. User tier
3. Query complexity
4. Presence of simulation data

---

## Mode Reference

| Mode | Length | Use Case | Tier Access | Disclaimer Format |
|------|--------|----------|-------------|-------------------|
| Quick | 1–3 lines | Status checks, navigation, simple facts | All | Abbreviated + link to full |
| Deep Mode 1 | 4–10 lines | Accessible explanation, entry-level FA | All | Inline |
| Deep Mode 2 | 10–30 lines | Technical with formulas, FA Pro + MFO | FA_PRO+ | Full inline |
| Deep Mode 3 | 30+ lines | Institutional methodology | MFO_INSTITUTIONAL, COMPLIANCE_ADMIN | Full + methodology refs |
| Simulation | Variable | HRD Engine outputs, "what if" scenarios | FA_LITE+ | DISC-002 mandatory before table |
| Compliance | Variable | Regulatory questions, escalations | All | DISC-006 in full |

---

## Quick Mode

**Format:** 1–3 lines, direct answer, link to module, abbreviated disclaimer if required.

```
Risk Number: 67 | Target: 60 | Gap: +7 → Flagged for review.
[Open Risk Dashboard]
```

**Constraints:**
- Required disclaimers must still appear, even abbreviated
- Not appropriate for simulation or compliance intents

---

## Deep Mode 1 — Accessible Explanation

**Format:** 4–10 lines, plain language, analogies permitted if not misleading, disclaimer inline.

**Example:**
> "Alignment Score measures how closely a portfolio matches the client's stated goals, risk tolerance, and time horizon. Think of it as a diagnostic checkup — 100 means fully aligned, below 70 indicates meaningful deviation that should be reviewed. The current score of 58 reflects three open flags: elevated risk, shortened horizon, and mandate deviation. These are diagnostic indicators for the advisor to review, not automated recommendations."

---

## Deep Mode 2 — Technical Explanation

**Format:** 10–30 lines, variables and formulas included, worked example with real values, methodology source referenced, full disclaimer block.

**Example:**
> "Sharpe Ratio = (Portfolio Return − Risk-Free Rate) / Portfolio Standard Deviation
>
> For the current portfolio:
> - Return (annualized, 36-month): 8.4%
> - Risk-Free Rate: 5.2%
> - Standard Deviation: 12.7%
> - Sharpe = (8.4% − 5.2%) / 12.7% = **0.25**
>
> A Sharpe of 0.25 indicates 0.25 units of excess return per unit of risk. Benchmark (S&P 500) Sharpe for the same period: 0.31. *Past performance does not guarantee future results.*"

---

## Deep Mode 3 — Institutional Methodology

**Format:** Full methodology exposition, TPT/MPT references, statistical framework, explicit model limitations.

**Tier:** MFO_INSTITUTIONAL, COMPLIANCE_ADMIN only.

**Required elements:**
- Model assumptions listed explicitly
- Known limitations stated
- Methodology source referenced
- Full disclaimer block

---

## Simulation Mode

**Format:** Before/After table, HRD Engine attribution, DISC-002 before the table.

**Required fields in every simulation output:**
- Risk Number (before/after)
- Projected CAGR (before/after)
- Max Drawdown (before/after)
- Horizon Gap (before/after)
- Alignment Score (before/after)

**Template:**
```
SIMULATION OUTPUT — HRD Engine | Hypothetical Scenario Only
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Scenario: [scenario description]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                     BEFORE          AFTER (Hypothetical)
Risk Number:           [X]              [Y]
Proj. CAGR:           [X]%             [Y]%
Max Drawdown:         [X]%             [Y]%
Horizon Gap:         +$[X]            +$[Y]
Alignment Score:       [X]              [Y]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠ [DISC-002 text]
```

---

## Compliance Mode

**Format:** Clear scope statement, regulatory reference, escalation pathway, full disclaimer.

**Example:**
> "This question involves a suitability determination, which is outside JIM's authorized function. Suitability requires the formal Reg BI best-interest analysis performed by a licensed advisor. JIM can provide the diagnostic data — Risk Number, Alignment Score, mandate flags — for the advisor's use in that process. This session has been flagged for advisor review. [DISC-006]"

---

*See also: [JIM_COMPLIANCE_RULES.md](JIM_COMPLIANCE_RULES.md) | [JIM_DISCLAIMER_LIBRARY.md](JIM_DISCLAIMER_LIBRARY.md)*
