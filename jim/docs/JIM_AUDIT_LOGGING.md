# JIM Audit Logging
## Immutable Log Schema & Retention Specification

**Version:** 1.0 | **Classification:** Confidential — Internal Use Only  
**Regulatory Basis:** FINRA Rule 4511, SEC Books and Records

---

## Principle

Every JIM response generates a mandatory, immutable audit log entry. Logs are write-once, hash-verified, and retained for a minimum of 7 years. No user tier — including Compliance Admin — may delete or modify a log entry after it is written.

---

## Mandatory Log Fields

| Field | Type | Description |
|-------|------|-------------|
| `log_id` | UUID | Unique identifier for this log entry |
| `timestamp` | ISO 8601 UTC | Exact time of response generation |
| `user_id` | String | HARPIAN user identifier |
| `session_id` | UUID | Session identifier |
| `tier` | Enum | User tier at time of interaction |
| `client_id` | String | Client discussed (if applicable) |
| `intent_id` | String | Classified intent |
| `input_original` | String | Raw user input, verbatim |
| `input_normalized` | String | Preprocessed/normalized input |
| `context_payload_hash` | SHA-256 | Hash of context payload from CAE |
| `model_provider` | String | LLM provider used |
| `model_id` | String | Specific model version |
| `response_mode` | Enum | Response mode used |
| `template_id` | String | Response template applied |
| `blocks_used` | Array[String] | Block IDs in response |
| `disclaimer_ids` | Array[String] | Disclaimer IDs appended |
| `compliance_flags` | Array[String] | CGE flags triggered |
| `forbidden_terms_detected` | Array[String] | Forbidden terms found (if any) |
| `confidence_score` | Float [0-1] | JIM confidence score |
| `escalation_status` | Enum | NONE / PENDING / RESOLVED |
| `escalation_reason` | String | Reason code if escalated |
| `response_final_hash` | SHA-256 | Hash of final delivered response |
| `human_approval_status` | Enum | NOT_REQUIRED / PENDING / APPROVED / REJECTED |
| `human_approver_id` | String | Approving user ID (if applicable) |
| `approval_timestamp` | ISO 8601 | Approval/rejection timestamp |
| `log_version` | String | Log schema version |

---

## Integrity Requirements

- **Write-once:** No UPDATE or DELETE operations permitted
- **Hash verification:** Each entry hash-verified on write and retrieval
- **Tamper evidence:** Any modification attempt triggers Compliance Admin alert
- **Export:** Exportable to CSV and JSON for regulatory review

---

## Retention Schedule

| Record Type | Retention Period |
|-------------|----------------|
| All JIM sessions | 7 years minimum |
| Simulation outputs | 7 years |
| External content approvals | 7 years |
| Escalation records | 7 years |
| Model version registry | Indefinite |
| Disclaimer version history | Indefinite |

---

## Access Control

| Tier | Access Level |
|------|-------------|
| FA Free / Lite / Pro | Own sessions only |
| MFO Lite / Institutional | Full book |
| Admin | Platform-wide |
| Compliance Admin | Platform-wide + approval authority |

---

*Full schema: `HARPIAN_JIM_COMPLIANCE_ENGINEERING_SPEC_v1.md` Section 13*
