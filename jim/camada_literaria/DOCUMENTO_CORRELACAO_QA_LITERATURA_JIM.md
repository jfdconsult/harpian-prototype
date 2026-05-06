# Camada adicional de literatura — correlação Q&A JIM x livros

Gerado em: 2026-05-02 22:33:39

## Escopo

- Pasta de literatura usada: `/mnt/c/Users/jfdco/OneDrive/Área de Trabalho/LIVROS PDF TEXTOS/BOOK FOR JIM`
- Pasta JIM usada: `/mnt/c/Users/jfdco/OneDrive/Área de Trabalho/HARPIAN/04_JIM_COMPLIANCE_QA`
- Perguntas/respostas tabulares extraídas e correlacionadas: **586**
- Fontes Q&A principais: Harpian_150_Questionnaire, Harpian_JIM_GM, Harpian_JIM_N, Harpian_JIM_v2 e perguntas adicionais da matriz QA quando não duplicadas.

Observação: o usuário mencionou 450 perguntas/respostas. Nesta execução, foram detectadas e correlacionadas 586 entradas tabulares disponíveis nos arquivos encontrados, portanto a matriz cobre mais entradas do que o número inicialmente mencionado. Se houver outro arquivo que deva compor a versão canônica, basta adicioná-lo à pasta Q&A ou indicar o caminho para integração.

## Entregáveis gerados

1. `MATRIZ_CORRELACAO_QA_LITERATURA_JIM.csv` — matriz linha a linha Q&A x literatura.
2. `BIBLIOTECA_LITERARIA_JIM.md` — biblioteca literária com cartões por livro.
3. `INSTRUCOES_USO_CAMADA_LITERARIA_JIM.md` — instruções para o JIM usar a camada literária.

## Separação conceitual obrigatória

- **Risk Number**: clientes, suitability, perfil de risco, tolerância, alinhamento de carteira.
- **Performance das estratégias**: retornos, drawdowns, Sharpe, CAGR, métricas, backtests, histórico AlphaDroid/Harpian.
- **Concorrentes**: hedge funds, ETFs, peers, comparativos de mercado.

## Clusters de literatura

- jim_architecture_communication: 155 perguntas/respostas
- momentum_regime_stormguard: 129 perguntas/respostas
- performance_backtest_metrics: 117 perguntas/respostas
- risk_number_suitability: 79 perguntas/respostas
- vehicle_tax_governance: 50 perguntas/respostas
- adversarial_failure_limits: 27 perguntas/respostas
- behavioral_decision: 23 perguntas/respostas
- macro_geopolitics: 3 perguntas/respostas
- competitors_hedge_funds: 3 perguntas/respostas

## Amostra de correlações

### JIM-LIT-0001 — 1. O que é um Risk Number em linguagem simples?

- Fonte: `Harpian_150_Questionnaire.docx`
- Cluster: risk_number_suitability
- Livros primários: B10: The Most Important Thing | B04: Thinking in Bets | B07: The Misbehavior of Markets
- Enriquecimento sugerido: Howard Marks, em The Most Important Thing, reforça risco é mais que volatilidade; Annie Duke, em Thinking in Bets, reforça boa decisão pode ter mau resultado; Benoit Mandelbrot, em The Misbehavior of Markets, reforça retornos têm caudas gordas.
- Guardrail: Não tratar Risk Number como recomendação; é linguagem de alinhamento de risco e deve exigir revisão humana/suitability.

### JIM-LIT-0002 — 2. Quais metodologias públicas existem para transformar risco em escala de 1 a 100?

- Fonte: `Harpian_150_Questionnaire.docx`
- Cluster: adversarial_failure_limits
- Livros primários: B11: Antifragile | B07: The Misbehavior of Markets | B04: Thinking in Bets
- Enriquecimento sugerido: Nassim Nicholas Taleb, em Antifragile, reforça sistemas frágeis quebram sob stress; Benoit Mandelbrot, em The Misbehavior of Markets, reforça retornos têm caudas gordas; Annie Duke, em Thinking in Bets, reforça boa decisão pode ter mau resultado.
- Guardrail: Enfatizar limites, cenários de falha e ausência de garantia; escalar para humano quando envolver ação financeira.

### JIM-LIT-0003 — 3. Como o Riskalyze/Nitrogen calcula ou comunica o Risk Number?

- Fonte: `Harpian_150_Questionnaire.docx`
- Cluster: risk_number_suitability
- Livros primários: B10: The Most Important Thing | B04: Thinking in Bets | B07: The Misbehavior of Markets
- Enriquecimento sugerido: Howard Marks, em The Most Important Thing, reforça risco é mais que volatilidade; Annie Duke, em Thinking in Bets, reforça boa decisão pode ter mau resultado; Benoit Mandelbrot, em The Misbehavior of Markets, reforça retornos têm caudas gordas.
- Guardrail: Não tratar Risk Number como recomendação; é linguagem de alinhamento de risco e deve exigir revisão humana/suitability.

### JIM-LIT-0004 — 4. Qual é a diferença entre Risk Number e volatilidade?

- Fonte: `Harpian_150_Questionnaire.docx`
- Cluster: performance_backtest_metrics
- Livros primários: B06: Advances in Financial Machine Learning | B07: The Misbehavior of Markets | B10: The Most Important Thing
- Enriquecimento sugerido: Marcos López de Prado, em Advances in Financial Machine Learning, reforça backtests sofrem risco de overfitting; Benoit Mandelbrot, em The Misbehavior of Markets, reforça retornos têm caudas gordas; Howard Marks, em The Most Important Thing, reforça risco é mais que volatilidade.
- Guardrail: Sempre acrescentar: performance passada/backtest não garante resultado futuro; considerar custos, slippage, liquidez, impostos, overfitting e suitability.

### JIM-LIT-0005 — 5. Qual é a diferença entre Risk Number e drawdown?

- Fonte: `Harpian_150_Questionnaire.docx`
- Cluster: performance_backtest_metrics
- Livros primários: B06: Advances in Financial Machine Learning | B07: The Misbehavior of Markets | B10: The Most Important Thing
- Enriquecimento sugerido: Marcos López de Prado, em Advances in Financial Machine Learning, reforça backtests sofrem risco de overfitting; Benoit Mandelbrot, em The Misbehavior of Markets, reforça retornos têm caudas gordas; Howard Marks, em The Most Important Thing, reforça risco é mais que volatilidade.
- Guardrail: Sempre acrescentar: performance passada/backtest não garante resultado futuro; considerar custos, slippage, liquidez, impostos, overfitting e suitability.

### JIM-LIT-0006 — 6. Qual é a diferença entre Risk Number e suitability?

- Fonte: `Harpian_150_Questionnaire.docx`
- Cluster: risk_number_suitability
- Livros primários: B10: The Most Important Thing | B04: Thinking in Bets | B07: The Misbehavior of Markets
- Enriquecimento sugerido: Howard Marks, em The Most Important Thing, reforça risco é mais que volatilidade; Annie Duke, em Thinking in Bets, reforça boa decisão pode ter mau resultado; Benoit Mandelbrot, em The Misbehavior of Markets, reforça retornos têm caudas gordas.
- Guardrail: Não tratar Risk Number como recomendação; é linguagem de alinhamento de risco e deve exigir revisão humana/suitability.

### JIM-LIT-0007 — 7. Como explicar Risk Number para um cliente leigo?

- Fonte: `Harpian_150_Questionnaire.docx`
- Cluster: risk_number_suitability
- Livros primários: B10: The Most Important Thing | B04: Thinking in Bets | B07: The Misbehavior of Markets
- Enriquecimento sugerido: Howard Marks, em The Most Important Thing, reforça risco é mais que volatilidade; Annie Duke, em Thinking in Bets, reforça boa decisão pode ter mau resultado; Benoit Mandelbrot, em The Misbehavior of Markets, reforça retornos têm caudas gordas.
- Guardrail: Não tratar Risk Number como recomendação; é linguagem de alinhamento de risco e deve exigir revisão humana/suitability.

### JIM-LIT-0008 — 8. Como explicar Risk Number para um Family Office?

- Fonte: `Harpian_150_Questionnaire.docx`
- Cluster: risk_number_suitability
- Livros primários: B10: The Most Important Thing | B04: Thinking in Bets | B07: The Misbehavior of Markets
- Enriquecimento sugerido: Howard Marks, em The Most Important Thing, reforça risco é mais que volatilidade; Annie Duke, em Thinking in Bets, reforça boa decisão pode ter mau resultado; Benoit Mandelbrot, em The Misbehavior of Markets, reforça retornos têm caudas gordas.
- Guardrail: Não tratar Risk Number como recomendação; é linguagem de alinhamento de risco e deve exigir revisão humana/suitability.

### JIM-LIT-0009 — 9. Quais inputs mínimos são necessários para estimar Risk Number?

- Fonte: `Harpian_150_Questionnaire.docx`
- Cluster: risk_number_suitability
- Livros primários: B10: The Most Important Thing | B04: Thinking in Bets | B07: The Misbehavior of Markets
- Enriquecimento sugerido: Howard Marks, em The Most Important Thing, reforça risco é mais que volatilidade; Annie Duke, em Thinking in Bets, reforça boa decisão pode ter mau resultado; Benoit Mandelbrot, em The Misbehavior of Markets, reforça retornos têm caudas gordas.
- Guardrail: Não tratar Risk Number como recomendação; é linguagem de alinhamento de risco e deve exigir revisão humana/suitability.

### JIM-LIT-0010 — 10. Como renda, patrimônio, horizonte e dependentes afetam capacidade de risco?

- Fonte: `Harpian_150_Questionnaire.docx`
- Cluster: risk_number_suitability
- Livros primários: B10: The Most Important Thing | B04: Thinking in Bets | B07: The Misbehavior of Markets
- Enriquecimento sugerido: Howard Marks, em The Most Important Thing, reforça risco é mais que volatilidade; Annie Duke, em Thinking in Bets, reforça boa decisão pode ter mau resultado; Benoit Mandelbrot, em The Misbehavior of Markets, reforça retornos têm caudas gordas.
- Guardrail: Não tratar Risk Number como recomendação; é linguagem de alinhamento de risco e deve exigir revisão humana/suitability.

### JIM-LIT-0011 — 11. Como tolerância a risco difere de capacidade de risco?

- Fonte: `Harpian_150_Questionnaire.docx`
- Cluster: risk_number_suitability
- Livros primários: B10: The Most Important Thing | B04: Thinking in Bets | B07: The Misbehavior of Markets
- Enriquecimento sugerido: Howard Marks, em The Most Important Thing, reforça risco é mais que volatilidade; Annie Duke, em Thinking in Bets, reforça boa decisão pode ter mau resultado; Benoit Mandelbrot, em The Misbehavior of Markets, reforça retornos têm caudas gordas.
- Guardrail: Não tratar Risk Number como recomendação; é linguagem de alinhamento de risco e deve exigir revisão humana/suitability.

### JIM-LIT-0012 — 12. Como objetivo de retorno muda o risco necessário?

- Fonte: `Harpian_150_Questionnaire.docx`
- Cluster: adversarial_failure_limits
- Livros primários: B11: Antifragile | B07: The Misbehavior of Markets | B04: Thinking in Bets
- Enriquecimento sugerido: Nassim Nicholas Taleb, em Antifragile, reforça sistemas frágeis quebram sob stress; Benoit Mandelbrot, em The Misbehavior of Markets, reforça retornos têm caudas gordas; Annie Duke, em Thinking in Bets, reforça boa decisão pode ter mau resultado.
- Guardrail: Enfatizar limites, cenários de falha e ausência de garantia; escalar para humano quando envolver ação financeira.

### JIM-LIT-0013 — 13. Como calcular perda potencial em 6 meses com 95% de confiança?

- Fonte: `Harpian_150_Questionnaire.docx`
- Cluster: performance_backtest_metrics
- Livros primários: B06: Advances in Financial Machine Learning | B07: The Misbehavior of Markets | B10: The Most Important Thing
- Enriquecimento sugerido: Marcos López de Prado, em Advances in Financial Machine Learning, reforça backtests sofrem risco de overfitting; Benoit Mandelbrot, em The Misbehavior of Markets, reforça retornos têm caudas gordas; Howard Marks, em The Most Important Thing, reforça risco é mais que volatilidade.
- Guardrail: Sempre acrescentar: performance passada/backtest não garante resultado futuro; considerar custos, slippage, liquidez, impostos, overfitting e suitability.

### JIM-LIT-0014 — 14. Como explicar intervalo de confiança aplicado a portfólios?

- Fonte: `Harpian_150_Questionnaire.docx`
- Cluster: behavioral_decision
- Livros primários: B04: Thinking in Bets | B10: The Most Important Thing | B11: Antifragile
- Enriquecimento sugerido: Annie Duke, em Thinking in Bets, reforça boa decisão pode ter mau resultado; Howard Marks, em The Most Important Thing, reforça risco é mais que volatilidade; Nassim Nicholas Taleb, em Antifragile, reforça sistemas frágeis quebram sob stress.
- Guardrail: Evitar aconselhamento pessoal; reforçar processo decisório, probabilidades e adequação ao perfil.

### JIM-LIT-0015 — 15. Quais limites regulatórios existem ao usar score de risco?

- Fonte: `Harpian_150_Questionnaire.docx`
- Cluster: adversarial_failure_limits
- Livros primários: B11: Antifragile | B07: The Misbehavior of Markets | B04: Thinking in Bets
- Enriquecimento sugerido: Nassim Nicholas Taleb, em Antifragile, reforça sistemas frágeis quebram sob stress; Benoit Mandelbrot, em The Misbehavior of Markets, reforça retornos têm caudas gordas; Annie Duke, em Thinking in Bets, reforça boa decisão pode ter mau resultado.
- Guardrail: Enfatizar limites, cenários de falha e ausência de garantia; escalar para humano quando envolver ação financeira.

### JIM-LIT-0016 — 16. Como explicar 'Approximate Risk Number' sem prometer precisão?

- Fonte: `Harpian_150_Questionnaire.docx`
- Cluster: risk_number_suitability
- Livros primários: B10: The Most Important Thing | B04: Thinking in Bets | B07: The Misbehavior of Markets
- Enriquecimento sugerido: Howard Marks, em The Most Important Thing, reforça risco é mais que volatilidade; Annie Duke, em Thinking in Bets, reforça boa decisão pode ter mau resultado; Benoit Mandelbrot, em The Misbehavior of Markets, reforça retornos têm caudas gordas.
- Guardrail: Não tratar Risk Number como recomendação; é linguagem de alinhamento de risco e deve exigir revisão humana/suitability.

### JIM-LIT-0017 — 17. Como comunicar baixa confiança no cálculo?

- Fonte: `Harpian_150_Questionnaire.docx`
- Cluster: behavioral_decision
- Livros primários: B04: Thinking in Bets | B10: The Most Important Thing | B11: Antifragile
- Enriquecimento sugerido: Annie Duke, em Thinking in Bets, reforça boa decisão pode ter mau resultado; Howard Marks, em The Most Important Thing, reforça risco é mais que volatilidade; Nassim Nicholas Taleb, em Antifragile, reforça sistemas frágeis quebram sob stress.
- Guardrail: Evitar aconselhamento pessoal; reforçar processo decisório, probabilidades e adequação ao perfil.

### JIM-LIT-0018 — 18. Quais frases evitar ao explicar score de risco?

- Fonte: `Harpian_150_Questionnaire.docx`
- Cluster: adversarial_failure_limits
- Livros primários: B11: Antifragile | B07: The Misbehavior of Markets | B04: Thinking in Bets
- Enriquecimento sugerido: Nassim Nicholas Taleb, em Antifragile, reforça sistemas frágeis quebram sob stress; Benoit Mandelbrot, em The Misbehavior of Markets, reforça retornos têm caudas gordas; Annie Duke, em Thinking in Bets, reforça boa decisão pode ter mau resultado.
- Guardrail: Enfatizar limites, cenários de falha e ausência de garantia; escalar para humano quando envolver ação financeira.

### JIM-LIT-0019 — 19. Quais disclaimers usar em risk profiling?

- Fonte: `Harpian_150_Questionnaire.docx`
- Cluster: adversarial_failure_limits
- Livros primários: B11: Antifragile | B07: The Misbehavior of Markets | B04: Thinking in Bets
- Enriquecimento sugerido: Nassim Nicholas Taleb, em Antifragile, reforça sistemas frágeis quebram sob stress; Benoit Mandelbrot, em The Misbehavior of Markets, reforça retornos têm caudas gordas; Annie Duke, em Thinking in Bets, reforça boa decisão pode ter mau resultado.
- Guardrail: Enfatizar limites, cenários de falha e ausência de garantia; escalar para humano quando envolver ação financeira.

### JIM-LIT-0020 — 20. Como documentar que o cliente aceitou desalinhamento?

- Fonte: `Harpian_150_Questionnaire.docx`
- Cluster: risk_number_suitability
- Livros primários: B10: The Most Important Thing | B04: Thinking in Bets | B07: The Misbehavior of Markets
- Enriquecimento sugerido: Howard Marks, em The Most Important Thing, reforça risco é mais que volatilidade; Annie Duke, em Thinking in Bets, reforça boa decisão pode ter mau resultado; Benoit Mandelbrot, em The Misbehavior of Markets, reforça retornos têm caudas gordas.
- Guardrail: Não tratar Risk Number como recomendação; é linguagem de alinhamento de risco e deve exigir revisão humana/suitability.

### JIM-LIT-0021 — 21. O que é volatilidade anualizada?

- Fonte: `Harpian_150_Questionnaire.docx`
- Cluster: performance_backtest_metrics
- Livros primários: B06: Advances in Financial Machine Learning | B07: The Misbehavior of Markets | B10: The Most Important Thing
- Enriquecimento sugerido: Marcos López de Prado, em Advances in Financial Machine Learning, reforça backtests sofrem risco de overfitting; Benoit Mandelbrot, em The Misbehavior of Markets, reforça retornos têm caudas gordas; Howard Marks, em The Most Important Thing, reforça risco é mais que volatilidade.
- Guardrail: Sempre acrescentar: performance passada/backtest não garante resultado futuro; considerar custos, slippage, liquidez, impostos, overfitting e suitability.

### JIM-LIT-0022 — 22. Como converter volatilidade diária em anualizada?

- Fonte: `Harpian_150_Questionnaire.docx`
- Cluster: performance_backtest_metrics
- Livros primários: B06: Advances in Financial Machine Learning | B07: The Misbehavior of Markets | B10: The Most Important Thing
- Enriquecimento sugerido: Marcos López de Prado, em Advances in Financial Machine Learning, reforça backtests sofrem risco de overfitting; Benoit Mandelbrot, em The Misbehavior of Markets, reforça retornos têm caudas gordas; Howard Marks, em The Most Important Thing, reforça risco é mais que volatilidade.
- Guardrail: Sempre acrescentar: performance passada/backtest não garante resultado futuro; considerar custos, slippage, liquidez, impostos, overfitting e suitability.

### JIM-LIT-0023 — 23. O que é drawdown?

- Fonte: `Harpian_150_Questionnaire.docx`
- Cluster: performance_backtest_metrics
- Livros primários: B06: Advances in Financial Machine Learning | B07: The Misbehavior of Markets | B10: The Most Important Thing
- Enriquecimento sugerido: Marcos López de Prado, em Advances in Financial Machine Learning, reforça backtests sofrem risco de overfitting; Benoit Mandelbrot, em The Misbehavior of Markets, reforça retornos têm caudas gordas; Howard Marks, em The Most Important Thing, reforça risco é mais que volatilidade.
- Guardrail: Sempre acrescentar: performance passada/backtest não garante resultado futuro; considerar custos, slippage, liquidez, impostos, overfitting e suitability.

### JIM-LIT-0024 — 24. O que é max drawdown?

- Fonte: `Harpian_150_Questionnaire.docx`
- Cluster: performance_backtest_metrics
- Livros primários: B06: Advances in Financial Machine Learning | B07: The Misbehavior of Markets | B10: The Most Important Thing
- Enriquecimento sugerido: Marcos López de Prado, em Advances in Financial Machine Learning, reforça backtests sofrem risco de overfitting; Benoit Mandelbrot, em The Misbehavior of Markets, reforça retornos têm caudas gordas; Howard Marks, em The Most Important Thing, reforça risco é mais que volatilidade.
- Guardrail: Sempre acrescentar: performance passada/backtest não garante resultado futuro; considerar custos, slippage, liquidez, impostos, overfitting e suitability.

### JIM-LIT-0025 — 25. O que é drawdown duration?

- Fonte: `Harpian_150_Questionnaire.docx`
- Cluster: performance_backtest_metrics
- Livros primários: B06: Advances in Financial Machine Learning | B07: The Misbehavior of Markets | B10: The Most Important Thing
- Enriquecimento sugerido: Marcos López de Prado, em Advances in Financial Machine Learning, reforça backtests sofrem risco de overfitting; Benoit Mandelbrot, em The Misbehavior of Markets, reforça retornos têm caudas gordas; Howard Marks, em The Most Important Thing, reforça risco é mais que volatilidade.
- Guardrail: Sempre acrescentar: performance passada/backtest não garante resultado futuro; considerar custos, slippage, liquidez, impostos, overfitting e suitability.

## Regra de uso final

O JIM só deve citar livros quando a referência aumentar clareza, educação ou contexto. A citação deve ser curta, sem pedantismo, e acompanhada de linguagem de incerteza e compliance quando houver risco, performance, simulação ou decisão de investimento.


## ATUALIZAÇÃO — Livro 00 como base principal

O livro `00 - Conquering the Seven Faces of Risk - Scott.pdf` foi adicionado como base de consulta número 1 para gestão de momentum, Temporal Portfolio Theory, rotação temporal, regimes e diferenciação da filosofia Harpian em relação a value investing, buy and hold e dividend investing. Ver `MANUAL_BOOK_FOR_JIM_TAXONOMIA_30_LIVROS_COM_BASE_SCOTT.md`.

