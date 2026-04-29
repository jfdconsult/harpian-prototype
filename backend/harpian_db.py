#!/usr/bin/env python3
"""
harpian_db.py — HARPIAN Portfolio Engineering Terminal
Main database layer (SQLite) for all platform data.

Tables:
  clients              — Family Office client profiles + mandate
  portfolios           — Portfolio snapshot per client (positions, RN, AUM)
  allocations          — HPC allocation history per client
  regime_snapshots     — Daily Regime Engine output (for timeline)
  alerts               — Generated alerts (RN breach, DD, regime change)
  hpc_performance      — Monthly HPC11/HPC22 performance data
  fo_profile           — Family Office institutional profile / settings

Usage:
  python harpian_db.py init          # create tables + seed mock data
  python harpian_db.py stats         # print row counts
  python harpian_db.py seed          # seed mock data only
"""

import json
import sqlite3
from datetime import datetime, timezone, date
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH  = BASE_DIR / "data" / "harpian.db"

# ─────────────────────────────────────────────────────────────────────────────
#  SCHEMA
# ─────────────────────────────────────────────────────────────────────────────
SCHEMA = """
-- ── Family Office clients ──────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS clients (
    client_id           TEXT PRIMARY KEY,
    name                TEXT NOT NULL,
    type                TEXT DEFAULT 'individual',   -- individual | family | institution
    status              TEXT DEFAULT 'active',       -- active | watch | misaligned | inactive
    aum                 REAL DEFAULT 0,
    currency            TEXT DEFAULT 'BRL',
    risk_number_mandate_min INTEGER DEFAULT 30,
    risk_number_mandate_max INTEGER DEFAULT 70,
    risk_number_current INTEGER DEFAULT 50,
    max_drawdown_limit  REAL DEFAULT -20.0,          -- e.g. -20.0 = -20%
    return_target       TEXT DEFAULT 'CDI+6%',
    investment_horizon  TEXT DEFAULT '5-10 anos',
    profile             TEXT DEFAULT 'Moderado',     -- Conservador | Moderado | Arrojado | Sofisticado
    regulatory          TEXT DEFAULT 'CVM',
    advisor             TEXT DEFAULT 'HARPIAN',
    created_at          TEXT,
    updated_at          TEXT
);

-- ── Portfolio snapshots ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS portfolios (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id           TEXT NOT NULL REFERENCES clients(client_id),
    snapshot_date       TEXT NOT NULL,
    aum_snapshot        REAL DEFAULT 0,
    risk_number         INTEGER DEFAULT 50,
    return_ytd          REAL DEFAULT 0,
    volatility          REAL DEFAULT 0,
    max_drawdown        REAL DEFAULT 0,
    sharpe_ratio        REAL DEFAULT 0,
    hpc11_pct           REAL DEFAULT 0,
    hpc22_pct           REAL DEFAULT 0,
    other_pct           REAL DEFAULT 0,
    positions_json      TEXT,   -- JSON array of {ticker, weight, country, currency}
    notes               TEXT,
    created_at          TEXT
);
CREATE INDEX IF NOT EXISTS idx_port_client ON portfolios(client_id);
CREATE INDEX IF NOT EXISTS idx_port_date   ON portfolios(snapshot_date DESC);

-- ── HPC allocation requests ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS allocations (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id           TEXT NOT NULL REFERENCES clients(client_id),
    requested_at        TEXT NOT NULL,
    hpc11_pct           REAL DEFAULT 0,
    hpc22_pct           REAL DEFAULT 0,
    volume_hpc11        REAL DEFAULT 0,
    volume_hpc22        REAL DEFAULT 0,
    rn_before           INTEGER,
    rn_projected        INTEGER,
    status              TEXT DEFAULT 'pending',  -- pending | sent | executed | rejected
    execution_ref       TEXT,   -- Lynx order reference (filled by 0JP integration)
    notes               TEXT,
    created_at          TEXT,
    updated_at          TEXT
);
CREATE INDEX IF NOT EXISTS idx_alloc_client ON allocations(client_id);
CREATE INDEX IF NOT EXISTS idx_alloc_status ON allocations(status);

-- ── Regime Engine snapshots ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS regime_snapshots (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_date           TEXT NOT NULL UNIQUE,
    final_regime_score      REAL DEFAULT 0,
    macro_trend_score       REAL DEFAULT 0,
    market_structure_score  REAL DEFAULT 0,
    risk_shield_score       REAL DEFAULT 0,
    risk_state              TEXT DEFAULT 'WATCH',  -- OFF | WATCH | ACTIVATE | DEFENSIVE
    regime_label            TEXT DEFAULT 'Neutral',
    stormguard_state        TEXT DEFAULT 'watch',
    -- JSON blobs for rich data
    score_decomposition_json    TEXT,
    top_positive_json           TEXT,
    top_negative_json           TEXT,
    anomalies_json              TEXT,
    correlations_json           TEXT,
    market_internals_json       TEXT,
    risk_shield_json            TEXT,
    narrative_json              TEXT,
    source                  TEXT DEFAULT 'manual', -- manual | alphaDroid | bloomberg
    created_at              TEXT
);
CREATE INDEX IF NOT EXISTS idx_regime_date ON regime_snapshots(snapshot_date DESC);

-- ── Alerts ─────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS alerts (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    alert_type      TEXT NOT NULL,  -- rn_breach | dd_breach | regime_change | rebalance | custom
    severity        TEXT DEFAULT 'medium',  -- critical | high | medium | low | info
    client_id       TEXT REFERENCES clients(client_id),  -- NULL = system-wide
    title           TEXT NOT NULL,
    diagnosis       TEXT,
    impact          TEXT,
    action          TEXT,
    is_read         INTEGER DEFAULT 0,
    is_resolved     INTEGER DEFAULT 0,
    triggered_at    TEXT NOT NULL,
    resolved_at     TEXT,
    metadata_json   TEXT,   -- extra context
    created_at      TEXT
);
CREATE INDEX IF NOT EXISTS idx_alert_client   ON alerts(client_id);
CREATE INDEX IF NOT EXISTS idx_alert_type     ON alerts(alert_type);
CREATE INDEX IF NOT EXISTS idx_alert_severity ON alerts(severity);
CREATE INDEX IF NOT EXISTS idx_alert_unread   ON alerts(is_read, is_resolved);

-- ── HPC Monthly Performance ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS hpc_performance (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    strategy        TEXT NOT NULL,   -- HPC11 | HPC22
    period_date     TEXT NOT NULL,   -- YYYY-MM-01
    return_monthly  REAL DEFAULT 0,
    return_cumul    REAL DEFAULT 0,  -- cumulative from inception (base 100)
    drawdown        REAL DEFAULT 0,
    volatility      REAL DEFAULT 0,
    sharpe_ttm      REAL DEFAULT 0,
    benchmark_id    TEXT DEFAULT 'sp500',
    benchmark_return REAL DEFAULT 0,
    stormguard_state TEXT DEFAULT 'off',
    notes           TEXT,
    source          TEXT DEFAULT 'mock',  -- mock | alphaDroid | manual
    created_at      TEXT,
    UNIQUE(strategy, period_date)
);
CREATE INDEX IF NOT EXISTS idx_hpc_strategy ON hpc_performance(strategy);
CREATE INDEX IF NOT EXISTS idx_hpc_date     ON hpc_performance(period_date DESC);

-- ── Family Office Profile / Settings ───────────────────────────────────────
CREATE TABLE IF NOT EXISTS fo_profile (
    id              INTEGER PRIMARY KEY CHECK (id = 1),  -- singleton row
    firm_name       TEXT DEFAULT 'HARPIAN Capital',
    aum_total       REAL DEFAULT 0,
    clients_count   INTEGER DEFAULT 0,
    regulatory      TEXT DEFAULT 'CVM · ANBIMA',
    rn_max_global   INTEGER DEFAULT 70,
    dd_max_global   REAL DEFAULT -20.0,
    return_target   TEXT DEFAULT 'CDI+8%',
    -- Integration config (filled by 0JP)
    lynx_api_url    TEXT,
    lynx_api_key    TEXT,
    bloomberg_api_key TEXT,
    alphadroid_api_url TEXT,
    alphadroid_api_key TEXT,
    -- Feature flags
    demo_mode       INTEGER DEFAULT 1,  -- 1 = demo, 0 = live
    updated_at      TEXT
);
"""

# ─────────────────────────────────────────────────────────────────────────────
#  CONNECTION
# ─────────────────────────────────────────────────────────────────────────────
def get_conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def init_db():
    with get_conn() as conn:
        conn.executescript(SCHEMA)
    print(f"[DB] Initialized → {DB_PATH}")

# ─────────────────────────────────────────────────────────────────────────────
#  CLIENTS
# ─────────────────────────────────────────────────────────────────────────────
def upsert_client(c: dict):
    now = datetime.now(timezone.utc).isoformat()
    c.setdefault("created_at", now)
    c["updated_at"] = now
    cols = list(c.keys())
    sql = f"""
        INSERT INTO clients ({', '.join(cols)})
        VALUES ({', '.join(['?']*len(cols))})
        ON CONFLICT(client_id) DO UPDATE SET
        {', '.join(f"{k}=excluded.{k}" for k in cols if k != 'client_id')}
    """
    with get_conn() as conn:
        conn.execute(sql, list(c.values()))

def get_clients(status=None) -> list[dict]:
    sql = "SELECT * FROM clients"
    params = []
    if status:
        sql += " WHERE status=?"; params.append(status)
    sql += " ORDER BY aum DESC"
    with get_conn() as conn:
        return [dict(r) for r in conn.execute(sql, params).fetchall()]

def get_client(client_id: str) -> dict | None:
    with get_conn() as conn:
        r = conn.execute("SELECT * FROM clients WHERE client_id=?", [client_id]).fetchone()
        return dict(r) if r else None

# ─────────────────────────────────────────────────────────────────────────────
#  PORTFOLIOS
# ─────────────────────────────────────────────────────────────────────────────
def insert_portfolio_snapshot(p: dict):
    now = datetime.now(timezone.utc).isoformat()
    p.setdefault("snapshot_date", date.today().isoformat())
    p.setdefault("created_at", now)
    if isinstance(p.get("positions_json"), list):
        p["positions_json"] = json.dumps(p["positions_json"], ensure_ascii=False)
    cols = list(p.keys())
    sql = f"INSERT OR REPLACE INTO portfolios ({', '.join(cols)}) VALUES ({', '.join(['?']*len(cols))})"
    with get_conn() as conn:
        conn.execute(sql, list(p.values()))

def get_latest_portfolio(client_id: str) -> dict | None:
    with get_conn() as conn:
        r = conn.execute(
            "SELECT * FROM portfolios WHERE client_id=? ORDER BY snapshot_date DESC LIMIT 1",
            [client_id]
        ).fetchone()
        if not r:
            return None
        d = dict(r)
        if d.get("positions_json"):
            try: d["positions_json"] = json.loads(d["positions_json"])
            except: pass
        return d

# ─────────────────────────────────────────────────────────────────────────────
#  ALLOCATIONS
# ─────────────────────────────────────────────────────────────────────────────
def create_allocation_request(alloc: dict) -> int:
    now = datetime.now(timezone.utc).isoformat()
    alloc.setdefault("requested_at", now)
    alloc.setdefault("created_at", now)
    alloc["updated_at"] = now
    alloc.setdefault("status", "pending")
    cols = list(alloc.keys())
    sql = f"INSERT INTO allocations ({', '.join(cols)}) VALUES ({', '.join(['?']*len(cols))})"
    with get_conn() as conn:
        cur = conn.execute(sql, list(alloc.values()))
        return cur.lastrowid

def get_allocations(client_id: str = None, status: str = None) -> list[dict]:
    clauses, params = [], []
    if client_id: clauses.append("client_id=?"); params.append(client_id)
    if status:    clauses.append("status=?");    params.append(status)
    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    with get_conn() as conn:
        return [dict(r) for r in conn.execute(
            f"SELECT * FROM allocations {where} ORDER BY requested_at DESC",
            params
        ).fetchall()]

# ─────────────────────────────────────────────────────────────────────────────
#  REGIME SNAPSHOTS
# ─────────────────────────────────────────────────────────────────────────────
def upsert_regime_snapshot(snap: dict):
    now = datetime.now(timezone.utc).isoformat()
    snap.setdefault("snapshot_date", date.today().isoformat())
    snap.setdefault("created_at", now)
    # JSON-encode dict fields
    for field in ("score_decomposition_json","top_positive_json","top_negative_json",
                  "anomalies_json","correlations_json","market_internals_json",
                  "risk_shield_json","narrative_json"):
        if isinstance(snap.get(field), (dict, list)):
            snap[field] = json.dumps(snap[field], ensure_ascii=False)
    cols = list(snap.keys())
    sql = f"""
        INSERT INTO regime_snapshots ({', '.join(cols)})
        VALUES ({', '.join(['?']*len(cols))})
        ON CONFLICT(snapshot_date) DO UPDATE SET
        {', '.join(f"{k}=excluded.{k}" for k in cols if k != 'snapshot_date')}
    """
    with get_conn() as conn:
        conn.execute(sql, list(snap.values()))

def get_latest_regime() -> dict | None:
    with get_conn() as conn:
        r = conn.execute(
            "SELECT * FROM regime_snapshots ORDER BY snapshot_date DESC LIMIT 1"
        ).fetchone()
        if not r:
            return None
        d = dict(r)
        for field in ("score_decomposition_json","top_positive_json","top_negative_json",
                      "anomalies_json","correlations_json","market_internals_json",
                      "risk_shield_json","narrative_json"):
            if d.get(field):
                try: d[field] = json.loads(d[field])
                except: pass
        return d

def get_regime_timeline(days: int = 365 * 10) -> list[dict]:
    from datetime import timedelta
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).date().isoformat()
    with get_conn() as conn:
        return [dict(r) for r in conn.execute(
            "SELECT snapshot_date, final_regime_score, regime_label, stormguard_state "
            "FROM regime_snapshots WHERE snapshot_date >= ? ORDER BY snapshot_date ASC",
            [cutoff]
        ).fetchall()]

# ─────────────────────────────────────────────────────────────────────────────
#  ALERTS
# ─────────────────────────────────────────────────────────────────────────────
def insert_alert(alert: dict) -> int:
    now = datetime.now(timezone.utc).isoformat()
    alert.setdefault("triggered_at", now)
    alert.setdefault("created_at", now)
    if isinstance(alert.get("metadata_json"), dict):
        alert["metadata_json"] = json.dumps(alert["metadata_json"], ensure_ascii=False)
    cols = list(alert.keys())
    sql = f"INSERT INTO alerts ({', '.join(cols)}) VALUES ({', '.join(['?']*len(cols))})"
    with get_conn() as conn:
        cur = conn.execute(sql, list(alert.values()))
        return cur.lastrowid

def get_alerts(client_id=None, unread_only=False, limit=50) -> list[dict]:
    clauses, params = ["is_resolved=0"], []
    if client_id:    clauses.append("(client_id=? OR client_id IS NULL)"); params.append(client_id)
    if unread_only:  clauses.append("is_read=0")
    params.append(limit)
    with get_conn() as conn:
        rows = conn.execute(
            f"SELECT * FROM alerts WHERE {' AND '.join(clauses)} "
            f"ORDER BY triggered_at DESC LIMIT ?",
            params
        ).fetchall()
    result = []
    for r in rows:
        d = dict(r)
        if d.get("metadata_json"):
            try: d["metadata_json"] = json.loads(d["metadata_json"])
            except: pass
        result.append(d)
    return result

def mark_alert_read(alert_id: int):
    with get_conn() as conn:
        conn.execute("UPDATE alerts SET is_read=1 WHERE id=?", [alert_id])

def resolve_alert(alert_id: int):
    now = datetime.now(timezone.utc).isoformat()
    with get_conn() as conn:
        conn.execute("UPDATE alerts SET is_resolved=1, resolved_at=? WHERE id=?", [now, alert_id])

# ─────────────────────────────────────────────────────────────────────────────
#  HPC PERFORMANCE
# ─────────────────────────────────────────────────────────────────────────────
def upsert_hpc_performance(rec: dict):
    now = datetime.now(timezone.utc).isoformat()
    rec.setdefault("created_at", now)
    cols = list(rec.keys())
    sql = f"""
        INSERT INTO hpc_performance ({', '.join(cols)})
        VALUES ({', '.join(['?']*len(cols))})
        ON CONFLICT(strategy, period_date) DO UPDATE SET
        {', '.join(f"{k}=excluded.{k}" for k in cols if k not in ('strategy','period_date'))}
    """
    with get_conn() as conn:
        conn.execute(sql, list(rec.values()))

def get_hpc_performance(strategy: str = None, years: int = 20) -> list[dict]:
    from datetime import timedelta
    cutoff = (datetime.now(timezone.utc) - timedelta(days=years*365)).date().strftime("%Y-%m-01")
    clauses, params = ["period_date >= ?"], [cutoff]
    if strategy: clauses.append("strategy=?"); params.append(strategy)
    with get_conn() as conn:
        return [dict(r) for r in conn.execute(
            f"SELECT * FROM hpc_performance WHERE {' AND '.join(clauses)} ORDER BY strategy, period_date ASC",
            params
        ).fetchall()]

# ─────────────────────────────────────────────────────────────────────────────
#  FO PROFILE
# ─────────────────────────────────────────────────────────────────────────────
def get_fo_profile() -> dict:
    with get_conn() as conn:
        r = conn.execute("SELECT * FROM fo_profile WHERE id=1").fetchone()
        return dict(r) if r else {}

def upsert_fo_profile(data: dict):
    data["id"] = 1
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    cols = list(data.keys())
    sql = f"""
        INSERT INTO fo_profile ({', '.join(cols)})
        VALUES ({', '.join(['?']*len(cols))})
        ON CONFLICT(id) DO UPDATE SET
        {', '.join(f"{k}=excluded.{k}" for k in cols if k != 'id')}
    """
    with get_conn() as conn:
        conn.execute(sql, list(data.values()))

# ─────────────────────────────────────────────────────────────────────────────
#  SEED — Mock data (mirrors terminal.html CLIENTS + data objects)
# ─────────────────────────────────────────────────────────────────────────────
def seed_mock_data():
    """Seed all tables with mock data mirroring the frontend JS constants."""
    now = datetime.now(timezone.utc).isoformat()
    today = date.today().isoformat()

    # ── FO Profile ──
    upsert_fo_profile({
        "firm_name": "HARPIAN Capital",
        "aum_total": 25400000,
        "clients_count": 12,
        "regulatory": "CVM · ANBIMA",
        "rn_max_global": 70,
        "dd_max_global": -20.0,
        "return_target": "CDI+8%",
        "demo_mode": 1,
    })
    print("  [SEED] FO Profile")

    # ── Clients ──
    clients = [
        {"client_id":"hollanda",  "name":"Vera Hollanda",      "type":"individual",  "status":"misaligned", "aum":890000,   "risk_number_mandate_min":45, "risk_number_mandate_max":62, "risk_number_current":78, "max_drawdown_limit":-20.0, "return_target":"CDI+8%",  "profile":"Arrojado"},
        {"client_id":"monteiro",  "name":"Família Monteiro",   "type":"family",      "status":"aligned",    "aum":4200000,  "risk_number_mandate_min":60, "risk_number_mandate_max":70, "risk_number_current":67, "max_drawdown_limit":-18.0, "return_target":"CDI+12%", "profile":"Sofisticado"},
        {"client_id":"viana",     "name":"Dr. Carlos Viana",   "type":"individual",  "status":"aligned",    "aum":1800000,  "risk_number_mandate_min":45, "risk_number_mandate_max":55, "risk_number_current":52, "max_drawdown_limit":-15.0, "return_target":"CDI+8%",  "profile":"Moderado"},
        {"client_id":"silveira",  "name":"Grupo Silveira FO",  "type":"institution", "status":"watch",      "aum":12100000, "risk_number_mandate_min":35, "risk_number_mandate_max":45, "risk_number_current":50, "max_drawdown_limit":-15.0, "return_target":"CDI+6%",  "profile":"Conservador"},
        {"client_id":"cavalcante","name":"Instituto Cavalcante","type":"institution","status":"aligned",    "aum":6400000,  "risk_number_mandate_min":30, "risk_number_mandate_max":40, "risk_number_current":38, "max_drawdown_limit":-12.0, "return_target":"CDI+5%",  "profile":"Conservador"},
    ]
    for c in clients:
        upsert_client(c)
    print(f"  [SEED] {len(clients)} clients")

    # ── Portfolio snapshots ──
    portfolios = [
        {"client_id":"hollanda",  "snapshot_date":today, "aum_snapshot":890000,   "risk_number":78, "return_ytd":-4.2, "volatility":19.4, "max_drawdown":-22.1, "sharpe_ratio":0.31, "hpc11_pct":0,  "hpc22_pct":0,   "other_pct":100},
        {"client_id":"monteiro",  "snapshot_date":today, "aum_snapshot":4200000,  "risk_number":67, "return_ytd":22.4, "volatility":11.8, "max_drawdown":-9.2,  "sharpe_ratio":1.94, "hpc11_pct":0,  "hpc22_pct":100, "other_pct":0},
        {"client_id":"viana",     "snapshot_date":today, "aum_snapshot":1800000,  "risk_number":52, "return_ytd":14.1, "volatility":8.3,  "max_drawdown":-6.8,  "sharpe_ratio":1.76, "hpc11_pct":80, "hpc22_pct":20,  "other_pct":0},
        {"client_id":"silveira",  "snapshot_date":today, "aum_snapshot":12100000, "risk_number":50, "return_ytd":9.8,  "volatility":7.1,  "max_drawdown":-12.4, "sharpe_ratio":1.28, "hpc11_pct":50, "hpc22_pct":0,   "other_pct":50},
        {"client_id":"cavalcante","snapshot_date":today, "aum_snapshot":6400000,  "risk_number":38, "return_ytd":11.2, "volatility":6.9,  "max_drawdown":-5.8,  "sharpe_ratio":1.64, "hpc11_pct":100,"hpc22_pct":0,   "other_pct":0},
    ]
    for p in portfolios:
        insert_portfolio_snapshot(p)
    print(f"  [SEED] {len(portfolios)} portfolio snapshots")

    # ── Alerts ──
    alerts = [
        {"alert_type":"rn_breach",    "severity":"critical","client_id":"hollanda", "title":"Vera Hollanda — RN Fora do Mandato",       "diagnosis":"RN 78 vs mandato 62. Desvio +16 pontos. Exposição crítica.","impact":"DD potencial -22.1% em evento como 2022. R$143K de risco extra.","action":"Migrar 35% HPC11 + 30% HPC22. Reduz RN→58. Alinha ao mandato.",       "triggered_at":"2026-04-29T08:14:00Z","is_read":0,"is_resolved":0},
        {"alert_type":"dd_breach",    "severity":"high",    "client_id":"silveira", "title":"Grupo Silveira — DD Próximo do Limite",    "diagnosis":"DD -12.4% vs limite -15%. Deterioração 0.4%/semana.",          "impact":"Limite violado em ~3 semanas se tendência continuar.",               "action":"Trailing stop parcial + hedge cambial + migração HPC11.",             "triggered_at":"2026-04-28T16:30:00Z","is_read":0,"is_resolved":0},
        {"alert_type":"regime_change","severity":"info",    "client_id":None,       "title":"Market Trends — WATCH Ativado",           "diagnosis":"Market Trend +22. VIX cruzou 22. StormGuard WATCH preventivo.", "impact":"RN > 55: R$5.1M em exposição aumentada.",                          "action":"HPC11/HPC22 têm proteção StormGuard integrada.",                     "triggered_at":"2026-04-27T11:22:00Z","is_read":0,"is_resolved":0},
    ]
    for a in alerts:
        insert_alert(a)
    print(f"  [SEED] {len(alerts)} alerts")

    # ── Regime snapshot (today) ──
    upsert_regime_snapshot({
        "snapshot_date": today,
        "final_regime_score": 22,
        "macro_trend_score": 25,
        "market_structure_score": 18,
        "risk_shield_score": 32,
        "risk_state": "WATCH",
        "regime_label": "Cautious Bull",
        "stormguard_state": "watch",
        "score_decomposition_json": {"macro_contribution":15.0,"structure_contribution":7.2,"risk_adjustment":-0.2,"final":22},
        "top_positive_json": [
            {"name":"Credit Normalization","score":8.4,"category":"credit"},
            {"name":"Earnings Beat Rate 68%","score":6.2,"category":"equities"},
            {"name":"Gold Safe Haven Bid","score":4.8,"category":"commodities"},
        ],
        "top_negative_json": [
            {"name":"Fed Hawkish Bias","score":-7.1,"category":"monetary"},
            {"name":"Yield Curve Inversion","score":-5.8,"category":"rates"},
            {"name":"VIX Elevation (22.4)","score":-4.6,"category":"volatility"},
        ],
        "anomalies_json": [
            {"severity":"medium","label":"Correlation Spike","type":"CORR","desc":"Equity-Bond correlation turned positive (+0.42)","ts":"09:14"},
            {"severity":"low","label":"Volatility Regime Shift","type":"VOL","desc":"VIX term structure flattening","ts":"11:02"},
        ],
        "correlations_json": {"equity_bonds":0.42,"equity_gold":-0.18,"equity_usd":-0.31,"diversification_idx":0.61},
        "market_internals_json": {"pct_above_ma50":54,"pct_above_ma200":61,"momentum_dispersion":0.38,"overextension_zscore":1.2,"volume_confirmation":"Neutral"},
        "risk_shield_json": {"volatility_spike":42,"correlation_spike":58,"credit_stress":24,"liquidity_stress":18,"tail_risk":31,"composite":32},
        "source": "manual",
    })
    print("  [SEED] Regime snapshot")

    print(f"[DB] Mock data seeded → {DB_PATH}")


# ─────────────────────────────────────────────────────────────────────────────
#  STATS
# ─────────────────────────────────────────────────────────────────────────────
def get_stats() -> dict:
    tables = ["clients","portfolios","allocations","regime_snapshots","alerts","hpc_performance"]
    with get_conn() as conn:
        return {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in tables}


# ─────────────────────────────────────────────────────────────────────────────
#  CLI
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "init"

    if cmd == "init":
        init_db()
        seed_mock_data()
    elif cmd == "seed":
        init_db()
        seed_mock_data()
    elif cmd == "stats":
        init_db()
        stats = get_stats()
        for t, n in stats.items():
            print(f"  {t:<25} {n} rows")
    else:
        print("Usage: python harpian_db.py [init | seed | stats]")
