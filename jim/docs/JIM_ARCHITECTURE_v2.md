# JIM Architecture v2 — Dual Engine System
## HARPIAN AI Intelligence Agent — Institutional Grade Pipeline

**Version:** 2.0 | **Supersedes:** JIM_ARCHITECTURE.md (v1.0) | **Classification:** Confidential — Internal Use Only  
**Status:** Active Specification | **Effective:** 2026-Q2

---

## Overview

JIM v2 introduces a **Dual Engine Architecture** that separates internal analytical reasoning from external advisor communication. Every query processed by JIM now produces two distinct outputs through two parallel processing engines.

This architecture enables:
- Full institutional-grade internal analysis (Decision Engine)
- Clean, compliant, advisor-ready client messaging (Advisor Communication Engine)
- Adversarial stress testing on every simulation and risk query
- Automated compliance guardrails on all output paths

---

## Core Principle: Two Outputs, One Pipeline

```
Every JIM query → DECISION ENGINE (Output 1: INTERNAL_ANALYSIS)
                → ADVISOR COMMUNICATION ENGINE (Output 2: CLIENT_READY_MESSAGE)
```

**Output 1 — INTERNAL_ANALYSIS** is never shown to clients. It is the full analytical layer available only to licensed advisors, compliance officers, and system auditors.

**Output 2 — CLIENT_READY_MESSAGE** is a maximum 5-line, plain-language message that advisors may copy-paste into client communications. It carries no jargon, no recommendations, no forward-looking certainty.

---

## v2 Full Processing Pipeline

```
USER INPUT (bilingual EN/PT)
        │
        ▼
┌─────────────────────────────────┐
│  INTENT CLASSIFIER (IC)         │
│  - 300+ question recognition    │
│  - Bilingual (EN + PT)          │
│  - ACTION_REQUEST detection     │
│  - intent_id, category,         │
│    risk_level, response_mode    │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│  CONTEXT ASSEMBLY ENGINE (CAE)  │
│  - Pulls data from HARPIAN Core │
│  - Risk Number, Alignment Score │
│  - Portfolio snapshot           │
│  - JIM never touches DB         │
│  - Validates context_payload    │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│  PERMISSION LAYER (PL)          │
│  - Validates user tier          │
│  - Filters features by tier     │
│  - Routes tier-locked content   │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│  RESPONSE ORCHESTRATOR (RO)     │
│  - Selects response level L1-L4 │
│  - Activates Adversarial Engine │
│    for SIMULATION/RISK queries  │
│  - Routes to Dual Engine split  │
└────────────────┬────────────────┘
                 │
         ┌───────┴───────┐
         │               │
         ▼               ▼
┌────────────────┐  ┌──────────────────────────┐
│  DECISION      │  │  ADVERSARIAL ENGINE (AE)  │
│  ENGINE (DE)   │  │  - Counter-thesis         │
│  OUTPUT 1:     │  │  - Adverse scenarios      │
│  INTERNAL_     │  │  - Model limitations      │
│  ANALYSIS      │  │  - Activates on L3/L4     │
└───────┬────────┘  └──────────────┬───────────┘
        │                          │
        └──────────┬───────────────┘
                   │
                   ▼
┌─────────────────────────────────┐
│  COMPLIANCE GUARDRAIL ENGINE    │
│  ★ MANDATORY — NO BYPASS        │
│  - Severity 1/2/3 scan          │
│  - Recommendation detection     │
│  - Both outputs processed       │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│  DISCLAIMER ENGINE (DISC)       │
│  - DISC-IDs injected by intent  │
│  - Output 1 + Output 2 paths    │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│  ADVISOR COMMUNICATION ENGINE   │
│  OUTPUT 2:                      │
│  CLIENT_READY_MESSAGE           │
│  - Max 5 lines                  │
│  - Plain language               │
│  - No jargon                    │
│  - No recommendations           │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│  AUDIT LOGGER                   │
│  - Immutable write-once log     │
│  - SHA-256 hash                 │
│  - Both outputs archived        │
│  - Books & Records compliant    │
└────────────────┬────────────────┘
                 │
         ┌───────┴───────┐
         │               │
         ▼               ▼
  OUTPUT 1            OUTPUT 2
  INTERNAL_           CLIENT_READY_
  ANALYSIS            MESSAGE
  (Advisor/           (Copy-paste
   Compliance         ready for
   only)              client)
```

---

## New Modules in v2

### 1. DINO — Data Ingestion & Knowledge Operations

DINO is the knowledge base ingestion system that converts Q&A documents into structured retrieval-ready format for JIM's response engine.

- **Source path:** `Q&A/` directory
- **Input formats:** .docx, .pdf, .md
- **Output:** Structured knowledge blocks indexed by intent_id
- **Ingestion method:** Document parsing → chunk extraction → intent tagging → knowledge index
- **Full spec:** `JIM_DINO.md`

### 2. Response Orchestrator (RO)

New in v2 — the RO replaces the simple Response Engine with a level-aware routing layer:

- Reads `intent_id`, `user_tier`, `context_payload`, `confidence_score`
- Selects response level: L1 / L2 / L3 / L4
- Determines if Adversarial Engine activation is required
- Routes to appropriate response template blocks
- Full spec: `JIM_RESPONSE_ENGINE.md`

### 3. Adversarial Engine (AE)

New in v2 — activates automatically for SIMULATION, RISK, ALIGNMENT queries at L3/L4 levels:

- Generates counter-thesis for every strategy presented
- Models adverse scenarios beyond the base case
- Surfaces model limitations and assumption dependencies
- Never promotional, always balanced
- Full spec: `JIM_ADVERSARIAL_ENGINE.md`

### 4. Advisor Communication Engine (ACE)

New in v2 — produces Output 2 from the processed Decision Engine output:

- Strips technical language
- Reduces to maximum 5 lines
- Removes all internal analytical content
- Applies advisor-appropriate neutral framing
- Full spec: `JIM_ADVISOR_COMMUNICATION.md`

---

## Response Level System

| Level | Name | Audience | Depth | Adversarial |
|-------|------|----------|-------|-------------|
| L1 | Client Simplified | Retail clients via advisor | 1–3 lines | No |
| L2 | Advisor Standard | Financial Advisor (FA_LITE, FA_PRO) | 4–10 lines | No |
| L3 | Institutional | MFO, FO Institutional | 10–30 lines | Yes |
| L4 | Adversarial | MFO Institutional, Compliance | 30+ lines | Full activation |

Level is auto-selected based on `user_tier` and `intent risk_level`. It cannot be manually downgraded by the user.

---

## ACTION_REQUEST — Unchanged from v1, Reinforced in v2

ACTION_REQUEST handling is identical to v1 but is now enforced at the Response Orchestrator level before any engine activates:

> *"JIM does not provide individualized investment recommendations. JIM can present the mathematical simulation, the portfolio diagnostic, and the risk/return impact based on data loaded in the terminal. The investment decision must be made by a licensed advisor, within the formal suitability process, in accordance with the client's best interest."*

No engine output is generated for ACTION_REQUEST. The mandatory response text is delivered directly from the Compliance Guardrail Engine.

---

## Data Flow Rules (Unchanged from v1, Enforced in v2)

1. **JIM never touches the database directly** — all data comes via HARPIAN Core API through CAE
2. **JIM never calculates** — the LLM explains; HARPIAN Core (HRD Engine) calculates
3. **Simulations are attributed to HRD Engine** — never presented as JIM outputs
4. **Both outputs pass through CGE** — no bypass, no exception, no tier exemption
5. **Audit Logger receives both outputs** — immutable, SHA-256 hashed, 7-year retention

---

## Compatibility with v1

All v1 intent IDs (INT-001 through INT-030) remain valid in v2. The v2 expansion adds metadata fields to each intent entry:

- `dual_engine_mode`: whether both engines activate
- `adversarial_trigger`: whether AE activates
- `output_2_template`: which ACE template is used
- `response_level_override`: if a specific level is forced

Existing config files remain in place. v2 config files use `_v2` suffix.

---

## File Index — JIM v2

| File | Purpose |
|------|---------|
| `JIM_ARCHITECTURE_v2.md` | This document — full pipeline |
| `JIM_DUAL_ENGINE.md` | Output 1 and Output 2 specifications |
| `JIM_RESPONSE_ENGINE.md` | L1–L4 level system and orchestration |
| `JIM_ADVISOR_COMMUNICATION.md` | ACE — client message templates |
| `JIM_ADVERSARIAL_ENGINE.md` | Adversarial Engine specification |
| `JIM_COMPLIANCE_RULES_v2.md` | Updated CGE with dual-engine rules |
| `JIM_DINO.md` | Knowledge base ingestion system |
| `config/intents_v2.json` | Expanded intent map (30+ intents, dual-engine metadata) |
| `config/response_templates.json` | Dual-engine response templates |
| `config/dual_engine_rules.json` | Dual-engine routing rules |

---

*Supersedes: JIM_ARCHITECTURE.md (v1.0)*  
*See also: JIM_COMPLIANCE_RULES.md (v1) | JIM_COMPLIANCE_RULES_v2.md | JIM_INTENT_MAP.md*  
*Regulatory basis: SEC Marketing Rule, Reg BI, Form CRS, FINRA Rule 2210, FINRA Books & Records*
