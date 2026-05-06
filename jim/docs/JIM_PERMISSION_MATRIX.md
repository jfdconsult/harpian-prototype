# JIM Permission Matrix
## Tier-Based Feature Access Control

**Version:** 1.0 | **Classification:** Confidential — Internal Use Only  
**Machine-readable format:** `config/permission_matrix.json`

---

## User Tiers

| Tier ID | Name | Description |
|---------|------|-------------|
| FA_FREE | FA Free | Entry-level; basic diagnostic and navigation |
| FA_LITE | FA Lite | Standard FA; most diagnostic and educational features |
| FA_PRO | FA Pro | Full FA; advanced analytics, simulations, comparisons |
| MFO_LITE | MFO Lite | Multi-Family Office with book management |
| MFO_INSTITUTIONAL | MFO Institutional | Full institutional; Deep Mode 3, bulk operations |
| ADMIN | Admin | Platform administration; user/config management |
| COMPLIANCE_ADMIN | Compliance Admin | Compliance oversight; approval and override authority |

---

## Access Matrix

| Feature | FA Free | FA Lite | FA Pro | MFO Lite | MFO Inst. | Admin | Comp. Admin |
|---------|:-------:|:-------:|:------:|:--------:|:---------:|:-----:|:-----------:|
| Risk Number — Own Clients | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Risk Number — Book-Level | ✗ | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Active Portfolio View | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Client Book Access | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Simulations — Basic | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Simulations — Advanced | ✗ | ✗ | ✓ | ✓ | ✓ | ✗ | ✓ |
| HPC Comparison | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| StormGuard — Status | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| StormGuard — Methodology | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| AlphaDroid — Summary Signals | ✗ | ✓ | ✓ | ✓ | ✓ | ✗ | ✓ |
| AlphaDroid — Raw Signals | ✗ | ✗ | ✓ | ✗ | ✓ | ✗ | ✓ |
| DIMA / News / Sentiment | ✗ | ✗ | ✓ | ✓ | ✓ | ✗ | ✓ |
| External Reports — Generate | ✗ | ✓ | ✓ | ✓ | ✓ | ✗ | ✓ |
| External Reports — Approve | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ |
| Social Media — Flag | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✓ |
| Social Media — Approve | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ |
| Audit Logs — Own Sessions | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Audit Logs — Full Book | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ | ✓ |
| Audit Logs — Platform-Wide | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ |
| Retraining Queue — Submit | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ |
| Compliance Override | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ |
| Intent Map Configuration | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ |
| Disclaimer Library Edit | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ |
| Deep Mode 3 (Institutional) | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ | ✓ |

---

## Important Notes

- The Compliance Guardrail Engine applies to **all tiers including Compliance Admin** for their own interactions — it cannot be disabled per-session
- Compliance Admin override authority applies to system-level guardrail configuration, not to bypassing rules in real-time sessions
- AlphaDroid raw signals access requires FA_PRO or MFO_INSTITUTIONAL; ADMIN does not have access (separation of duties)
- Social media approval authority is exclusively COMPLIANCE_ADMIN — no other tier may approve content for publication

---

*Config: `config/permission_matrix.json` | Full spec: `HARPIAN_JIM_COMPLIANCE_ENGINEERING_SPEC_v1.md` Section 12*
