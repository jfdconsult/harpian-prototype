# Sistema Único — HARPIAN Risk Number MFO + HARPIAN Information System

## Arquivo de orientação para JP / Codex / Claude / Hermes

A partir desta decisão, o HARPIAN Information System deve seguir a mesma linha do sistema de risco. Não criar um produto separado fora desta pasta.

Pasta oficial do sistema:

`C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\Risk Number MFO`

## Componentes existentes nesta pasta

- `hrd_engine.py` — motor de risco/HRD já existente. Preservar.
- `HTLM DOCUMENTATIONM/` — documentação visual e arquitetural do Risk Alignment.
- `Portifolios modelos para HIS/` — planilhas de portfolios modelo para alimentar HIS.
- `harpian-information-system/` — nova camada front-end do Portfolio Builder / Strategy Builder.

## Regra de ouro

O front-end não reprograma motor quantitativo. Ele organiza, visualiza, configura e chama backend.

## Como rodar a UI

```bash
cd '/mnt/c/Users/jfdco/OneDrive/Área de Trabalho/HARPIAN/Risk Number MFO/harpian-information-system'
npm install
npm test
npm run build
npm run dev -- --port 5174
```

## Próxima etapa técnica

Criar API backend que exponha `hrd_engine.py` para o front-end:

- `POST /api/risk-number/portfolio`
- `POST /api/risk-number/client-alignment`
- `POST /api/backtest/run`
- `POST /api/reports/generate`

Até existir API real, a UI usa mocks marcados como `MOCK_BACKEND_PLACEHOLDER`.
