# HARPIAN Portfolio Engineering Terminal — Architecture Guide

> **Para 0JP:** Este documento descreve toda a arquitetura, o que já está construído, e exatamente o que você precisa conectar. Cada integration point está marcado com `0JP:`.

---

## Visão Geral

```
┌─────────────────────────────────────────────────────────────────────┐
│                    HARPIAN TERMINAL (frontend)                       │
│                      terminal.html (SPA)                            │
│   16 screens · Bloomberg dark UI · Space Grotesk / DM Mono fonts    │
│   Hosted: Vercel / npx serve -l 3131                                │
└──────────────────┬──────────────────────────────────────────────────┘
                   │  HTTP REST (localhost:5050 / api.harpian.io)
                   │  Fallback: embedded mock data (zero downtime)
┌──────────────────▼──────────────────────────────────────────────────┐
│                    HARPIAN API (backend)                             │
│                    api/server.py  (Flask)                           │
│  /api/clients  /api/alerts  /api/regime  /api/hpc  /api/social      │
└──────┬────────────────┬──────────────┬──────────────────────────────┘
       │                │              │
┌──────▼──────┐  ┌──────▼──────┐  ┌──▼──────────────────────────────┐
│ harpian.db  │  │harpian_     │  │  JD NEWS Pipeline               │
│ (SQLite)    │  │social.db    │  │  harpian_scraper.py             │
│             │  │(SQLite)     │  │  harpian_curator.py  (Claude)   │
│ clients     │  │             │  │  social_scraper.py              │
│ portfolios  │  │monitored_   │  │  social_processor.py (Claude)   │
│ allocations │  │sources      │  │  → data/articles_DDMMYYYY.json  │
│ alerts      │  │social_feed  │  │  → curadoria_output/*.docx      │
│ regime_     │  │             │  │  Runs: Task Scheduler 30min     │
│ snapshots   │  └─────────────┘  └─────────────────────────────────┘
│ hpc_        │
│ performance │
│ fo_profile  │
└─────────────┘
```

---

## Estrutura de Arquivos

```
harpian-prototype/
│
├── terminal.html          # Frontend SPA — todos os 16 screens
│   └── (API layer: HARPIAN_API + harpianFetch() com fallback mock)
│
├── api/
│   ├── server.py          # Flask REST API — todos os endpoints
│   └── requirements.txt   # Python deps para a API
│
├── backend/
│   ├── harpian_db.py      # Schema + queries: clients, portfolios, alerts, regime
│   └── alerts_engine.py   # Motor de alertas por regras (RN, DD, regime change)
│
├── data/
│   ├── harpian.db         # (gerado pelo init_db) — DB principal
│   ├── harpian_social.db  # (gerado pelo JD NEWS) — social feed
│   ├── clients.json       # Dados mock de clientes (seed)
│   ├── regime.json        # Regime Engine data (seed)
│   ├── fo_profile.json    # Configuração institucional
│   └── articles_DDMMYYYY.json  # Notícias diárias (gerado pelo scraper)
│
├── docs/
│   ├── ARCHITECTURE.md    # Este arquivo
│   └── API_REFERENCE.md   # Referência de endpoints
│
├── .env.example           # Template de variáveis de ambiente
├── requirements.txt       # Deps Python completo
└── start.ps1              # Script de inicialização (Windows)
```

---

## Screens: Status de Implementação

| Screen | Status | Dados | API Ready |
|--------|--------|-------|-----------|
| Dashboard | ✅ Completo | Mock + Live regime | ✅ |
| Market Intelligence | ✅ Completo | Mock + JD NEWS | ✅ |
| Market Trends (Regime) | ✅ Completo | Mock + `/api/regime` | ✅ |
| Social Media Radar | ✅ Completo | Mock + `/api/social/feed` | ✅ |
| Clients Overview | ✅ Completo | Mock + `/api/clients` | ✅ |
| Client Profile | ✅ Completo | Mock + `/api/clients/:id` | ✅ |
| Onboarding | ✅ UI pronto | Form → `POST /api/clients` | 🔧 0JP: salvar no DB |
| Portfolio Upload | ✅ UI pronto | Simulado | 🔧 0JP: parser CSV/PDF |
| HPC Strategies | ✅ Completo | Mock + `/api/hpc/performance` | ✅ |
| Sector Momentum | ✅ Completo | Mock + `/api/sectors` | 🔧 0JP: AlphaDroid |
| RPM Momentum | ✅ Completo | Mock + `/api/rpm` | 🔧 0JP: AlphaDroid |
| Alerts | ✅ Completo | Mock + `/api/alerts` | ✅ |
| Compounding Gap | ✅ Completo | Calculado no frontend | — |
| Performance | ✅ Completo | Mock | 🔧 0JP: AlphaDroid |
| Integrations | ✅ UI pronto | Demo | 🔧 0JP: Lynx |
| Settings / FO Profile | ✅ Completo | Mock + `/api/fo/profile` | ✅ |

---

## Integration Points para 0JP

### 1. 🔴 CRÍTICO — AlphaDroid API (HPC Performance + Regime Engine)

**O que é:** AlphaDroid é a engine que gera os dados de performance HPC11/HPC22 e o Market Regime Engine.

**Endpoints que precisam ser conectados:**

```python
# 0JP: Após cada run do AlphaDroid, POST os dados aqui:

# Regime Engine (diário)
POST /api/regime/snapshot
{
  "snapshot_date": "2026-04-29",
  "final_regime_score": 22,
  "macro_trend_score": 25,
  "market_structure_score": 18,
  "risk_shield_score": 32,
  "risk_state": "WATCH",
  "regime_label": "Cautious Bull",
  "stormguard_state": "watch",
  "score_decomposition_json": {...},
  "top_positive_json": [...],
  "top_negative_json": [...],
  "anomalies_json": [...],
  "correlations_json": {...},
  "market_internals_json": {...},
  "risk_shield_json": {...},
  "source": "alphaDroid"
}

# HPC Performance (mensal)
POST /api/hpc/performance
{
  "strategy": "HPC11",       # ou "HPC22"
  "period_date": "2026-04-01",
  "return_monthly": 1.24,
  "return_cumul": 1842.50,   # base 100 desde inception
  "drawdown": -3.2,
  "volatility": 8.1,
  "sharpe_ttm": 1.82,
  "stormguard_state": "watch",
  "source": "alphaDroid"
}
```

**Onde está no código:**
- `api/server.py` linhas `POST /api/regime/snapshot` e `POST /api/hpc/performance`
- `backend/harpian_db.py` funções `upsert_regime_snapshot()` e `upsert_hpc_performance()`
- `terminal.html` → `loadRegimeFromAPI()` já está implementado e atualiza o REGIME_ENGINE

---

### 2. 🔴 CRÍTICO — Lynx Execution API

**O que é:** Sistema de execução de ordens para alocação HPC11/HPC22.

**Fluxo atual (demo):**
1. Advisor clica "Confirmar Alocação" no Client Profile
2. Frontend chama `apiRequestAllocation()` → `POST /api/clients/:id/allocation`
3. API cria registro na tabela `allocations` com `status='pending'`
4. Lynx webhook (`POST /api/lynx/order`) está preparado mas em demo mode

**O que 0JP precisa implementar em `api/server.py`:**

```python
# Em api/server.py, função lynx_order():
# 1. Validar allocation_id no DB
# 2. Montar payload Lynx:
payload = {
    "client_id": body["client_id"],
    "strategy": "HPC11",
    "amount": body["volume_hpc11"],
    "type": "allocation",
    "reference": str(alloc_id),
}
# 3. POST para Lynx API:
resp = requests.post(
    f"{os.environ['LYNX_API_URL']}/v1/alloc",
    headers={"Authorization": f"Bearer {os.environ['LYNX_API_KEY']}"},
    json=payload
)
# 4. Update DB: allocations.status = 'sent', execution_ref = resp.json()["ref"]
# 5. Return { lynx_ref, status: "sent" }
```

**Variáveis de ambiente necessárias:** `LYNX_API_URL`, `LYNX_API_KEY`

---

### 3. 🟡 IMPORTANTE — Market Data (Bloomberg / Yahoo Finance)

**O que é:** Preços em tempo real para cotações, yields, etc.

**Onde integrar no terminal.html:**
- Topbar clock → adicionar cotações USD/BRL, S&P500, Gold
- Client Profile → preço de mercado dos ativos
- Dashboard KPIs → valores live

**Sugestão de implementação:**

```python
# Em api/server.py — adicionar endpoint:
@app.get("/api/market/quotes")
def market_quotes():
    # 0JP: integrar Yahoo Finance (yfinance) ou Bloomberg
    # import yfinance as yf
    # tickers = ["^GSPC","GLD","BRL=X","^VIX"]
    # data = yf.download(tickers, period="1d", interval="1m")
    pass  # retorna mock por agora
```

**Variáveis de ambiente:** `BLOOMBERG_API_KEY` (se usar Bloomberg)

---

### 4. 🟡 IMPORTANTE — Custodians (BTG / XP / Itaú Private)

**O que é:** Importação automática de posições dos custodiantes.

**Endpoints de destino:**
- `POST /api/clients/:id/portfolio` — recebe snapshot de posições
- `backend/harpian_db.py` → `insert_portfolio_snapshot()`

**O que 0JP precisa construir:**
- Script de sync com API do BTG Pactual: `backend/sync_btg.py`
- Script de sync com API da XP: `backend/sync_xp.py`
- Agendamento via Task Scheduler (similar ao run_social.ps1)

---

### 5. 🟢 NICE TO HAVE — Portfolio Upload Parser

**O que é:** Parse de CSV/Excel/PDF com posições.

**Onde:** `backend/portfolio_parser.py` (não existe ainda)

**Interface esperada:**
```python
def parse_portfolio_file(filepath: str) -> dict:
    """
    Input:  arquivo CSV/Excel/PDF com posições
    Output: {
        "client_id": "...",
        "positions": [{"ticker": "AAPL", "weight": 15.2, "country": "US", "currency": "USD"}],
        "risk_number": 72,  # se calculado
        "aum": 1800000,
    }
    """
```

**Upload endpoint já existe:** `POST /api/clients/:id/portfolio` (recebe o JSON)

---

## Database Schemas

### harpian.db (principal)

| Tabela | Descrição | Rows (mock) |
|--------|-----------|-------------|
| `clients` | Perfis dos clientes FO | 5 |
| `portfolios` | Snapshots diários | 5 |
| `allocations` | Histórico de alocações HPC | 0 |
| `regime_snapshots` | Regime Engine diário | 1 |
| `alerts` | Alertas gerados | 3 |
| `hpc_performance` | Performance mensal HPC11/HPC22 | 0 |
| `fo_profile` | Config institucional | 1 |

### harpian_social.db (JD NEWS)

| Tabela | Descrição |
|--------|-----------|
| `monitored_sources` | 50+ contas monitoradas (YouTube, Twitter, LinkedIn) |
| `social_feed` | Posts processados pelo Claude |

---

## Como Rodar Localmente

```powershell
# 1. Setup ambiente Python
cd C:\dev\harpian-prototype
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2. Configurar variáveis de ambiente
copy .env.example .env
# Editar .env com suas keys

# 3. Inicializar banco de dados
python backend/harpian_db.py init

# 4. Rodar API
python api/server.py
# API disponível em http://localhost:5050

# 5. Rodar frontend
npx serve -l 3131 .
# Frontend em http://localhost:3131/terminal.html

# OU: tudo em um comando:
.\start.ps1
```

---

## API Endpoints — Referência Rápida

| Method | Endpoint | Descrição | Status |
|--------|----------|-----------|--------|
| GET | `/api/health` | Status + DB stats | ✅ Live |
| GET | `/api/clients` | Lista todos os clientes | ✅ Live |
| GET | `/api/clients/:id` | Perfil completo do cliente | ✅ Live |
| POST | `/api/clients/:id/allocation` | Criar pedido de alocação | ✅ Live |
| GET | `/api/alerts` | Lista alertas ativos | ✅ Live |
| POST | `/api/alerts/:id/resolve` | Resolver alerta | ✅ Live |
| GET | `/api/regime/latest` | Regime Engine atual | ✅ Live |
| GET | `/api/regime/timeline` | Histórico de regime | ✅ Live |
| POST | `/api/regime/snapshot` | Push AlphaDroid → regime | 🔧 0JP |
| GET | `/api/hpc/performance` | Performance HPC11/HPC22 | ✅ Mock |
| POST | `/api/hpc/performance` | Push AlphaDroid → HPC | 🔧 0JP |
| GET | `/api/social/feed` | Feed social radar | ✅ Live |
| GET | `/api/news/latest` | Notícias JD NEWS | ✅ Live |
| POST | `/api/lynx/order` | Enviar ordem para Lynx | 🔧 0JP |
| GET | `/api/sectors` | Sector Momentum | ✅ Mock |
| GET | `/api/rpm` | RPM Engine | ✅ Mock |
| GET | `/api/fo/profile` | Perfil FO / settings | ✅ Live |
| PUT | `/api/fo/profile` | Atualizar settings | ✅ Live |

---

## Variáveis de Ambiente

Copiar `.env.example` → `.env` e preencher:

```env
# Anthropic (já usado pelo JD NEWS)
ANTHROPIC_API_KEY=sk-ant-...

# AlphaDroid (0JP: obter com a equipe HARPIAN)
ALPHADROID_API_URL=https://api.alphadroid.com/v4
ALPHADROID_API_KEY=...

# Lynx Execution
LYNX_API_URL=https://api.lynx.harpian.io/v1
LYNX_API_KEY=...

# Market Data (escolher um)
BLOOMBERG_API_KEY=...
# ou usar yfinance (gratuito, sem key)

# Custodians (opcional)
BTG_API_KEY=...
XP_API_KEY=...

# App config
PORT=5050
DEMO_MODE=true  # false em produção
SECRET_KEY=...  # para sessões Flask
```

---

## Próximos Passos Prioritários (para 0JP)

1. **[ ]** Conectar AlphaDroid → `POST /api/regime/snapshot` (diário, cron)
2. **[ ]** Conectar AlphaDroid → `POST /api/hpc/performance` (mensal)
3. **[ ]** Implementar Lynx em `api/server.py` → função `lynx_order()`
4. **[ ]** Parser de portfolio upload → `backend/portfolio_parser.py`
5. **[ ]** Sync com BTG/XP → `backend/sync_custodians.py`
6. **[ ]** Deploy na Vercel (API) + CDN (frontend)
7. **[ ]** Auth layer (JWT ou Supabase) — sem auth hoje
8. **[ ]** Market data live quotes no topbar

---

*Gerado em 2026-04-29 · HARPIAN Capital Advisors*
