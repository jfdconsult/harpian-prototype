# JIM Response Engine v2
## Response Orchestrator + Level System (L1–L4)

**Version:** 2.0 | **Classification:** Confidential — Internal Use Only  
**Supersedes:** JIM_RESPONSE_MODES.md (v1.0)

---

## Overview

The Response Engine in v2 is replaced by a two-component system:

1. **Response Orchestrator (RO)** — routes the query to the correct level and activates engines
2. **Response Level System (L1–L4)** — defines depth, blocks, and format for each output

The orchestrator is the decision layer. It reads the classified intent, user tier, context payload completeness, and confidence score to determine the full processing path before any engine generates content.

---

## Response Orchestrator (RO)

### Inputs

| Field | Source | Required |
|-------|--------|----------|
| `intent_id` | Intent Classifier | Yes |
| `intent_category` | Intent Classifier | Yes |
| `risk_level` | Intent Classifier | Yes |
| `user_tier` | Permission Layer | Yes |
| `context_payload` | CAE | Yes |
| `confidence_score` | Intent Classifier | Yes |
| `session_flags` | Session state | Yes |
| `language` | Detected from input | Yes |

### Orchestrator Decision Tree

```
1. Is this ACTION_REQUEST (INT-027/028/029/030)?
   YES → Deliver mandatory ACTION_REQUEST response → stop, log, escalate
   NO  → Continue

2. Is confidence_score < 0.40?
   YES → Deliver clarification request → ESC-012 → stop
   NO  → Continue

3. Is context_payload critically incomplete?
   YES → Deliver partial response with DISC-011 → flag for FA
   NO  → Continue

4. Select response level:
   - user_tier = CLIENT      → L1
   - user_tier = FA_LITE     → L2
   - user_tier = FA_PRO      → L2 (with technical blocks)
   - user_tier = MFO         → L3
   - user_tier = FO_INST     → L3/L4 based on intent risk_level
   - user_tier = COMPLIANCE  → L4 (full adversarial)
   - user_tier = ADMIN       → L2 (navigation/admin only)

5. Activate Adversarial Engine?
   - response_level = L3 AND intent_category IN [SIMULATION, PORTFOLIO_ALIGNMENT, HIDDEN_RISK, STRESS_TESTING] → YES
   - response_level = L4 → ALWAYS YES
   - Otherwise → NO

6. Select block set:
   Based on intent_id → select applicable blocks from BLOCK_SET_MAP (see below)

7. Route to Dual Engine:
   - DECISION ENGINE → build Output 1
   - ADVISOR COMMUNICATION ENGINE → build Output 2 (if applicable)
```

---

## Response Levels

### L1 — Client Simplified

**Audience:** End clients (via advisor relay only)  
**Trigger:** `user_tier = CLIENT` or any CLIENT_RELAY context  
**Output 1 depth:** 1–3 lines (DIAGNOSTIC block only)  
**Output 2:** Yes — always generated at L1  
**Adversarial Engine:** No  
**Disclaimer injection:** Minimal — DISC-003 if Risk Number, DISC-001 if historical data  

**Format:**
```
[DIAGNOSTIC]
Portfolio risk level: above your agreed target.
Monitoring system status: flagged for advisor review.

[CLIENT_READY_MESSAGE]
[5-line plain language message — see ACE spec]
```

**Tone rules:**
- No numbers (Risk Number, Sharpe, etc.) visible to client directly
- No simulation outputs at L1
- No adverse scenarios at L1

---

### L2 — Advisor Standard

**Audience:** Financial Advisors (FA_LITE, FA_PRO)  
**Trigger:** `user_tier = FA_LITE` or `FA_PRO`  
**Output 1 depth:** 4–10 lines — DIAGNOSTIC + CAUSE + RISK  
**Output 2:** Yes — generated from Output 1 summary  
**Adversarial Engine:** No  
**Disclaimer injection:** Standard — applicable DISC-IDs by intent  

**Format:**
```
[DIAGNOSTIC]
[Measured values with full metrics]

[CAUSE]
[Factor attribution for flagged metrics]

[RISK]
[Key risk metrics — Sharpe, Drawdown, Volatility]

[NEUTRAL_CONCLUSION]
[2–3 line analytical close]
```

**FA_PRO extension:**
FA_PRO tier receives additional technical depth within L2:
- Formula definitions if relevant to query
- Methodology source reference (e.g., "Risk Number: Riskalyze methodology")
- Period specification for all historical metrics

---

### L3 — Institutional

**Audience:** MFO, FO Institutional  
**Trigger:** `user_tier = MFO` or `FO_INST` with non-critical risk_level  
**Output 1 depth:** 10–30 lines — all applicable blocks  
**Output 2:** Yes — institutional-adapted message  
**Adversarial Engine:** Yes (for SIMULATION, PORTFOLIO_ALIGNMENT, STRESS_TESTING)  
**Disclaimer injection:** Full — all applicable DISC-IDs  

**Format:**
```
[DIAGNOSTIC]
[Full metric set with period specification]

[CAUSE]
[Multi-factor attribution]

[SIMULATION]  (if applicable)
[HRD Engine hypothetical table — Before/After]

[RISK]
[Full risk metric table]

[ADVERSE_SCENARIO]  (Adversarial Engine output)
[Named adverse scenario with quantified impact]

[MODEL_LIMITATION]
[Model assumptions and material limitations]

[NEUTRAL_CONCLUSION]
[Institutional-grade analytical close]
```

---

### L4 — Adversarial

**Audience:** MFO Institutional (senior), Compliance Admin  
**Trigger:** `user_tier = FO_INST` with HIGH/CRITICAL risk_level, or `user_tier = COMPLIANCE`  
**Output 1 depth:** 30+ lines — all blocks, full adversarial activation  
**Output 2:** Internal-only institutional summary (not client-facing)  
**Adversarial Engine:** Full activation — all blocks  
**Disclaimer injection:** Full + reinforced  

**Format (all 8 blocks):**
```
[DIAGNOSTIC]
[CAUSE]
[SIMULATION]
[RISK]
[ADVERSE_SCENARIO]
[COUNTER_THESIS]
[MODEL_LIMITATION]
[NEUTRAL_CONCLUSION]
```

**L4-specific rules:**
- COUNTER_THESIS is mandatory — cannot be suppressed
- ADVERSE_SCENARIO must present at minimum 2 named scenarios
- MODEL_LIMITATION must be specific per model used (HRD Engine, StormGuard, AlphaDroid)
- NEUTRAL_CONCLUSION must explicitly reference formal suitability process

---

## Block Set Map

For each `intent_id`, the Response Orchestrator selects applicable blocks:

| Intent Category | DIAG | CAUSE | SIM | RISK | ADV | CTR | LIMIT | CONCL |
|----------------|------|-------|-----|------|-----|-----|-------|-------|
| RISK_NUMBER | ✓ | ✓ | — | — | — | — | — | ✓ |
| QUANTITATIVE_METRICS | ✓ | ✓ | — | ✓ | — | — | ✓ | ✓ |
| STORMGUARD | ✓ | ✓ | — | ✓ | — | — | ✓ | ✓ |
| ALPHADROID | ✓ | ✓ | — | ✓ | — | — | ✓ | ✓ |
| PORTFOLIO_ALIGNMENT | ✓ | ✓ | ✓* | ✓ | L3+ | L4 | ✓ | ✓ |
| SIMULATION_ENGINE | ✓ | — | ✓ | ✓ | ✓ | L4 | ✓ | ✓ |
| DAILY_DASHBOARD | ✓ | — | — | — | — | — | — | — |
| HIDDEN_RISK | ✓ | ✓ | — | ✓ | L3+ | L4 | ✓ | ✓ |
| STRESS_TESTING | ✓ | — | ✓ | ✓ | ✓ | L4 | ✓ | ✓ |
| COMPLIANCE | — | — | — | — | — | — | — | — |
| FO_INSTITUTIONAL | ✓ | ✓ | ✓ | ✓ | L4 | L4 | ✓ | ✓ |
| UX_NAVIGATION | NAV | — | — | — | — | — | — | — |
| ACTION_REQUEST | — | — | — | — | — | — | — | — |

*SIM block for PORTFOLIO_ALIGNMENT only when HRD Engine simulation is available in context

Legend: ✓ = always present | L3+ = L3 and above only | L4 = L4 only | — = not applicable

---

## Confidence Score Thresholds

| Score | Action |
|-------|--------|
| ≥ 0.90 | Proceed normally |
| 0.70–0.89 | Proceed + append DISC-012 |
| 0.40–0.69 | Proceed at reduced depth + DISC-012 + flag for review |
| < 0.40 | Clarification request → ESC-012 |

---

## Language Handling

JIM v2 is bilingual (EN / PT-BR). The Response Orchestrator detects input language and routes to the matching template set in `config/response_templates.json`. All regulatory text (DISC-IDs, ACTION_REQUEST mandatory response, NEUTRAL_CONCLUSION regulatory closes) is maintained in both languages.

Language detection is input-based. The user does not select language manually.

---

## Session State Flags

The Orchestrator reads session flags to detect escalation conditions:

| Flag | Condition | Action |
|------|-----------|--------|
| `repeated_query` | Same intent_id > 3× in session | ESC-014 → FA of Record |
| `override_request` | User asks to bypass compliance | ESC-015 → Compliance Admin |
| `distress_language` | Emotional/panic language detected | ESC-006 → FA of Record |
| `suitability_topic` | Suitability determination requested | ESC-009 → FA of Record → DISC-006 |
| `social_share_request` | Social media content requested | ESC-011 → Compliance Admin |

---

*Supersedes: JIM_RESPONSE_MODES.md (v1.0)*  
*See also: JIM_DUAL_ENGINE.md | JIM_ADVERSARIAL_ENGINE.md | JIM_ARCHITECTURE_v2.md*
