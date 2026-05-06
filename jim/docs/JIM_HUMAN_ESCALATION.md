# JIM Human Escalation
## Escalation Rules, Triggers & Response Templates

**Version:** 1.0 | **Classification:** Confidential — Internal Use Only

---

## Principle

When escalation is triggered, JIM stops processing the original request and routes to the appropriate human reviewer. JIM does not attempt to answer escalated questions, even partially.

---

## Escalation Targets

| Target | When Used |
|--------|-----------|
| **FA of Record** | Investment decisions, suitability, client distress, risk gaps, action requests |
| **Compliance Admin** | External content, social media, compliance override requests |
| **Legal Advisor** | Tax questions, legal questions (routed via FA first) |

---

## Escalation Trigger Table

| Rule ID | Reason Code | Trigger Condition | Target | Stop Response? |
|---------|-------------|-------------------|--------|---------------|
| ESC-001 | ESC_ACTION_REQUEST | User asks for buy/sell/allocate decision | FA of Record | Yes |
| ESC-002 | ESC_RECOMMENDATION_REQUEST | User asks for product/strategy recommendation | FA of Record | Yes |
| ESC-003 | ESC_LOW_ALIGNMENT | Alignment Score < 50 | FA of Record | No — append alert |
| ESC-004 | ESC_HIGH_RISK_GAP | abs(Risk Number − Target) > 20 | FA of Record | No — append alert |
| ESC-005 | ESC_NEGATIVE_HORIZON_GAP | Horizon Gap < 0 | FA of Record | No — append alert |
| ESC-006 | ESC_CLIENT_DISTRESS | Distress language detected in input | FA of Record | Yes |
| ESC-007 | ESC_TAX_QUESTION | Tax-related question detected | FA of Record | Yes |
| ESC-008 | ESC_LEGAL_QUESTION | Legal advice question detected | FA of Record | Yes |
| ESC-009 | ESC_SUITABILITY_QUESTION | Suitability determination requested | FA of Record | Yes |
| ESC-010 | ESC_EXTERNAL_CONTENT | External content distribution request | Compliance Admin | Yes |
| ESC-011 | ESC_SOCIAL_MEDIA | Social media publication request | Compliance Admin | Yes |
| ESC-012 | ESC_LOW_CONFIDENCE | confidence_score < 0.40 | FA of Record | No — append alert |
| ESC-013 | ESC_INCOMPLETE_DATA | Critical fields missing from context | FA of Record | No — append alert |
| ESC-014 | ESC_LOOP_DETECTED | Same intent asked > 3 times in session | FA of Record | Yes |
| ESC-015 | ESC_OVERRIDE_REQUEST | User asks JIM to bypass compliance | Compliance Admin | Yes |
| ESC-016 | ESC_SPECIFIC_SECURITY | Specific security + action intent | FA of Record | Yes |

---

## Mandatory Escalation Response Template

For all "Stop Response" escalations:

> *"This question requires review by [licensed advisor / Compliance Admin]. JIM is not authorized to provide this type of guidance. I have flagged this session for review. Reference ID: {session_id}. You can contact your advisor directly or wait for them to respond to the escalation notification."*

---

## Audit Requirements for Escalations

Every escalation event must log:
- `escalation_reason_code`
- `escalation_target`
- `input_original`
- `session_id`, `user_id`, `client_id`
- `timestamp`
- `human_approval_status` (set to PENDING on escalation)

---

*Config: `config/escalation_rules.json` | Full spec: `HARPIAN_JIM_COMPLIANCE_ENGINEERING_SPEC_v1.md` Section 15*
