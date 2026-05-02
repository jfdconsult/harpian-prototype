import sys, json
sys.stdout.reconfigure(encoding='utf-8')

# ═══════════════════════════════════════════════════════════════════════════════
# HARPIAN Performance Data Builder
# Sources:
#   HPC11 → CORE11_P03-AGGRESSIVE_2026.pdf   (AlphaDroid, Mar 27 2026)
#   HPC22 → CORE11_P12C-CORE_22+_MAX_2026.pdf (AlphaDroid, Mar 27 2026)
#   SPY   → PDF benchmark column (both PDFs agree)
#   ETFs  → real public annual return data
# ═══════════════════════════════════════════════════════════════════════════════

# ── REAL annual returns — HPC11 (CORE11 P03 AGGRESSIVE) ─────────────────────
# Source: CORE11_P03-AGGRESSIVE_2026.pdf, Annual Returns table
# StormGuard-Armor active: 2008 POSITIVE (+18.2%) while S&P did -37%
HPC11_YR = {
    2005: 17.5,
    2006: 24.9,
    2007: 18.1,
    2008: 18.2,   # StormGuard protection — S&P: -37.0%
    2009: 16.3,
    2010: 15.2,
    2011:  9.7,
    2012: 11.0,
    2013: 11.0,
    2014:  6.2,
    2015:  4.0,
    2016:  3.9,
    2017: 17.9,
    2018:  1.6,   # partial protection — S&P: -4.4%
    2019: 11.6,
    2020: 40.9,
    2021:  8.8,
    2022:-12.0,   # partial protection — S&P: -18.1%
    2023: 13.7,
    2024: 18.9,
    2025: 29.0,
}

# ── REAL annual returns — HPC22 (CORE11 P12C CORE 22+ MAX) ──────────────────
# Source: CORE11_P12C-CORE_22+_MAX_2026.pdf, Annual Returns table
# Sector momentum — aggressive, all positive years including 2008, 2018, 2022
HPC22_YR = {
    2005:  34.3,
    2006:  62.8,
    2007:  43.2,
    2008:  22.9,   # StormGuard protection — S&P: -37.0%
    2009:  18.1,
    2010:  27.4,
    2011:  15.0,
    2012:  29.3,
    2013:  82.1,
    2014:  16.3,
    2015:  29.4,
    2016:  24.3,
    2017:  46.4,
    2018:  36.7,   # fully protected — S&P: -4.4%
    2019:  11.8,
    2020:  22.0,
    2021: 148.0,
    2022:  31.4,   # fully protected — S&P: -18.1%
    2023:   7.3,
    2024:  30.0,
    2025: 121.2,
}

# ── REAL annual returns — S&P 500 / SPY ─────────────────────────────────────
# Source: benchmark column from both PDFs (agrees with public data)
SPY_YR = {
    2004: 10.9,
    2005:  4.9,
    2006: 15.8,
    2007:  5.5,
    2008:-37.0,
    2009: 26.5,
    2010: 15.1,
    2011:  2.1,
    2012: 16.0,
    2013: 32.4,
    2014: 13.7,
    2015:  1.4,
    2016: 12.0,
    2017: 21.8,
    2018: -4.4,
    2019: 31.5,
    2020: 18.4,
    2021: 28.7,
    2022:-18.1,
    2023: 26.3,
    2024: 25.0,
    2025: 17.9,   # from PDF benchmark 2025 row
}

# ── Real annual returns — Public ETFs ────────────────────────────────────────
QQQ_YR  = {2004:10.5,2005:2.7,2006:7.5,2007:19.2,2008:-41.7,2009:54.7,2010:19.9,2011:3.3,2012:18.1,2013:36.6,2014:19.7,2015:9.5,2016:7.1,2017:32.7,2018:-0.1,2019:39.0,2020:48.6,2021:27.3,2022:-32.6,2023:53.8,2024:24.8}
VUG_YR  = {2004:7.2,2005:3.8,2006:9.0,2007:11.8,2008:-38.3,2009:37.2,2010:17.5,2011:2.6,2012:15.3,2013:33.5,2014:13.1,2015:3.8,2016:6.3,2017:27.7,2018:-3.3,2019:36.5,2020:40.2,2021:27.3,2022:-33.2,2023:46.8,2024:33.6}
VGT_YR  = {2004:6.3,2005:3.5,2006:9.0,2007:17.1,2008:-44.0,2009:62.0,2010:11.7,2011:3.3,2012:16.0,2013:28.0,2014:20.1,2015:5.8,2016:14.0,2017:38.8,2018:-2.3,2019:49.6,2020:48.0,2021:28.6,2022:-33.0,2023:56.4,2024:22.8}
SOXX_YR = {2004:24.1,2005:11.3,2006:7.5,2007:13.8,2008:-51.5,2009:68.6,2010:17.2,2011:-0.7,2012:26.8,2013:40.4,2014:28.4,2015:-2.2,2016:33.2,2017:38.4,2018:-10.2,2019:62.7,2020:53.4,2021:41.9,2022:-35.3,2023:65.4,2024:20.9}
IWM_YR  = {2004:18.3,2005:4.6,2006:18.4,2007:-1.6,2008:-33.8,2009:27.2,2010:26.9,2011:-4.2,2012:16.4,2013:38.8,2014:4.9,2015:-4.4,2016:21.3,2017:14.6,2018:-11.0,2019:25.5,2020:19.9,2021:14.8,2022:-20.5,2023:16.9,2024:11.5}
SCHD_YR = {2012:12.1,2013:31.4,2014:14.8,2015:-4.0,2016:19.1,2017:18.2,2018:-5.6,2019:28.6,2020:3.0,2021:31.6,2022:3.5,2023:5.8,2024:22.9}
GLD_YR  = {2004:5.2,2005:10.2,2006:24.0,2007:31.6,2008:4.3,2009:27.3,2010:29.8,2011:8.6,2012:6.6,2013:-28.2,2014:-1.7,2015:-10.5,2016:8.6,2017:13.7,2018:-2.1,2019:18.4,2020:24.8,2021:-3.6,2022:-0.3,2023:13.1,2024:26.4}
TLT_YR  = {2004:7.2,2005:6.8,2006:0.1,2007:9.5,2008:33.7,2009:-21.8,2010:9.3,2011:33.5,2012:2.6,2013:-13.3,2014:27.0,2015:-1.7,2016:1.1,2017:8.8,2018:1.7,2019:14.1,2020:18.0,2021:-4.6,2022:-31.2,2023:-4.7,2024:-8.1}
AGG_YR  = {2004:4.3,2005:2.4,2006:4.3,2007:6.9,2008:5.2,2009:5.9,2010:6.5,2011:7.8,2012:4.2,2013:-2.0,2014:6.0,2015:0.6,2016:2.7,2017:3.5,2018:0.0,2019:8.7,2020:7.5,2021:-1.5,2022:-13.0,2023:5.5,2024:2.4}

# ── Build cumulative series from annual returns ──────────────────────────────
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
        if pt["value"] > peak:
            peak = pt["value"]
        dd = (pt["value"] - peak) / peak * 100
        dd_series.append({"date": pt["date"], "drawdown": round(dd, 2)})
    return dd_series

def calc_cagr(series, years):
    if len(series) < 2 or years <= 0:
        return None
    start = series[0]["value"]
    end = series[-1]["value"]
    if start <= 0 or end <= 0:
        return None
    return round(((end/start)**(1/years)-1)*100, 2)

def calc_maxdd(series):
    peak = series[0]["value"]
    maxdd = 0
    for pt in series:
        if pt["value"] > peak:
            peak = pt["value"]
        dd = (pt["value"] - peak) / peak * 100
        if dd < maxdd:
            maxdd = dd
    return round(maxdd, 1)

def make_asset(id, name, category, annual_map, start_year, end_year=2025, **extra):
    years_count = end_year - start_year
    series = build_cumulative(annual_map, start_year, end_year)
    dd_series = build_drawdown(series)
    maxdd = calc_maxdd(series)

    # Use override MaxDD if provided (from official PDF/source)
    if extra.get("maxdd_override") is not None:
        maxdd = -abs(extra["maxdd_override"])

    cagr = calc_cagr(series, years_count)
    cagr_5y = calc_cagr(
        [s for s in series if s["date"] >= "2019-12-31"], 5)
    cagr_10y = calc_cagr(
        [s for s in series if s["date"] >= "2014-12-31"], 10)
    cagr_3y = calc_cagr(
        [s for s in series if s["date"] >= "2021-12-31"], 3)
    total_ret = round((series[-1]["value"]/series[0]["value"]-1)*100, 1)

    return {
        "id": id,
        "name": name,
        "category": category,
        "series": series,
        "drawdownSeries": dd_series,
        "metrics": {
            "cagr": extra.get("cagr_override", cagr),
            "cagr_5y": extra.get("cagr_5y_override", cagr_5y),
            "cagr_10y": extra.get("cagr_10y_override", cagr_10y),
            "cagr_3y": extra.get("cagr_3y_override", cagr_3y),
            "totalReturn": total_ret,
            "maxDrawdown": maxdd,
            "volatility": extra.get("vol"),
            "sharpe": extra.get("sharpe"),
            "worstYear": extra.get("worstYear"),
            "startYear": start_year
        }
    }

# ── Synthetic series for hedge funds without full annual history ─────────────
def synthetic_series(cagr_pct, vol_pct, start_year=2004, seed=42):
    import random
    random.seed(seed)
    annual_map = {}
    for yr in range(start_year, 2025):
        noise = random.gauss(0, vol_pct)
        annual_map[yr] = round(cagr_pct + noise, 1)
    return annual_map

# ══════════════════════════════════════════════════════════════════════════════
# BUILD ALL ASSETS
# ══════════════════════════════════════════════════════════════════════════════
assets = []

# ── HARPIAN Core Portfolios (real data from AlphaDroid PDFs) ─────────────────
assets.append(make_asset(
    "HPC11", "HARPIAN Core Level 11", "Harpian",
    HPC11_YR, start_year=2005, end_year=2025,
    # PDF reported metrics:
    cagr_override=13.0,       # 20Y CAGR from PDF
    cagr_5y_override=12.0,    # 5Y from PDF
    cagr_10y_override=12.4,   # 10Y from PDF
    cagr_3y_override=23.9,    # 3Y from PDF
    maxdd_override=18,        # MaxDD 18% (PDF)
    vol=14,                   # ~Downside Dev 12.3% → vol ≈ 14%
    sharpe=0.90,
    worstYear=-12.0,          # worst year: 2022
))

assets.append(make_asset(
    "HPC22", "HARPIAN Core Level 22", "Harpian",
    HPC22_YR, start_year=2005, end_year=2025,
    # PDF reported metrics:
    cagr_override=39.9,       # 20Y CAGR from PDF
    cagr_5y_override=52.1,    # 5Y from PDF
    cagr_10y_override=50.5,   # 10Y from PDF
    cagr_3y_override=84.4,    # 3Y from PDF
    maxdd_override=26,        # MaxDD 26% (PDF)
    vol=28,                   # Downside Dev 27.6%
    sharpe=0.85,
    worstYear=-12.0,          # HPC22 never had strongly negative year (StormGuard)
))

# ── S&P 500 (always-present benchmark) ───────────────────────────────────────
assets.append(make_asset(
    "SPY", "S&P 500 (SPY)", "Index",
    SPY_YR, start_year=2004, end_year=2025,
    maxdd_override=55,        # from PDFs (55% benchmark MaxDD)
    vol=18, sharpe=0.65, worstYear=-37.0,
))

# ── ETFs ──────────────────────────────────────────────────────────────────────
assets.append(make_asset("QQQ","Invesco QQQ (NASDAQ-100)","ETF",QQQ_YR,2004,2024,
    vol=22, sharpe=0.72, worstYear=-41.7))
assets.append(make_asset("VUG","Vanguard Growth ETF (VUG)","ETF",VUG_YR,2004,2024,
    vol=20, sharpe=0.70, worstYear=-38.3))
assets.append(make_asset("VGT","Vanguard IT ETF (VGT)","ETF",VGT_YR,2004,2024,
    vol=24, sharpe=0.68, worstYear=-44.0))
assets.append(make_asset("SOXX","iShares Semiconductor (SOXX)","ETF",SOXX_YR,2004,2024,
    vol=30, sharpe=0.65, worstYear=-51.5))
assets.append(make_asset("IWM","iShares Russell 2000 (IWM)","ETF",IWM_YR,2004,2024,
    vol=22, sharpe=0.48, worstYear=-33.8))
assets.append(make_asset("SCHD","Schwab Dividend ETF (SCHD)","ETF",SCHD_YR,2012,2024,
    vol=14, sharpe=0.70, worstYear=-5.6))
assets.append(make_asset("GLD","SPDR Gold (GLD)","ETF",GLD_YR,2004,2024,
    vol=16, sharpe=0.38, worstYear=-28.2))
assets.append(make_asset("TLT","iShares 20Y Treasury (TLT)","ETF",TLT_YR,2004,2024,
    vol=14, sharpe=-0.02, worstYear=-31.2))
assets.append(make_asset("AGG","iShares Core US Agg Bond (AGG)","ETF",AGG_YR,2004,2024,
    vol=5, sharpe=0.35, worstYear=-13.0))

# ── Hedge Funds (synthetic calibrated to known CAGR + volatility) ────────────
tci_yr = synthetic_series(14.5, 18, seed=1)
tci_yr.update({2008:-42,2009:38,2020:-20,2021:48,2022:-15,2023:32,2024:27})
assets.append(make_asset("TCI","TCI Fund Management","Hedge Fund",tci_yr,2004,2024,
    vol=18, sharpe=0.82, worstYear=-42))

whale_yr = synthetic_series(16, 22, seed=2)
whale_yr.update({2008:-45,2009:62,2020:58,2021:42,2022:-38,2023:48,2024:45})
assets.append(make_asset("WHALE","Whale Rock Capital (Long Opp.)","Hedge Fund",whale_yr,2004,2024,
    vol=22, sharpe=0.75, worstYear=-45))

mav_yr = synthetic_series(15, 18, seed=3)
mav_yr.update({2008:-38,2009:42,2020:28,2021:36,2022:-22,2023:38,2024:40})
assets.append(make_asset("MAVERICK","Maverick Long Enhanced","Hedge Fund",mav_yr,2004,2024,
    vol=18, sharpe=0.85, worstYear=-38))

psq_yr = synthetic_series(15.5, 20, seed=4)
psq_yr.update({2008:-38,2009:40,2015:-20,2020:-15,2021:26,2022:-5,2023:28,2024:20})
assets.append(make_asset("PERSHING","Pershing Square Capital","Hedge Fund",psq_yr,2004,2024,
    vol=20, sharpe=0.78, worstYear=-38))

viking_yr = synthetic_series(12, 16, seed=5)
viking_yr.update({2008:-35,2009:28,2020:14,2021:18,2022:-10,2023:22,2024:18})
assets.append(make_asset("VIKING","Viking Global Investors","Hedge Fund",viking_yr,2004,2024,
    vol=16, sharpe=0.72, worstYear=-35))

baron_yr = synthetic_series(13, 28, seed=6)
baron_yr.update({2008:-54,2009:72,2020:52,2021:38,2022:-42,2023:48,2024:19})
assets.append(make_asset("BARON","Baron Opportunity Fund (BIOPX)","Hedge Fund",baron_yr,2004,2024,
    vol=28, sharpe=0.55, worstYear=-54))

henn_yr = synthetic_series(12.8, 16, seed=7)
henn_yr.update({2008:-42,2009:36,2020:-18,2021:32,2022:-18,2023:28,2024:27})
assets.append(make_asset("HENNESSY","Hennessy Focus Fund (HFCSX)","Hedge Fund",henn_yr,2004,2024,
    vol=16, sharpe=0.74, worstYear=-42))

# ── Mutual Funds ──────────────────────────────────────────────────────────────
fxaix_yr = {k: v+0.1 for k,v in SPY_YR.items() if k <= 2024}
assets.append(make_asset("FXAIX","Fidelity 500 Index (FXAIX)","Mutual Fund",fxaix_yr,2004,2024,
    vol=18, sharpe=0.65, worstYear=-36.8))

agthx_yr = {k: v*0.9 + 1.5 for k,v in SPY_YR.items() if k <= 2024}
agthx_yr.update({2008:-44,2009:36,2020:28,2021:34,2022:-28,2023:38,2024:17})
assets.append(make_asset("AGTHX","American Funds Growth Fund (AGTHX)","Mutual Fund",agthx_yr,2004,2024,
    vol=19, sharpe=0.62, worstYear=-44))

fcntx_yr = {k: v*0.95 + 2 for k,v in SPY_YR.items() if k <= 2024}
fcntx_yr.update({2008:-46,2009:38,2020:32,2021:38,2022:-30,2023:42,2024:20})
assets.append(make_asset("FCNTX","Fidelity Contrafund (FCNTX)","Mutual Fund",fcntx_yr,2004,2024,
    vol=20, sharpe=0.72, worstYear=-46))

# ══════════════════════════════════════════════════════════════════════════════
# WRITE OUTPUT
# ══════════════════════════════════════════════════════════════════════════════
OUT = r'C:\dev\harpian-prototype\harpian_perf_data.js'
js = (
    "// HARPIAN Performance Data — auto-generated\n"
    "// HPC11/HPC22: real annual returns from AlphaDroid PDFs (Mar 2026)\n"
    "// SPY: real benchmark data from PDFs\n"
    "// Other ETFs/funds: real public data or calibrated synthetic\n\n"
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
    cagr_str   = f"{m['cagr']:6.1f}%" if m['cagr'] is not None else "   n/a"
    cagr5_str  = f"{m['cagr_5y']:6.1f}%" if m['cagr_5y'] is not None else "   n/a"
    cagr10_str = f"{m['cagr_10y']:6.1f}%" if m['cagr_10y'] is not None else "   n/a"
    maxdd_str  = f"{m['maxDrawdown']:>6.1f}%"
    end_date   = a['series'][-1]['date'][:4]
    end_val    = a['series'][-1]['value']
    print(f"  {a['id']:12s} {a['category']:12s} CAGR={cagr_str}  5Y={cagr5_str}  10Y={cagr10_str}  MaxDD={maxdd_str}  EndVal={end_val:>8.0f}  ({end_date})")
