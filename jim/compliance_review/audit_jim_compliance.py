import csv
import json
import re
import zipfile
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(r"C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN")
BASE = ROOT / "04_JIM_COMPLIANCE_QA"
LIB = BASE / "JIM Biblioteca Estrutura all docs"
CONFIG = LIB / "config"
DOCS = LIB / "docs" / "jim"
EXTRACTED = BASE / "compliance_audit_extracted"
FRONT = ROOT / "harpian-front"
OUT = BASE / "REVISAO_CODEX_COMPLIANCE_JIM_2026-05-02"


PRIORITY_FILES = [
    CONFIG / "response_templates.json",
    CONFIG / "intents_v2.json",
    CONFIG / "dual_engine_rules.json",
    DOCS / "JIM_COMPLIANCE_RULES_v2.md",
    DOCS / "JIM_RESPONSE_ENGINE.md",
    DOCS / "JIM_ADVISOR_COMMUNICATION.md",
    DOCS / "JIM_ADVERSARIAL_ENGINE.md",
    BASE / "COMPLIANCE_AUDIT_QA_HARPIAN.md",
    EXTRACTED / "qa_validation_matrix.csv",
    EXTRACTED / "HARPIAN_QA_CONSOLIDADO_COM_DISCLAIMERS.docx",
    LIB / "Harpian_JIM_QuantDD.docx",
    LIB / "Harpian_JIM_Objections.docx",
    LIB / "Harpian_JIM_4Layers.docx",
    FRONT / "docs" / "JIM_TECHNICAL_ARCHITECTURE_SOTA.md",
    FRONT / "docs" / "jim" / "COMPLIANCE_AUDIT_QA_HARPIAN.md",
    FRONT / "docs" / "jim" / "qa_validation_matrix.csv",
]


SRC_DIRS = [
    FRONT / "src" / "app" / "intelligence",
    FRONT / "src" / "components" / "intelligence",
    FRONT / "src" / "lib",
    FRONT / "src" / "services",
    FRONT / "src" / "data",
]


SEVERITY_RANK = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1", errors="replace")


def docx_text(path: Path) -> str:
    try:
        with zipfile.ZipFile(path) as zf:
            xml = zf.read("word/document.xml")
        ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
        root = ET.fromstring(xml)
        paragraphs = []
        for para in root.findall(".//w:p", ns):
            texts = [node.text or "" for node in para.findall(".//w:t", ns)]
            if texts:
                paragraphs.append("".join(texts))
        return "\n".join(paragraphs)
    except Exception as exc:
        return f"[DOCX_EXTRACTION_ERROR] {exc}"


def iter_json_strings(obj, prefix=""):
    if isinstance(obj, dict):
        for key, value in obj.items():
            new_prefix = f"{prefix}.{key}" if prefix else str(key)
            yield from iter_json_strings(value, new_prefix)
    elif isinstance(obj, list):
        for idx, value in enumerate(obj):
            yield from iter_json_strings(value, f"{prefix}[{idx}]")
    elif isinstance(obj, str):
        yield prefix, obj


def file_items(path: Path):
    if not path.exists():
        return []
    suffix = path.suffix.lower()
    rel = str(path)
    if suffix == ".json":
        text = read_text(path)
        items = []
        try:
            data = json.loads(text)
            items.extend(iter_json_strings(data))
        except Exception as exc:
            items.append(("json_parse_error", f"JSON parse error: {exc}"))
        return [(rel, loc, value) for loc, value in items if value and value.strip()]
    if suffix == ".docx":
        text = docx_text(path)
        return [(rel, f"paragraph_block_{i+1}", chunk) for i, chunk in enumerate(chunk_text(text, 900))]
    if suffix in {".md", ".txt", ".csv", ".ts", ".tsx", ".js", ".jsx"}:
        text = read_text(path)
        return [(rel, f"line_block_{i+1}", chunk) for i, chunk in enumerate(chunk_text(text, 900))]
    return []


def chunk_text(text, size=900):
    clean = re.sub(r"\s+", " ", text).strip()
    if not clean:
        return []
    chunks = []
    start = 0
    while start < len(clean):
        end = min(start + size, len(clean))
        if end < len(clean):
            split = clean.rfind(". ", start, end)
            if split > start + 250:
                end = split + 1
        chunks.append(clean[start:end].strip())
        start = end
    return chunks


def has_any(text, patterns):
    return any(re.search(pattern, text, re.I) for pattern in patterns)


DISCLAIMER_PATTERNS = [
    r"past performance|performance passada|resultado futuro|future results",
    r"n[ãa]o (garante|constitui garantia|representa garantia)",
    r"hypothetical|hipot[eé]tic|simula",
    r"backtest|walk-forward|fora da amostra",
    r"taxas|fees|custos|costs|impostos|slippage|liquidez|execution|execu[cç][aã]o",
    r"suitability|perfil do investidor|objetivos|horizonte|restri[cç][oõ]es",
]


RISK_RULES = [
    {
        "type": "Promessa proibida / garantia",
        "severity": "CRITICAL",
        "patterns": [
            r"\bgarantid[oa]s?\b|\bgarantia\b|\bguarantee[ds]?\b",
            r"sem risco|no risk|risk[- ]free",
            r"prote[cç][aã]o total|total protection",
            r"retorno garantido|guaranteed return",
            r"alpha garantido|guaranteed alpha",
            r"will outperform|vai superar|superar[aá] o benchmark",
        ],
        "problem": "A linguagem pode ser lida como promessa, garantia ou projeção de resultado.",
    },
    {
        "type": "Recomendação direta / suitability",
        "severity": "HIGH",
        "patterns": [
            r"\beu recomendo\b|\brecomendo\b|\bwe recommend\b|\bi recommend\b",
            r"voc[eê] deve investir|you should invest|deve alocar|should allocate",
            r"compre\b|comprar agora|buy now|\bvenda\b|sell now",
            r"melhor op[cç][aã]o para voc[eê]|best option for you",
            r"carteira adequada\b|is suitable for you|adequate for you",
        ],
        "problem": "O trecho pode transformar JIM em recomendador/autoadvisor sem processo formal de suitability.",
    },
    {
        "type": "Performance sem disclosure suficiente",
        "severity": "HIGH",
        "patterns": [
            r"performance|retorno|return|drawdown|sharpe|sortino|alpha\b|benchmark|hedge fund",
            r"backtest|walk[- ]forward|simula[cç][aã]o|projection|proje[cç][aã]o",
        ],
        "problem": "O trecho discute performance, simulação ou métrica de risco/retorno e deve carregar disclaimer completo.",
        "requires_missing_disclaimer_check": True,
    },
    {
        "type": "Risk Number misturado com performance",
        "severity": "HIGH",
        "patterns": [
            r"risk number|n[uú]mero de risco",
        ],
        "problem": "Risk Number deve ficar separado de retorno, Sharpe, drawdown e performance de estratégia.",
        "requires_rn_perf_check": True,
    },
    {
        "type": "JIM como advisor autônomo",
        "severity": "HIGH",
        "patterns": [
            r"JIM recomenda|JIM recommends|JIM vai recomendar",
            r"JIM decide|JIM determines the allocation|JIM monta a carteira",
            r"advisor aut[oô]nomo|autonomous advisor",
        ],
        "problem": "JIM deve ser assistente analítico/de suporte, não consultor financeiro autônomo.",
    },
    {
        "type": "Comparação potencialmente enganosa",
        "severity": "MEDIUM",
        "patterns": [
            r"melhor que hedge funds|better than hedge funds|beats hedge funds",
            r"melhor que ETF|better than ETF|superior ao S&P|superior to S&P",
            r"top quartile|best[- ]in[- ]class|institutional grade",
        ],
        "problem": "Comparações exigem período, universo comparável, metodologia, custos, limitações e riscos.",
    },
    {
        "type": "Linguagem promocional excessiva",
        "severity": "MEDIUM",
        "patterns": [
            r"revolucion[aá]rio|revolutionary|extraordin[aá]rio|extraordinary",
            r"diferenciado|unmatched|unparalleled|superior\b|best\b",
            r"protege\b|protects\b|seguro\b|safe\b",
        ],
        "problem": "Comunicação regulada deve ser factual, balanceada e não promocional.",
    },
]


def suggested_fix(risk_type, text):
    if risk_type == "Promessa proibida / garantia":
        return (
            "Substituir por linguagem condicional e factual: 'A estratégia pode ser analisada como parte de um processo de suitability; "
            "resultados variam e não há garantia de retorno, proteção ou superação de benchmark.'"
        )
    if risk_type == "Recomendação direta / suitability":
        return (
            "Trocar por: 'Essa alternativa pode ser avaliada pelo advisor dentro do processo formal de suitability, considerando objetivos, "
            "horizonte, liquidez, restrições, custos e tolerância a risco do investidor.'"
        )
    if risk_type == "Performance sem disclosure suficiente":
        return (
            "Rotular a métrica como backtest, walk-forward, live track record, model index ou client actual; informar data-base, metodologia, "
            "bruto/líquido e limitações; incluir disclaimer completo antes ou junto ao número."
        )
    if risk_type == "Risk Number misturado com performance":
        return (
            "Separar a resposta: Risk Number mede perfil/tolerância/alinhamento de risco do cliente; performance de estratégias trata de retornos, "
            "drawdowns e métricas históricas. Não inferir retorno esperado a partir do Risk Number."
        )
    if risk_type == "JIM como advisor autônomo":
        return (
            "Descrever JIM como ferramenta de suporte analítico para advisor/family office, sem decisão autônoma ou recomendação personalizada."
        )
    if risk_type == "Comparação potencialmente enganosa":
        return (
            "Adicionar critérios de comparação: período, benchmark/universo, moeda, dados, bruto/líquido, volatilidade, drawdown, custos e limitações."
        )
    if risk_type == "Linguagem promocional excessiva":
        return "Reescrever em tom institucional, factual e balanceado, com riscos e limitações próximos aos benefícios."
    return "Corrigir codificação para UTF-8 e revisar acentuação antes de aprovação compliance."


def disclaimer_for(risk_type):
    if risk_type == "Performance sem disclosure suficiente":
        return (
            "Performance passada, simulada, hipotética, walk-forward, de índice/modelo ou backtest não garante nem projeta resultados futuros. "
            "Resultados podem variar por custos, taxas, impostos, liquidez, slippage, execução, data de entrada, restrições e perfil do investidor. "
            "Quando indicado como bruto, o resultado não reflete taxas de administração, performance, corretagem, spreads, impostos e demais despesas."
        )
    if risk_type == "Recomendação direta / suitability":
        return (
            "Este material é informativo e analítico. Não constitui recomendação individual de investimento. Qualquer decisão deve passar por suitability, "
            "avaliação do advisor responsável e documentação do perfil, objetivos, horizonte, restrições e riscos."
        )
    if risk_type == "Risk Number misturado com performance":
        return (
            "Risk Number é uma ferramenta de avaliação de perfil e alinhamento de risco; não é previsão de retorno, garantia de performance ou recomendação de alocação."
        )
    if risk_type in {"Promessa proibida / garantia", "Comparação potencialmente enganosa", "Linguagem promocional excessiva"}:
        return (
            "As informações são educacionais e devem ser avaliadas com riscos, limitações, custos e suitability. Não há promessa, garantia ou projeção de retorno."
        )
    return ""


def analyze_item(file_path, loc, text):
    findings = []
    normalized = re.sub(r"\s+", " ", text).strip()
    if not normalized:
        return findings
    for rule in RISK_RULES:
        if not has_any(normalized, rule["patterns"]):
            continue
        if rule["type"] == "Promessa proibida / garantia":
            has_negative_disclaimer = has_any(normalized, [
                r"does not guarantee|do not guarantee|not guarantee|not a guarantee",
                r"n[ãa]o garante|n[ãa]o representam resultados garantidos|n[ãa]o [eé] garantia",
                r"n[ãa]o h[aá] garantia",
            ])
            has_standalone_promise = has_any(normalized, [
                r"sem risco|no risk|risk[- ]free",
                r"retorno garantido|guaranteed return",
                r"alpha garantido|guaranteed alpha",
                r"garante que|guarantees? that",
                r"will outperform|vai superar|superar[aá] o benchmark",
                r"prote[cç][aã]o total|total protection",
                r"garantidas por|guaranteed by",
            ])
            if has_negative_disclaimer and not has_standalone_promise:
                continue
        if rule.get("requires_missing_disclaimer_check") and has_any(normalized, DISCLAIMER_PATTERNS):
            continue
        if rule.get("requires_rn_perf_check"):
            if not has_any(normalized, [r"performance|retorno|return|drawdown|sharpe|alpha|benchmark|backtest"]):
                continue
        excerpt = normalized[:650]
        findings.append({
            "arquivo_origem": file_path,
            "trecho_ou_template": f"{loc}: {excerpt}",
            "tipo_risco": rule["type"],
            "severidade": rule["severity"],
            "problema": rule["problem"],
            "resposta_corrigida_sugerida": suggested_fix(rule["type"], normalized),
            "disclaimer_recomendado": disclaimer_for(rule["type"]),
            "status": "SUGERIR_CORRECAO" if rule["severity"] in {"LOW", "MEDIUM"} else "REVISAO_OBRIGATORIA",
        })
    return findings


def collect_files():
    files = []
    for path in PRIORITY_FILES:
        if path.exists():
            files.append(path)
    for src_dir in SRC_DIRS:
        if src_dir.exists():
            for ext in ("*.ts", "*.tsx", "*.js", "*.jsx", "*.json", "*.md"):
                files.extend(src_dir.rglob(ext))
    # Keep scope useful; exclude build caches and node_modules.
    return sorted(set(files), key=lambda p: str(p).lower())


def file_level_findings(files):
    findings = []
    for path in files:
        if path.suffix.lower() not in {".json", ".md", ".txt", ".csv", ".ts", ".tsx", ".js", ".jsx"}:
            continue
        text = read_text(path)
        if re.search(r"Ã.|â€|�", text):
            findings.append({
                "arquivo_origem": str(path),
                "trecho_ou_template": "arquivo: sinais de mojibake/encoding corrompido detectados",
                "tipo_risco": "Qualidade textual / encoding",
                "severidade": "LOW",
                "problema": "Há provável problema de codificação de caracteres, podendo prejudicar clareza e revisão formal.",
                "resposta_corrigida_sugerida": suggested_fix("Qualidade textual / encoding", text),
                "disclaimer_recomendado": "",
                "status": "SUGERIR_CORRECAO",
            })
    return findings


def write_csv(findings):
    out_path = OUT / "MATRIZ_REVISAO_RESPOSTAS_JIM.csv"
    with out_path.open("w", encoding="utf-8-sig", newline="") as fh:
        fieldnames = [
            "id",
            "arquivo_origem",
            "trecho_ou_template",
            "tipo_risco",
            "severidade",
            "problema",
            "resposta_corrigida_sugerida",
            "disclaimer_recomendado",
            "status",
        ]
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for idx, row in enumerate(findings, 1):
            row = dict(row)
            row["id"] = f"JIM-COMP-{idx:04d}"
            writer.writerow(row)


def md_table(rows, headers):
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        vals = []
        for header in headers:
            val = str(row.get(header, "")).replace("\n", " ").replace("|", "\\|")
            vals.append(val)
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def write_report(findings, files):
    by_sev = Counter(f["severidade"] for f in findings)
    by_type = Counter(f["tipo_risco"] for f in findings)
    by_file = Counter(f["arquivo_origem"] for f in findings)
    critical_files = [
        {"arquivo": file, "achados": count}
        for file, count in by_file.most_common(20)
    ]
    top_findings = sorted(findings, key=lambda f: -SEVERITY_RANK[f["severidade"]])[:25]
    content = []
    content.append("# Relatorio Executivo Compliance JIM\n")
    content.append(f"Data da revisao: {date.today().isoformat()}\n")
    content.append("Escopo: respostas, templates, regras, Q&A, documentos e codigo relacionado ao JIM/Intelligence, com foco em compliance, suitability e comunicacao segura para advisor/family office.\n")
    content.append("Nenhum arquivo fonte foi alterado. Esta revisao gerou apenas artefatos na pasta de saida datada.\n")
    content.append("Nota: este material e um diagnostico tecnico de compliance por heuristicas, leitura amostral e referencias reguladoras publicas. Nao substitui revisao juridica formal nem aprovacao do CCO/compliance officer.\n")
    content.append("## Principais riscos encontrados\n")
    content.append("- Linguagem de performance ainda exige classificacao operacional obrigatoria: backtest, walk-forward, live track record, model index, client actual ou unknown/bloqueado.")
    content.append("- Templates e regras ja possuem boa base de guardrails, mas precisam de reforco mecanico para impedir recomendacao direta e separar Risk Number de performance.")
    content.append("- Respostas com retorno, Sharpe, drawdown, AlphaDroid, benchmark, hedge funds, simulacao ou carteira precisam de disclaimer proximo ao numero, nao apenas em rodape generico.")
    content.append("- Arquivos com sinais de encoding incorreto devem ser normalizados para UTF-8 antes de aprovacao formal, pois acentuacao corrompida prejudica comunicacao client-facing.")
    content.append("- Front-end e documentacao tecnica devem tratar JIM como assistente analitico, nao como consultor autonomo.\n")
    content.append("## Severidade\n")
    content.append(md_table([
        {"severidade": sev, "quantidade": by_sev.get(sev, 0)}
        for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
    ], ["severidade", "quantidade"]))
    content.append("\n## Tipos de risco\n")
    content.append(md_table([
        {"tipo_risco": key, "quantidade": val}
        for key, val in by_type.most_common()
    ], ["tipo_risco", "quantidade"]))
    content.append("\n## Arquivos revisados\n")
    content.append(f"Total de arquivos revisados: {len(files)}\n")
    content.extend([f"- `{path}`" for path in files[:120]])
    if len(files) > 120:
        content.append(f"- ... mais {len(files) - 120} arquivos de codigo/documentacao.")
    content.append("\n## Arquivos com mais achados\n")
    content.append(md_table(critical_files, ["arquivo", "achados"]))
    content.append("\n## Achados prioritarios\n")
    rows = []
    for f in top_findings:
        rows.append({
            "severidade": f["severidade"],
            "tipo_risco": f["tipo_risco"],
            "arquivo": f["arquivo_origem"],
            "problema": f["problema"],
        })
    content.append(md_table(rows, ["severidade", "tipo_risco", "arquivo", "problema"]))
    content.append("\n## Recomendacoes executivas\n")
    content.append("1. Transformar os disclaimers em regras executaveis no CGE, nao apenas texto documental.")
    content.append("2. Adicionar campo obrigatorio `performance_label` para qualquer numero de performance.")
    content.append("3. Bloquear respostas client-facing quando performance estiver `unknown`, sem data-base, sem metodologia ou apenas bruta sem aviso.")
    content.append("4. Inserir teste adversarial para perguntas recorrentes: 'isso e retorno real ou backtest?', 'qual vai render mais?', 'garante que nao vou perder?', 'devo investir tudo?'.")
    content.append("5. Criar fluxo de aprovacao humana para alteracoes em templates client-facing.")
    content.append("\n## Bases reguladoras usadas como referencia\n")
    content.append("- FINRA Rule 2210: comunicacoes devem ser justas, balanceadas, sem declaracoes falsas, exageradas, promissorias ou enganosas; projecoes de performance sao limitadas. Fonte: https://www.finra.org/rules-guidance/rulebooks/finra-rules/2210")
    content.append("- FINRA Advertising Regulation FAQ: reforca que Rule 2210 proibe predicoes/projecoes de performance e implicacao de que performance passada vai se repetir. Fonte: https://www.finra.org/rules-guidance/guidance/faqs/advertising-regulation")
    content.append("- SEC Investment Adviser Marketing Rule: performance bruta, liquida, hipotetica/modelo/extracted performance exigem condicoes, politicas, informacoes de metodologia e tratamento justo de riscos/limitacoes. Fonte: https://www.sec.gov/investment/investment-adviser-marketing")
    content.append("- SEC Marketing Compliance FAQ atualizada em 2026: reforca cuidado com metricas brutas, net performance e caracteristicas extraidas quando usadas em comunicacao de marketing. Fonte: https://www.sec.gov/rules-regulations/staff-guidance/division-investment-management-frequently-asked-questions/marketing-compliance-frequently-asked-questions")
    (OUT / "RELATORIO_EXECUTIVO_COMPLIANCE_JIM.md").write_text("\n".join(content), encoding="utf-8")


def write_rules():
    content = """# Regras Compliance JIM Atualizadas

Data: 2026-05-02

## Principio central

JIM e uma ferramenta de suporte analitico, educacional e operacional para advisor/family office. JIM nao e consultor financeiro autonomo, nao recomenda compra/venda/alocacao personalizada e nao promete retorno, protecao, alpha ou superacao de benchmark.

## Regras obrigatorias

1. Toda resposta passa por Compliance Guardrail Engine antes de ser exibida.
2. Linguagem proibida bloqueia a resposta: garantia, sem risco, retorno garantido, alpha garantido, melhor opcao para voce, voce deve investir, compre/venda agora.
3. Recomendacoes diretas devem virar linguagem analitica: pode ser avaliado pelo advisor dentro de suitability.
4. Risk Number deve ser tratado como perfil/tolerancia/alinhamento de risco, nao como previsao de retorno.
5. Performance de estrategia deve ficar separada de Risk Number.
6. Todo numero de performance precisa de fonte, data-base, metodologia e rotulo.
7. Rotulos aceitos: backtest, walk_forward, live_track_record, model_index, client_actual, unknown.
8. `unknown` bloqueia exibicao client-facing.
9. Backtest/walk-forward/model index exigem disclaimer de hipotetico/modelo e nao podem ser tratados como retorno de cliente.
10. Performance bruta deve dizer claramente que e antes de taxas, impostos, custos, slippage, spreads, custodia e execucao.
11. Para publico dos EUA, materiais de marketing devem ser encaminhados para revisao quando exibirem gross performance sem net performance comparavel.
12. Comparacoes com hedge funds, ETFs ou benchmarks exigem universo comparavel, periodo, moeda, custos, riscos, drawdown e limitacoes.
13. Perguntas perigosas devem ser respondidas com recusa segura ou escalacao: garantia, retorno futuro, melhor fundo, investir tudo, recomendacao personalizada.
14. Toda resposta client-facing deve fechar com status: informativo, nao recomendacao, sujeito a suitability e revisao do advisor.

## Resposta padrao: retorno real ou backtest?

Essa e uma otima pergunta. Nos separamos performance em tres camadas: backtest, teste walk-forward e historico acompanhado ao vivo.

O backtest e a etapa inicial de pesquisa, em que uma estrategia e calibrada usando dados historicos. Ele ajuda a entender o comportamento do modelo, mas nao deve ser tratado como promessa, porque qualquer backtest pode sofrer influencia de ajuste ao passado.

Depois disso vem o walk-forward, ou teste fora da amostra. Nessa etapa, aplicamos regras ja definidas da estrategia em dados reais de mercado que aconteceram depois da janela usada na calibracao inicial. O mercado foi real, mas o acompanhamento ainda nao era uma carteira ao vivo naquele periodo.

A partir da data operacional indicada, quando aplicavel e documentado, passa a existir acompanhamento em tempo real da estrategia/modelo. Esse periodo e diferente do backtest e do walk-forward.

Mesmo assim, performance passada, simulada, hipotetica, walk-forward, de indice/modelo ou acompanhada ao vivo nao garante nem projeta resultados futuros.
"""
    (OUT / "REGRAS_COMPLIANCE_JIM_ATUALIZADAS.md").write_text(content, encoding="utf-8")


def write_prompts():
    content = """# Prompts Seguros JIM

Data: 2026-05-02

## System prompt recomendado

Voce e JIM, assistente analitico da Harpian para advisors e family offices. Sua funcao e organizar informacoes, explicar dados, apontar riscos, sugerir perguntas de diligence e apoiar o processo de suitability. Voce nao e consultor financeiro autonomo e nao deve recomendar compra, venda, manutencao ou alocacao personalizada.

Regras:
- Nao prometa retorno, protecao, alpha, reducao garantida de risco ou superacao de benchmark.
- Nao diga "voce deve investir", "eu recomendo", "melhor opcao para voce", "garantido", "sem risco" ou equivalentes.
- Quando falar de performance, informe se e backtest, walk-forward, live track record, model index, client actual ou unknown.
- Se a classificacao da performance for unknown, recuse apresentar o numero e peca fonte/metodologia.
- Quando falar de Risk Number, limite-se a perfil, tolerancia, suitability e alinhamento de risco; nao inferir retorno esperado.
- Decisoes de investimento dependem de advisor licenciado, suitability, objetivos, horizonte, liquidez, restricoes, custos e documentacao.

## Template seguro: recomendacao direta

Nao posso indicar uma decisao de investimento personalizada ou dizer que voce deve comprar, vender ou alocar em uma estrategia especifica. Posso ajudar a organizar a analise: objetivos, horizonte, liquidez, restricoes, tolerancia a risco, Risk Number, custos, cenarios adversos e aderencia ao mandato. A decisao deve ser feita pelo advisor responsavel dentro do processo formal de suitability.

## Template seguro: garantia de retorno

Nao ha garantia de retorno, protecao ou preservacao de capital. Posso explicar o historico, a metodologia, os riscos e os cenarios de perda, desde que os dados tenham fonte, data-base e classificacao adequada. Performance passada, simulada, hipotetica, walk-forward ou de modelo nao garante resultados futuros.

## Template seguro: qual estrategia vai render mais?

Nao e apropriado afirmar qual estrategia vai render mais no futuro. Podemos comparar historico, risco, drawdown, volatilidade, exposicoes, custos e comportamento em cenarios adversos. Essa comparacao deve ser usada como insumo analitico, nao como promessa ou recomendacao.

## Template seguro: Risk Number

O Risk Number e uma ferramenta para avaliar perfil de risco, tolerancia, alinhamento da carteira e suitability. Ele nao e previsao de retorno nem ranking de estrategias. Performance de estrategia deve ser analisada separadamente, com fonte, periodo, metodologia, custos e limitacoes.

## Template seguro: backtest vs walk-forward vs live

Parte do historico pode ser backtest ou walk-forward, e parte pode ser acompanhamento ao vivo a partir da data operacional indicada. Backtest e pesquisa calibrada com dados historicos; walk-forward aplica regras ja definidas em dados posteriores que nao fizeram parte da calibracao; performance ao vivo e o periodo acompanhado em tempo real. Nenhum desses numeros deve ser lido como promessa ou garantia de resultado futuro.
"""
    (OUT / "PROMPTS_SEGUROS_JIM.md").write_text(content, encoding="utf-8")


def write_files_to_change(findings):
    by_file = defaultdict(list)
    for f in findings:
        if f["severidade"] in {"CRITICAL", "HIGH", "MEDIUM"}:
            by_file[f["arquivo_origem"]].append(f)
    rows = []
    for file, items in sorted(by_file.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        types = ", ".join(sorted(set(i["tipo_risco"] for i in items)))
        max_sev = max((i["severidade"] for i in items), key=lambda s: SEVERITY_RANK[s])
        rows.append({
            "arquivo": file,
            "severidade_maxima": max_sev,
            "quantidade": len(items),
            "motivo": types,
        })
    content = ["# Lista de Arquivos que Devem ser Alterados\n", "Nenhum arquivo fonte foi alterado nesta revisao. Antes de qualquer alteracao futura, criar backup datado do arquivo original.\n"]
    content.append(md_table(rows[:80], ["arquivo", "severidade_maxima", "quantidade", "motivo"]))
    content.append("\n## Backup obrigatorio antes de editar\n")
    content.append("Exemplo: `response_templates.json.bak_2026-05-02_HHMMSS`.\n")
    content.append("Prioridade de alteracao sugerida:\n")
    content.append("1. `response_templates.json`, `intents_v2.json`, `dual_engine_rules.json`.")
    content.append("2. `JIM_COMPLIANCE_RULES_v2.md`, `JIM_RESPONSE_ENGINE.md`, `JIM_ADVISOR_COMMUNICATION.md`, `JIM_ADVERSARIAL_ENGINE.md`.")
    content.append("3. `qa_validation_matrix.csv` e consolidado Q&A, apos aprovacao dos textos seguros.")
    content.append("4. Codigo em `harpian-front/src` para transformar regras em validacoes executaveis.")
    (OUT / "LISTA_DE_ARQUIVOS_QUE_DEVEM_SER_ALTERADOS.md").write_text("\n".join(content), encoding="utf-8")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    files = collect_files()
    findings = []
    for path in files:
        for file_path, loc, text in file_items(path):
            findings.extend(analyze_item(file_path, loc, text))
    findings.extend(file_level_findings(files))
    # De-duplicate exact repeated findings.
    dedup = {}
    for f in findings:
        key = (f["arquivo_origem"], f["trecho_ou_template"][:180], f["tipo_risco"])
        current = dedup.get(key)
        if current is None or SEVERITY_RANK[f["severidade"]] > SEVERITY_RANK[current["severidade"]]:
            dedup[key] = f
    findings = sorted(dedup.values(), key=lambda f: (-SEVERITY_RANK[f["severidade"]], f["arquivo_origem"], f["tipo_risco"]))
    write_csv(findings)
    write_report(findings, [str(p) for p in files])
    write_rules()
    write_prompts()
    write_files_to_change(findings)
    manifest = {
        "date": date.today().isoformat(),
        "files_reviewed": len(files),
        "findings": len(findings),
        "outputs": [
            "RELATORIO_EXECUTIVO_COMPLIANCE_JIM.md",
            "MATRIZ_REVISAO_RESPOSTAS_JIM.csv",
            "REGRAS_COMPLIANCE_JIM_ATUALIZADAS.md",
            "PROMPTS_SEGUROS_JIM.md",
            "LISTA_DE_ARQUIVOS_QUE_DEVEM_SER_ALTERADOS.md",
        ],
    }
    (OUT / "manifest_revisao_codex.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
