# JIM Compliance Rules v2
## Updated CGE Specification for Dual Engine Architecture

**Version:** 2.0 | **Supersedes:** JIM_COMPLIANCE_RULES.md (v1.0) | **Classification:** Confidential — Internal Use Only  
**Regulatory Basis:** SEC Marketing Rule, Reg BI, Form CRS, SEC Fiduciary Interpretation, FINRA Rule 2210, FINRA Books & Records, FINRA Social Media Guidance

---

## What Changed in v2

| Component | v1 | v2 |
|-----------|----|----|
| CGE applies to | Single output | Both Output 1 and Output 2 independently |
| Adversarial content | Not present | ADVERSE_SCENARIO, COUNTER_THESIS require CGE pass |
| ACE output | Not present | Output 2 has dedicated CGE pass |
| Forbidden language | Same list | Extended with simulation-specific terms |
| Disclaimer injection | End of response | Per-block injection at point of use |

---

## Regulatory First Principle (Unchanged)

> **No response from JIM shall be delivered to the user without passing through the Compliance Guardrail Engine (CGE).**

This applies independently to:
- Output 1 (INTERNAL_ANALYSIS)
- Output 2 (CLIENT_READY_MESSAGE)

Both outputs are processed sequentially through CGE before delivery. A Severity 1 violation in either output blocks both.

---

## What JIM Can Do (v2 Extension)

| Function | Regulatory Boundary | v2 Addition |
|----------|---------------------|-------------|
| Explain | Factual, balanced, not promotional | Unchanged |
| Diagnose | May not prescribe action | Unchanged |
| Simulate | Must carry DISC-002; HRD Engine attribution | Attribution in every block, not just footer |
| Compare | Balanced; disclose period | Now requires ADVERSE_SCENARIO at L3+ |
| Contextualize | Must not imply predictive certainty | Now enforced by MODEL_LIMITATION block |
| Educate | Must not be promotional; must be balanced | Unchanged |
| Flag Misalignment | Must not prescribe solution | Unchanged |
| Show Mathematical Impact | Must include simulation disclaimer | DISC-002 before table, not after |
| Present Adverse Scenarios | Must label as adverse/hypothetical | New in v2 — required at L3/L4 |
| Present Counter-Thesis | Must be labeled as alternative view | New in v2 — required at L4 |

---

## What JIM Cannot Do (v2 — Extended List)

| Prohibited Action | Regulatory Basis |
|-------------------|-----------------|
| Recommend buy/sell/hold | Reg BI, Fiduciary Interpretation |
| Say "I recommend" | Marketing Rule, Reg BI |
| Say "you should invest" | Marketing Rule, Fiduciary Interpretation |
| Say "the best product for you" | Reg BI, Marketing Rule |
| Promise a return | Marketing Rule |
| Suggest absolute safety | Marketing Rule, FINRA 2210 |
| Claim guaranteed protection | Marketing Rule, FINRA 2210 |
| Project performance as certainty | Marketing Rule, FINRA 2210 |
| Omit material risks | Marketing Rule, Reg BI |
| Use selective performance without adverse case | Marketing Rule, FINRA 2210 |
| Use promotional language without disclosure | Marketing Rule, FINRA 2210 |
| Convert simulation into personalized recommendation | Reg BI, Fiduciary Interpretation |
| Present adverse scenario as likely/probable | Marketing Rule |
| Present counter-thesis as advocacy | FINRA 2210 |
| Omit MODEL_LIMITATION when citing HRD Engine | Marketing Rule 206(4)-1(a)(1)(vii) |
| Present Output 2 (CLIENT_READY_MESSAGE) without regulatory close | FINRA 2210 |

---

## CGE Processing Steps — v2

### Pass 1 — Output 1 (INTERNAL_ANALYSIS)

1. **Forbidden Language Scan** — check against `config/forbidden_language.json` (Severity 1/2/3)
2. **Recommendation Detection** — pattern-match action directives across all 8 blocks
3. **Promise/Guarantee Detection** — detect forward-looking certainty claims
4. **Adversarial Balance Check** — if [SIMULATION] present at L3+, verify [ADVERSE_SCENARIO] exists; if missing, inject warning and flag
5. **Disclaimer Injection** — per-block injection at point of use (not footer-only)
6. **Block Integrity Check** — verify [NEUTRAL_CONCLUSION] present and compliant

### Pass 2 — Output 2 (CLIENT_READY_MESSAGE)

1. **Jargon Scan** — detect any technical terms that passed through ACE translation
2. **Recommendation Detection** — same pattern-match as Pass 1
3. **5-Line Enforcement** — count lines; if >5, flag for review
4. **Regulatory Close Verification** — confirm Line 5 is from approved template library
5. **Simulation Label Check** — if any simulation numbers present, verify "(hypothetical)" label

---

## Severity Levels (Unchanged from v1)

| Severity | Action | Log Flag |
|----------|--------|----------|
| 1 | Block response → safe fallback | SEVERITY_1_VIOLATION |
| 2 | Rewrite affected phrase → continue | SEVERITY_2_REWRITE |
| 3 | Append disclaimer → continue | SEVERITY_3_DISCLAIMER |

A Severity 1 violation in either output blocks both outputs. The user receives the safe fallback only.

---

## Forbidden Language — v2 Extensions

The base forbidden_language.json list remains. v2 adds the following simulation-specific terms:

### Severity 1 Additions (Block)

| Term | Language | Reason |
|------|----------|--------|
| "this will perform better" | EN | Forward certainty claim |
| "isso vai performar melhor" | PT | Forward certainty claim |
| "proven strategy" | EN | Performance guarantee implication |
| "estratégia comprovada" | PT | Performance guarantee implication |
| "you can't lose" | EN | Absolute safety claim |
| "você não vai perder" | PT | Absolute safety claim |
| "the simulation confirms" | EN | Simulation as certainty |
| "a simulação confirma" | PT | Simulation as certainty |
| "results are guaranteed" | EN | Explicit guarantee |
| "resultados garantidos" | PT | Explicit guarantee |

### Severity 2 Additions (Rewrite)

| Term → Replacement | Language |
|-------------------|----------|
| "the simulation shows improvement" → "the HRD Engine hypothetical output shows a reduction in the measured gap" | EN |
| "better allocation" → "alternative allocation with different measured characteristics" | EN |
| "alocação melhor" → "alocação alternativa com características medidas diferentes" | PT |
| "outperforms" → "shows higher measured return in the tested period" | EN |
| "supera" → "apresenta retorno medido mais alto no período testado" | PT |
| "optimal" → "aligned with the tested parameters" | EN |
| "ótimo" → "alinhado com os parâmetros testados" | PT |

### Severity 3 Additions (Disclaimer Append)

| Term | Disclaimer Required |
|------|-------------------|
| Any reference to adverse scenario results | DISC-009 |
| Any reference to counter-thesis as "likely" | DISC-013 |
| Model accuracy claims | DISC-001 + DISC-002 |
| Historical pattern extrapolation | DISC-001 |

---

## Per-Block Disclaimer Injection Rules (v2)

In v2, disclaimers are injected at the block level, not only at the end of the response:

| Block | Required Disclaimers |
|-------|---------------------|
| [DIAGNOSTIC] with historical data | DISC-001 |
| [SIMULATION] | DISC-002 (BEFORE the table) |
| [RISK] with historical metrics | DISC-001 |
| [ADVERSE_SCENARIO] | DISC-002, DISC-009 |
| [COUNTER_THESIS] | None at block level — handled by closing statement |
| [MODEL_LIMITATION] | DISC-001, DISC-002 (reinforce) |
| [NEUTRAL_CONCLUSION] | DISC-006 if suitability reference made |
| Output 2 [CLIENT_READY_MESSAGE] | Template-embedded regulatory close (Line 5) |

---

## ACTION_REQUEST — Mandatory Response (Unchanged)

When an ACTION_REQUEST is detected, the Response Orchestrator stops all engine processing before any content is generated. CGE delivers the mandatory response directly:

> *"JIM does not provide individualized investment recommendations. JIM can present the mathematical simulation, the portfolio diagnostic, and the risk/return impact based on data loaded in the terminal. The investment decision must be made by a licensed advisor, within the formal suitability process, in accordance with the client's best interest."*

**v2 addition:** The mandatory response is delivered in the detected language (EN or PT-BR). A Portuguese version is maintained in `config/response_templates.json`:

> *"JIM não fornece recomendações de investimento individualizadas. JIM pode apresentar a simulação matemática, o diagnóstico de portfólio e o impacto de risco/retorno com base nos dados carregados no terminal. A decisão de investimento deve ser tomada por um assessor licenciado, dentro do processo formal de adequação, de acordo com o melhor interesse do cliente."*

---

## Audit Logging — v2

Both outputs are logged independently:

```json
{
  "session_id": "uuid",
  "timestamp": "ISO-8601",
  "user_tier": "FA_PRO",
  "intent_id": "INT-015",
  "response_level": "L3",
  "output_1": {
    "sha256": "hash",
    "blocks_present": ["DIAGNOSTIC", "SIMULATION", "RISK", "ADVERSE_SCENARIO", "MODEL_LIMITATION", "NEUTRAL_CONCLUSION"],
    "disclaimers_injected": ["DISC-001", "DISC-002", "DISC-009"],
    "cge_pass_1_result": "SEVERITY_3_DISCLAIMER",
    "cge_flags": []
  },
  "output_2": {
    "sha256": "hash",
    "template_id": "CAT-2-EN",
    "modified_by_advisor": false,
    "cge_pass_2_result": "PASS",
    "cge_flags": []
  },
  "escalation": null
}
```

Retention: 7 years (FINRA Books & Records Rule 4511)  
Immutability: write-once; SHA-256 hash on both outputs at time of generation

---

## Compliance Admin — Override Scope (Unchanged)

Compliance Admin tier does NOT bypass CGE. The only difference for Compliance Admin is:
- Access to L4 response level
- Access to COUNTER_THESIS blocks
- Access to full audit log
- Access to session escalation queue
- Ability to approve or reject `MODIFIED_BY_ADVISOR` messages

Compliance Admin cannot disable, pause, or reconfigure CGE.

---

*Supersedes: JIM_COMPLIANCE_RULES.md (v1.0)*  
*Config: config/forbidden_language.json | config/escalation_rules.json | config/response_templates.json*  
*See also: JIM_DISCLAIMER_LIBRARY.md | JIM_DUAL_ENGINE.md | JIM_ADVERSARIAL_ENGINE.md*
