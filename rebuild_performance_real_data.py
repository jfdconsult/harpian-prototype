"""
Update terminal.html:
1. Add <script src="harpian_strategies_data.js"> reference
2. Rewrite renderPerformance() to use HPC11_STRATEGIES real data
3. Add HPC11/HPC22 tab toggle in Performance screen left panel
"""

PATH = r"C:\dev\harpian-prototype\terminal.html"

with open(PATH, "r", encoding="utf-8") as f:
    html = f.read()

# ─── 1. Inject script tag before closing </head> or before first <script> ───
SCRIPT_TAG = '<script src="harpian_strategies_data.js"></script>'
if SCRIPT_TAG not in html:
    # Insert before the first <script> tag
    first_script = html.find('<script')
    if first_script != -1:
        html = html[:first_script] + SCRIPT_TAG + '\n' + html[first_script:]
        print("OK script tag injected")
    else:
        print("ERROR: no <script> tag found")
        exit(1)
else:
    print("OK script tag already present")

# ─── 2. Replace Performance screen HTML ───
OLD_PERF_HTML = '''<!-- ══ PERFORMANCE ══ -->
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
</div>'''

NEW_PERF_HTML = '''<!-- ══ PERFORMANCE ══ -->
<div class="screen" id="screen-performance">
  <div class="mb16"><div class="kicker">Analytics · Strategy Intelligence</div><div class="page-title">Performance Comparison</div><div class="page-sub">Dados reais AlphaDroid · HPC11 (11 estratégias) · HPC22 (22 sub-estratégias) · Compare vs S&amp;P 500</div></div>
  <div style="display:flex;gap:12px;align-items:flex-start;">
    <!-- Left: strategy selector -->
    <div style="width:210px;flex-shrink:0;background:var(--panel);border:1px solid var(--border);border-radius:var(--r);overflow:hidden;">
      <!-- Tab toggle HPC11 / HPC22 -->
      <div style="display:flex;border-bottom:1px solid var(--border);">
        <button id="perf-tab-hpc11" onclick="perfSetTab('hpc11')" style="flex:1;padding:8px 4px;background:rgba(212,175,69,0.08);border:none;border-right:1px solid var(--border);font-family:var(--mono);font-size:9px;letter-spacing:0.1em;color:var(--gold);cursor:pointer;">HPC11</button>
        <button id="perf-tab-hpc22" onclick="perfSetTab('hpc22')" style="flex:1;padding:8px 4px;background:transparent;border:none;font-family:var(--mono);font-size:9px;letter-spacing:0.1em;color:var(--text4);cursor:pointer;">HPC22</button>
      </div>
      <div id="perf-strat-list" style="overflow-y:auto;max-height:460px;"></div>
    </div>
    <!-- Right: controls + chart + metrics + year table -->
    <div style="flex:1;display:flex;flex-direction:column;gap:10px;min-width:0;">
      <!-- Control bar -->
      <div class="panel" style="padding:10px 14px;display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
        <div style="display:flex;gap:4px;">
          <button class="tb-btn" id="perf-tf-5y" onclick="perfSetTf('5y')">5A</button>
          <button class="tb-btn" id="perf-tf-10y" onclick="perfSetTf('10y')">10A</button>
          <button class="tb-btn au" id="perf-tf-all" onclick="perfSetTf('all')">Tudo</button>
        </div>
        <div style="margin-left:auto;display:flex;align-items:center;gap:8px;">
          <span style="font-family:var(--mono);font-size:9px;color:var(--text4);">vs SPY</span>
          <span id="perf-spy-badge" style="font-family:var(--mono);font-size:10px;color:var(--text3);">—</span>
        </div>
        <div style="font-family:var(--mono);font-size:9px;color:var(--text4);">Last: <span id="perf-last-trade" style="color:var(--text2);">—</span></div>
        <div style="font-family:var(--mono);font-size:9px;color:var(--text4);">Score: <span id="perf-score-badge" style="color:var(--gold);">—</span></div>
      </div>
      <!-- Chart -->
      <div class="panel" style="padding:0;overflow:hidden;">
        <div style="padding:10px 14px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:12px;flex-wrap:wrap;">
          <span id="perf-chart-title" style="font-family:var(--mono);font-size:10px;letter-spacing:0.12em;text-transform:uppercase;color:var(--text2);">—</span>
          <div style="display:flex;gap:14px;margin-left:auto;font-family:var(--mono);font-size:9px;color:var(--text4);">
            <span style="display:flex;align-items:center;gap:5px;"><span style="display:inline-block;width:16px;height:2px;background:var(--gold);"></span><span id="perf-selected-label">Strategy</span></span>
            <span style="display:flex;align-items:center;gap:5px;"><span style="display:inline-block;width:16px;height:2px;background:rgba(255,255,255,0.25);border-top:2px dashed rgba(255,255,255,0.25);"></span>SPY</span>
          </div>
        </div>
        <div style="padding:12px 14px 8px;">
          <svg id="perf-chart-svg" viewBox="0 0 800 200" width="100%" height="200" preserveAspectRatio="none" style="display:block;"></svg>
        </div>
      </div>
      <!-- Metrics row -->
      <div class="panel" style="padding:12px 16px;">
        <div style="display:grid;grid-template-columns:repeat(7,1fr);gap:12px;margin-bottom:12px;" id="perf-metrics"></div>
        <!-- Year-by-year table -->
        <div style="border-top:1px solid var(--border);padding-top:12px;">
          <div style="font-family:var(--mono);font-size:9px;letter-spacing:0.14em;text-transform:uppercase;color:var(--text4);margin-bottom:8px;">Retorno por Ano vs S&amp;P 500</div>
          <div id="perf-year-table" style="display:flex;flex-wrap:wrap;gap:4px;"></div>
        </div>
        <div style="margin-top:10px;font-family:var(--mono);font-size:9px;color:var(--text4);line-height:1.65;border-top:1px solid var(--border);padding-top:8px;">
          Dados históricos refletem performance backtestada do AlphaDroid. Performance passada não garante resultados futuros. · Uso educacional e informativo apenas — não constitui recomendação de investimento.
        </div>
      </div>
    </div>
  </div>
</div>'''

if OLD_PERF_HTML not in html:
    print("ERROR: old Performance HTML not found")
    exit(1)
html = html.replace(OLD_PERF_HTML, NEW_PERF_HTML, 1)
print("OK Performance HTML replaced")

# ─── 3. Replace renderPerformance() and helpers ───
OLD_RPERF = '''// ─── Performance screen state ───
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
}'''

NEW_RPERF = '''// ─── Performance screen state ───
let perfSelectedId = 'S26';
let perfCurrentTab = 'hpc11';
let perfTimeframe = 'all';

function perfSetTab(tab) {
  perfCurrentTab = tab;
  const t11 = document.getElementById('perf-tab-hpc11');
  const t22 = document.getElementById('perf-tab-hpc22');
  if(t11) { t11.style.background = tab==='hpc11'?'rgba(212,175,69,0.08)':'transparent'; t11.style.color = tab==='hpc11'?'var(--gold)':'var(--text4)'; }
  if(t22) { t22.style.background = tab==='hpc22'?'rgba(212,175,69,0.08)':'transparent'; t22.style.color = tab==='hpc22'?'var(--gold)':'var(--text4)'; }
  // default selection
  const pool = tab === 'hpc11' ? (typeof HPC11_STRATEGIES !== 'undefined' ? HPC11_STRATEGIES : []) : (typeof HPC22_STRATEGIES !== 'undefined' ? HPC22_STRATEGIES : []);
  if(pool.length) perfSelectedId = pool[0].id;
  renderPerformance();
}

function perfSetTf(tf) {
  perfTimeframe = tf;
  ['5y','10y','all'].forEach(t => {
    const btn = document.getElementById('perf-tf-' + t);
    if(btn) btn.className = t === tf ? 'tb-btn au' : 'tb-btn';
  });
  renderPerformance();
}

function perfSelectStrat(id) {
  perfSelectedId = id;
  document.querySelectorAll('.perf-strat-item').forEach(el => {
    el.classList.toggle('perf-sector-selected', el.dataset.id === id);
  });
  renderPerformance();
}

// Build cumulative return series from year-by-year data
function perfBuildSeries(years, tf) {
  const allYears = Object.keys(years).map(Number).sort((a,b)=>a-b);
  let startYear;
  const now = 2025;
  if(tf === '5y') startYear = now - 4;
  else if(tf === '10y') startYear = now - 9;
  else startYear = allYears[0];
  const filtered = allYears.filter(y => y >= startYear && y <= now);
  let stratVal = 100, spyVal = 100;
  const stratSeries = [100], spySeries = [100];
  for(const yr of filtered) {
    const d = years[yr] || years[String(yr)];
    if(!d) continue;
    stratVal *= (1 + d.s / 100);
    spyVal   *= (1 + d.spy / 100);
    stratSeries.push(+stratVal.toFixed(2));
    spySeries.push(+spyVal.toFixed(2));
  }
  return {stratSeries, spySeries, labels: ['Start', ...filtered.map(String)]};
}

function renderPerformance() {
  const pool = perfCurrentTab === 'hpc11'
    ? (typeof HPC11_STRATEGIES !== 'undefined' ? HPC11_STRATEGIES : [])
    : (typeof HPC22_STRATEGIES !== 'undefined' ? HPC22_STRATEGIES : []);

  // ── Strategy list ──
  const listEl = document.getElementById('perf-strat-list');
  if(listEl && pool.length) {
    listEl.innerHTML = pool.map(s => {
      const isSel = s.id === perfSelectedId;
      const cagrVal = parseFloat(s.cagr_all) || 0;
      const cagrCol = cagrVal > 20 ? 'var(--green)' : cagrVal > 10 ? 'var(--yellow)' : 'var(--red)';
      return `<div class="perf-strat-item perf-sector-item${isSel?' perf-sector-selected':''}" data-id="${s.id}" onclick="perfSelectStrat('${s.id}')">
        <div style="flex:1;min-width:0;">
          <div style="font-size:11px;color:${isSel?'var(--text)':'var(--text2)'};white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${s.label}</div>
          <div style="font-family:var(--mono);font-size:9px;color:var(--text4);margin-top:1px;">${s.id}${s.category?' · '+s.category:s.sector?' · '+s.sector:''}</div>
        </div>
        <span style="font-family:var(--mono);font-size:11px;color:${cagrCol};flex-shrink:0;">${s.cagr_all ? s.cagr_all+'%' : '—'}</span>
      </div>`;
    }).join('');
  }

  const strat = pool.find(s => s.id === perfSelectedId) || pool[0];
  if(!strat) return;

  // ── Header info ──
  const titleEl = document.getElementById('perf-chart-title');
  if(titleEl) titleEl.textContent = strat.id + ' — ' + strat.label;
  const selLbl = document.getElementById('perf-selected-label');
  if(selLbl) selLbl.textContent = strat.id;
  const ltEl = document.getElementById('perf-last-trade');
  if(ltEl) ltEl.textContent = strat.last_trade || '—';
  const scEl = document.getElementById('perf-score-badge');
  if(scEl) { const sc = parseFloat(strat.score)||0; scEl.textContent = sc ? sc.toFixed(1) : '—'; scEl.style.color = sc > 80 ? 'var(--green)' : sc > 40 ? 'var(--gold)' : 'var(--red)'; }
  const spyBadge = document.getElementById('perf-spy-badge');
  if(spyBadge) {
    const diff = parseFloat(strat.cagr_all) - parseFloat(strat.spy_cagr_all);
    if(!isNaN(diff)) { spyBadge.textContent = (diff>=0?'+':'')+diff.toFixed(1)+'% vs SPY (CAGR all)'; spyBadge.style.color = diff>=0?'var(--green)':'var(--red)'; }
  }

  // ── Chart from real year data ──
  const svgEl = document.getElementById('perf-chart-svg');
  if(svgEl && strat.years && Object.keys(strat.years).length > 0) {
    const {stratSeries, spySeries, labels} = perfBuildSeries(strat.years, perfTimeframe);
    const W = 800, H = 200;
    const allVals = [...stratSeries, ...spySeries];
    const minV = Math.min(...allVals), maxV = Math.max(...allVals);
    const range = maxV - minV || 1;
    const pad = {l:52, r:18, t:12, b:24};
    const cw = W - pad.l - pad.r, ch = H - pad.t - pad.b;
    const n = stratSeries.length - 1;
    function toX(i) { return pad.l + (n > 0 ? (i/n)*cw : 0); }
    function toY(v) { return pad.t + ch - ((v - minV) / range) * ch; }
    function pathStr(arr) { return arr.map((v,i)=>(i===0?'M':'L')+toX(i).toFixed(1)+','+toY(v).toFixed(1)).join(' '); }

    // Grid lines
    const gVals = [0.25, 0.5, 0.75, 1.0].map(f => minV + range * f);
    const grid = gVals.map(v => {
      const y = toY(v).toFixed(1);
      const lbl = ((v/100-1)*100).toFixed(0);
      return `<line x1="${pad.l}" y1="${y}" x2="${W-pad.r}" y2="${y}" stroke="rgba(255,255,255,0.04)" stroke-dasharray="3,5"/><text x="${pad.l-4}" y="${parseFloat(y)+3}" font-family="DM Mono" font-size="8" fill="rgba(255,255,255,0.18)" text-anchor="end">${lbl}%</text>`;
    }).join('');

    // X labels (first, mid, last year)
    const xIdx = [0, Math.floor(n/2), n];
    const xLbls = xIdx.map(i => `<text x="${toX(i).toFixed(1)}" y="${H-4}" font-family="DM Mono" font-size="8" fill="rgba(255,255,255,0.18)" text-anchor="middle">${labels[i]||''}</text>`).join('');

    const areaPath = pathStr(stratSeries) + ' L'+toX(n).toFixed(1)+','+(H-pad.b)+' L'+toX(0).toFixed(1)+','+(H-pad.b)+' Z';
    let svg = grid + xLbls;
    svg += `<path d="${areaPath}" fill="var(--gold)" fill-opacity="0.04"/>`;
    svg += `<path d="${pathStr(stratSeries)}" fill="none" stroke="var(--gold)" stroke-width="2.5"/>`;
    svg += `<path d="${pathStr(spySeries)}" fill="none" stroke="rgba(255,255,255,0.22)" stroke-width="1.5" stroke-dasharray="5,3"/>`;
    svgEl.innerHTML = svg;
  }

  // ── Metrics ──
  const metricsEl = document.getElementById('perf-metrics');
  if(metricsEl) {
    const tf = perfTimeframe;
    const cagrVal = tf==='5y' ? strat.cagr_5y : tf==='10y' ? strat.cagr_10y : strat.cagr_all;
    const cagrF = parseFloat(cagrVal)||0;
    const ddF = parseFloat(strat.maxdd)||0;
    const shrpF = parseFloat(strat.sharpe)||0;
    const sortF = parseFloat(strat.sortino)||0;
    const volF = parseFloat(strat.vol)||0;
    const cagrCol = cagrF>20?'var(--green)':cagrF>10?'var(--text)':'var(--red)';
    const ddCol = ddF<15?'var(--green)':ddF<30?'var(--orange)':'var(--red)';
    const shrpCol = shrpF>1.0?'var(--green)':shrpF>0.5?'var(--orange)':'var(--red)';
    const tfLbl = tf==='5y'?'5Y':tf==='10y'?'10Y':'All';
    metricsEl.innerHTML = [
      {lbl:'CAGR '+tfLbl,    val:(cagrF>=0?'+':'')+cagrF.toFixed(1)+'%', col:cagrCol},
      {lbl:'1Y',             val:(parseFloat(strat.cagr_1y)>=0?'+':'')+parseFloat(strat.cagr_1y||0).toFixed(1)+'%', col:parseFloat(strat.cagr_1y)>=0?'var(--green)':'var(--red)'},
      {lbl:'3Y CAGR',        val:(parseFloat(strat.cagr_3y)>=0?'+':'')+parseFloat(strat.cagr_3y||0).toFixed(1)+'%', col:'var(--text2)'},
      {lbl:'MAX DD',         val:'-'+ddF.toFixed(1)+'%', col:ddCol},
      {lbl:'SHARPE',         val:shrpF.toFixed(2), col:shrpCol},
      {lbl:'SORTINO',        val:sortF.toFixed(2), col:'var(--text2)'},
      {lbl:'YTD',            val:(parseFloat(strat.ytd)>=0?'+':'')+parseFloat(strat.ytd||0).toFixed(1)+'%', col:parseFloat(strat.ytd)>=0?'var(--green)':'var(--red)'},
    ].map(m=>`<div><div style="font-family:var(--mono);font-size:8px;letter-spacing:0.12em;text-transform:uppercase;color:var(--text4);margin-bottom:4px;">${m.lbl}</div><div style="font-family:var(--g);font-size:20px;font-weight:700;color:${m.col};line-height:1;">${m.val}</div></div>`).join('');
  }

  // ── Year-by-year table ──
  const yrEl = document.getElementById('perf-year-table');
  if(yrEl && strat.years) {
    const years = Object.keys(strat.years).map(Number).sort((a,b)=>b-a).slice(0,15);
    yrEl.innerHTML = years.map(yr => {
      const d = strat.years[yr] || strat.years[String(yr)];
      if(!d) return '';
      const s = d.s, spy = d.spy;
      const sCol = s >= 0 ? 'var(--green)' : 'var(--red)';
      const excess = s - spy;
      const excCol = excess >= 0 ? 'var(--green)' : 'var(--red)';
      return `<div style="background:rgba(255,255,255,0.02);border:1px solid var(--border);border-radius:4px;padding:5px 8px;min-width:64px;">
        <div style="font-family:var(--mono);font-size:8px;color:var(--text4);">${yr}</div>
        <div style="font-family:var(--mono);font-size:11px;font-weight:600;color:${sCol};">${s>=0?'+':''}${s.toFixed(1)}%</div>
        <div style="font-family:var(--mono);font-size:8px;color:${excCol};">${excess>=0?'+':''}${excess.toFixed(1)}</div>
      </div>`;
    }).join('');
  }
}'''

if OLD_RPERF not in html:
    print("ERROR: old renderPerformance block not found")
    exit(1)
html = html.replace(OLD_RPERF, NEW_RPERF, 1)
print("OK renderPerformance() replaced with real data version")

# ─── Write output ───
with open(PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("\nDone — terminal.html updated")
print("  Performance screen now uses real AlphaDroid data")
print("  HPC11: 11 strategies | HPC22: 22 sub-strategies")
print("  Chart: real cumulative returns from year-by-year data")
print("  Metrics: CAGR / 1Y / 3Y / MaxDD / Sharpe / Sortino / YTD")
print("  Year table: last 15 years, strategy vs SPY excess return")
