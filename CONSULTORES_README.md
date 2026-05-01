# HARPIAN Prototype - Pacote para Consultores

Este pacote contem o prototipo local do HARPIAN Portfolio Engineering Terminal.

## Arquivos principais

- `terminal.html`: terminal principal, incluindo Client Profile, Risk Number, News/Social Radar, Sector Momentum e Jim AI.
- `presentation-mode.html`: modo apresentacao.
- `api/`: API local Flask/mock para dados do terminal.
- `backend/`: backend auxiliar do prototipo.
- `data/`: dados e fontes mockadas do terminal.
- `docs/`: documentos de apoio do prototipo.
- `.claude/`: configuracao local de launch do ambiente.

## Jim AI

O Jim AI esta embutido principalmente em `terminal.html`.

Pontos importantes para revisar:

- CSS e UI do painel Jim: procurar por `JIM AI`.
- Painel flutuante: bloco HTML `jim-panel`.
- Funcoes JS: procurar por `jimToggle`, `jimSend`, `jimAutoTrigger`, `jimOpenAlert`.
- Command Center diario: procurar por `JIM DAILY COMMAND CENTER`.

## Observacao operacional

As simulacoes de portfolio/Risk Number sao locais e nao validam ordens. A validacao operacional no terminal permanece restrita a alocacoes dos ETPs `HPC11` e `HPC22`.
