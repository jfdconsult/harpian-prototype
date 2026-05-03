# JIM Architecture
## Pipeline Specification & Component Design

**Version:** 1.0 | **Classification:** Confidential — Internal Use Only

---

## Processing Pipeline

Every user interaction must pass through each stage in order. No stage may be skipped.

```
USER INPUT
    │
    ▼
INTENT CLASSIFIER
  ├─ Classifies: intent_id, category, risk_level
  ├─ Detects: ACTION_REQUEST, INVESTMENT_RECOMMENDATION_REQUEST
  └─ Output: {intent_id, category, risk_level, escalate_flag}
    │
    ▼
CONTEXT ASSEMBLY ENGINE (CAE)
  ├─ Source: HARPIAN Core (not direct DB)
  ├─ Pulls: portfolio metrics, Risk Number, client profile, StormGuard, AlphaDroid, HRD outputs
  └─ Output: context_payload (structured JSON)
    │
    ▼
PERMISSION LAYER
  ├─ Validates: tier + feature access
  ├─ Filters: context_payload to tier-authorized data only
  └─ On fail: ACCESS_DENIED response
    │
    ▼
RESPONSE ENGINE
  ├─ Selects: response_mode (Quick / Deep 1/2/3 / Simulation / Compliance)
  ├─ Assembles: blocks (DIAGNOSTIC, EDUCATION, SIMULATION, etc.)
  └─ Output: draft_response + block_ids + template_id
    │
    ▼
COMPLIANCE GUARDRAIL ENGINE ◄── MANDATORY — cannot be bypassed
  ├─ Severity 1: block + safe fallback + SEVERITY_1_VIOLATION log
  ├─ Severity 2: rewrite + SEVERITY_2_REWRITE log
  ├─ Severity 3: disclaimer append + SEVERITY_3_DISCLAIMER log
  ├─ Recommendation detection: block → ACTION_REQUEST handler
  └─ Output: validated_response OR blocked_response
    │
    ▼
DISCLAIMER ENGINE
  ├─ Selects: DISC-IDs from disclaimer_library.json by intent + blocks
  ├─ Positions: inline or footnote per response mode
  └─ Output: response_with_disclaimers
    │
    ▼
AUDIT LOGGER
  ├─ Writes: immutable log entry (all mandatory fields)
  ├─ Hashes: input, context_payload, final_response
  └─ Output: audit_record (write-once, hash-verified)
    │
    ▼
USER OUTPUT
    │
    └─ [if escalation_flag = true]
         │
         ▼
    REVIEW QUEUE / HUMAN ESCALATION
      ├─ Routes: to FA of record, Compliance Admin, or legal
      └─ Status: pending until human resolution
```

---

## Component Specifications

### Intent Classifier

**Inputs:** raw user text, session context, user tier  
**Outputs:** intent_id, category, risk_level, escalate_flag, language detected  
**Key behaviors:**
- Bilingual detection (English + Portuguese)
- ACTION_REQUEST detection in both languages
- Confidence score output on every classification

### Context Assembly Engine (CAE)

**Interface:** REST API or message queue from HARPIAN Core  
**Output format:** Structured JSON context_payload  
**JIM never calls the database directly**  
**Required fields vary by intent_id** (see intents.json: `required_context_fields`)

### Compliance Guardrail Engine (CGE)

**Trigger:** Every response, no exceptions  
**Inputs:** draft_response, intent_id, user_input  
**Processing order:** Severity 1 → Severity 2 → Severity 3 → Recommendation check  
**Config source:** forbidden_language.json  
**Cannot be disabled by any user tier, including Compliance Admin**

### Disclaimer Engine

**Config source:** disclaimer_library.json  
**Selection logic:** intent_id + blocks_used → required DISC-IDs  
**Placement rules:**
- DISC-002 must appear *before* simulation table
- DISC-009 must appear *before* stress test output
- DISC-006 must appear in full (never abbreviated) for ACTION_REQUEST

### Audit Logger

**Write mode:** Append-only, hash-verified  
**Retention:** Minimum 7 years  
**Schema:** See [JIM_AUDIT_LOGGING.md](JIM_AUDIT_LOGGING.md)  
**Access:** Compliance Admin + Admin (platform-wide); FA/MFO (own sessions)

---

## Source Files

| Component | Source File |
|-----------|-------------|
| Intent Classifier | `src/jim/intentClassifier.ts` |
| Compliance Guardrail Engine | `src/jim/complianceGuardrails.ts` |
| Disclaimer Engine | `src/jim/disclaimerEngine.ts` |
| Response Composer | `src/jim/responseComposer.ts` |
| Audit Logger | `src/jim/auditLogger.ts` |
| Escalation Engine | `src/jim/escalationEngine.ts` |

---

*See also: [JIM_COMPLIANCE_RULES.md](JIM_COMPLIANCE_RULES.md) | [JIM_AUDIT_LOGGING.md](JIM_AUDIT_LOGGING.md)*
