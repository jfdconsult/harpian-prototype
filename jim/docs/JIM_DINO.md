# JIM DINO — Data Ingestion & Knowledge Operations
## Knowledge Base Ingestion System Specification

**Version:** 2.0 | **Classification:** Confidential — Internal Use Only  
**New in:** JIM Architecture v2

---

## Overview

DINO (Data Ingestion & Knowledge Operations) is the subsystem responsible for converting source documents from the `Q&A/` directory into structured, retrieval-ready knowledge blocks that the JIM Response Engine can access.

DINO does not operate in real-time. It is a batch ingestion process that runs when new documents are added to the knowledge base. Its output is a static indexed knowledge store that JIM queries during response generation.

---

## Source Directory

```
C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\JIM Biblioteca Estrutura all docs\Q&A\
```

### Current Source Documents

| File | Type | Content Domain |
|------|------|---------------|
| Harpian_150_Questionnaire.docx | DOCX | 150 Q&A pairs — client/advisor scenarios |
| Harpian_JIM_GM.docx | DOCX | JIM methodology — general market |
| Harpian_JIM_N.docx | DOCX | JIM methodology — narrative |
| Harpian_JIM_v2.docx | DOCX | JIM v2 Q&A pairs and responses |
| Jim_AI_Architecture_v1.docx | DOCX | JIM architecture — v1 specification |
| JIM_Architecture_v2.docx | DOCX | JIM architecture — v2 specification |
| Documentação de produção e base de conhecimento do DMA.pdf | PDF | DMA production documentation |

### Adding New Documents

New Q&A files should be placed in the `Q&A/` directory. DINO ingestion should be re-run after any new document is added. Supported formats:
- `.docx` — Microsoft Word documents
- `.pdf` — PDF documents
- `.md` — Markdown files

---

## Ingestion Pipeline

```
SOURCE DOCUMENT (Q&A/)
        │
        ▼
┌─────────────────────────┐
│  DOCUMENT PARSER        │
│  - Extract raw text     │
│  - Preserve structure   │
│  - Identify Q&A pairs   │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  CHUNK EXTRACTOR        │
│  - Split into chunks    │
│  - Minimum 50 tokens    │
│  - Maximum 500 tokens   │
│  - Overlap: 50 tokens   │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  INTENT TAGGER          │
│  - Tag each chunk with  │
│    matching intent_id   │
│  - Confidence score     │
│  - Bilingual detection  │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  KNOWLEDGE INDEX        │
│  - Indexed by intent_id │
│  - Ranked by confidence │
│  - Version stamped      │
│  - SHA-256 hashed       │
└───────────┬─────────────┘
            │
            ▼
    KNOWLEDGE STORE
    (available to JIM
     Response Engine)
```

---

## Knowledge Block Structure

Each ingested chunk becomes a knowledge block in the index:

```json
{
  "block_id": "KB-001-0042",
  "source_file": "Harpian_150_Questionnaire.docx",
  "source_page": 12,
  "ingested_at": "2026-04-28T00:00:00Z",
  "sha256": "abc123...",
  "intent_tags": ["INT-001", "INT-003"],
  "primary_intent": "INT-001",
  "confidence": 0.91,
  "language": "PT",
  "content": "O Risk Number é um indicador que mede o risco do portfólio em uma escala de 0 a 99...",
  "content_en": "The Risk Number is an indicator that measures portfolio risk on a scale of 0 to 99...",
  "response_level_target": "L2",
  "regulatory_flags": ["DISC-003"]
}
```

---

## Intent Tagging Rules

The Intent Tagger assigns `intent_id` tags to each chunk based on keyword and semantic matching:

| Pattern | Intent Tags |
|---------|------------|
| "Risk Number", "Número de Risco", "RN" | INT-001, INT-002, INT-003 |
| "Sharpe", "Sortino", "drawdown" | INT-004, INT-005 |
| "Alignment Score", "alinhamento" | INT-006, INT-013 |
| "Horizon Gap", "horizonte", "aposentadoria" | INT-007 |
| "StormGuard", "regime", "proteção" | INT-008, INT-009, INT-010 |
| "AlphaDroid", "sinal", "momentum" | INT-011, INT-012 |
| "simulação", "simulation", "hipotético" | INT-015, INT-016 |
| "stress test", "cenário adverso" | INT-016, INT-020 |
| "suitability", "adequação", "melhor interesse" | INT-021, INT-022 |

---

## Re-Ingestion Protocol

When new Q&A documents are added:

1. Place new file in `Q&A/` directory
2. Run DINO ingestion batch
3. New blocks are added to Knowledge Index — existing blocks are NOT overwritten
4. Version stamp is updated in knowledge store metadata
5. SHA-256 hashes are recorded for audit trail

**Rule:** DINO never deletes or overwrites existing knowledge blocks. New versions of the same content are added as new blocks with higher version numbers. The Response Engine selects the highest-confidence, most recent block for each intent.

---

## Knowledge Store Metadata

```json
{
  "knowledge_store_version": "2.1.0",
  "last_updated": "2026-04-28",
  "total_blocks": 847,
  "source_documents": 7,
  "intent_coverage": {
    "INT-001": 34,
    "INT-002": 18,
    "INT-003": 12,
    "INT-004": 29,
    "INT-005": 41
  },
  "language_coverage": {
    "EN": 312,
    "PT": 398,
    "bilingual": 137
  }
}
```

---

## Integration with Response Engine

When the Response Orchestrator assembles Output 1, it queries the Knowledge Store:

1. **Query:** `intent_id` + `response_level` + `language`
2. **Result:** Top 3 knowledge blocks by confidence score
3. **Selection:** Response Engine merges knowledge blocks with `context_payload` data
4. **Attribution:** Knowledge content used verbatim from approved blocks (no LLM rewriting of regulatory methodology content)

The LLM layer synthesizes the response structure and language — but regulatory methodology definitions, indicator explanations, and compliance language come directly from approved DINO knowledge blocks.

---

*New in JIM Architecture v2 | See also: JIM_ARCHITECTURE_v2.md | JIM_RESPONSE_ENGINE.md*
