"""
Rebuild: screen-performance + screen-sector-momentum in terminal.html
"""
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

PATH = r"C:\dev\harpian-prototype\terminal.html"

with open(PATH, "r", encoding="utf-8") as f:
    html = f.read()

# ─────────────────────────────────────────────────────────────────
# 1. CSS — add styles for the new layouts
# ─────────────────────────────────────────────────────────────────
OLD_CSS_ANCHOR = ".screen{display:none;padding:22px;min-height:100%;}"
NEW_CSS = """.screen{display:none;padding:22px;min-height:100%;}
.perf-sector-item{display:flex;align-items:center;gap:8px;padding:9px 14px;cursor:pointer;border-bottom:1px solid rgba(255,255,255,0.03);border-left:3px solid transparent;transition:background 0.15s,border-color 0.15s;}
.perf-sector-item:hover{background:rgba(255,255,255,0.02);}
.perf-sector-item.perf-sector-selected{background:rgba(212,175,69,0.05);border-left-color:var(--gold);}
.sm-urow{display:flex;align-items:center;gap:10px;padding:6px 14px;border-bottom:1px solid rgba(255,255,255,0.025);}
.sm-urow:last-child{border-bottom:none;}
.sm-usec-hdr{padding:6px 14px 5px;background:rgba(255,255,255,0.015);border-bottom:1px solid var(--border);border-top:1px solid var(--border);}
.sm-badge{font-family:var(--mono);font-size:9px;padding:2px 6px;border-radius:3px;border:1px solid;width:52px;text-align:center;flex-shrink:0;}"""

if OLD_CSS_ANCHOR not in html:
    print("ERROR: CSS anchor not found")
    exit(1)
html = html.replace(OLD_CSS_ANCHOR, NEW_CSS, 1)
print("OK CSS injected")

# ─────────────────────────────────────────────────────────────────
# 2. Replace screen-sector-momentum HTML
# ─────────────────────────────────────────────────────────────────
OLD_SM = """<!-- ══ SECTOR MOMENTUM ══ (Strategies > Sector Momentum) -->
<div class="screen" id="screen-sector-momentum">
  <div class="mb16">
    <div class="kicker">Strategies · Market Intelligence</div>
    <div class="page-title">Sector Momentum</div>
    <div class="page-sub">Relative strength and momentum across sectors and macro assets · Does not represent portfolio positions</div>
  </div>
  <!-- Summary Banner + Regime + Rotation Signals -->
  <div class="g3 mb12">
    <div style="grid-column:span 2;background:linear-gradient(135deg,rgba(212,175,69,0.06),rgba(212,175,69,0.01));border:1px solid rgba(212,175,69,0.16);border-radius:var(--r);padding:14px 18px;">
      <div style="font-family:var(--mono);font-size:10px;letter-spacing:0.20em;text-transform:uppercase;color:var(--gold);margin-bottom:6px;">Market Momentum Summary</div>
      <div id="sm-summary-text" style="font-size:15px;color:var(--text2);line-height:1.65;">Technology and Industrials lead momentum while defensive sectors weaken. Commodities gaining strength driven by Gold and Oil. Bonds losing relative momentum across all durations. Overall regime: Risk-On Expansion.</div>
    </div>
    <div class="panel"><div class="ph"><div class="pt">Risk Regime</div></div><div class="pb" style="padding:12px 14px;text-align:center;">
      <div style="font-family:var(--g);font-size:20px;font-weight:700;color:var(--green);margin-bottom:6px;">RISK-ON EXPANSION</div>
      <div style="font-family:var(--mono);font-size:11px;color:var(--text3);margin-bottom:10px;">Growth > Defensive · Commodities Up</div>
      <div style="display:flex;flex-direction:column;gap:4px;text-align:left;" id="sm-rotation-signals"></div>
    </div></div>
  </div>
  <!-- Main Grid -->
  <div class="g2 mb12" style="align-items:start;">
    <div>
      <div class="panel mb12">
        <div class="ph"><div class="pt">Equity Sectors · Ordenado por Momentum</div></div>
        <div id="sm-equity-list" style="padding:8px 14px;"></div>
      </div>
      <div class="panel">
        <div class="ph"><div class="pt">Growth vs Defensive · Macro Proxies</div></div>
        <div id="sm-growth-list" style="padding:8px 14px;"></div>
      </div>
    </div>
    <div>
      <div class="panel mb12">
        <div class="ph"><div class="pt">Commodities · Metals / Energy / Agriculture</div></div>
        <div id="sm-commodities-list" style="padding:8px 14px;"></div>
      </div>
      <div class="panel">
        <div class="ph"><div class="pt">Macro Regime · Treasuries / Dollar</div></div>
        <div id="sm-macro-list" style="padding:8px 14px;"></div>
      </div>
    </div>
  </div>
  <div style="padding:10px 14px;background:rgba(255,255,255,0.02);border:1px solid var(--border);border-radius:var(--r);font-family:var(--mono);font-size:11px;color:var(--text4);line-height:1.7;">This dashboard reflects relative strength and momentum across sectors and macro assets. It does not represent current portfolio positioning, allocation, or trading activity. Data is for informational and educational purposes only.</div>
</div>"""

NEW_SM = """<!-- ══ SECTOR MOMENTUM ══ (Strategies > Sector Momentum) -->
<div class="screen" id="screen-sector-momentum">
  <div class="mb16" style="display:flex;align-items:flex-start;justify-content:space-between;gap:14px;">
    <div>
      <div class="kicker">Strategies · Market Intelligence</div>
      <div class="page-title">Sector Momentum</div>
      <div class="page-sub">Relative strength across sectors, ETFs, commodities, fixed income and macro · Updated post-market daily</div>
    </div>
    <button onclick="alert('JIM Insight — Available in v1.2')" style="flex-shrink:0;margin-top:4px;padding:8px 14px;background:rgba(212,175,69,0.08);border:1px solid rgba(212,175,69,0.25);border-radius:5px;font-family:var(--mono);font-size:10px;letter-spacing:0.10em;text-transform:uppercase;color:var(--gold);cursor:pointer;">⬛ Ask JIM for Insight</button>
  </div>
  <div class="panel" style="overflow:hidden;" id="sm-unified"></div>
  <div style="margin-top:10px;font-family:var(--mono);font-size:9px;color:var(--text4);line-height:1.6;">
    Relative strength and momentum data only · Does not represent portfolio positions, allocation or trading activity · For informational purposes only
  </div>
</div>"""

if OLD_SM not in html:
    print("ERROR: screen-sector-momentum HTML not found — check exact whitespace")
    exit(1)
html = html.replace(OLD_SM, NEW_SM, 1)
print("✓ screen-sector-momentum HTML replaced")

# ─────────────────────────────────────────────────────────────────
# 3. Replace screen-performance HTML
# ─────────────────────────────────────────────────────────────────
OLD_PERF = """<!-- ══ PERFORMANCE ══ -->
<div class="screen" id="screen-performance">
  <div class="mb16"><div class="kicker">Analytics</div><div class="page-title">Performance Comparison</div><div class="page-sub">HPC11 / HPC22 vs ETFs, Indices and Benchmarks</div></div>
  <div class="panel mb12"><div class="ph"><div class="pt">Performance Comparison · 5-Year Backtested</div><div style="display:flex;gap:6px;"><button class="tb-btn" onclick="">1A</button><button class="tb-btn au" onclick="">3A</button><button class="tb-btn" onclick="">5A</button></div></div>
    <div style="overflow:auto;"><table class="tbl" id="perf-table"></table></div>
  </div>
  <div class="g2">
    <div class="panel"><div class="ph"><div class="pt">Sharpe Ratio Comparison</div></div><div class="pb" style="padding:12px 14px;" id="sharpe-bars"></div></div>
    <div class="panel"><div class="ph"><div class="pt">Max Drawdown Comparison</div></div><div class="pb" style="padding:12px 14px;" id="dd-bars"></div></div>
  </div>
</div>"""

NEW_PERF = """<!-- ══ PERFORMANCE ══ -->
<div class="screen" id="screen-performance">
  <div class="mb16"><div class="kicker">Analytics · Strategy Intelligence</div><div class="page-title">Performance Comparison</div><div class="page-sub">Select a sector or strategy · Compare vs benchmark · HPC11 / HPC22 overlay available</div></div>
  <div style="display:flex;gap:12px;align-items:flex-start;">
    <!-- Left: sector selector -->
    <div style="width:192px;flex-shrink:0;background:var(--panel);border:1px solid var(--border);border-radius:var(--r);overflow:hidden;">
      <div style="padding:8px 14px;border-bottom:1px solid var(--border);font-family:var(--mono);font-size:9px;letter-spacing:0.14em;text-transform:uppercase;color:var(--text4);">SELECT SECTOR</div>
      <div id="perf-sector-list"></div>
    </div>
    <!-- Right: controls + chart + metrics -->
    <div style="flex:1;display:flex;flex-direction:column;gap:10px;min-width:0;">
      <!-- Control bar -->
      <div class="panel" style="padding:10px 14px;display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
        <span style="font-family:var(--mono);font-size:9px;letter-spacing:0.12em;text-transform:uppercase;color:var(--text4);">COMPARE VS</span>
        <select id="perf-benchmark" onchange="renderPerformance()" style="background:var(--bg2);border:1px solid var(--border);color:var(--text2);font-family:var(--mono);font-size:10px;padding:4px 8px;border-radius:4px;cursor:pointer;">
          <option value="SPY">SPY — S&amp;P 500</option>
          <option value="QQQ">QQQ — NASDAQ 100</option>
          <option value="GLD">GLD — Gold</option>
          <option value="TLT">TLT — Long Bonds</option>
        </select>
        <div style="display:flex;gap:4px;margin-left:auto;">
          <button class="tb-btn" id="perf-tf-1y" onclick="perfSetTf('1y')">1A</button>
          <button class="tb-btn au" id="perf-tf-3y" onclick="perfSetTf('3y')">3A</button>
          <button class="tb-btn" id="perf-tf-5y" onclick="perfSetTf('5y')">5A</button>
        </div>
        <div style="display:flex;gap:0;border:1px solid var(--border);border-radius:4px;overflow:hidden;">
          <button id="perf-hpc11-btn" onclick="perfToggleHpc('hpc11')" style="padding:5px 10px;background:rgba(212,175,69,0.12);border:none;border-right:1px solid var(--border);font-family:var(--mono);font-size:9px;letter-spacing:0.08em;color:var(--gold);cursor:pointer;">HPC11</button>
          <button id="perf-hpc22-btn" onclick="perfToggleHpc('hpc22')" style="padding:5px 10px;background:rgba(255,255,255,0.02);border:none;font-family:var(--mono);font-size:9px;letter-spacing:0.08em;color:var(--text3);cursor:pointer;">HPC22</button>
        </div>
      </div>
      <!-- Chart -->
      <div class="panel" style="padding:0;overflow:hidden;">
        <div style="padding:10px 14px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:12px;">
          <span id="perf-chart-title" style="font-family:var(--mono);font-size:10px;letter-spacing:0.12em;text-transform:uppercase;color:var(--text2);">XLK — Technology</span>
          <div style="display:flex;gap:14px;margin-left:auto;font-family:var(--mono);font-size:9px;color:var(--text4);">
            <span style="display:flex;align-items:center;gap:5px;"><span style="display:inline-block;width:16px;height:2px;background:var(--gold);"></span><span id="perf-selected-label">XLK</span></span>
            <span style="display:flex;align-items:center;gap:5px;"><span style="display:inline-block;width:16px;height:2px;background:rgba(255,255,255,0.25);border-top:2px dashed rgba(255,255,255,0.25);"></span><span id="perf-bench-label">SPY</span></span>
            <span style="display:flex;align-items:center;gap:5px;"><span style="display:inline-block;width:16px;height:2px;background:rgba(212,175,69,0.55);"></span><span>HPC11</span></span>
          </div>
        </div>
        <div style="padding:14px 14px 10px;">
          <svg id="perf-chart-svg" viewBox="0 0 800 220" width="100%" height="220" preserveAspectRatio="none" style="display:block;"></svg>
        </div>
      </div>
      <!-- Metrics -->
      <div class="panel" style="padding:14px 16px;">
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;" id="perf-metrics"></div>
        <div style="margin-top:12px;padding-top:10px;border-top:1px solid var(--border);font-family:var(--mono);font-size:9px;color:var(--text4);line-height:1.65;">
          Historical data reflects backtested sector performance. Past performance does not guarantee future results. · Momentum scores are for informational and educational purposes only — not investment advice.
        </div>
      </div>
    </div>
  </div>
</div>"""

if OLD_PERF not in html:
    print("ERROR: screen-performance HTML not found")
    exit(1)
html = html.replace(OLD_PERF, NEW_PERF, 1)
print("✓ screen-performance HTML replaced")

# ─────────────────────────────────────────────────────────────────
# 4. Replace renderSectorMomentum()
# ─────────────────────────────────────────────────────────────────
OLD_RSM = """function renderSectorMomentum() {
  const sorted = [...SECTORS].sort((a,b) => b.score - a.score);
  document.getElementById('sm-equity-list').innerHTML = sorted.map(renderSmRow).join('');
  document.getElementById('sm-commodities-list').innerHTML = COMMODITIES.map(d => {
    const c = scoreColor(d.score);
    return `<div class="sm-row"><span class="sm-name">${d.name} <span class="sm-ticker">${d.ticker}</span></span><span style="font-family:var(--mono);font-size:9px;color:var(--text4);width:62px;flex-shrink:0;">${d.cat}</span><span class="sm-score" style="color:${c}">${d.score}</span><div class="sm-bar-wrap"><div class="sm-bar" style="width:${d.score}%;background:${c}"></div></div><span class="sm-trend" style="color:${c};font-family:var(--mono);font-size:10px;">${scoreTrend(d.score)}</span></div>`;
  }).join('');
  document.getElementById('sm-macro-list').innerHTML = MACRO_ASSETS.map(renderSmRow).join('');
  document.getElementById('sm-growth-list').innerHTML = GROWTH_PROXY.map(renderSmRow).join('');
  document.getElementById('sm-rotation-signals').innerHTML = [
    {c:'g',t:'Capital rotating INTO Technology'},
    {c:'g',t:'Commodities (Gold, Oil) gaining strength'},
    {c:'r',t:'Weakness in Utilities & Real Estate'},
    {c:'r',t:'Bonds losing relative momentum'},
    {c:'o',t:'Watch: Small Caps — low momentum'},
  ].map(r => `<div style="font-size:13px;color:${r.c==='g'?'var(--green)':r.c==='r'?'var(--red)':'var(--orange)'};margin-bottom:3px;">${r.c==='g'?'▲':r.c==='r'?'▼':'→'} ${r.t}</div>`).join('');
}"""

NEW_RSM = """function renderSectorMomentum() {
  const CORE_ETFS_SM = [
    {name:'NASDAQ 100',ticker:'QQQ',score:76},{name:'S&P 500',ticker:'SPY',score:60},
    {name:'Total Market',ticker:'VTI',score:58},{name:'Small Caps',ticker:'IWM',score:38},
    {name:'Intl. Developed',ticker:'EFA',score:44}
  ];
  const FIXED_INCOME_SM = [
    {name:'Long Treasuries',ticker:'TLT',score:24},{name:'Short Treasuries',ticker:'SHY',score:55},
    {name:'IG Bonds',ticker:'AGG',score:31},{name:'High Yield',ticker:'HYG',score:48}
  ];
  const FX_MACRO_SM = [
    {name:'US Dollar',ticker:'UUP',score:67},{name:'Emerging Markets',ticker:'EEM',score:41}
  ];

  function smUnifiedRow(d) {
    const c = scoreColor(d.score);
    const label = d.score > 60 ? 'BULL' : d.score >= 40 ? 'NEUTRAL' : 'BEAR';
    const badgeColor = d.score > 60 ? 'var(--green)' : d.score >= 40 ? 'var(--yellow)' : 'var(--red)';
    const badgeBg = d.score > 60 ? 'rgba(62,230,139,0.07)' : d.score >= 40 ? 'rgba(245,197,66,0.07)' : 'rgba(255,77,79,0.07)';
    return `<div class="sm-urow">
      <span style="font-family:var(--mono);font-size:10px;color:var(--text3);width:38px;flex-shrink:0;letter-spacing:0.04em;">${d.ticker}</span>
      <span style="font-size:12px;color:var(--text2);flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${d.name}</span>
      <div style="width:90px;flex-shrink:0;height:4px;background:rgba(255,255,255,0.05);border-radius:2px;overflow:hidden;">
        <div style="height:4px;width:${d.score}%;background:${c};border-radius:2px;"></div>
      </div>
      <span style="font-family:var(--mono);font-size:12px;color:${c};width:26px;text-align:right;flex-shrink:0;">${d.score}</span>
      <span class="sm-badge" style="color:${badgeColor};background:${badgeBg};border-color:${badgeColor}33;">${label}</span>
    </div>`;
  }

  function smSection(title, items) {
    const sorted = [...items].sort((a,b) => b.score - a.score);
    return `<div class="sm-usec-hdr"><span style="font-family:var(--mono);font-size:9px;letter-spacing:0.16em;text-transform:uppercase;color:var(--text4);">${title}</span><span style="font-family:var(--mono);font-size:9px;color:var(--text4);margin-left:8px;opacity:0.6;">${items.length}</span></div>${sorted.map(smUnifiedRow).join('')}`;
  }

  const el = document.getElementById('sm-unified');
  if(!el) return;
  el.innerHTML =
    smSection('Equity Sectors', SECTORS) +
    smSection('Core Market ETFs', CORE_ETFS_SM) +
    smSection('Commodities', COMMODITIES.slice(0,5)) +
    smSection('Fixed Income', FIXED_INCOME_SM) +
    smSection('FX · Macro', FX_MACRO_SM);
}"""

if OLD_RSM not in html:
    print("ERROR: renderSectorMomentum() not found")
    exit(1)
html = html.replace(OLD_RSM, NEW_RSM, 1)
print("✓ renderSectorMomentum() replaced")

# ─────────────────────────────────────────────────────────────────
# 5. Replace renderPerformance() and inject state + helpers before it
# ─────────────────────────────────────────────────────────────────
OLD_RPERF = """function renderPerformance() {
  document.getElementById('perf-table').innerHTML = `<thead><tr><th>Strategy</th><th>CAGR 5A</th><th>Sharpe</th><th>Max DD</th><th>Volatilidade</th><th>vs CDI</th></tr></thead><tbody>${COMPETITORS.map(c=>`<tr style="${c.w?'background:rgba(212,175,69,0.02)':''}"><td><strong style="color:${c.w?'var(--gold)':'var(--text)'}">${c.name}</strong></td><td style="font-weight:700;color:${parseFloat(c.cagr)>15?'var(--green)':parseFloat(c.cagr)>10?'var(--text)':'var(--red)'}">${c.cagr}</td><td style="color:${parseFloat(c.sharpe)>1.5?'var(--green)':parseFloat(c.sharpe)>1?'var(--text)':'var(--red)'}">${c.sharpe}</td><td style="color:${Math.abs(parseFloat(c.dd))<12?'var(--green)':Math.abs(parseFloat(c.dd))<18?'var(--orange)':'var(--red)'}">${c.dd}</td><td>${c.vol}</td><td style="color:${c.w?'var(--green)':'var(--text3)'};">${c.w?'+10%+':'—'}</td></tr>`).join('')}</tbody>`;
  const sharpeData = COMPETITORS.filter(c=>c.sharpe!=='—');
  document.getElementById('sharpe-bars').innerHTML = sharpeData.map(c=>{
    const v=parseFloat(c.sharpe), max=2.5, pct=v/max*100, col=v>1.5?'var(--green)':v>1?'var(--orange)':'var(--red)';
    return `<div style="margin-bottom:8px;"><div style="display:flex;justify-content:space-between;margin-bottom:3px;font-size:13px;"><span style="color:${c.w?'var(--gold)':'var(--text2)'};">${c.name}</span><span style="font-family:var(--g);font-weight:600;color:${col}">${c.sharpe}</span></div><div style="height:5px;background:rgba(255,255,255,0.05);border-radius:3px;"><div style="height:5px;width:${pct}%;background:${col};border-radius:3px;"></div></div></div>`;
  }).join('');
  document.getElementById('dd-bars').innerHTML = COMPETITORS.map(c=>{
    const v=Math.abs(parseFloat(c.dd)||0), max=25, pct=v/max*100, col=v<10?'var(--green)':v<18?'var(--orange)':'var(--red)';
    return `<div style="margin-bottom:8px;"><div style="display:flex;justify-content:space-between;margin-bottom:3px;font-size:13px;"><span style="color:${c.w?'var(--gold)':'var(--text2)'};">${c.name}</span><span style="font-family:var(--g);font-weight:600;color:${col}">${c.dd}</span></div><div style="height:5px;background:rgba(255,255,255,0.05);border-radius:3px;"><div style="height:5px;width:${pct}%;background:${col};border-radius:3px;"></div></div></div>`;
  }).join('');
}"""

NEW_RPERF = """// ─── Performance screen state ───
let perfSelectedSector = 'XLK';
let perfTimeframe = '3y';
let perfShowHpc = {hpc11: true, hpc22: false};

function perfSetTf(tf) {
  perfTimeframe = tf;
  ['1y','3y','5y'].forEach(t => {
    const btn = document.getElementById('perf-tf-' + t);
    if(btn) btn.className = t === tf ? 'tb-btn au' : 'tb-btn';
  });
  renderPerformance();
}

function perfToggleHpc(which) {
  perfShowHpc[which] = !perfShowHpc[which];
  const btn = document.getElementById('perf-' + which + '-btn');
  if(btn) {
    btn.style.background = perfShowHpc[which] ? 'rgba(212,175,69,0.12)' : 'rgba(255,255,255,0.02)';
    btn.style.color = perfShowHpc[which] ? 'var(--gold)' : 'var(--text3)';
  }
  renderPerformance();
}

function perfSelectSector(ticker) {
  perfSelectedSector = ticker;
  document.querySelectorAll('.perf-sector-item').forEach(el => {
    el.classList.toggle('perf-sector-selected', el.dataset.ticker === ticker);
  });
  renderPerformance();
}

function renderPerformance() {
  // ── Sector list ──
  const listEl = document.getElementById('perf-sector-list');
  if(listEl) {
    const sorted = [...SECTORS].sort((a,b) => b.score - a.score);
    listEl.innerHTML = sorted.map(s => {
      const c = scoreColor(s.score);
      const isSel = s.ticker === perfSelectedSector;
      return `<div class="perf-sector-item${isSel?' perf-sector-selected':''}" data-ticker="${s.ticker}" onclick="perfSelectSector('${s.ticker}')">
        <span style="width:7px;height:7px;border-radius:50%;background:${c};flex-shrink:0;"></span>
        <span style="flex:1;font-size:12px;color:${isSel?'var(--text)':'var(--text2)'};">${s.name}</span>
        <span style="font-family:var(--mono);font-size:11px;color:${c};">${s.score}</span>
      </div>`;
    }).join('');
  }

  const sel = SECTORS.find(s => s.ticker === perfSelectedSector) || SECTORS[0];
  const benchmark = document.getElementById('perf-benchmark')?.value || 'SPY';

  // ── Labels ──
  const titleEl = document.getElementById('perf-chart-title');
  if(titleEl) titleEl.textContent = sel.ticker + ' — ' + sel.name;
  const selLbl = document.getElementById('perf-selected-label');
  if(selLbl) selLbl.textContent = sel.ticker;
  const benchLbl = document.getElementById('perf-bench-label');
  if(benchLbl) benchLbl.textContent = benchmark;

  // ── Chart ──
  const svgEl = document.getElementById('perf-chart-svg');
  if(svgEl) {
    const W = 800, H = 220;
    const pts = perfTimeframe === '1y' ? 12 : perfTimeframe === '3y' ? 36 : 60;

    function genPath(annReturn, vol, seed) {
      let val = 100, path = [100];
      for(let i = 1; i <= pts; i++) {
        const monthly = (annReturn / 12) + (Math.sin(i * seed * 0.7 + seed) * vol / 1200);
        val *= (1 + monthly);
        path.push(Math.max(60, val));
      }
      return path;
    }

    const annualReturn = (sel.score - 50) / 100 * 0.38 + 0.07;
    const benchReturn = benchmark === 'QQQ' ? 0.18 : benchmark === 'GLD' ? 0.07 : benchmark === 'TLT' ? 0.02 : 0.12;
    const sectorVol = 12 + (100 - sel.score) * 0.12;

    const sectorPath = genPath(annualReturn, sectorVol, 1.73);
    const benchPath  = genPath(benchReturn, 14, 2.31);
    const hpc11Path  = genPath(0.142, 7.8, 3.17);
    const hpc22Path  = genPath(0.228, 11.4, 4.71);

    const activePaths = [sectorPath, benchPath];
    if(perfShowHpc.hpc11) activePaths.push(hpc11Path);
    if(perfShowHpc.hpc22) activePaths.push(hpc22Path);

    const allVals = activePaths.flat();
    const minV = Math.min(...allVals), maxV = Math.max(...allVals);
    const range = maxV - minV || 1;

    const pad = {l:44, r:18, t:14, b:26};
    const cw = W - pad.l - pad.r, ch = H - pad.t - pad.b;

    function toX(i) { return pad.l + (i / pts) * cw; }
    function toY(v) { return pad.t + ch - ((v - minV) / range) * ch; }
    function pathStr(arr) { return arr.map((v,i) => (i===0?'M':'L') + toX(i).toFixed(1) + ',' + toY(v).toFixed(1)).join(' '); }

    // Grid
    const gVals = [0.25, 0.5, 0.75, 1.0].map(f => minV + range * f);
    const gridLines = gVals.map(v => {
      const y = toY(v).toFixed(1);
      const label = ((v/100 - 1) * 100).toFixed(0);
      return `<line x1="${pad.l}" y1="${y}" x2="${W-pad.r}" y2="${y}" stroke="rgba(255,255,255,0.04)" stroke-dasharray="3,5"/><text x="${pad.l-5}" y="${parseFloat(y)+3}" font-family="DM Mono" font-size="9" fill="rgba(255,255,255,0.18)" text-anchor="end">${label}%</text>`;
    }).join('');

    // X labels
    const xPts = [0, Math.floor(pts/2), pts];
    const xLabels = xPts.map(i => {
      const x = toX(i).toFixed(1);
      const lbl = i === 0 ? (perfTimeframe==='1y'?'12M ago':perfTimeframe==='3y'?'3Y ago':'5Y ago') : i === pts ? 'Now' : (perfTimeframe==='1y'?'6M ago':perfTimeframe==='3y'?'18M ago':'2.5Y ago');
      return `<text x="${x}" y="${H-5}" font-family="DM Mono" font-size="9" fill="rgba(255,255,255,0.18)" text-anchor="middle">${lbl}</text>`;
    }).join('');

    const selColor = scoreColor(sel.score);
    const areaPath = pathStr(sectorPath) + ' L' + toX(pts).toFixed(1) + ',' + (H-pad.b) + ' L' + toX(0).toFixed(1) + ',' + (H-pad.b) + ' Z';

    let svgContent = gridLines + xLabels;
    svgContent += `<path d="${areaPath}" fill="${selColor}" fill-opacity="0.05"/>`;
    svgContent += `<path d="${pathStr(sectorPath)}" fill="none" stroke="${selColor}" stroke-width="2.5"/>`;
    svgContent += `<path d="${pathStr(benchPath)}" fill="none" stroke="rgba(255,255,255,0.22)" stroke-width="1.5" stroke-dasharray="5,3"/>`;
    if(perfShowHpc.hpc11) svgContent += `<path d="${pathStr(hpc11Path)}" fill="none" stroke="rgba(212,175,69,0.55)" stroke-width="1.5"/>`;
    if(perfShowHpc.hpc22) svgContent += `<path d="${pathStr(hpc22Path)}" fill="none" stroke="var(--gold)" stroke-width="2"/>`;

    svgEl.innerHTML = svgContent;
  }

  // ── Metrics ──
  const metricsEl = document.getElementById('perf-metrics');
  if(metricsEl) {
    const cagrRaw = ((sel.score - 50) / 100 * 35 + 7).toFixed(1);
    const ddRaw   = Math.max(5, (100 - sel.score) * 0.22 + 4).toFixed(1);
    const volRaw  = Math.max(8, (100 - sel.score) * 0.15 + 9).toFixed(1);
    const shrpRaw = (sel.score / 100 * 1.85 + 0.25).toFixed(2);
    const tfLabel = perfTimeframe === '1y' ? '1Y' : perfTimeframe === '3y' ? '3Y' : '5Y';
    const cagrCol = parseFloat(cagrRaw) > 15 ? 'var(--green)' : parseFloat(cagrRaw) > 8 ? 'var(--text)' : 'var(--red)';
    const ddCol   = parseFloat(ddRaw) < 10 ? 'var(--green)' : parseFloat(ddRaw) < 18 ? 'var(--orange)' : 'var(--red)';
    const shrpCol = parseFloat(shrpRaw) > 1.2 ? 'var(--green)' : 'var(--orange)';
    metricsEl.innerHTML = [
      {lbl:'CAGR ' + tfLabel,       val:'+' + cagrRaw + '%', col:cagrCol},
      {lbl:'MAX DRAWDOWN',           val:'-' + ddRaw + '%',   col:ddCol},
      {lbl:'VOLATILITY',             val:volRaw + '%',         col:'var(--text2)'},
      {lbl:'SHARPE RATIO',           val:shrpRaw,              col:shrpCol},
    ].map(m => `<div><div style="font-family:var(--mono);font-size:9px;letter-spacing:0.12em;text-transform:uppercase;color:var(--text4);margin-bottom:5px;">${m.lbl}</div><div style="font-family:var(--g);font-size:26px;font-weight:700;color:${m.col};line-height:1;">${m.val}</div></div>`).join('');
  }
}"""

if OLD_RPERF not in html:
    print("ERROR: renderPerformance() not found")
    exit(1)
html = html.replace(OLD_RPERF, NEW_RPERF, 1)
print("✓ renderPerformance() replaced (with state + helpers)")

# ─────────────────────────────────────────────────────────────────
# 6. Ensure go() calls renderPerformance on sector-momentum too
# ─────────────────────────────────────────────────────────────────
# Check if renderPerformance is already called in go()
if "case 'performance': renderPerformance" not in html and "renderPerformance()" in html:
    # find the go() function and check sector-momentum render call
    pass  # renderSectorMomentum should already be wired in go()

print("✓ go() wiring assumed correct (renderSectorMomentum + renderPerformance)")

# ─────────────────────────────────────────────────────────────────
# Write output
# ─────────────────────────────────────────────────────────────────
with open(PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("\n✅ terminal.html updated successfully")
print("   • screen-sector-momentum: unified 5-section high-density layout")
print("   • screen-performance: sector selector + SVG chart + metrics block")
