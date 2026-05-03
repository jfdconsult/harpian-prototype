# Relatorio Executivo Compliance JIM

Data da revisao: 2026-05-02

Escopo: respostas, templates, regras, Q&A, documentos e codigo relacionado ao JIM/Intelligence, com foco em compliance, suitability e comunicacao segura para advisor/family office.

Nenhum arquivo fonte foi alterado. Esta revisao gerou apenas artefatos na pasta de saida datada.

Nota: este material e um diagnostico tecnico de compliance por heuristicas, leitura amostral e referencias reguladoras publicas. Nao substitui revisao juridica formal nem aprovacao do CCO/compliance officer.

## Principais riscos encontrados

- Linguagem de performance ainda exige classificacao operacional obrigatoria: backtest, walk-forward, live track record, model index, client actual ou unknown/bloqueado.
- Templates e regras ja possuem boa base de guardrails, mas precisam de reforco mecanico para impedir recomendacao direta e separar Risk Number de performance.
- Respostas com retorno, Sharpe, drawdown, AlphaDroid, benchmark, hedge funds, simulacao ou carteira precisam de disclaimer proximo ao numero, nao apenas em rodape generico.
- Arquivos com sinais de encoding incorreto devem ser normalizados para UTF-8 antes de aprovacao formal, pois acentuacao corrompida prejudica comunicacao client-facing.
- Front-end e documentacao tecnica devem tratar JIM como assistente analitico, nao como consultor autonomo.

## Severidade

| severidade | quantidade |
| --- | --- |
| CRITICAL | 51 |
| HIGH | 1009 |
| MEDIUM | 155 |
| LOW | 1 |

## Tipos de risco

| tipo_risco | quantidade |
| --- | --- |
| Performance sem disclosure suficiente | 876 |
| Linguagem promocional excessiva | 152 |
| Risk Number misturado com performance | 105 |
| Promessa proibida / garantia | 51 |
| Recomendação direta / suitability | 28 |
| Comparação potencialmente enganosa | 3 |
| Qualidade textual / encoding | 1 |

## Arquivos revisados

Total de arquivos revisados: 126

- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\compliance_audit_extracted\HARPIAN_QA_CONSOLIDADO_COM_DISCLAIMERS.docx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\compliance_audit_extracted\qa_validation_matrix.csv`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\COMPLIANCE_AUDIT_QA_HARPIAN.md`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\JIM Biblioteca Estrutura all docs\config\dual_engine_rules.json`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\JIM Biblioteca Estrutura all docs\config\intents_v2.json`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\JIM Biblioteca Estrutura all docs\config\response_templates.json`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\JIM Biblioteca Estrutura all docs\docs\jim\JIM_ADVERSARIAL_ENGINE.md`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\JIM Biblioteca Estrutura all docs\docs\jim\JIM_ADVISOR_COMMUNICATION.md`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\JIM Biblioteca Estrutura all docs\docs\jim\JIM_COMPLIANCE_RULES_v2.md`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\JIM Biblioteca Estrutura all docs\docs\jim\JIM_RESPONSE_ENGINE.md`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\JIM Biblioteca Estrutura all docs\Harpian_JIM_4Layers.docx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\JIM Biblioteca Estrutura all docs\Harpian_JIM_Objections.docx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\JIM Biblioteca Estrutura all docs\Harpian_JIM_QuantDD.docx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\docs\jim\COMPLIANCE_AUDIT_QA_HARPIAN.md`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\docs\jim\qa_validation_matrix.csv`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\docs\JIM_TECHNICAL_ARCHITECTURE_SOTA.md`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\app\intelligence\[clientId]\loading.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\app\intelligence\[clientId]\page.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\app\intelligence\[clientId]\simulator\page.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\app\intelligence\[clientId]\upload\page.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\app\intelligence\actions.ts`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\app\intelligence\dtl\page.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\app\intelligence\error.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\app\intelligence\family-office\page.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\app\intelligence\family-office\questionnaire\FOQuestionnaireForm.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\app\intelligence\family-office\questionnaire\page.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\app\intelligence\layout.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\app\intelligence\loading.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\app\intelligence\market-intelligence\page.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\app\intelligence\overview\page.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\app\intelligence\page.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\app\intelligence\presentation\[id]\page.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\app\intelligence\presentation\[id]\present\page.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\app\intelligence\presentation\page.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\app\intelligence\stormguard\page.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\app\intelligence\strategies\[number]\page.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\app\intelligence\strategies\page.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\app\intelligence\watchlist\page.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\AnalysisDashboard.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\AnimatedNumber.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\AttributeWheel.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\CompoundingChart.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\CorrelationHeatmap.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\CrisisPanel.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\DTLPanel.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\EditProfileModal.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\FamilyOfficeDashboard.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\IntelligenceAuth.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\IntelligenceDashboard.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\IntelligenceNav.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\IntelligenceUpload.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\MomentumMap.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\NotesPanel.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\OverviewDashboard.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\PortfolioCard.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\PresentationDashboard.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\PresentationHub.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\PresentationPlayer.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\RiskScatterPlot.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\RiskTable.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\RnDriftBadge.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\SimulatorClient.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\StormGuardPanel.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\strategy-detail\DrawdownsTab.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\strategy-detail\ForwardReturnsTab.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\strategy-detail\MonthlyReturnsTab.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\strategy-detail\OverviewTab.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\strategy-detail\ReportsTab.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\strategy-detail\RiskComparisonTab.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\strategy-detail\RiskProfileTab.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\strategy-detail\RollingPerformanceTab.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\strategy-detail\shared.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\strategy-detail\StrategyDetailShell.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\strategy-detail\StressTestingTab.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\strategy-detail\ui-AnimatedNumber.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\strategy-detail\ui-BenchmarkBar.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\strategy-detail\ui-EquityCurve.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\strategy-detail\ui-Heatmap.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\strategy-detail\ui-HeroHeader.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\strategy-detail\ui-Histogram.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\strategy-detail\ui-RiskRing.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\strategy-detail\ui-RollingChart.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\strategy-detail\ui-ScenarioCard.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\SurveyLinkModal.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\WatchlistClient.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\YearlyBars.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\data\assetClassProfiles.ts`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\data\assetCrisisProfiles.ts`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\data\familyOfficeQuestions.ts`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\data\familyOfficeTemplates.ts`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\data\harpianCoreStrategies.ts`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\data\harpianStrategyMetrics.ts`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\data\portfolioStats.ts`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\data\riskBands.ts`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\data\riskMultipliers.ts`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\data\riskQuestions.ts`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\data\siteContent.ts`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\data\stressScenarios.ts`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\lib\advanced-metrics.ts`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\lib\alphadroid.ts`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\lib\animations.ts`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\lib\auth.ts`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\lib\constants.ts`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\lib\crisis-cache.ts`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\lib\db.ts`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\lib\equity-curve-stats.ts`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\lib\equity-curve-utils.ts`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\lib\fonts.ts`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\lib\hrd-engine.ts`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\lib\i18n.tsx`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\lib\intelligence-scoring.ts`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\lib\live-prices.ts`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\lib\live-strategy-metrics.ts`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\lib\llm.ts`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\lib\logger.ts`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\lib\migrate.ts`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\lib\portfolio-crisis.ts`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\lib\portfolio-parser.ts`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\lib\portfolio-risk.ts`
- `C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\lib\presentation-types.ts`
- ... mais 6 arquivos de codigo/documentacao.

## Arquivos com mais achados

| arquivo | achados |
| --- | --- |
| C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\compliance_audit_extracted\HARPIAN_QA_CONSOLIDADO_COM_DISCLAIMERS.docx | 181 |
| C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\JIM Biblioteca Estrutura all docs\Harpian_JIM_4Layers.docx | 121 |
| C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\JIM Biblioteca Estrutura all docs\Harpian_JIM_Objections.docx | 98 |
| C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\JIM Biblioteca Estrutura all docs\Harpian_JIM_QuantDD.docx | 48 |
| C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\app\intelligence\actions.ts | 35 |
| C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\lib\portfolio-parser.ts | 25 |
| C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\strategy-detail\RiskComparisonTab.tsx | 24 |
| C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\strategy-detail\MonthlyReturnsTab.tsx | 23 |
| C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\strategy-detail\RiskProfileTab.tsx | 22 |
| C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\PresentationPlayer.tsx | 22 |
| C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\strategy-detail\OverviewTab.tsx | 21 |
| C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\JIM Biblioteca Estrutura all docs\config\intents_v2.json | 21 |
| C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\lib\advanced-metrics.ts | 21 |
| C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\lib\equity-curve-utils.ts | 19 |
| C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\AnalysisDashboard.tsx | 17 |
| C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\strategy-detail\DrawdownsTab.tsx | 17 |
| C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\strategy-detail\StressTestingTab.tsx | 16 |
| C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\components\intelligence\strategy-detail\ForwardReturnsTab.tsx | 15 |
| C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\lib\alphadroid.ts | 15 |
| C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\harpian-front\src\lib\equity-curve-stats.ts | 13 |

## Achados prioritarios

| severidade | tipo_risco | arquivo | problema |
| --- | --- | --- | --- |
| CRITICAL | Promessa proibida / garantia | C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\COMPLIANCE_AUDIT_QA_HARPIAN.md | A linguagem pode ser lida como promessa, garantia ou projeção de resultado. |
| CRITICAL | Promessa proibida / garantia | C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\JIM Biblioteca Estrutura all docs\Harpian_JIM_4Layers.docx | A linguagem pode ser lida como promessa, garantia ou projeção de resultado. |
| CRITICAL | Promessa proibida / garantia | C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\JIM Biblioteca Estrutura all docs\Harpian_JIM_4Layers.docx | A linguagem pode ser lida como promessa, garantia ou projeção de resultado. |
| CRITICAL | Promessa proibida / garantia | C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\JIM Biblioteca Estrutura all docs\Harpian_JIM_4Layers.docx | A linguagem pode ser lida como promessa, garantia ou projeção de resultado. |
| CRITICAL | Promessa proibida / garantia | C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\JIM Biblioteca Estrutura all docs\Harpian_JIM_4Layers.docx | A linguagem pode ser lida como promessa, garantia ou projeção de resultado. |
| CRITICAL | Promessa proibida / garantia | C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\JIM Biblioteca Estrutura all docs\Harpian_JIM_4Layers.docx | A linguagem pode ser lida como promessa, garantia ou projeção de resultado. |
| CRITICAL | Promessa proibida / garantia | C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\JIM Biblioteca Estrutura all docs\Harpian_JIM_Objections.docx | A linguagem pode ser lida como promessa, garantia ou projeção de resultado. |
| CRITICAL | Promessa proibida / garantia | C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\JIM Biblioteca Estrutura all docs\Harpian_JIM_QuantDD.docx | A linguagem pode ser lida como promessa, garantia ou projeção de resultado. |
| CRITICAL | Promessa proibida / garantia | C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\JIM Biblioteca Estrutura all docs\config\response_templates.json | A linguagem pode ser lida como promessa, garantia ou projeção de resultado. |
| CRITICAL | Promessa proibida / garantia | C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\JIM Biblioteca Estrutura all docs\docs\jim\JIM_ADVISOR_COMMUNICATION.md | A linguagem pode ser lida como promessa, garantia ou projeção de resultado. |
| CRITICAL | Promessa proibida / garantia | C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\JIM Biblioteca Estrutura all docs\docs\jim\JIM_COMPLIANCE_RULES_v2.md | A linguagem pode ser lida como promessa, garantia ou projeção de resultado. |
| CRITICAL | Promessa proibida / garantia | C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\JIM Biblioteca Estrutura all docs\docs\jim\JIM_COMPLIANCE_RULES_v2.md | A linguagem pode ser lida como promessa, garantia ou projeção de resultado. |
| CRITICAL | Promessa proibida / garantia | C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\JIM Biblioteca Estrutura all docs\docs\jim\JIM_COMPLIANCE_RULES_v2.md | A linguagem pode ser lida como promessa, garantia ou projeção de resultado. |
| CRITICAL | Promessa proibida / garantia | C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\compliance_audit_extracted\HARPIAN_QA_CONSOLIDADO_COM_DISCLAIMERS.docx | A linguagem pode ser lida como promessa, garantia ou projeção de resultado. |
| CRITICAL | Promessa proibida / garantia | C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\compliance_audit_extracted\HARPIAN_QA_CONSOLIDADO_COM_DISCLAIMERS.docx | A linguagem pode ser lida como promessa, garantia ou projeção de resultado. |
| CRITICAL | Promessa proibida / garantia | C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\compliance_audit_extracted\HARPIAN_QA_CONSOLIDADO_COM_DISCLAIMERS.docx | A linguagem pode ser lida como promessa, garantia ou projeção de resultado. |
| CRITICAL | Promessa proibida / garantia | C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\compliance_audit_extracted\HARPIAN_QA_CONSOLIDADO_COM_DISCLAIMERS.docx | A linguagem pode ser lida como promessa, garantia ou projeção de resultado. |
| CRITICAL | Promessa proibida / garantia | C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\compliance_audit_extracted\HARPIAN_QA_CONSOLIDADO_COM_DISCLAIMERS.docx | A linguagem pode ser lida como promessa, garantia ou projeção de resultado. |
| CRITICAL | Promessa proibida / garantia | C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\compliance_audit_extracted\HARPIAN_QA_CONSOLIDADO_COM_DISCLAIMERS.docx | A linguagem pode ser lida como promessa, garantia ou projeção de resultado. |
| CRITICAL | Promessa proibida / garantia | C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\compliance_audit_extracted\HARPIAN_QA_CONSOLIDADO_COM_DISCLAIMERS.docx | A linguagem pode ser lida como promessa, garantia ou projeção de resultado. |
| CRITICAL | Promessa proibida / garantia | C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\compliance_audit_extracted\HARPIAN_QA_CONSOLIDADO_COM_DISCLAIMERS.docx | A linguagem pode ser lida como promessa, garantia ou projeção de resultado. |
| CRITICAL | Promessa proibida / garantia | C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\compliance_audit_extracted\HARPIAN_QA_CONSOLIDADO_COM_DISCLAIMERS.docx | A linguagem pode ser lida como promessa, garantia ou projeção de resultado. |
| CRITICAL | Promessa proibida / garantia | C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\compliance_audit_extracted\HARPIAN_QA_CONSOLIDADO_COM_DISCLAIMERS.docx | A linguagem pode ser lida como promessa, garantia ou projeção de resultado. |
| CRITICAL | Promessa proibida / garantia | C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\compliance_audit_extracted\HARPIAN_QA_CONSOLIDADO_COM_DISCLAIMERS.docx | A linguagem pode ser lida como promessa, garantia ou projeção de resultado. |
| CRITICAL | Promessa proibida / garantia | C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\04_JIM_COMPLIANCE_QA\compliance_audit_extracted\HARPIAN_QA_CONSOLIDADO_COM_DISCLAIMERS.docx | A linguagem pode ser lida como promessa, garantia ou projeção de resultado. |

## Recomendacoes executivas

1. Transformar os disclaimers em regras executaveis no CGE, nao apenas texto documental.
2. Adicionar campo obrigatorio `performance_label` para qualquer numero de performance.
3. Bloquear respostas client-facing quando performance estiver `unknown`, sem data-base, sem metodologia ou apenas bruta sem aviso.
4. Inserir teste adversarial para perguntas recorrentes: 'isso e retorno real ou backtest?', 'qual vai render mais?', 'garante que nao vou perder?', 'devo investir tudo?'.
5. Criar fluxo de aprovacao humana para alteracoes em templates client-facing.

## Bases reguladoras usadas como referencia

- FINRA Rule 2210: comunicacoes devem ser justas, balanceadas, sem declaracoes falsas, exageradas, promissorias ou enganosas; projecoes de performance sao limitadas. Fonte: https://www.finra.org/rules-guidance/rulebooks/finra-rules/2210
- FINRA Advertising Regulation FAQ: reforca que Rule 2210 proibe predicoes/projecoes de performance e implicacao de que performance passada vai se repetir. Fonte: https://www.finra.org/rules-guidance/guidance/faqs/advertising-regulation
- SEC Investment Adviser Marketing Rule: performance bruta, liquida, hipotetica/modelo/extracted performance exigem condicoes, politicas, informacoes de metodologia e tratamento justo de riscos/limitacoes. Fonte: https://www.sec.gov/investment/investment-adviser-marketing
- SEC Marketing Compliance FAQ atualizada em 2026: reforca cuidado com metricas brutas, net performance e caracteristicas extraidas quando usadas em comunicacao de marketing. Fonte: https://www.sec.gov/rules-regulations/staff-guidance/division-investment-management-frequently-asked-questions/marketing-compliance-frequently-asked-questions