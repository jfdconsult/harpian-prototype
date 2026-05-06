# JIM Intent Map
## Operational Intent Classification Table

**Version:** 1.0 | **Classification:** Confidential — Internal Use Only  
**Machine-readable format:** `config/intents.json`

---

## Intent Categories

| Category | Intent IDs |
|----------|-----------|
| RISK_NUMBER | INT-001 through INT-003 |
| QUANTITATIVE_METRICS | INT-004 through INT-007 |
| STORMGUARD | INT-008 through INT-010 |
| ALPHADROID | INT-011 through INT-012 |
| PORTFOLIO_ALIGNMENT | INT-013 through INT-014 |
| SIMULATION_ENGINE | INT-015 through INT-016 |
| DAILY_DASHBOARD | INT-017 through INT-018 |
| HIDDEN_RISK | INT-019 |
| STRESS_TESTING | INT-020 |
| COMPLIANCE_SUITABILITY | INT-021 through INT-022 |
| FO_INSTITUTIONAL | INT-023 through INT-024 |
| UX_NAVIGATION | INT-025 through INT-026 |
| ACTION_REQUEST | INT-027 through INT-030 |

---

## Full Intent Map

| INTENT_ID | Category | Example Questions | Required Data | Response Type | Regulatory Risk | Disclaimers | Escalate? |
|-----------|----------|-------------------|---------------|---------------|-----------------|-------------|-----------|
| INT-001 | RISK_NUMBER | "What is my client's Risk Number?" "Why did Risk Number change?" | risk_number, target, mandate | DIAGNOSTIC | Low | DISC-003 | No |
| INT-002 | RISK_NUMBER | "What does a Risk Number of 65 mean?" | — | EDUCATION | Low | — | No |
| INT-003 | RISK_NUMBER | "How is Risk Number calculated?" | — | EDUCATION | Low | — | No |
| INT-004 | QUANT_METRICS | "What is the Sharpe Ratio?" | sharpe, benchmark, period | DIAGNOSTIC | Low | DISC-001 | No |
| INT-005 | QUANT_METRICS | "What is CAGR?" "Show drawdown." | cagr, max_drawdown, period | DIAGNOSTIC | Medium | DISC-001 | No |
| INT-006 | QUANT_METRICS | "What is the Alignment Score?" | alignment_score, target | DIAGNOSTIC | Low | DISC-007 | If score < 50 |
| INT-007 | QUANT_METRICS | "What is Horizon Gap?" "Am I on track?" | horizon_gap, retirement_date | DIAGNOSTIC | Medium | DISC-013 | If negative |
| INT-008 | STORMGUARD | "Is StormGuard active?" "What regime?" | stormguard_status, regime | DIAGNOSTIC | Low | DISC-004 | No |
| INT-009 | STORMGUARD | "How does StormGuard protect?" | — | EDUCATION | Medium | DISC-004 | No |
| INT-010 | STORMGUARD | "When was last StormGuard trigger?" | stormguard_history | DIAGNOSTIC | Low | DISC-004 | No |
| INT-011 | ALPHADROID | "What is AlphaDroid showing?" | alphadroid_signal, date | DIAGNOSTIC | Medium | DISC-005 | No |
| INT-012 | ALPHADROID | "How does AlphaDroid work?" | — | EDUCATION | Low | DISC-005 | No |
| INT-013 | PORTFOLIO_ALIGN | "Is this portfolio aligned?" "What is misaligned?" | risk_number, alignment_score, flags | DIAGNOSTIC | Medium | DISC-007 | If score < 50 |
| INT-014 | PORTFOLIO_ALIGN | "Why is the portfolio misaligned?" | risk_number, factors | CAUSE | Medium | DISC-007 | No |
| INT-015 | SIMULATION | "What if I add 10% to HPC22?" | hrd_simulation_output | SIMULATION | High | DISC-002, DISC-003 | No |
| INT-016 | SIMULATION | "Run a stress test for 2008." | hrd_stress_test_output | SIMULATION | High | DISC-002, DISC-009 | No |
| INT-017 | DAILY_DASHBOARD | "What does the dashboard show today?" | dashboard_data, date | DIAGNOSTIC | Low | — | No |
| INT-018 | DAILY_DASHBOARD | "What are the alerts?" | alerts_list, severity | ALERT | Low | — | If Sev 1 alert |
| INT-019 | HIDDEN_RISK | "Are there hidden risks?" | risk_factors, correlation | DIAGNOSTIC | Medium | DISC-007, DISC-011 | No |
| INT-020 | STRESS_TESTING | "How does portfolio perform in rate shock?" | hrd_stress_output | SIMULATION | High | DISC-002, DISC-009 | No |
| INT-021 | COMPLIANCE | "Is this portfolio suitable?" | mandate, risk_number, client_profile | COMPLIANCE | Critical | DISC-006, DISC-008 | Always |
| INT-022 | COMPLIANCE | "Can I approve this portfolio?" | — | ESCALATION | Critical | DISC-006 | Always |
| INT-023 | FO_INST | "Can I show this to a prospect?" | — | COMPLIANCE | High | DISC-010 | Compliance Admin |
| INT-024 | FO_INST | "Generate a client report." | report_template, client_data | OUTPUT | Medium | DISC-001, DISC-002* | No (internal) |
| INT-025 | UX_NAV | "Where is the stress test module?" | terminal_nav_map | NAVIGATION | Low | — | No |
| INT-026 | UX_NAV | "How do I set a client's risk target?" | terminal_nav_map | NAVIGATION | Low | — | No |
| **INT-027** | **ACTION_REQUEST** | **"What should I do now?" "Should I buy?"** | — | **ACTION_REQUEST** | **Critical** | **DISC-006** | **Always** |
| **INT-028** | **ACTION_REQUEST** | **"Post this to LinkedIn."** | — | **COMPLIANCE** | **High** | **DISC-010** | **Compliance Admin** |
| **INT-029** | **ACTION_REQUEST** | **"Increase risk?" "Move to HPC22?"** | — | **ACTION_REQUEST** | **Critical** | **DISC-006** | **Always** |
| **INT-030** | **ACTION_REQUEST** | **"What's the best product for me?"** | — | **ACTION_REQUEST** | **Critical** | **DISC-006** | **Always** |

*DISC-002 required in INT-024 only if simulation data is included in the report.

---

## Permitted vs. Prohibited Response — Quick Reference

**INT-015 (Simulation):**
- Permitted: "The HRD Engine simulation for a hypothetical 10% allocation to HPC22 shows Risk Number changing from X to Y. [DISC-002]"
- Prohibited: "Adding 10% to HPC22 will improve your returns."

**INT-021 (Suitability):**
- Permitted: "Suitability requires formal best-interest analysis by a licensed advisor. JIM has flagged this session. [DISC-006]"
- Prohibited: "Yes, this portfolio is suitable." OR "No, this portfolio is not suitable."

**INT-027/029/030 (Action Request):**
- Permitted: Mandatory ACTION_REQUEST response text (see JIM_COMPLIANCE_RULES.md)
- Prohibited: Any direct action guidance, implication, or recommendation

---

*Config: `config/intents.json` | Full spec: `HARPIAN_JIM_COMPLIANCE_ENGINEERING_SPEC_v1.md` Section 5*
