# Auditoria de Compliance - Q&A Harpian

Data: 2026-04-30  
Escopo: arquivos em `JIM Biblioteca Estrutura all docs/Q&A` confrontados com a base local em `JURIDICO/regulatory-ingestion` e `JURIDICO/orgaos reguladores`.  
Nota: esta revisao e uma auditoria de compliance documental, nao parecer juridico.

## Resultado executivo

Foram extraidos 7 documentos e identificadas 280 perguntas/respostas estruturadas, alem de 4 documentos/secoes auditados em nivel documental. A matriz completa esta em `compliance_audit_extracted/qa_validation_matrix.csv`.

Distribuicao da matriz apos triagem conservadora:

- `APROVADO`: 120 itens.
- `APROVADO_COM_CORRECAO`: 83 itens.
- `APROVADO_COM_RESSALVAS`: 4 documentos/secoes sem Q&A tabular detectado.
- `BLOQUEAR_ATE_CORRIGIR`: 77 itens.

Conclusao: o material tem boa consciencia de compliance em varios pontos, especialmente quando diferencia simulacao de recomendacao. Ainda assim, as respostas marcadas como `BLOQUEAR_ATE_CORRIGIR` nao devem ser usadas externamente antes de ajuste. O principal problema e que algumas respostas combinam produto, performance, beneficio fiscal, estrutura offshore, comparacao com benchmarks e linguagem categorica. Isso aciona risco sob FINRA 2210, SEC Marketing Rule, Reg BI/Form CRS e camada Florida/OFR.

## Base regulatoria usada

- FINRA Rule 2210: comunicacoes devem ser fair and balanced, dar base razoavel para avaliar fatos e nao omitir qualificacoes materiais; tambem veda declaracoes falsas, exageradas, promissorias ou enganosas. Fonte local: `JURIDICO/regulatory-ingestion/communications/sources/finra-rule-2210-communications-with-public.html`.
- FINRA Rule 4511: livros e registros exigidos devem ser preservados; quando nao houver prazo especifico, minimo de seis anos, em formato compativel com SEA Rule 17a-4. Fonte local: `JURIDICO/regulatory-ingestion/communications/sources/supplemental/finra-rule-4511-general-books-records.html`.
- SEC Marketing Rule IA-5653: anuncios nao podem conter statement material falso, omitir fato material, induzir inferencia enganosa, discutir beneficios sem tratamento justo de riscos/limitacoes, nem apresentar performance sem requisitos aplicaveis. Fonte local: `JURIDICO/regulatory-ingestion/adviser-marketing/sources/sec-ia-5653-investment-adviser-marketing-final-rule.pdf`.
- Regulation Best Interest/Form CRS: cuidado especial quando houver recomendacao para retail customer, disclosure de conflitos, custos e natureza da relacao. Fonte local: `JURIDICO/regulatory-ingestion/adviser-marketing/sources/supplemental/sec-reg-bi-faq.html`.
- Florida Layer: OFR/FAC e a camada estadual principal para adviser/securities compliance; DFS deve ser usado apenas para fraude, educacao, reporting e awareness. Fonte local: `JURIDICO/regulatory-ingestion/florida-layer/README.md`.

## Achados criticos

1. Performance e benchmark com linguagem muito forte

Exemplos:

- `Harpian_JIM_GM.txt:88`, I6 compara HPC22 ao S&P 500 com numeros de retorno e drawdown, incluindo "supera" e "superior". Apesar de conter ressalvas, a narrativa ainda prioriza vantagem de performance antes dos riscos.
- `Harpian_JIM_GM.txt:121`, J7 apresenta drawdowns esperados por perfil, incluindo cenarios 2008/2020/2022.
- `Harpian_JIM_GM.txt:124`, J8 apresenta CAGR historico/live e performance YTD.
- `Harpian_150_Questionnaire.txt:286`, Q92 apresenta retornos de HPC11/HPC22 contra S&P 500.

Validacao: bloquear ate reescrever em formato equilibrado, com metodologia, periodo, fonte dos dados, net/gross, taxas, custos, limitacoes, data de corte, comparabilidade de benchmark e disclaimers antes ou junto dos numeros.

2. Beneficios fiscais/offshore tratados como vantagem central

Exemplos:

- `Harpian_JIM_GM.txt:13`, G1 afirma que a vantagem central do ETP offshore e diferimento fiscal e quantifica tax drag.
- `Harpian_JIM_GM.txt:19`, G3 cita regime 2025-2026 e PL 1.087/2025 como se estivesse estabilizado.
- `Harpian_JIM_GM.txt:22`, G4 quantifica capital adicional por diferimento.
- `Harpian_JIM_GM.txt:40`, G10 afirma obrigacoes para residente fiscal brasileiro, inclusive CBE "independentemente do valor".

Validacao: bloquear ate revisao por counsel tributario. A resposta deve dizer "pode haver", "depende da jurisdicao", "sujeito a confirmacao", e remover calculos ilustrativos que parecam promessa de ganho liquido fiscal.

3. Estrutura/custodia com afirmacoes absolutas

Exemplos:

- `Harpian_150_Questionnaire.txt:313`, Q101 diz que a estrutura "garante bankruptcy remoteness".
- `JIM_Architecture_v2.txt:344` diz que, em insolvencia, ativos "permanecem protegidos".
- `Harpian_JIM_GM.txt:16`, G2 afirma que custodia independente gera bankruptcy remoteness do emissor.

Validacao: bloquear ate qualificar por offering documents, custodiante, tipo juridico do instrumento, riscos de emissor, contraparte, operacional, mercado secundario e insolvencia. Evitar "garante".

4. Recomendacao/advice ainda aparece em pontos de encaminhamento

Exemplos:

- `Harpian_150_Questionnaire.txt:460`, Q150 usa "Recomendo uma conversa direta com seu advisor". Como a propria politica bane "recomendo", trocar por "esta pergunta deve ser tratada por um advisor humano".
- `JIM_Architecture_v2.txt:133` usa "recomendo" em exemplo de loop para advisor.
- `Harpian_150_Questionnaire.txt:391`, Q127 usa "Recomendamos que o investidor consulte..."; para consistencia do filtro, trocar por "O investidor deve consultar..." ou "E apropriado consultar...".

Validacao: aprovavel com correcao. A palavra "recomendo/recomendamos" deve ser reservada apenas a exemplos negativos claramente marcados como proibidos.

5. Simulacao pode virar recomendacao se vier depois de suitability fraca

Exemplos:

- `Harpian_JIM_GM.txt:64`, H8 acerta ao dizer que suitability e simulation nao sao substitutos, mas tambem diz que simulacoes "ajudam a calibrar a alocacao"; precisa deixar claro que a ferramenta nao determina alocacao final.
- `JIM_Architecture_v2.txt:259` mostra simulacao com percentuais HPC11/HPC22. O disclaimer existe, mas a resposta precisa tambem registrar que requer review humano/suitability antes de qualquer acao.

Validacao: aprovavel com correcao. Toda simulacao de alocacao deve trazer status "diagnostico matematico", nao "proposta", e acionar trilha de suitability/approval quando o usuario pedir acao.

## Correcoes obrigatorias antes de uso externo

- Incluir bloco padrao de disclosure para toda resposta com performance, simulacao, benchmark, risco, drawdown, CAGR ou alocacao.
- Separar materiais por audiencia: institutional, advisor, non-US qualified, US person, retail/prospect. Nao usar o mesmo Q&A para todos.
- Trocar linguagem absoluta: "garante", "seguro", "superior", "sem risco", "protegido", "ideal", "deve comprar/investir".
- Vincular performance a fonte, periodo, data de corte, metodologia, net/gross, custos e limitacoes.
- Encaminhar temas fiscais, sucessorios, Regulation S, US Person, Form CRS, RIA, CBE, IOF e PL/lei brasileira para counsel ou assessor qualificado.
- Registrar logs e retencao: manter pergunta, resposta, template, dados usados, versao do modelo/template, data de corte e disclaimers aplicados.

## Status por documento

- `Harpian_150_Questionnaire.docx`: 150 Q&As; muitos itens conceituais aprovaveis, mas blocos HPC/ETP/performance/fiscal exigem correcao.
- `Harpian_JIM_GM.docx`: 70 Q&As; maior concentracao de risco critico em ETP offshore, tributacao, US/non-US, performance e comparativos.
- `Harpian_JIM_v2.docx`: 60 Q&As; bom arcabouco de limites, mas precisa limpar exemplos com palavra banida e reforcar suitability antes de alocacao.
- `Harpian_JIM_N.docx`: sem Q&A tabular detectado pelo parser; revisar em nivel documental antes de publicar.
- `Jim_AI_Architecture_v1.docx` e `JIM_Architecture_v2.docx`: especificacoes de arquitetura com controles relevantes; ajustar exemplos e politicas para refletir a matriz acima.
- `Documentacao de producao e base de conhecimento do DMA.pdf`: contem boa politica de compliance, mas deve ser usado como baseline interno e nao como material promocional.

## Proxima acao recomendada

Criar uma versao "clean room" das respostas bloqueadas: primeiro performance/produto, depois fiscal/legal, depois arquitetura de disclaimers e log. A matriz CSV ja identifica os itens para edicao por arquivo, linha, ID e tipo de risco.
