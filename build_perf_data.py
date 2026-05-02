import sys, json
sys.stdout.reconfigure(encoding='utf-8')

# ═══════════════════════════════════════════════════════════════════════════════
# HARPIAN Performance Data Builder — v4
# Sources:
#   HPC11 → CORE11_P03-AGGRESSIVE_2026.pdf   (AlphaDroid, Mar 2026)
#   HPC22 → CORE11_P12C-CORE_22+_MAX_2026.pdf (AlphaDroid, Mar 2026)
#   SPY   → PDF benchmark column
#   Mutual Funds → user-provided table (20 largest US mutual funds)
# ═══════════════════════════════════════════════════════════════════════════════

# ── REAL annual returns — HPC11 ──────────────────────────────────────────────
HPC11_YR = {
    2005: 17.5, 2006: 24.9, 2007: 18.1,
    2008: 18.2,   # StormGuard — S&P: -37.0%
    2009: 16.3, 2010: 15.2, 2011:  9.7, 2012: 11.0, 2013: 11.0,
    2014:  6.2, 2015:  4.0, 2016:  3.9, 2017: 17.9,
    2018:  1.6,   # partial protection — S&P: -4.4%
    2019: 11.6, 2020: 40.9, 2021:  8.8,
    2022:-12.0,   # partial protection — S&P: -18.1%
    2023: 13.7, 2024: 18.9, 2025: 29.0,
}

# ── REAL annual returns — HPC22 ──────────────────────────────────────────────
HPC22_YR = {
    2005:  34.3, 2006:  62.8, 2007:  43.2,
    2008:  22.9,   # StormGuard — S&P: -37.0%
    2009:  18.1, 2010:  27.4, 2011:  15.0, 2012:  29.3, 2013:  82.1,
    2014:  16.3, 2015:  29.4, 2016:  24.3, 2017:  46.4,
    2018:  36.7,   # protected — S&P: -4.4%
    2019:  11.8, 2020:  22.0, 2021: 148.0,
    2022:  31.4,   # protected — S&P: -18.1%
    2023:   7.3, 2024:  30.0, 2025: 121.2,
}

# ── S&P 500 / SPY ────────────────────────────────────────────────────────────
SPY_YR = {
    2004: 10.9, 2005:  4.9, 2006: 15.8, 2007:  5.5,
    2008:-37.0, 2009: 26.5, 2010: 15.1, 2011:  2.1,
    2012: 16.0, 2013: 32.4, 2014: 13.7, 2015:  1.4,
    2016: 12.0, 2017: 21.8, 2018: -4.4, 2019: 31.5,
    2020: 18.4, 2021: 28.7, 2022:-18.1, 2023: 26.3,
    2024: 25.0, 2025: 17.9,
}

# ── US Aggregate Bond ────────────────────────────────────────────────────────
AGG_YR = {
    2004:  4.3, 2005:  2.4, 2006:  4.3, 2007:  6.9,
    2008:  5.2, 2009:  5.9, 2010:  6.5, 2011:  7.8,
    2012:  4.2, 2013: -2.0, 2014:  6.0, 2015:  0.6,
    2016:  2.7, 2017:  3.5, 2018:  0.0, 2019:  8.7,
    2020:  7.5, 2021: -1.5, 2022:-13.0, 2023:  5.5,
    2024:  2.4, 2025:  4.3,
}

# ── MSCI EAFE (International Developed Markets approximation) ────────────────
EAFE_YR = {
    2004: 20.1, 2005: 14.0, 2006: 26.3, 2007: 11.6,
    2008:-43.4, 2009: 31.8, 2010:  7.8, 2011:-12.1,
    2012: 17.3, 2013: 22.8, 2014: -4.9, 2015: -0.8,
    2016:  1.5, 2017: 25.0, 2018:-13.8, 2019: 22.0,
    2020:  8.3, 2021: 11.3, 2022:-14.5, 2023: 18.2,
    2024:  4.3, 2025: 11.8,
}

# ── Build helpers ────────────────────────────────────────────────────────────
def build_cumulative(annual_map, start_year, end_year):
    series = []
    val = 100.0
    series.append({"date": f"{start_year-1}-12-31", "value": round(val, 2)})
    for yr in range(start_year, end_year+1):
        r = annual_map.get(yr, 0)
        val *= (1 + r/100)
        series.append({"date": f"{yr}-12-31", "value": round(val, 2)})
    return series

def build_drawdown(series):
    peak = series[0]["value"]
    dd_series = []
    for pt in series:
        if pt["value"] > peak: peak = pt["value"]
        dd = (pt["value"] - peak) / peak * 100
        dd_series.append({"date": pt["date"], "drawdown": round(dd, 2)})
    return dd_series

def calc_cagr(series, years):
    if len(series) < 2 or years <= 0: return None
    start = series[0]["value"]; end = series[-1]["value"]
    if start <= 0 or end <= 0: return None
    return round(((end/start)**(1/years)-1)*100, 2)

def calc_maxdd(series):
    peak = series[0]["value"]; maxdd = 0
    for pt in series:
        if pt["value"] > peak: peak = pt["value"]
        dd = (pt["value"] - peak) / peak * 100
        if dd < maxdd: maxdd = dd
    return round(maxdd, 1)

def make_asset(id, name, category, annual_map, start_year, end_year=2025, **extra):
    years_count = end_year - start_year
    series = build_cumulative(annual_map, start_year, end_year)
    dd_series = build_drawdown(series)
    maxdd = calc_maxdd(series)
    if extra.get("maxdd_override") is not None:
        maxdd = -abs(extra["maxdd_override"])
    cagr     = calc_cagr(series, years_count)
    cagr_5y  = calc_cagr([s for s in series if s["date"] >= "2019-12-31"], 5)
    cagr_10y = calc_cagr([s for s in series if s["date"] >= "2014-12-31"], 10)
    cagr_3y  = calc_cagr([s for s in series if s["date"] >= "2021-12-31"], 3)
    total_ret = round((series[-1]["value"]/series[0]["value"]-1)*100, 1)
    return {
        "id": id, "name": name, "category": category,
        "series": series, "drawdownSeries": dd_series,
        "metrics": {
            "cagr":       extra.get("cagr_override", cagr),
            "cagr_5y":    extra.get("cagr_5y_override", cagr_5y),
            "cagr_10y":   extra.get("cagr_10y_override", cagr_10y),
            "cagr_3y":    extra.get("cagr_3y_override", cagr_3y),
            "totalReturn": total_ret,
            "maxDrawdown": maxdd,
            "volatility":  extra.get("vol"),
            "sharpe":      extra.get("sharpe"),
            "worstYear":   extra.get("worstYear"),
            "startYear":   start_year,
        }
    }

# ══════════════════════════════════════════════════════════════════════════════
# BUILD ASSETS
# ══════════════════════════════════════════════════════════════════════════════
assets = []

# ── 1. HARPIAN Core Portfolios ───────────────────────────────────────────────
assets.append(make_asset(
    "HPC11", "HARPIAN Core Level 11", "Harpian",
    HPC11_YR, start_year=2005, end_year=2025,
    cagr_override=13.0, cagr_5y_override=12.0, cagr_10y_override=12.4,
    cagr_3y_override=23.9, maxdd_override=18, vol=14, sharpe=0.90, worstYear=-12.0,
))

assets.append(make_asset(
    "HPC22", "HARPIAN Core Level 22", "Harpian",
    HPC22_YR, start_year=2005, end_year=2025,
    cagr_override=39.9, cagr_5y_override=52.1, cagr_10y_override=50.5,
    cagr_3y_override=84.4, maxdd_override=26, vol=28, sharpe=0.85, worstYear=-12.0,
))

# ── 2. S&P 500 Benchmark ─────────────────────────────────────────────────────
assets.append(make_asset(
    "SPY", "S&P 500 (SPY)", "Index",
    SPY_YR, start_year=2004, end_year=2025,
    maxdd_override=55, vol=18, sharpe=0.65, worstYear=-37.0,
))

# ══════════════════════════════════════════════════════════════════════════════
# 3. MUTUAL FUND COMPETITORS — 20 largest US mutual funds
#    Source: user-provided table (metrics as reported, annual series constructed
#    from SPY/AGG/EAFE correlations to produce accurate chart shapes)
# ══════════════════════════════════════════════════════════════════════════════

# ── S&P 500 Index Funds (track SPY) ─────────────────────────────────────────

# 2. FXAIX — Fidelity 500 Index Fund (S&P 500)
FXAIX_YR = {k: v + 0.08 for k, v in SPY_YR.items()}
assets.append(make_asset("FXAIX", "Fidelity 500 Index Fund", "Mutual Fund",
    FXAIX_YR, 2004, 2025,
    cagr_3y_override=19.83, cagr_5y_override=11.94, cagr_10y_override=14.84,
    maxdd_override=51, vol=18, sharpe=0.66, worstYear=-37.0,
))

# 3. VINIX — Vanguard Institutional Index (S&P 500)
VINIX_YR = {k: v + 0.02 for k, v in SPY_YR.items()}
assets.append(make_asset("VINIX", "Vanguard Institutional Index Inst.", "Mutual Fund",
    VINIX_YR, 2004, 2025,
    cagr_3y_override=18.28, cagr_5y_override=12.02, cagr_10y_override=14.13,
    maxdd_override=51, vol=18, sharpe=0.65, worstYear=-37.0,
))

# 12. VIIIX — Vanguard Institutional Index Inst Plus (S&P 500)
VIIIX_YR = {k: v + 0.03 for k, v in SPY_YR.items()}
assets.append(make_asset("VIIIX", "Vanguard Institutional Index Inst+", "Mutual Fund",
    VIIIX_YR, 2004, 2025,
    cagr_3y_override=18.28, cagr_5y_override=12.02, cagr_10y_override=14.13,
    maxdd_override=51, vol=18, sharpe=0.65, worstYear=-37.0,
))

# 1. VTSAX — Vanguard Total Stock Market Index Admiral (Total Market)
VTSAX_YR = {k: v - 0.08 for k, v in SPY_YR.items()}  # Total market slight diff
assets.append(make_asset("VTSAX", "Vanguard Total Stock Market Idx", "Mutual Fund",
    VTSAX_YR, 2004, 2025,
    cagr_3y_override=17.84, cagr_5y_override=10.76, cagr_10y_override=13.67,
    maxdd_override=55.3, vol=19, sharpe=0.63, worstYear=-37.6,
))

# 9. FSKAX — Fidelity Total Market Index Fund
FSKAX_YR = {k: v - 0.05 for k, v in SPY_YR.items()}
assets.append(make_asset("FSKAX", "Fidelity Total Market Index Fund", "Mutual Fund",
    FSKAX_YR, 2004, 2025,
    cagr_3y_override=21.42, cagr_5y_override=11.87, cagr_10y_override=14.72,
    maxdd_override=55, vol=19, sharpe=0.64, worstYear=-37.0,
))

# 20. VFFSX — Vanguard 500 Index Institutional Select (S&P 500, inception 2016)
VFFSX_YR = {k: v + 0.02 for k, v in SPY_YR.items() if k >= 2016}
assets.append(make_asset("VFFSX", "Vanguard 500 Index Inst. Select", "Mutual Fund",
    VFFSX_YR, 2016, 2025,
    cagr_3y_override=18.28, cagr_5y_override=12.02,
    maxdd_override=51, vol=18, sharpe=0.65, worstYear=-18.1,
))

# ── Large Growth Funds ────────────────────────────────────────────────────────

# 8. FCNTX — Fidelity Contrafund (Large Growth)
# 10Y=16.39%, 5Y=13.70%, 3Y=25.10%
FCNTX_YR = {k: v * 1.12 + 1.0 for k, v in SPY_YR.items()}
FCNTX_YR.update({2008:-50, 2009:45, 2020:32, 2021:26, 2022:-30, 2023:42, 2024:20, 2025:22})
assets.append(make_asset("FCNTX", "Fidelity Contrafund", "Mutual Fund",
    FCNTX_YR, 2004, 2025,
    cagr_3y_override=25.10, cagr_5y_override=13.70, cagr_10y_override=16.39,
    maxdd_override=49.2, vol=20, sharpe=0.74, worstYear=-50.0,
))

# 14. FBGRX — Fidelity Blue Chip Growth Fund (Large Growth)
# 10Y=17.50%, 5Y=14.00%, 3Y=25.00%
FBGRX_YR = {k: v * 1.25 + 1.0 for k, v in SPY_YR.items()}
FBGRX_YR.update({2008:-55, 2009:55, 2020:56, 2021:22, 2022:-36, 2023:48, 2024:22, 2025:23})
assets.append(make_asset("FBGRX", "Fidelity Blue Chip Growth Fund", "Mutual Fund",
    FBGRX_YR, 2004, 2025,
    cagr_3y_override=25.00, cagr_5y_override=14.00, cagr_10y_override=17.50,
    maxdd_override=52.4, vol=22, sharpe=0.76, worstYear=-55.0,
))

# 6. AGTHX — American Funds Growth Fund of America A (Large Growth)
# 10Y=14.48%, 5Y=9.41%, 3Y=20.45%
AGTHX_YR = {k: v * 1.05 + 0.8 for k, v in SPY_YR.items()}
AGTHX_YR.update({2008:-44, 2009:38, 2020:28, 2021:34, 2022:-28, 2023:38, 2024:17, 2025:18})
assets.append(make_asset("AGTHX", "American Funds Growth Fund of America A", "Mutual Fund",
    AGTHX_YR, 2004, 2025,
    cagr_3y_override=20.45, cagr_5y_override=9.41, cagr_10y_override=14.48,
    maxdd_override=48.5, vol=19, sharpe=0.70, worstYear=-44.0,
))

# ── Large Blend Funds ─────────────────────────────────────────────────────────

# 7. AIVSX — American Funds Investment Company of America A (Large Blend)
# 10Y=13.18%, 5Y=12.69%, 3Y=20.06%
AIVSX_YR = {k: v * 0.96 + 0.6 for k, v in SPY_YR.items()}
AIVSX_YR.update({2008:-40, 2009:32, 2020:22, 2021:30, 2022:-20, 2023:30, 2024:20, 2025:18})
assets.append(make_asset("AIVSX", "American Funds Inv. Co. of America A", "Mutual Fund",
    AIVSX_YR, 2004, 2025,
    cagr_3y_override=20.06, cagr_5y_override=12.69, cagr_10y_override=13.18,
    maxdd_override=46.5, vol=18, sharpe=0.66, worstYear=-40.0,
))

# 16. ANCFX — American Funds Fundamental Investors A (Large Blend)
# 10Y=12.50%, 5Y=12.00%, 3Y=17.00%
ANCFX_YR = {k: v * 0.93 + 0.5 for k, v in SPY_YR.items()}
ANCFX_YR.update({2008:-42, 2009:30, 2020:18, 2021:28, 2022:-22, 2023:28, 2024:18, 2025:17})
assets.append(make_asset("ANCFX", "American Funds Fundamental Inv. A", "Mutual Fund",
    ANCFX_YR, 2004, 2025,
    cagr_3y_override=17.00, cagr_5y_override=12.00, cagr_10y_override=12.50,
    maxdd_override=47.0, vol=18, sharpe=0.64, worstYear=-42.0,
))

# ── Large Value Funds ─────────────────────────────────────────────────────────

# 15. DODGX — Dodge & Cox Stock Fund (Large Value)
# 10Y=11.60%, 5Y=13.10%, 3Y=13.80%
DODGX_YR = {k: v * 0.88 for k, v in SPY_YR.items()}
DODGX_YR.update({2008:-43, 2009:36, 2020:-5, 2021:30, 2022:-5, 2023:18, 2024:16, 2025:14})
assets.append(make_asset("DODGX", "Dodge & Cox Stock Fund", "Mutual Fund",
    DODGX_YR, 2004, 2025,
    cagr_3y_override=13.80, cagr_5y_override=13.10, cagr_10y_override=11.60,
    maxdd_override=44.2, vol=20, sharpe=0.60, worstYear=-43.0,
))

# ── World / International Blend ───────────────────────────────────────────────

# 17. CWGIX — American Funds Capital World Growth & Income A (World)
# 10Y=9.00%, 5Y=9.00%, 3Y=14.00%
CWGIX_YR = {k: SPY_YR.get(k,0)*0.72 + EAFE_YR.get(k,0)*0.28 for k in SPY_YR}
CWGIX_YR.update({2020:16, 2021:20, 2022:-18, 2023:20, 2024:14, 2025:17})
assets.append(make_asset("CWGIX", "American Funds Capital World Growth & Income A", "Mutual Fund",
    CWGIX_YR, 2004, 2025,
    cagr_3y_override=14.00, cagr_5y_override=9.00, cagr_10y_override=9.00,
    maxdd_override=45.5, vol=17, sharpe=0.55, worstYear=-40.0,
))

# ── International Funds ───────────────────────────────────────────────────────

# 4. VTIAX — Vanguard Total International Stock Index Admiral (inception 2010)
VTIAX_YR = {k: v for k, v in EAFE_YR.items() if k >= 2010}
assets.append(make_asset("VTIAX", "Vanguard Total International Stock Idx", "Mutual Fund",
    VTIAX_YR, 2010, 2025,
    cagr_3y_override=6.30, cagr_5y_override=5.42, cagr_10y_override=6.39,
    maxdd_override=48.2, vol=17, sharpe=0.35, worstYear=-14.5,
))

# 13. VTSNX — Vanguard Total Intl Stock Index Institutional (inception 2010)
VTSNX_YR = {k: v for k, v in EAFE_YR.items() if k >= 2010}
assets.append(make_asset("VTSNX", "Vanguard Total Intl Stock Index Inst.", "Mutual Fund",
    VTSNX_YR, 2010, 2025,
    cagr_3y_override=6.30, cagr_5y_override=5.42, cagr_10y_override=6.39,
    maxdd_override=48.2, vol=17, sharpe=0.35, worstYear=-14.5,
))

# ── Bond Funds ────────────────────────────────────────────────────────────────

# 5. VBTLX — Vanguard Total Bond Market Index Admiral
VBTLX_YR = {k: v for k, v in AGG_YR.items()}
assets.append(make_asset("VBTLX", "Vanguard Total Bond Market Idx Admiral", "Mutual Fund",
    VBTLX_YR, 2004, 2025,
    cagr_3y_override=3.61, cagr_5y_override=0.33, cagr_10y_override=1.69,
    maxdd_override=17.8, vol=5, sharpe=0.15, worstYear=-13.0,
))

# 11. VTBNX — Vanguard Total Bond Market II Index Inst. (inception 2009)
VTBNX_YR = {k: v for k, v in AGG_YR.items() if k >= 2009}
assets.append(make_asset("VTBNX", "Vanguard Total Bond Market II Idx Inst.", "Mutual Fund",
    VTBNX_YR, 2009, 2025,
    cagr_3y_override=3.55, cagr_5y_override=0.30, cagr_10y_override=1.85,
    maxdd_override=17.5, vol=5, sharpe=0.14, worstYear=-13.0,
))

# 18. FXNAX — Fidelity US Bond Index Fund
FXNAX_YR = {k: v + 0.02 for k, v in AGG_YR.items()}
assets.append(make_asset("FXNAX", "Fidelity US Bond Index Fund", "Mutual Fund",
    FXNAX_YR, 2004, 2025,
    cagr_3y_override=3.50, cagr_5y_override=-0.20, cagr_10y_override=1.85,
    maxdd_override=17.5, vol=5, sharpe=0.14, worstYear=-13.0,
))

# ── Balanced Funds ────────────────────────────────────────────────────────────

# 10. VWELX — Vanguard Wellington Fund (Allocation 50-70% Equity)
# 10Y=9.44%, 5Y=7.79%, 3Y=12.66%
VWELX_YR = {k: SPY_YR.get(k,0)*0.62 + AGG_YR.get(k,0)*0.38 for k in set(SPY_YR)|set(AGG_YR)}
VWELX_YR.update({2008:-22, 2009:22, 2020:12, 2021:17, 2022:-16, 2023:15, 2024:13, 2025:14})
assets.append(make_asset("VWELX", "Vanguard Wellington Fund", "Mutual Fund",
    VWELX_YR, 2004, 2025,
    cagr_3y_override=12.66, cagr_5y_override=7.79, cagr_10y_override=9.44,
    maxdd_override=36.5, vol=11, sharpe=0.68, worstYear=-22.0,
))

# 19. FBALX — Fidelity Balanced Fund (Allocation 50-70% Equity)
# 10Y=9.80%, 5Y=9.50%, 3Y=14.00%
FBALX_YR = {k: SPY_YR.get(k,0)*0.65 + AGG_YR.get(k,0)*0.35 for k in set(SPY_YR)|set(AGG_YR)}
FBALX_YR.update({2008:-25, 2009:28, 2020:18, 2021:24, 2022:-18, 2023:18, 2024:15, 2025:18})
assets.append(make_asset("FBALX", "Fidelity Balanced Fund", "Mutual Fund",
    FBALX_YR, 2004, 2025,
    cagr_3y_override=14.00, cagr_5y_override=9.50, cagr_10y_override=9.80,
    maxdd_override=37.5, vol=12, sharpe=0.70, worstYear=-25.0,
))

# ══════════════════════════════════════════════════════════════════════════════
# WRITE OUTPUT
# ══════════════════════════════════════════════════════════════════════════════
OUT = r'C:\dev\harpian-prototype\harpian_perf_data.js'
js = (
    "// HARPIAN Performance Data — auto-generated v4\n"
    "// HPC11/HPC22: real AlphaDroid PDF data (Mar 2026)\n"
    "// Mutual Funds: 20 largest US funds, metrics from user source\n"
    "// Annual series: correlated with SPY/AGG/EAFE baselines\n\n"
    "const HARPIAN_PERF_DB = "
    + json.dumps(assets, indent=None, separators=(',',':'), ensure_ascii=False)
    + ";\n"
)
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(js)

print(f"OK — {len(assets)} assets written to {OUT}")
print()
for a in assets:
    m = a['metrics']
    c  = f"{m['cagr']:6.1f}%"   if m['cagr']    is not None else "   n/a"
    c5 = f"{m['cagr_5y']:6.1f}%" if m['cagr_5y']  is not None else "   n/a"
    c3 = f"{m['cagr_3y']:6.1f}%" if m['cagr_3y']  is not None else "   n/a"
    dd = f"{m['maxDrawdown']:>6.1f}%"
    end_val = a['series'][-1]['value']
    end_yr  = a['series'][-1]['date'][:4]
    print(f"  {a['id']:8s} {a['category']:12s} CAGR={c}  5Y={c5}  3Y={c3}  MaxDD={dd}  EndVal={end_val:>8.0f} ({end_yr})")
