#!/usr/bin/env python3
"""
alerts_engine.py — HARPIAN Portfolio Engineering Terminal
Rule-based alert generator. Runs after each regime snapshot + portfolio update.

Rules:
  1. RN_BREACH       — client RN > mandate max
  2. DD_BREACH       — client DD% approaching / exceeding limit
  3. REGIME_CHANGE   — StormGuard state changed (e.g., OFF → WATCH → ACTIVATE)
  4. REBALANCE       — Client HPC allocation drift > 10pp from target
  5. STORMGUARD_ACT  — StormGuard switched to ACTIVATE or DEFENSIVE

Usage:
  python backend/alerts_engine.py              # run all rules
  python backend/alerts_engine.py --dry-run    # print without saving
  python backend/alerts_engine.py --client hollanda
"""

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "backend"))
import harpian_db as db

# ─────────────────────────────────────────────────────────────────────────────
#  RULE ENGINE
# ─────────────────────────────────────────────────────────────────────────────

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def check_rn_breach(client: dict, portfolio: dict, dry_run: bool = False) -> dict | None:
    """
    Rule: Risk Number exceeds mandate max.
    Severity: critical if > max+10, high if > max+5, medium otherwise.
    """
    rn_current = portfolio.get("risk_number") or client.get("risk_number_current", 0)
    rn_max     = client.get("risk_number_mandate_max", 70)
    if rn_current <= rn_max:
        return None

    gap = rn_current - rn_max
    if gap > 10:
        severity = "critical"
    elif gap > 5:
        severity = "high"
    else:
        severity = "medium"

    aum        = portfolio.get("aum_snapshot") or client.get("aum", 0)
    extra_risk = round(aum * (gap / 100), 0)
    dd_pct     = portfolio.get("max_drawdown", -15.0)

    alert = {
        "alert_type": "rn_breach",
        "severity":   severity,
        "client_id":  client["client_id"],
        "title":      f"{client['name']} — RN Fora do Mandato",
        "diagnosis":  f"RN atual {rn_current} vs mandato máximo {rn_max}. Desvio +{gap} pontos.",
        "impact":     f"DD potencial {dd_pct:.1f}% em evento de estresse. R${extra_risk:,.0f} de risco extra.",
        "action":     f"Revisar alocação. Migração para HPC11/HPC22 pode reduzir RN→{rn_max - 4}.",
        "triggered_at": _now(),
        "metadata_json": {
            "rn_current": rn_current,
            "rn_max": rn_max,
            "gap": gap,
            "aum": aum,
        },
    }
    if not dry_run:
        db.insert_alert(alert)
    return alert


def check_dd_breach(client: dict, portfolio: dict, dry_run: bool = False) -> dict | None:
    """
    Rule: Portfolio max drawdown approaching or exceeding mandate limit.
    Warning at 80% of limit, critical at limit.
    """
    dd_current = portfolio.get("max_drawdown", 0.0)  # negative number e.g. -12.4
    dd_limit   = client.get("max_drawdown_limit", -20.0)

    if dd_current >= dd_limit * 0.8:  # not yet at warning threshold
        return None

    at_limit = dd_current <= dd_limit
    severity = "critical" if at_limit else "high"
    pct_used = abs(dd_current / dd_limit) * 100

    alert = {
        "alert_type": "dd_breach",
        "severity":   severity,
        "client_id":  client["client_id"],
        "title":      f"{client['name']} — {'DD no Limite' if at_limit else 'DD Próximo do Limite'}",
        "diagnosis":  f"DD {dd_current:.1f}% vs limite {dd_limit:.1f}%. {pct_used:.0f}% do limite utilizado.",
        "impact":     f"{'Limite violado.' if at_limit else 'Tendência de deterioração.'} Revisão urgente.",
        "action":     "Aplicar trailing stop parcial. Avaliar hedge cambial e migração para HPC11.",
        "triggered_at": _now(),
        "metadata_json": {
            "dd_current": dd_current,
            "dd_limit": dd_limit,
            "pct_used": round(pct_used, 1),
        },
    }
    if not dry_run:
        db.insert_alert(alert)
    return alert


def check_stormguard_state_change(prev_state: str, new_state: str, regime: dict,
                                  dry_run: bool = False) -> dict | None:
    """
    Rule: StormGuard state changed.
    Only alert on escalations: off→watch→activate→defensive
    """
    STATE_RANK = {"off": 0, "watch": 1, "activate": 2, "defensive": 3}
    prev_rank = STATE_RANK.get(prev_state, 0)
    new_rank  = STATE_RANK.get(new_state, 0)

    if new_rank <= prev_rank:
        return None  # de-escalation or same — don't alert

    if new_rank >= 3:
        severity = "critical"
    elif new_rank >= 2:
        severity = "high"
    else:
        severity = "medium"

    STATE_LABELS = {"off":"OFF","watch":"WATCH","activate":"ACTIVATE","defensive":"DEFENSIVE"}
    score = regime.get("final_regime_score", 0)

    alert = {
        "alert_type": "regime_change",
        "severity":   severity,
        "client_id":  None,  # system-wide
        "title":      f"StormGuard: {STATE_LABELS[prev_state]} → {STATE_LABELS[new_state]}",
        "diagnosis":  f"Regime Score {score}. StormGuard escalou de {STATE_LABELS[prev_state]} para {STATE_LABELS[new_state]}.",
        "impact":     f"Clientes com RN > 55 em exposição aumentada. Proteção {'parcial' if new_rank == 2 else 'total'} ativada.",
        "action":     "Revisar clientes com RN alto. HPC11/HPC22 reduzem automaticamente exposição.",
        "triggered_at": _now(),
        "metadata_json": {
            "prev_state": prev_state,
            "new_state": new_state,
            "regime_score": score,
        },
    }
    if not dry_run:
        db.insert_alert(alert)
    return alert


def check_hpc_allocation_drift(client: dict, portfolio: dict, dry_run: bool = False) -> dict | None:
    """
    Rule: HPC allocation drifted > 10pp from the last approved allocation.
    (Simple: if client has hpc target but current allocation differs significantly.)
    """
    hpc11_curr = portfolio.get("hpc11_pct", 0)
    hpc22_curr = portfolio.get("hpc22_pct", 0)

    # Get last executed allocation
    allocs = db.get_allocations(client_id=client["client_id"], status="executed")
    if not allocs:
        return None

    last = allocs[0]
    hpc11_target = last.get("hpc11_pct", 0)
    hpc22_target = last.get("hpc22_pct", 0)

    drift11 = abs(hpc11_curr - hpc11_target)
    drift22 = abs(hpc22_curr - hpc22_target)
    max_drift = max(drift11, drift22)

    if max_drift < 10:
        return None

    alert = {
        "alert_type": "rebalance",
        "severity":   "medium",
        "client_id":  client["client_id"],
        "title":      f"{client['name']} — Drift de Alocação HPC",
        "diagnosis":  f"HPC11 drift: {drift11:.1f}pp. HPC22 drift: {drift22:.1f}pp. Desvio acima de 10pp.",
        "impact":     "Portfólio desviou do alvo estratégico. Rebalanceamento recomendado.",
        "action":     "Rebalancear para HPC11: {:.0f}% / HPC22: {:.0f}%.".format(hpc11_target, hpc22_target),
        "triggered_at": _now(),
        "metadata_json": {
            "hpc11_current": hpc11_curr, "hpc11_target": hpc11_target,
            "hpc22_current": hpc22_curr, "hpc22_target": hpc22_target,
        },
    }
    if not dry_run:
        db.insert_alert(alert)
    return alert


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN RUN FUNCTION
# ─────────────────────────────────────────────────────────────────────────────

def run(client_id: str = None, dry_run: bool = False) -> dict:
    """
    Run all alert rules against current DB state.
    Returns dict: { alerts_generated: int, by_type: {...} }
    """
    db.init_db()
    generated = []

    # ── Get regime ──
    regime = db.get_latest_regime()
    sg_state = (regime or {}).get("stormguard_state", "off")

    # ── Check StormGuard change ──
    # Compare with previous snapshot
    if regime:
        timeline = db.get_regime_timeline(days=7)
        if len(timeline) >= 2:
            prev_sg = timeline[-2].get("stormguard_state", "off")
            alert = check_stormguard_state_change(prev_sg, sg_state, regime, dry_run)
            if alert:
                generated.append(alert)
                print(f"  [ALERT] StormGuard: {prev_sg} → {sg_state}")

    # ── Per-client checks ──
    clients = db.get_clients() if not client_id else [db.get_client(client_id)]
    clients = [c for c in clients if c]

    for client in clients:
        portfolio = db.get_latest_portfolio(client["client_id"])
        if not portfolio:
            continue

        cid = client["client_id"]

        # RN breach
        a = check_rn_breach(client, portfolio, dry_run)
        if a:
            generated.append(a)
            print(f"  [ALERT] RN breach: {cid} RN={portfolio.get('risk_number')} > {client.get('risk_number_mandate_max')}")

        # DD breach
        a = check_dd_breach(client, portfolio, dry_run)
        if a:
            generated.append(a)
            print(f"  [ALERT] DD breach: {cid} DD={portfolio.get('max_drawdown'):.1f}%")

        # HPC drift
        a = check_hpc_allocation_drift(client, portfolio, dry_run)
        if a:
            generated.append(a)
            print(f"  [ALERT] HPC drift: {cid}")

    by_type: dict[str, int] = {}
    for a in generated:
        t = a.get("alert_type", "unknown")
        by_type[t] = by_type.get(t, 0) + 1

    print(f"\n[ALERTS] Generated: {len(generated)} | {by_type}")
    return {"alerts_generated": len(generated), "by_type": by_type, "dry_run": dry_run}


# ─────────────────────────────────────────────────────────────────────────────
#  CLI
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HARPIAN Alert Engine")
    parser.add_argument("--dry-run", action="store_true", help="Don't write to DB")
    parser.add_argument("--client", help="Run for specific client_id only")
    args = parser.parse_args()
    run(client_id=args.client, dry_run=args.dry_run)
