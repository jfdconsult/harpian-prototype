#!/usr/bin/env python3
"""
api/server.py — HARPIAN Portfolio Engineering Terminal
Flask REST API — serves all data to the terminal frontend.

Endpoints:
  GET  /api/health
  GET  /api/clients
  GET  /api/clients/<id>
  GET  /api/clients/<id>/portfolio
  POST /api/clients/<id>/allocation
  GET  /api/alerts
  POST /api/alerts/<id>/read
  POST /api/alerts/<id>/resolve
  GET  /api/regime/latest
  GET  /api/regime/timeline
  GET  /api/hpc/performance
  GET  /api/social/feed
  GET  /api/social/stats
  GET  /api/news/latest
  GET  /api/fo/profile
  PUT  /api/fo/profile
  POST /api/regime/snapshot    (0JP: AlphaDroid pushes here)
  POST /api/lynx/order         (0JP: Lynx execution webhook)

All endpoints fall back to mock data if DB is empty.
CORS enabled for local dev (terminal.html served via npx serve).

Run:
  pip install flask flask-cors
  python api/server.py
  # or with gunicorn:
  # gunicorn -w 2 -b 0.0.0.0:5050 "api.server:create_app()"
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS

# ── path setup ───────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "backend"))

import harpian_db as db

# Social DB (JD NEWS pipeline)
SOCIAL_DB_PATH = ROOT / "data" / "harpian_social.db"
try:
    sys.path.insert(0, str(ROOT.parent / "JD NEWS"))   # dev path
    import social_db
    HAS_SOCIAL_DB = True
except ImportError:
    HAS_SOCIAL_DB = False

# ─────────────────────────────────────────────────────────────────────────────
#  APP FACTORY
# ─────────────────────────────────────────────────────────────────────────────
def create_app():
    app = Flask(__name__)
    CORS(app, origins=["http://localhost:3131", "http://127.0.0.1:3131",
                        "https://*.vercel.app", "https://harpian.io"])

    # Init DB on startup
    db.init_db()

    # ── helpers ──────────────────────────────────────────────────────────────
    def _ok(data, **kwargs):
        return jsonify({"ok": True, "data": data, **kwargs})

    def _err(msg, code=400):
        return jsonify({"ok": False, "error": msg}), code

    def _now():
        return datetime.now(timezone.utc).isoformat()

    # ─────────────────────────────────────────────────────────────────────────
    #  HEALTH
    # ─────────────────────────────────────────────────────────────────────────
    @app.get("/api/health")
    def health():
        stats = db.get_stats()
        return _ok({
            "status": "ok",
            "version": "1.0.0",
            "db_stats": stats,
            "social_db": HAS_SOCIAL_DB,
            "demo_mode": True,
            "ts": _now(),
        })

    # ─────────────────────────────────────────────────────────────────────────
    #  CLIENTS
    # ─────────────────────────────────────────────────────────────────────────
    @app.get("/api/clients")
    def list_clients():
        status = request.args.get("status")
        clients = db.get_clients(status=status)
        if not clients:
            clients = _mock_clients()
        # Enrich each client with latest portfolio snapshot
        enriched = []
        for c in clients:
            port = db.get_latest_portfolio(c["client_id"])
            c["portfolio"] = port
            enriched.append(c)
        return _ok(enriched, total=len(enriched))

    @app.get("/api/clients/<client_id>")
    def get_client(client_id):
        c = db.get_client(client_id)
        if not c:
            mock = {m["client_id"]: m for m in _mock_clients()}
            c = mock.get(client_id)
        if not c:
            return _err("Client not found", 404)
        c["portfolio"] = db.get_latest_portfolio(client_id)
        c["alerts"]    = db.get_alerts(client_id=client_id)
        return _ok(c)

    @app.get("/api/clients/<client_id>/portfolio")
    def get_client_portfolio(client_id):
        port = db.get_latest_portfolio(client_id)
        if not port:
            return _err("No portfolio found", 404)
        return _ok(port)

    # ─────────────────────────────────────────────────────────────────────────
    #  ALLOCATIONS
    # ─────────────────────────────────────────────────────────────────────────
    @app.post("/api/clients/<client_id>/allocation")
    def create_allocation(client_id):
        """
        Body: { hpc11_pct, hpc22_pct, rn_before, rn_projected, notes }
        Returns: allocation request ID + status
        0JP: hook this into Lynx execution API
        """
        body = request.get_json() or {}
        c = db.get_client(client_id)
        if not c:
            return _err("Client not found", 404)

        aum = c.get("aum", 0)
        alloc = {
            "client_id":   client_id,
            "hpc11_pct":   float(body.get("hpc11_pct", 0)),
            "hpc22_pct":   float(body.get("hpc22_pct", 0)),
            "volume_hpc11": aum * float(body.get("hpc11_pct", 0)) / 100,
            "volume_hpc22": aum * float(body.get("hpc22_pct", 0)) / 100,
            "rn_before":   body.get("rn_before"),
            "rn_projected": body.get("rn_projected"),
            "notes":       body.get("notes", ""),
            "status":      "pending",
        }
        alloc_id = db.create_allocation_request(alloc)
        return _ok({
            "allocation_id": alloc_id,
            "status": "pending",
            "message": "Allocation request created. Awaiting HARPIAN review.",
            # 0JP: POST this to Lynx API:
            # POST https://api.lynx.harpian.io/v1/alloc
            # { client_id, hpc11_pct, hpc22_pct, volume_hpc11, volume_hpc22 }
        }), 201

    @app.get("/api/clients/<client_id>/allocations")
    def get_client_allocations(client_id):
        allocs = db.get_allocations(client_id=client_id)
        return _ok(allocs)

    # ─────────────────────────────────────────────────────────────────────────
    #  ALERTS
    # ─────────────────────────────────────────────────────────────────────────
    @app.get("/api/alerts")
    def list_alerts():
        client_id   = request.args.get("client_id")
        unread_only = request.args.get("unread") == "1"
        limit       = int(request.args.get("limit", 50))
        alerts = db.get_alerts(client_id=client_id, unread_only=unread_only, limit=limit)
        if not alerts:
            alerts = _mock_alerts()
        return _ok(alerts, total=len(alerts))

    @app.post("/api/alerts/<int:alert_id>/read")
    def mark_read(alert_id):
        db.mark_alert_read(alert_id)
        return _ok({"alert_id": alert_id, "is_read": True})

    @app.post("/api/alerts/<int:alert_id>/resolve")
    def resolve_alert(alert_id):
        db.resolve_alert(alert_id)
        return _ok({"alert_id": alert_id, "is_resolved": True})

    # ─────────────────────────────────────────────────────────────────────────
    #  REGIME ENGINE
    # ─────────────────────────────────────────────────────────────────────────
    @app.get("/api/regime/latest")
    def regime_latest():
        snap = db.get_latest_regime()
        if not snap:
            snap = _mock_regime()
        return _ok(snap)

    @app.get("/api/regime/timeline")
    def regime_timeline():
        days = int(request.args.get("days", 3650))
        timeline = db.get_regime_timeline(days=days)
        if not timeline:
            timeline = _mock_regime_timeline()
        return _ok(timeline)

    @app.post("/api/regime/snapshot")
    def push_regime_snapshot():
        """
        0JP: AlphaDroid pushes daily regime data here.
        Body: full regime snapshot dict (see harpian_db schema)
        """
        body = request.get_json() or {}
        if not body:
            return _err("Empty body")
        db.upsert_regime_snapshot(body)
        return _ok({"message": "Regime snapshot saved", "date": body.get("snapshot_date")}), 201

    # ─────────────────────────────────────────────────────────────────────────
    #  HPC PERFORMANCE
    # ─────────────────────────────────────────────────────────────────────────
    @app.get("/api/hpc/performance")
    def hpc_performance():
        strategy = request.args.get("strategy")    # HPC11 | HPC22 | None=both
        years    = int(request.args.get("years", 20))
        data = db.get_hpc_performance(strategy=strategy, years=years)
        if not data:
            data = _mock_hpc_performance(strategy=strategy)
        return _ok(data)

    @app.post("/api/hpc/performance")
    def push_hpc_performance():
        """
        0JP: AlphaDroid pushes monthly HPC performance here.
        Body: { strategy, period_date, return_monthly, return_cumul, drawdown, ... }
        """
        body = request.get_json() or {}
        if not body.get("strategy") or not body.get("period_date"):
            return _err("strategy and period_date required")
        db.upsert_hpc_performance(body)
        return _ok({"message": "HPC performance saved"}), 201

    # ─────────────────────────────────────────────────────────────────────────
    #  SOCIAL MEDIA FEED
    # ─────────────────────────────────────────────────────────────────────────
    @app.get("/api/social/feed")
    def social_feed():
        platform   = request.args.get("platform")
        impact     = request.args.get("impact")
        hours      = int(request.args.get("hours", 48))
        limit      = int(request.args.get("limit", 100))
        sentiment  = request.args.get("sentiment")
        category   = request.args.get("category")

        if HAS_SOCIAL_DB:
            try:
                posts = social_db.get_feed(
                    platform=platform, market_impact=impact,
                    hours=hours, limit=limit
                )
                if sentiment:
                    posts = [p for p in posts if p.get("sentiment") == sentiment]
                if category:
                    posts = [p for p in posts if p.get("account_category") == category]
                if posts:
                    return _ok(posts, total=len(posts), source="live")
            except Exception as e:
                print(f"[SOCIAL] DB error: {e}")

        # Fallback to mock
        posts = _mock_social_posts()
        if platform and platform != "all":
            posts = [p for p in posts if p.get("platform") == platform]
        if impact and impact != "all":
            posts = [p for p in posts if p.get("market_impact") == impact]
        if sentiment and sentiment != "all":
            posts = [p for p in posts if p.get("sentiment") == sentiment]
        return _ok(posts[:limit], total=len(posts), source="mock")

    @app.get("/api/social/stats")
    def social_stats():
        if HAS_SOCIAL_DB:
            try:
                return _ok(social_db.get_feed_stats(), source="live")
            except Exception:
                pass
        return _ok({"total": 247, "today": 31, "by_impact": {"High": 8, "Medium": 14, "Low": 9}, "source": "mock"})

    # ─────────────────────────────────────────────────────────────────────────
    #  NEWS
    # ─────────────────────────────────────────────────────────────────────────
    @app.get("/api/news/latest")
    def news_latest():
        """Serve the latest curated articles from JD NEWS pipeline."""
        limit = int(request.args.get("limit", 8))
        data_dir = ROOT.parent / "JD NEWS" / "data"   # dev path
        if not data_dir.exists():
            data_dir = ROOT / "data"

        # Try today's file, then walk back up to 3 days
        from datetime import date, timedelta
        for delta in range(4):
            d = (date.today() - timedelta(days=delta)).strftime("%d%m%Y")
            f = data_dir / f"articles_{d}.json"
            if f.exists():
                try:
                    with open(f, "r", encoding="utf-8") as fp:
                        articles = json.load(fp)
                    return _ok(articles[:limit], source="live", file=f.name)
                except Exception:
                    pass

        # Fallback mock
        return _ok(_mock_news()[:limit], source="mock")

    # ─────────────────────────────────────────────────────────────────────────
    #  FO PROFILE
    # ─────────────────────────────────────────────────────────────────────────
    @app.get("/api/fo/profile")
    def fo_profile():
        profile = db.get_fo_profile()
        if not profile:
            profile = {"firm_name": "HARPIAN Capital", "aum_total": 25400000,
                       "clients_count": 12, "demo_mode": 1}
        return _ok(profile)

    @app.put("/api/fo/profile")
    def update_fo_profile():
        body = request.get_json() or {}
        # Strip protected fields
        for key in ("id", "lynx_api_key", "bloomberg_api_key", "alphadroid_api_key"):
            body.pop(key, None)
        db.upsert_fo_profile(body)
        return _ok({"message": "Profile updated"})

    # ─────────────────────────────────────────────────────────────────────────
    #  LYNX EXECUTION WEBHOOK (0JP fills this in)
    # ─────────────────────────────────────────────────────────────────────────
    @app.post("/api/lynx/order")
    def lynx_order():
        """
        0JP INTEGRATION POINT
        ─────────────────────
        This endpoint receives allocation requests and should forward them
        to the Lynx execution API.

        Expected body:
          { client_id, hpc11_pct, hpc22_pct, volume_hpc11, volume_hpc22,
            allocation_id, notes }

        What 0JP needs to implement:
          1. Validate the allocation_id exists in DB
          2. POST to https://api.lynx.harpian.io/v1/alloc
          3. Update allocations.status = 'sent' + store execution_ref
          4. Return { ok: true, lynx_ref: "...", status: "sent" }

        For now: returns demo response.
        """
        body = request.get_json() or {}
        profile = db.get_fo_profile()
        demo = profile.get("demo_mode", 1)

        if demo:
            return _ok({
                "lynx_ref": f"DEMO-{body.get('client_id','?').upper()}-{_now()[:10]}",
                "status": "demo_sent",
                "message": "Demo mode — no real order executed. 0JP: integrate Lynx API here.",
                "payload_echo": body,
            })

        # 0JP: real implementation goes here
        return _err("Lynx integration not yet configured. Set demo_mode=0 and configure lynx_api_url.", 503)

    # ─────────────────────────────────────────────────────────────────────────
    #  SECTORS / MOMENTUM (static data — 0JP: replace with AlphaDroid feed)
    # ─────────────────────────────────────────────────────────────────────────
    @app.get("/api/sectors")
    def sectors():
        """
        0JP INTEGRATION POINT
        Replace static data with AlphaDroid sector momentum endpoint.
        """
        return _ok(_mock_sectors(), source="mock")

    @app.get("/api/rpm")
    def rpm():
        """
        0JP INTEGRATION POINT
        Replace with AlphaDroid RPM feed.
        """
        return _ok(_mock_rpm(), source="mock")

    return app


# ─────────────────────────────────────────────────────────────────────────────
#  MOCK DATA HELPERS (mirrors terminal.html JS constants exactly)
# ─────────────────────────────────────────────────────────────────────────────
def _mock_clients():
    return [
        {"client_id":"hollanda",  "name":"Vera Hollanda",      "type":"individual",  "status":"misaligned", "aum":890000,   "risk_number_mandate_min":45,"risk_number_mandate_max":62,"risk_number_current":78, "max_drawdown_limit":-20.0,"return_target":"CDI+8%",  "profile":"Arrojado"},
        {"client_id":"monteiro",  "name":"Família Monteiro",   "type":"family",      "status":"aligned",    "aum":4200000,  "risk_number_mandate_min":60,"risk_number_mandate_max":70,"risk_number_current":67, "max_drawdown_limit":-18.0,"return_target":"CDI+12%", "profile":"Sofisticado"},
        {"client_id":"viana",     "name":"Dr. Carlos Viana",   "type":"individual",  "status":"aligned",    "aum":1800000,  "risk_number_mandate_min":45,"risk_number_mandate_max":55,"risk_number_current":52, "max_drawdown_limit":-15.0,"return_target":"CDI+8%",  "profile":"Moderado"},
        {"client_id":"silveira",  "name":"Grupo Silveira FO",  "type":"institution", "status":"watch",      "aum":12100000, "risk_number_mandate_min":35,"risk_number_mandate_max":45,"risk_number_current":50, "max_drawdown_limit":-15.0,"return_target":"CDI+6%",  "profile":"Conservador"},
        {"client_id":"cavalcante","name":"Instituto Cavalcante","type":"institution","status":"aligned",    "aum":6400000,  "risk_number_mandate_min":30,"risk_number_mandate_max":40,"risk_number_current":38, "max_drawdown_limit":-12.0,"return_target":"CDI+5%",  "profile":"Conservador"},
    ]

def _mock_alerts():
    return [
        {"id":1,"alert_type":"rn_breach","severity":"critical","client_id":"hollanda","title":"Vera Hollanda — RN Fora do Mandato","diagnosis":"RN 78 vs mandato 62. Desvio +16 pontos.","impact":"DD potencial -22.1% em evento como 2022. R$143K de risco extra.","action":"Migrar 35% HPC11 + 30% HPC22. Reduz RN→58.","triggered_at":"2026-04-29T08:14:00Z","is_read":0,"is_resolved":0},
        {"id":2,"alert_type":"dd_breach","severity":"high","client_id":"silveira","title":"Grupo Silveira — DD Próximo do Limite","diagnosis":"DD -12.4% vs limite -15%.","impact":"Limite violado em ~3 semanas.","action":"Trailing stop parcial + hedge cambial.","triggered_at":"2026-04-28T16:30:00Z","is_read":0,"is_resolved":0},
        {"id":3,"alert_type":"regime_change","severity":"info","client_id":None,"title":"Market Trends — WATCH Ativado","diagnosis":"VIX cruzou 22. StormGuard WATCH preventivo.","impact":"R$5.1M em exposição aumentada.","action":"HPC11/HPC22 têm proteção StormGuard.","triggered_at":"2026-04-27T11:22:00Z","is_read":0,"is_resolved":0},
    ]

def _mock_regime():
    return {
        "snapshot_date": "2026-04-29",
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
        "correlations_json": {"equity_bonds":0.42,"equity_gold":-0.18,"equity_usd":-0.31,"diversification_idx":0.61},
        "market_internals_json": {"pct_above_ma50":54,"pct_above_ma200":61,"momentum_dispersion":0.38,"overextension_zscore":1.2,"volume_confirmation":"Neutral"},
        "risk_shield_json": {"volatility_spike":42,"correlation_spike":58,"credit_stress":24,"liquidity_stress":18,"tail_risk":31,"composite":32},
        "source": "mock",
    }

def _mock_regime_timeline():
    # Sparse monthly data 2006-2026 for 20Y display
    import random
    random.seed(42)
    entries = []
    score = 0.0
    from datetime import date, timedelta
    d = date(2006, 1, 1)
    end = date(2026, 4, 1)
    while d <= end:
        score = max(-80, min(80, score + random.gauss(0, 8)))
        entries.append({
            "snapshot_date": d.isoformat(),
            "final_regime_score": round(score, 1),
            "regime_label": "Mock",
            "stormguard_state": "activate" if score < -30 else ("watch" if score < 0 else "off"),
        })
        # advance ~monthly
        d = date(d.year + (1 if d.month == 12 else 0), (d.month % 12) + 1, 1)
    return entries

def _mock_hpc_performance(strategy=None):
    import random
    random.seed(7)
    results = []
    from datetime import date
    strategies = ["HPC11","HPC22"] if not strategy else [strategy]
    for strat in strategies:
        cumul = 100.0
        drift = 0.008 if strat == "HPC22" else 0.006
        vol   = 0.04  if strat == "HPC22" else 0.025
        d = date(2006, 1, 1)
        end = date(2026, 4, 1)
        while d <= end:
            monthly = random.gauss(drift, vol)
            cumul *= (1 + monthly)
            results.append({
                "strategy": strat,
                "period_date": d.isoformat(),
                "return_monthly": round(monthly * 100, 2),
                "return_cumul": round(cumul, 2),
                "drawdown": round(random.gauss(-2, 3), 2),
                "source": "mock",
            })
            d = date(d.year + (1 if d.month == 12 else 0), (d.month % 12) + 1, 1)
    return results

def _mock_social_posts():
    return [
        {"id":1,"platform":"twitter","account_name":"Jerome Powell","account_category":"central_bank","raw_text":"The Federal Reserve remains committed to returning inflation to our 2% goal. We will maintain restrictive policy as long as appropriate.","headline_summary":"Fed Chair Powell reaffirms commitment to 2% inflation target; restrictive stance to continue","tags":["Fed Policy","Inflation","Interest Rates"],"asset_tags":["FED","USD","UST"],"sentiment":"Bearish","relevance_score":0.95,"market_impact":"Market Moving","timestamp_published":"2026-04-29T09:14:00Z"},
        {"id":2,"platform":"twitter","account_name":"Elon Musk","account_category":"tech_ai","raw_text":"Tesla Q1 deliveries beat expectations. Full self-driving making incredible progress. Robotaxi launch on track.","headline_summary":"Musk: Tesla Q1 deliveries beat; FSD progress strong, Robotaxi on track","tags":["Tesla","EV","Technology"],"asset_tags":["TSLA","NVDA"],"sentiment":"Bullish","relevance_score":0.82,"market_impact":"High","timestamp_published":"2026-04-29T08:55:00Z"},
        {"id":3,"platform":"youtube","account_name":"Ray Dalio","account_category":"macro_investor","raw_text":"The debt cycle is at a critical inflection point. Cash is no longer trash — it's a legitimate asset class in this environment. Gold remains the best long-term hedge.","headline_summary":"Dalio: Debt cycle at inflection; cash now legitimate, gold best long-term hedge","tags":["Macro","Debt Cycle","Gold","Cash"],"asset_tags":["XAU","USD","DXY"],"sentiment":"Bearish","relevance_score":0.91,"market_impact":"High","timestamp_published":"2026-04-29T07:30:00Z"},
        {"id":4,"platform":"twitter","account_name":"Stanley Druckenmiller","account_category":"macro_investor","raw_text":"I've never seen the Fed in a more difficult position. Inflation sticky, growth slowing. This doesn't end well for bonds.","headline_summary":"Druckenmiller: Fed in unprecedented difficulty; bonds at risk as inflation stays sticky","tags":["Fed Policy","Bonds","Macro"],"asset_tags":["FED","UST","USD"],"sentiment":"Bearish","relevance_score":0.88,"market_impact":"High","timestamp_published":"2026-04-29T06:45:00Z"},
        {"id":5,"platform":"twitter","account_name":"Cathie Wood","account_category":"asset_manager","raw_text":"AI is the most transformative technology since the internet. ARK's 5-year price target for NVDA: $1,400. The innovation wave is just beginning.","headline_summary":"Wood raises NVDA 5Y target to $1,400; calls AI most transformative tech since internet","tags":["AI","Technology","Innovation"],"asset_tags":["NVDA","AAPL","MSFT"],"sentiment":"Bullish","relevance_score":0.74,"market_impact":"Medium","timestamp_published":"2026-04-28T22:10:00Z"},
        {"id":6,"platform":"linkedin","account_name":"Larry Fink — BlackRock","account_category":"asset_manager","raw_text":"Infrastructure is the new fixed income. In a world of higher-for-longer rates, real assets provide the yield and stability that traditional bonds once offered.","headline_summary":"Fink: Infrastructure replacing fixed income as core allocation in higher-rate world","tags":["Infrastructure","Fixed Income","Asset Allocation"],"asset_tags":["BLK","UST"],"sentiment":"Neutral","relevance_score":0.79,"market_impact":"Medium","timestamp_published":"2026-04-28T18:00:00Z"},
        {"id":7,"platform":"truth_social","account_name":"Donald Trump","account_category":"political","raw_text":"Tariffs on Chinese goods will stay at 145% until a fair deal is reached. America First means American workers first. The trade war is over when China plays fair.","headline_summary":"Trump: 145% China tariffs permanent until fair deal; no timeline for resolution","tags":["Trade War","Tariffs","China","Geopolitics"],"asset_tags":["CN","CNY","SPX","AMZN"],"sentiment":"Bearish","relevance_score":0.93,"market_impact":"Market Moving","timestamp_published":"2026-04-28T15:30:00Z"},
        {"id":8,"platform":"youtube","account_name":"Michael Saylor","account_category":"crypto","raw_text":"Bitcoin is digital energy. Every corporation that doesn't hold Bitcoin on their balance sheet is leaving value on the table. Target: $1M per BTC by 2030.","headline_summary":"Saylor: Bitcoin = digital energy; $1M/BTC target by 2030, corporate adoption urgent","tags":["Bitcoin","Crypto","Corporate Treasury"],"asset_tags":["BTC","CRYPTO"],"sentiment":"Bullish","relevance_score":0.68,"market_impact":"Medium","timestamp_published":"2026-04-28T12:00:00Z"},
    ]

def _mock_news():
    return [
        {"title":"Fed mantém juros; sem corte previsto para 2026","source":"Reuters","time":"10:14","tag":"r","tagLbl":"Macro","summary":"FOMC votou por unanimidade para manter fed funds em 4.25%-4.5%."},
        {"title":"Nvidia supera estimativas em 38%; guidance robusto para IA","source":"Bloomberg","time":"09:52","tag":"g","tagLbl":"Tech","summary":"NVDA reporta receita de $26B no trimestre, acima do consenso."},
        {"title":"Tesouro americano 10Y atinge 4.72%; pressão em RF longa","source":"Valor Econômico","time":"09:38","tag":"r","tagLbl":"Bonds","summary":"Yield da treasury 10Y subiu 14bps após dados de emprego acima do esperado."},
        {"title":"Gold atinge novo ATH; fluxo defensivo global aumenta","source":"Investing","time":"09:21","tag":"g","tagLbl":"Gold","summary":"XAU/USD tocou $2,341, impulsionado por demanda de bancos centrais."},
        {"title":"JPMorgan rotaciona para energy e industrials","source":"Bloomberg","time":"08:55","tag":"o","tagLbl":"Inst.","summary":"Maior fundo institucional reduz exposição a tech de alta beta."},
        {"title":"Inflação no Brasil sobe para 4.8%; COPOM sob pressão","source":"Valor Econômico","time":"08:31","tag":"o","tagLbl":"Brasil","summary":"IPCA de março surpreende ao alta. Mercado precifica manutenção da Selic."},
    ]

def _mock_sectors():
    return {
        "equity_sectors": [
            {"name":"Technology","ticker":"XLK","score":82},{"name":"Industrials","ticker":"XLI","score":74},
            {"name":"Healthcare","ticker":"XLV","score":68},{"name":"Financials","ticker":"XLF","score":65},
            {"name":"Energy","ticker":"XLE","score":61},{"name":"Materials","ticker":"XLB","score":55},
            {"name":"Consumer Disc.","ticker":"XLY","score":48},{"name":"Consumer Staples","ticker":"XLP","score":38},
            {"name":"Comm. Services","ticker":"XLC","score":35},
            {"name":"Real Estate","ticker":"XLRE","score":22},{"name":"Utilities","ticker":"XLU","score":18},
        ],
        "commodities": [
            {"name":"Gold","ticker":"GLD","score":78,"cat":"Metals"},{"name":"Silver","ticker":"SLV","score":65,"cat":"Metals"},
            {"name":"Oil (Crude)","ticker":"USO","score":62,"cat":"Energy"},{"name":"Natural Gas","ticker":"UNG","score":42,"cat":"Energy"},
        ],
        "macro_assets": [
            {"name":"Long Treasuries","ticker":"TLT","score":24},{"name":"Short Treasuries","ticker":"SHY","score":55},
            {"name":"Dollar (DXY)","ticker":"UUP","score":67},
        ],
        "growth_proxy": [
            {"name":"QQQ — NASDAQ 100","ticker":"QQQ","score":76},
            {"name":"SPY — S&P 500","ticker":"SPY","score":60},
            {"name":"IWM — Small Caps","ticker":"IWM","score":38},
        ],
    }

def _mock_rpm():
    return [
        {"name":"HPC22 — Growth Portfolio","sector":"Multi-Asset","score":78,"dir":1,"status":"active"},
        {"name":"Tech Momentum","sector":"Technology","score":82,"dir":1,"status":"watching"},
        {"name":"Gold/Metals Trend","sector":"Commodities","score":74,"dir":1,"status":"watching"},
        {"name":"HPC11 — Conservative","sector":"Multi-Asset","score":65,"dir":1,"status":"active"},
        {"name":"Healthcare Defense","sector":"Healthcare","score":54,"dir":0,"status":"watching"},
        {"name":"Consumer Defensive","sector":"Consumer Staples","score":38,"dir":-1,"status":"avoid"},
        {"name":"Real Estate Hedge","sector":"Real Estate","score":22,"dir":-1,"status":"avoid"},
        {"name":"Long Duration Bonds","sector":"Fixed Income","score":18,"dir":-1,"status":"avoid"},
    ]


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    app = create_app()
    print(f"[HARPIAN API] Running on http://localhost:{port}")
    print(f"[HARPIAN API] Demo mode: ON — no real integrations active")
    app.run(host="0.0.0.0", port=port, debug=True)
