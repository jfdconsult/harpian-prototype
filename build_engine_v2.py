import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HARPIAN — Market Trend Decision Engine v2.0</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600;700&family=Playfair+Display:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{--bg:#09090f;--bg2:#0f0f1a;--bg3:#13131f;--surface:#1a1a2e;--surface2:#1e1e35;--border:#2a2a45;--border2:#333355;--accent:#4f6ef7;--accent2:#6b8aff;--accent-glow:rgba(79,110,247,0.15);--gold:#c8a96e;--gold2:#e0c080;--text:#e8e8f0;--text2:#a0a0c0;--text3:#666688;--bull:#22c55e;--bull-dim:rgba(34,197,94,0.15);--cautious-bull:#84cc16;--neutral:#94a3b8;--cautious-bear:#f97316;--bear:#ef4444;--bear-dim:rgba(239,68,68,0.15);--strong-bear:#dc2626;--mono:'IBM Plex Mono',monospace;--sans:'IBM Plex Sans',sans-serif;--serif:'Playfair Display',serif}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--bg);color:var(--text);font-family:var(--sans);font-size:14px;line-height:1.7;overflow-x:hidden}
.cover{min-height:100vh;display:flex;flex-direction:column;justify-content:center;align-items:flex-start;padding:80px 10%;position:relative;background:linear-gradient(135deg,#09090f 0%,#0d0d1f 60%,#0a0a18 100%);overflow:hidden}
.cover::before{content:'';position:absolute;top:-200px;right:-200px;width:600px;height:600px;border-radius:50%;background:radial-gradient(circle,rgba(79,110,247,0.08) 0%,transparent 70%);pointer-events:none}
.cover-grid{position:absolute;top:0;right:0;width:45%;height:100%;background-image:linear-gradient(rgba(79,110,247,0.04) 1px,transparent 1px),linear-gradient(90deg,rgba(79,110,247,0.04) 1px,transparent 1px);background-size:40px 40px;mask-image:linear-gradient(to left,rgba(0,0,0,0.4),transparent);pointer-events:none}
.cover-tag{font-family:var(--mono);font-size:11px;letter-spacing:0.2em;color:var(--accent);text-transform:uppercase;margin-bottom:32px;opacity:0.8}
.cover-title{font-family:var(--serif);font-size:clamp(32px,5vw,64px);font-weight:700;color:var(--text);line-height:1.15;max-width:800px;margin-bottom:16px}
.cover-title span{color:var(--gold)}
.cover-sub{font-family:var(--sans);font-size:16px;color:var(--text2);max-width:620px;margin-bottom:48px;font-weight:300;line-height:1.6}
.cover-meta{display:flex;gap:48px;flex-wrap:wrap}
.cover-meta-item{display:flex;flex-direction:column;gap:4px}
.cover-meta-label{font-family:var(--mono);font-size:10px;letter-spacing:0.15em;color:var(--text3);text-transform:uppercase}
.cover-meta-value{font-family:var(--mono);font-size:13px;color:var(--gold)}
.doc-body{max-width:1200px;margin:0 auto;padding:0 5%}
.section{padding:80px 0;border-bottom:1px solid var(--border)}
.section:last-child{border-bottom:none}
.section-tag{font-family:var(--mono);font-size:10px;letter-spacing:0.25em;color:var(--accent);text-transform:uppercase;margin-bottom:12px;opacity:0.7}
.section-title{font-family:var(--serif);font-size:clamp(22px,3vw,36px);color:var(--text);margin-bottom:8px;line-height:1.2}
.section-title span{color:var(--gold)}
.section-lead{font-size:15px;color:var(--text2);max-width:700px;margin-bottom:48px;line-height:1.7;font-weight:300}
h3{font-family:var(--sans);font-size:13px;letter-spacing:0.12em;text-transform:uppercase;color:var(--gold);margin:40px 0 16px;font-weight:600}
h4{font-family:var(--mono);font-size:12px;color:var(--accent2);margin:28px 0 12px;letter-spacing:0.05em}
p{color:var(--text2);margin-bottom:16px;font-size:14px;line-height:1.75}
.table-wrap{overflow-x:auto;margin:24px 0 40px;border-radius:6px;border:1px solid var(--border)}
table{width:100%;border-collapse:collapse;font-size:13px}
thead tr{background:var(--surface)}
th{font-family:var(--mono);font-size:10px;letter-spacing:0.12em;text-transform:uppercase;color:var(--text3);padding:12px 16px;text-align:left;border-bottom:1px solid var(--border);font-weight:500;white-space:nowrap}
td{padding:12px 16px;border-bottom:1px solid var(--border);color:var(--text2);vertical-align:top}
tr:last-child td{border-bottom:none}
tr:hover td{background:rgba(79,110,247,0.03)}
td.mono{font-family:var(--mono);font-size:12px;color:var(--text)}
td.bold{color:var(--text);font-weight:500}
.state-sb{color:#22c55e;font-weight:600;font-family:var(--mono);font-size:12px}
.state-b{color:#4ade80;font-weight:600;font-family:var(--mono);font-size:12px}
.state-cb{color:#a3e635;font-weight:600;font-family:var(--mono);font-size:12px}
.state-n{color:#94a3b8;font-weight:600;font-family:var(--mono);font-size:12px}
.state-cbe{color:#fb923c;font-weight:600;font-family:var(--mono);font-size:12px}
.state-be{color:#f87171;font-weight:600;font-family:var(--mono);font-size:12px}
.state-sbe{color:#ef4444;font-weight:600;font-family:var(--mono);font-size:12px}
.score-bar-wrap{display:flex;align-items:center;gap:12px;margin:8px 0}
.score-bar-label{font-family:var(--mono);font-size:11px;color:var(--text3);width:180px;flex-shrink:0}
.score-bar-track{flex:1;height:6px;background:var(--surface2);border-radius:3px;overflow:hidden}
.score-bar-fill{height:100%;border-radius:3px}
.score-bar-val{font-family:var(--mono);font-size:11px;color:var(--text);width:40px;text-align:right;flex-shrink:0}
.code-block{background:var(--bg2);border:1px solid var(--border);border-left:3px solid var(--accent);border-radius:0 4px 4px 0;padding:20px 24px;margin:20px 0;font-family:var(--mono);font-size:12px;color:var(--text2);overflow-x:auto;line-height:1.8}
.code-block .kw{color:var(--accent2)}.code-block .str{color:var(--gold)}.code-block .num{color:#a78bfa}.code-block .cmt{color:var(--text3);font-style:italic}.code-block .key{color:#34d399}
.card-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px;margin:24px 0}
.card{background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:24px;transition:border-color 0.2s}
.card:hover{border-color:var(--border2)}
.card-head{display:flex;align-items:center;gap:12px;margin-bottom:16px}
.card-icon{width:36px;height:36px;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0}
.card-title{font-weight:600;font-size:13px;color:var(--text)}
.card-sub{font-family:var(--mono);font-size:10px;color:var(--text3);letter-spacing:0.1em}
.card p{font-size:13px;line-height:1.65}
.pillar{background:var(--bg2);border:1px solid var(--border);border-radius:6px;margin:24px 0;overflow:hidden}
.pillar-header{display:flex;align-items:center;justify-content:space-between;padding:16px 24px;background:var(--surface);border-bottom:1px solid var(--border)}
.pillar-title{font-weight:600;font-size:14px;color:var(--text);display:flex;align-items:center;gap:12px}
.pillar-weight{font-family:var(--mono);font-size:11px;color:var(--gold);background:rgba(200,169,110,0.1);padding:3px 10px;border-radius:20px;border:1px solid rgba(200,169,110,0.2)}
.pillar-body{padding:20px 24px}
.pillar-body p{font-size:13px;margin-bottom:12px}
.score-legend{display:flex;gap:6px;flex-wrap:wrap;margin:12px 0}
.score-badge{font-family:var(--mono);font-size:10px;padding:3px 8px;border-radius:3px;border:1px solid}
.sb-bull{color:var(--bull);border-color:var(--bull);background:var(--bull-dim)}
.sb-neutral{color:var(--neutral);border-color:rgba(148,163,184,0.3);background:rgba(148,163,184,0.08)}
.sb-bear{color:var(--bear);border-color:var(--bear);background:var(--bear-dim)}
.state-block{border-radius:6px;margin:16px 0;overflow:hidden;border:1px solid var(--border)}
.state-header{padding:14px 24px;display:flex;align-items:center;justify-content:space-between}
.state-name{font-family:var(--mono);font-size:14px;font-weight:600}
.state-range{font-family:var(--mono);font-size:11px;opacity:0.7}
.state-content{padding:20px 24px;display:grid;grid-template-columns:1fr 1fr;gap:16px}
.state-content-full{grid-column:1/-1}
.state-item-label{font-family:var(--mono);font-size:10px;letter-spacing:0.12em;text-transform:uppercase;color:var(--text3);margin-bottom:6px}
.state-item-text{font-size:13px;color:var(--text2)}
.decision-list{display:flex;flex-direction:column;gap:12px;margin:24px 0}
.decision-item{background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:16px 20px;display:flex;align-items:flex-start;gap:16px}
.decision-tag{font-family:var(--mono);font-size:10px;letter-spacing:0.1em;padding:4px 10px;border-radius:3px;white-space:nowrap;flex-shrink:0;margin-top:2px}
.tag-green{background:var(--bull-dim);color:var(--bull);border:1px solid rgba(34,197,94,0.3)}
.tag-yellow{background:rgba(234,179,8,0.1);color:#fbbf24;border:1px solid rgba(234,179,8,0.3)}
.tag-orange{background:rgba(249,115,22,0.1);color:var(--cautious-bear);border:1px solid rgba(249,115,22,0.3)}
.tag-red{background:var(--bear-dim);color:var(--bear);border:1px solid rgba(239,68,68,0.3)}
.tag-blue{background:var(--accent-glow);color:var(--accent2);border:1px solid rgba(79,110,247,0.3)}
.tag-gold{background:rgba(200,169,110,0.1);color:var(--gold);border:1px solid rgba(200,169,110,0.3)}
.decision-detail{flex:1}
.decision-title{font-weight:600;font-size:13px;color:var(--text);margin-bottom:4px}
.decision-desc{font-size:12px;color:var(--text2);line-height:1.6}
.break-item{background:var(--bg2);border:1px solid var(--border);border-left:3px solid var(--bear);border-radius:0 6px 6px 0;padding:16px 20px;margin:10px 0}
.break-title{font-weight:600;font-size:13px;color:var(--text);margin-bottom:6px}
.break-meta{display:flex;gap:24px;flex-wrap:wrap}
.break-meta-item{display:flex;flex-direction:column;gap:2px}
.break-meta-label{font-family:var(--mono);font-size:9px;letter-spacing:0.12em;color:var(--text3);text-transform:uppercase}
.break-meta-value{font-family:var(--mono);font-size:11px;color:var(--bear)}
.tf-matrix{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;margin:24px 0}
.tf-cell{background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:20px}
.tf-label{font-family:var(--mono);font-size:10px;letter-spacing:0.15em;color:var(--text3);text-transform:uppercase;margin-bottom:12px}
.tf-title{font-weight:600;font-size:14px;color:var(--text);margin-bottom:8px}
.tf-items{list-style:none}
.tf-items li{font-size:12px;color:var(--text2);padding:3px 0;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:8px}
.tf-items li:last-child{border-bottom:none}
.tf-items li::before{content:'—';color:var(--accent);font-family:var(--mono);font-size:10px;flex-shrink:0}
.scenario{background:var(--surface);border:1px solid var(--border);border-radius:8px;margin:20px 0;overflow:hidden}
.scenario-header{background:linear-gradient(90deg,var(--surface) 0%,var(--bg2) 100%);padding:16px 24px;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between}
.scenario-title{font-weight:600;font-size:14px;color:var(--text)}
.scenario-badge{font-family:var(--mono);font-size:10px;padding:3px 10px;border-radius:20px}
.scenario-body{padding:24px}
.scenario-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;margin-bottom:20px}
.scenario-tf{text-align:center}
.scenario-tf-label{font-family:var(--mono);font-size:9px;letter-spacing:0.12em;color:var(--text3);text-transform:uppercase;margin-bottom:8px}
.scenario-tf-state{font-family:var(--mono);font-size:13px;font-weight:600;margin-bottom:4px}
.scenario-tf-score{font-family:var(--mono);font-size:11px;color:var(--text3)}
.scenario-arrow{background:var(--bg3);border:1px solid var(--border);border-radius:4px;padding:12px 16px;margin:16px 0;font-family:var(--mono);font-size:12px;color:var(--gold)}
.scenario-output{background:var(--bg3);border:1px solid var(--border2);border-radius:6px;padding:16px 20px}
.scenario-output-row{display:flex;gap:16px;align-items:flex-start;margin:6px 0}
.scenario-output-key{font-family:var(--mono);font-size:10px;letter-spacing:0.1em;color:var(--text3);text-transform:uppercase;flex-shrink:0;width:100px;padding-top:2px}
.scenario-output-val{font-size:13px;color:var(--text);flex:1}
.confidence-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:24px 0}
.confidence-block{border-radius:6px;padding:20px;border:1px solid var(--border);text-align:center}
.confidence-range{font-family:var(--mono);font-size:18px;font-weight:600;margin-bottom:8px}
.confidence-label{font-size:12px;color:var(--text2);margin-bottom:8px}
.confidence-desc{font-size:11px;color:var(--text3)}
.jim-output{background:var(--bg2);border:1px solid var(--border);border-radius:8px;overflow:hidden;margin:20px 0}
.jim-header{background:var(--surface);padding:12px 20px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:10px;font-family:var(--mono);font-size:11px;color:var(--text3);letter-spacing:0.1em;text-transform:uppercase}
.jim-dot{width:8px;height:8px;border-radius:50%;background:var(--accent)}
.jim-section{padding:16px 20px;border-bottom:1px solid var(--border)}
.jim-section:last-child{border-bottom:none}
.jim-section-label{font-family:var(--mono);font-size:9px;letter-spacing:0.15em;text-transform:uppercase;color:var(--text3);margin-bottom:8px}
.jim-section-text{font-size:13px;color:var(--text);line-height:1.65}
.jim-headline{font-size:16px;font-weight:600;color:var(--gold);line-height:1.4}
.json-block{background:var(--bg);border:1px solid var(--border);border-radius:6px;padding:24px;font-family:var(--mono);font-size:12px;line-height:1.8;overflow-x:auto;color:var(--text2)}
.json-key{color:#93c5fd}.json-str{color:#86efac}.json-num{color:#fca5a5}.json-bool{color:#fbbf24}.json-null{color:var(--text3)}.json-comment{color:var(--text3);font-style:italic}
.callout{border-radius:6px;padding:20px 24px;margin:24px 0;border:1px solid}
.callout-blue{background:var(--accent-glow);border-color:rgba(79,110,247,0.3)}
.callout-gold{background:rgba(200,169,110,0.08);border-color:rgba(200,169,110,0.25)}
.callout-red{background:var(--bear-dim);border-color:rgba(239,68,68,0.3)}
.callout-green{background:rgba(34,197,94,0.06);border-color:rgba(34,197,94,0.25)}
.callout-label{font-family:var(--mono);font-size:10px;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:10px}
.callout-blue .callout-label{color:var(--accent2)}.callout-gold .callout-label{color:var(--gold)}.callout-red .callout-label{color:var(--bear)}.callout-green .callout-label{color:var(--bull)}
.callout p{margin-bottom:0;font-size:14px;color:var(--text)}
.sep{display:flex;align-items:center;gap:16px;margin:48px 0 32px}
.sep-line{flex:1;height:1px;background:var(--border)}
.sep-label{font-family:var(--mono);font-size:10px;letter-spacing:0.2em;color:var(--text3);text-transform:uppercase;white-space:nowrap}
.badge{display:inline-block;font-family:var(--mono);font-size:10px;padding:2px 8px;border-radius:3px;margin:0 3px;vertical-align:middle}
.badge-blue{background:var(--accent-glow);color:var(--accent2);border:1px solid rgba(79,110,247,0.3)}
.badge-gold{background:rgba(200,169,110,0.1);color:var(--gold);border:1px solid rgba(200,169,110,0.25)}
.badge-green{background:var(--bull-dim);color:var(--bull);border:1px solid rgba(34,197,94,0.3)}
.badge-red{background:var(--bear-dim);color:var(--bear);border:1px solid rgba(239,68,68,0.3)}
.arch-flow{display:flex;align-items:stretch;gap:0;margin:40px 0;overflow-x:auto}
.arch-node{flex:1;min-width:120px;background:var(--surface);border:1px solid var(--border);padding:20px 16px;text-align:center;position:relative}
.arch-node:first-child{border-radius:6px 0 0 6px}
.arch-node:last-child{border-radius:0 6px 6px 0}
.arch-node+.arch-node::before{content:'→';position:absolute;left:-14px;top:50%;transform:translateY(-50%);color:var(--accent);font-size:16px;z-index:1}
.arch-node-label{font-family:var(--mono);font-size:9px;letter-spacing:0.15em;color:var(--text3);text-transform:uppercase;margin-bottom:8px}
.arch-node-title{font-family:var(--sans);font-size:12px;font-weight:600;color:var(--text)}
.weight-grid{display:flex;flex-direction:column;gap:8px;margin:20px 0}
/* Risk Mode Table */
.risk-mode-row{display:grid;grid-template-columns:140px 100px 160px 1fr 1fr;gap:0;border-bottom:1px solid var(--border)}
.risk-mode-row:last-child{border-bottom:none}
.risk-mode-cell{padding:12px 14px;font-size:12px;color:var(--text2);border-right:1px solid var(--border)}
.risk-mode-cell:last-child{border-right:none}
.risk-mode-cell.mode-label{font-family:var(--mono);font-weight:700;font-size:11px}
/* Memory Engine */
.memory-block{background:var(--bg2);border:1px solid var(--border);border-radius:6px;padding:20px 24px;margin:16px 0}
.memory-block-title{font-family:var(--mono);font-size:11px;letter-spacing:0.12em;text-transform:uppercase;color:var(--accent2);margin-bottom:12px}
/* JIM Validation */
.jim-val-row{display:grid;grid-template-columns:120px 200px 80px 1fr;gap:0;border-bottom:1px solid var(--border)}
.jim-val-row:last-child{border-bottom:none}
.jim-val-cell{padding:10px 14px;font-size:12px;border-right:1px solid var(--border)}
.jim-val-cell:last-child{border-right:none}
.status-full{color:var(--bull);font-family:var(--mono);font-size:11px;font-weight:700}
.status-partial{color:var(--gold);font-family:var(--mono);font-size:11px;font-weight:700}
.status-missing{color:var(--bear);font-family:var(--mono);font-size:11px;font-weight:700}
/* Signal Block */
.signal-block{background:var(--bg2);border:1px solid var(--border);border-left:3px solid var(--accent);border-radius:0 6px 6px 0;padding:20px 24px;margin:16px 0}
.signal-block-id{font-family:var(--mono);font-size:10px;letter-spacing:0.15em;color:var(--accent);text-transform:uppercase;margin-bottom:4px}
.signal-block-title{font-size:15px;font-weight:600;color:var(--text);margin-bottom:8px}
.signal-block-indicators{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0}
.signal-indicator{font-family:var(--mono);font-size:10px;padding:2px 8px;border-radius:3px;background:rgba(79,110,247,0.08);color:var(--accent2);border:1px solid rgba(79,110,247,0.2)}
.regime-box{border-radius:6px;padding:20px 24px;border:1px solid;margin:16px 0}
footer{background:var(--bg2);border-top:1px solid var(--border);padding:40px 10%;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px}
footer .brand{font-family:var(--serif);font-size:18px;color:var(--gold)}
footer .note{font-family:var(--mono);font-size:11px;color:var(--text3)}
@media(max-width:768px){.cover{padding:60px 6%}.doc-body{padding:0 4%}.section{padding:48px 0}.tf-matrix{grid-template-columns:1fr}.scenario-grid{grid-template-columns:1fr}.confidence-grid{grid-template-columns:repeat(2,1fr)}.state-content{grid-template-columns:1fr}.arch-flow{flex-direction:column}}
</style>
</head>
<body>

<!-- COVER -->
<section class="cover">
  <div class="cover-grid"></div>
  <div class="cover-tag">// HARPIAN Portfolio Engineering Terminal · Internal Documentation · v2.0</div>
  <h1 class="cover-title">Market Trend<br><span>Decision Engine</span></h1>
  <p class="cover-sub">Complete Institutional Architecture — Scoring Engine, Risk Mode System, Memory Engine, JIM Validation & Current Regime. Consolidated from all source documents. For Family Office and Internal Use Only.</p>
  <div class="cover-meta">
    <div class="cover-meta-item"><span class="cover-meta-label">Version</span><span class="cover-meta-value">2.0 — Consolidated</span></div>
    <div class="cover-meta-item"><span class="cover-meta-label">Date</span><span class="cover-meta-value">May 2026</span></div>
    <div class="cover-meta-item"><span class="cover-meta-label">Sources</span><span class="cover-meta-value">Engine v1.0 + Institutional Architecture Doc</span></div>
    <div class="cover-meta-item"><span class="cover-meta-label">Classification</span><span class="cover-meta-value">Proprietary · Restricted</span></div>
  </div>
</section>

<div class="doc-body">

<!-- 01 EXECUTIVE SUMMARY -->
<section class="section">
  <div class="section-tag">// 01</div>
  <h2 class="section-title">Executive <span>Summary</span></h2>
  <p class="section-lead">The Market Trend module is the primary Decision Layer of the HARPIAN Terminal. It transforms multi-source institutional data into an actionable allocation posture, answering one question with precision: <em>what does the market environment demand from capital right now?</em></p>
  <div class="callout callout-gold">
    <div class="callout-label">Core Mandate</div>
    <p>"Trend is not what is happening. Trend is what deserves capital."<br>
    The system translates context into posture — not prediction, not commentary, but allocation-ready conviction with explicit confidence and break conditions. The right question is never "which asset is beautiful?" but "which regime is paying a premium for risk, which trend has been confirmed, and which execution still compensates?"</p>
  </div>
  <div class="card-grid">
    <div class="card"><div class="card-head"><div class="card-icon" style="background:rgba(79,110,247,0.12)">⚙</div><div><div class="card-title">6 Signal Blocks + 8 Pillars</div><div class="card-sub">Macro → Tactical → Execution</div></div></div><p>Three-tier architecture: Structural Regime (6–24M), Tactical Trend (1–6M), Execution (1D–4W). Six macro signal blocks feed eight weighted context pillars.</p></div>
    <div class="card"><div class="card-head"><div class="card-icon" style="background:rgba(200,169,110,0.12)">⏱</div><div><div class="card-title">Timeframe Matrix</div><div class="card-sub">Intraday / Weekly / Monthly</div></div></div><p>Independent scores across three timeframes with explicit conflict resolution. Confluence pattern drives final decision posture and modifies confidence score.</p></div>
    <div class="card"><div class="card-head"><div class="card-icon" style="background:rgba(34,197,94,0.12)">◈</div><div><div class="card-title">7 Trend States + 7 Risk Modes</div><div class="card-sub">Strong Bull → Strong Bear</div></div></div><p>Seven classified states mapped to seven codified risk modes, each carrying allocation posture, JIM language rules, and explicit break conditions.</p></div>
    <div class="card"><div class="card-head"><div class="card-icon" style="background:rgba(239,68,68,0.12)">⚠</div><div><div class="card-title">Break Conditions + Auto-Vetos</div><div class="card-sub">Regime Invalidation</div></div></div><p>Eight explicit threshold-based conditions that bypass scoring and trigger mandatory posture review. Six automatic veto rules from macro signal conflict logic.</p></div>
    <div class="card"><div class="card-head"><div class="card-icon" style="background:rgba(100,200,200,0.12)">🗄</div><div><div class="card-title">Memory Engine</div><div class="card-sub">State Persistence &amp; Audit</div></div></div><p>State change log, score history (90 days), break condition timeline, confidence evolution tracker, and SHA-256 narrative audit trail for compliance.</p></div>
    <div class="card"><div class="card-head"><div class="card-icon" style="background:rgba(251,191,36,0.12)">🗣</div><div><div class="card-title">JIM Narrative — Validated</div><div class="card-sub">Intent Coverage Map</div></div></div><p>Three-level output (Dashboard / CIO / Advisor). Full validation of intent coverage: which existing JIM intents apply, which are partially covered, and which are missing.</p></div>
  </div>
</section>

<!-- 02 ARCHITECTURE -->
<section class="section">
  <div class="section-tag">// 02</div>
  <h2 class="section-title">Conceptual <span>Architecture</span></h2>
  <p class="section-lead">The system operates as a sequential pipeline from raw inputs through scoring, classification, and narrative generation. Every layer is explicit, auditable, and override-capable. Market Regime and Market Trend are computed in parallel.</p>
  <div class="arch-flow">
    <div class="arch-node"><div class="arch-node-label">Layer 1</div><div class="arch-node-title">6 Signal Blocks</div></div>
    <div class="arch-node"><div class="arch-node-label">Layer 2</div><div class="arch-node-title">8 Context Pillars</div></div>
    <div class="arch-node"><div class="arch-node-label">Layer 3</div><div class="arch-node-title">Weighted Score</div></div>
    <div class="arch-node"><div class="arch-node-label">Layer 4</div><div class="arch-node-title">Trend State</div></div>
    <div class="arch-node"><div class="arch-node-label">Layer 5</div><div class="arch-node-title">Risk Mode</div></div>
    <div class="arch-node"><div class="arch-node-label">Layer 6</div><div class="arch-node-title">Break Conditions</div></div>
    <div class="arch-node"><div class="arch-node-label">Layer 7</div><div class="arch-node-title">Memory Engine</div></div>
    <div class="arch-node"><div class="arch-node-label">Layer 8</div><div class="arch-node-title">JIM Narrative</div></div>
  </div>

  <h3>Three-Tier Macro Architecture</h3>
  <div class="table-wrap"><table>
    <thead><tr><th>Tier</th><th>Horizon</th><th>Primary Inputs</th><th>Weight in Composite</th><th>JIM Access</th></tr></thead>
    <tbody>
      <tr><td class="bold">Structural Regime</td><td class="mono">6–24 months</td><td>Valuation, real rate, risk premium, earnings cycle, country allocation</td><td class="mono" style="color:var(--gold)">50%</td><td>FO_INST / MFO</td></tr>
      <tr><td class="bold">Tactical Trend</td><td class="mono">1–6 months</td><td>Growth, inflation, credit, curve, sector confirmation</td><td class="mono" style="color:var(--gold)">35%</td><td>FA_PRO+</td></tr>
      <tr><td class="bold">Execution Layer</td><td class="mono">1 day–4 weeks</td><td>Price structure, breadth, volatility, flow, funding</td><td class="mono" style="color:var(--gold)">15%</td><td>All tiers</td></tr>
    </tbody>
  </table></div>
  <div class="callout callout-blue"><div class="callout-label">Design Principle</div><p>The external Macro Architecture tells the system <em>where the wind blows</em>. It must not compete with the internal risk engine (StormGuard). When StormGuard activates, it forces Capital Preservation Mode regardless of Trend State. The Structural Regime weight dominates precisely because momentum and positioning can persist in wrong directions — macro provides the anchor.</p></div>
</section>

<!-- 03 SIX SIGNAL BLOCKS -->
<section class="section">
  <div class="section-tag">// 03</div>
  <h2 class="section-title">Six Macro <span>Signal Blocks</span></h2>
  <p class="section-lead">Each block aggregates related data sources into a single scored input for the Context Engine. The frescor (freshness) coefficient decays automatically when data exceeds staleness threshold. Stale blocks trigger Confidence Score penalty and must be flagged in JIM output.</p>

  <div class="signal-block">
    <div class="signal-block-id">Block 1 — Activity &amp; Growth</div>
    <div class="signal-block-title">GDP · Payroll · PMI · Consumer</div>
    <p>Primary growth trajectory signal. Answers: is growth accelerating, decelerating, or changing quality? Not just "growing or not."</p>
    <div class="signal-block-indicators">
      <span class="signal-indicator">GDP (BEA)</span><span class="signal-indicator">Real PCE</span><span class="signal-indicator">Payroll (BLS)</span><span class="signal-indicator">Unemployment</span><span class="signal-indicator">ISM Manufacturing PMI</span><span class="signal-indicator">ISM Services</span><span class="signal-indicator">Hours Worked</span><span class="signal-indicator">Housing Starts</span><span class="signal-indicator">Nowcast (Atlanta Fed)</span>
    </div>
    <p style="font-size:12px;color:var(--text3)">Current reading (May 2026): GDP Q1 +2.0% ann. · Payroll Mar +178k · Unemployment 4.3% · Manufacturing PMI Apr 52.7</p>
  </div>

  <div class="signal-block">
    <div class="signal-block-id">Block 2 — Inflation &amp; Persistence</div>
    <div class="signal-block-title">CPI · PCE · Breakevens · MCT</div>
    <p>Trend is "good for risk" only when inflation falls faster than market expectations OR, at minimum, does not re-accelerate faster than earnings support. Headline + persistence measures must be tracked separately.</p>
    <div class="signal-block-indicators">
      <span class="signal-indicator">CPI YoY (BLS)</span><span class="signal-indicator">Core CPI</span><span class="signal-indicator">PCE Headline</span><span class="signal-indicator">Core PCE</span><span class="signal-indicator">10Y Breakeven</span><span class="signal-indicator">MCT (NY Fed)</span><span class="signal-indicator">Supercore CPI</span>
    </div>
    <p style="font-size:12px;color:var(--text3)">Current reading (May 2026): CPI 3.3% · Core CPI 2.6% · PCE 3.5% · Core PCE 3.2% · MCT 3.2% · Breakeven 10Y 2.46%</p>
  </div>

  <div class="signal-block">
    <div class="signal-block-id">Block 3 — Monetary Policy, Liquidity &amp; Curve</div>
    <div class="signal-block-title">FOMC · Yields · TIPS · NFCI · Term Premium</div>
    <p>Rate nominal, real, and implied inflation tell three different stories. A trend in equities or bonds is only robust when these three stories converge. The term premium alone is not a reliable recession predictor — the economic signal is in the curve slope.</p>
    <div class="signal-block-indicators">
      <span class="signal-indicator">EFFR</span><span class="signal-indicator">2Y Treasury</span><span class="signal-indicator">10Y Treasury</span><span class="signal-indicator">TIPS 10Y (real)</span><span class="signal-indicator">10Y Breakeven</span><span class="signal-indicator">Term Premium (ACM)</span><span class="signal-indicator">NFCI (Chicago Fed)</span><span class="signal-indicator">2s10s slope</span>
    </div>
    <p style="font-size:12px;color:var(--text3)">Current reading (May 2026): EFFR 3.64% · 2Y 3.92% · 10Y 4.42% · TIPS 1.96% · NFCI −0.52 (loose) · 2s10s +50bp</p>
  </div>

  <div class="signal-block">
    <div class="signal-block-id">Block 4 — Credit &amp; Financial Stability</div>
    <div class="signal-block-title">HY OAS · IG Spreads · SLOOS · Default Rates</div>
    <p>Fed monitors four financial stability vectors: valuation, private leverage, system leverage, and funding/liquidity risk. A rally with compressed spreads and tightening bank credit can persist but becomes increasingly vulnerable to growth or funding shock.</p>
    <div class="signal-block-indicators">
      <span class="signal-indicator">HY OAS (ICE BofA)</span><span class="signal-indicator">IG OAS</span><span class="signal-indicator">Baa/Treasury spread</span><span class="signal-indicator">SLOOS (C&amp;I)</span><span class="signal-indicator">SCOOS</span><span class="signal-indicator">Default rate (Moody's)</span><span class="signal-indicator">TED spread</span>
    </div>
    <p style="font-size:12px;color:var(--text3)">Current reading (May 2026): HY OAS 2.83% · Baa/Treasury 1.69% · SLOOS net 5.3% tightening C&amp;I large/mid</p>
  </div>

  <div class="signal-block">
    <div class="signal-block-id">Block 5 — Equity Fundamentals &amp; Sector Sensitivity</div>
    <div class="signal-block-title">Corporate Profits · Margins · Revision Trend · Sector Coefficients</div>
    <p>Rotation must not be done by stereotype ("growth vs. value"). The operationally useful signal is sector sensitivity to long rates, GDP growth, and inflation — quantified via Damodaran sector coefficients. Duration of cash flow, pricing power, leverage, and cycle elasticity determine which sectors benefit.</p>
    <div class="signal-block-indicators">
      <span class="signal-indicator">Corporate Profits (BEA)</span><span class="signal-indicator">Operating Margins</span><span class="signal-indicator">EPS Revision Ratio</span><span class="signal-indicator">Buyback activity</span><span class="signal-indicator">Capex/reinvestment</span><span class="signal-indicator">Sector β to 10Y</span><span class="signal-indicator">Sector β to CPI</span><span class="signal-indicator">Damodaran ERP</span>
    </div>
  </div>

  <div class="signal-block">
    <div class="signal-block-id">Block 6 — Flow, Volatility, Positioning &amp; Dollar</div>
    <div class="signal-block-title">VIX · COT · ETF Flows · DXY · Skew</div>
    <p>The dollar is not an FX detail — it is a global liquidity channel. BIS evidence shows the dollar became a primary driver of capital flows to EM bonds and equities. ETF net issuance reached $1.5T in 2025 (ICI record). VIX is measured not by level but by trend, term structure, and vol-of-vol.</p>
    <div class="signal-block-indicators">
      <span class="signal-indicator">VIX (CBOE)</span><span class="signal-indicator">VVIX</span><span class="signal-indicator">SKEW</span><span class="signal-indicator">MOVE (bond vol)</span><span class="signal-indicator">COT Net Positioning</span><span class="signal-indicator">ETF Net Issuance (ICI)</span><span class="signal-indicator">Put/Call ratio</span><span class="signal-indicator">DXY trend</span><span class="signal-indicator">GEX (dealer gamma)</span>
    </div>
  </div>
</section>

<!-- 04 CONTEXT ENGINE — 8 PILLARS -->
<section class="section">
  <div class="section-tag">// 04</div>
  <h2 class="section-title">Context Engine — <span>8 Scoring Pillars</span></h2>
  <p class="section-lead">Eight scoring pillars produce a weighted composite score from −3.0 to +3.0. Each pillar is independently scored before aggregation. No single pillar can dominate the final output. Scores are on a 7-point scale: −3 (Extremely Bearish) to +3 (Extremely Bullish).</p>

  <h3>Score Aggregation Formula</h3>
  <div class="code-block">
<span class="cmt">// HARPIAN Composite Score — incorporating frescor (freshness) and confiança (confidence)</span>

<span class="key">Score_h</span> = Σ( peso × sinal × confiança × frescor ) − penalidades

<span class="cmt">// Where:
//   peso      = pillar weight (below)
//   sinal     = pillar score −3 to +3
//   confiança = data confidence 0.0–1.0 (decays on noisy/revision-prone data)
//   frescor   = freshness coefficient 1.0→0.0 (decays when data exceeds staleness threshold)
//   penalidades = crowding penalty + correlation-break penalty + divergence penalty</span>

<span class="cmt">// Monthly Default Weights (Structural Regime dominant)</span>
<span class="key">Final_Score</span> =
  (Price_Structure   × <span class="num">0.25</span>)   <span class="cmt">// Pillar A</span>
  + (Momentum        × <span class="num">0.20</span>)   <span class="cmt">// Pillar B</span>
  + (Macro_Trend     × <span class="num">0.15</span>)   <span class="cmt">// Pillar C</span>
  + (Volatility      × <span class="num">0.10</span>)   <span class="cmt">// Pillar D</span>
  + (Liquidity       × <span class="num">0.10</span>)   <span class="cmt">// Pillar E</span>
  + (Positioning     × <span class="num">0.10</span>)   <span class="cmt">// Pillar F</span>
  + (Sentiment       × <span class="num">0.05</span>)   <span class="cmt">// Pillar G</span>
  + (Correlation     × <span class="num">0.05</span>)   <span class="cmt">// Pillar H</span>

<span class="cmt">// Non-linear override: if any pillar scores −3 → apply −0.2 to final score
// Confidence penalty: each stale source → Confidence Score −0.5</span>

<span class="cmt">// Intraday weight adjustment: Volatility→20%, Sentiment→10%, Price→20%, Macro→5%
// Weekly adjustment: Momentum→22%, Positioning→13%, Macro→12%
// Macro→18% during Fed cycle inflection periods</span>

<span class="cmt">// Three-tier composite:
// Final = 0.50 × Structural_Regime_Score + 0.35 × Tactical_Trend_Score + 0.15 × Execution_Score</span>
  </div>

  <h3>Pillar Weights — Monthly Default</h3>
  <div class="weight-grid">
    <div class="score-bar-wrap"><span class="score-bar-label">A · Price Structure</span><div class="score-bar-track"><div class="score-bar-fill" style="width:25%;background:var(--accent)"></div></div><span class="score-bar-val">25%</span></div>
    <div class="score-bar-wrap"><span class="score-bar-label">B · Momentum</span><div class="score-bar-track"><div class="score-bar-fill" style="width:20%;background:var(--accent)"></div></div><span class="score-bar-val">20%</span></div>
    <div class="score-bar-wrap"><span class="score-bar-label">C · Macro Trend</span><div class="score-bar-track"><div class="score-bar-fill" style="width:15%;background:var(--accent2)"></div></div><span class="score-bar-val">15%</span></div>
    <div class="score-bar-wrap"><span class="score-bar-label">D · Volatility</span><div class="score-bar-track"><div class="score-bar-fill" style="width:10%;background:var(--gold)"></div></div><span class="score-bar-val">10%</span></div>
    <div class="score-bar-wrap"><span class="score-bar-label">E · Liquidity</span><div class="score-bar-track"><div class="score-bar-fill" style="width:10%;background:var(--gold)"></div></div><span class="score-bar-val">10%</span></div>
    <div class="score-bar-wrap"><span class="score-bar-label">F · Positioning</span><div class="score-bar-track"><div class="score-bar-fill" style="width:10%;background:var(--gold)"></div></div><span class="score-bar-val">10%</span></div>
    <div class="score-bar-wrap"><span class="score-bar-label">G · Sentiment</span><div class="score-bar-track"><div class="score-bar-fill" style="width:5%;background:var(--cautious-bear)"></div></div><span class="score-bar-val">5%</span></div>
    <div class="score-bar-wrap"><span class="score-bar-label">H · Correlation/Fragility</span><div class="score-bar-track"><div class="score-bar-fill" style="width:5%;background:var(--cautious-bear)"></div></div><span class="score-bar-val">5%</span></div>
  </div>

  <div class="sep"><div class="sep-line"></div><div class="sep-label">Pillar Definitions</div><div class="sep-line"></div></div>

  <div class="pillar"><div class="pillar-header"><div class="pillar-title"><span style="color:var(--accent);font-family:var(--mono);font-size:12px">A</span> Price Structure</div><div class="pillar-weight">25%</div></div><div class="pillar-body"><p><strong>Key Indicators:</strong> HH/HL structure · ATH proximity · % stocks above MA50/200 · SMA/EMA slope · New highs vs. lows · A/D line · Drawdown from ATH · Breakout confirmation</p><div class="score-legend"><span class="score-badge sb-bull">+3: HH/HL intact, >60% above MA50, ATH confirmed</span><span class="score-badge sb-bull">+2: Uptrend intact, consolidation above MAs</span><span class="score-badge sb-bull">+1: Above MA200, mixed breadth</span><span class="score-badge sb-neutral">0: MA200 test, A/D flat</span><span class="score-badge sb-bear">−1: HL/LL forming, below MA50</span><span class="score-badge sb-bear">−2: Failed breakout, below MA200</span><span class="score-badge sb-bear">−3: LL/LH confirmed, breadth collapse</span></div><p style="margin-top:12px"><strong>Breadth Divergence Override:</strong> If price at new highs while % above MA50 declining AND new highs/lows compressing → apply −1 override to Price Structure regardless of other readings.</p></div></div>

  <div class="pillar"><div class="pillar-header"><div class="pillar-title"><span style="color:var(--accent);font-family:var(--mono);font-size:12px">B</span> Momentum</div><div class="pillar-weight">20%</div></div><div class="pillar-body"><p><strong>Key Indicators:</strong> Sector RS · 12-1M momentum factor · Risk-on/off cross-asset signals · Leadership quality (cyclicals vs. defensives) · Momentum dispersion · RSI trend · MACD slope</p><div class="score-legend"><span class="score-badge sb-bull">+3: Broad sector leadership, cyclicals dominating</span><span class="score-badge sb-bull">+2: Momentum intact, risk-on flows confirmed</span><span class="score-badge sb-bull">+1: Selective momentum, narrow leadership</span><span class="score-badge sb-neutral">0: Rotation without direction</span><span class="score-badge sb-bear">−1: Defensives outperforming</span><span class="score-badge sb-bear">−2: Momentum collapse, breadth diverging</span><span class="score-badge sb-bear">−3: Factor momentum deeply negative</span></div><p style="margin-top:8px"><span class="badge badge-gold">Elite / White Label Only</span> — Asset-level momentum details</p></div></div>

  <div class="pillar"><div class="pillar-header"><div class="pillar-title"><span style="color:var(--accent);font-family:var(--mono);font-size:12px">C</span> Macro Trend</div><div class="pillar-weight">15%</div></div><div class="pillar-body"><p><strong>Key Indicators:</strong> Fed Funds futures curve · 10Y real yield · 2s10s slope · CPI/PCE trend · GDP surprises · PMI composite · EPS revision trend · DXY · Geopolitical risk premium</p><div class="table-wrap"><table><thead><tr><th>Macro State</th><th>Conditions</th><th>Score Bias</th></tr></thead><tbody><tr><td class="bold">Growth Supportive</td><td>+GDP surprises, PMI >50, positive revisions</td><td class="mono" style="color:var(--bull)">+2 to +3</td></tr><tr><td class="bold">Soft Landing</td><td>Inflation falling, growth stable, Fed pausing</td><td class="mono" style="color:var(--bull)">+1 to +2</td></tr><tr><td class="bold">Inflation Pressure</td><td>CPI sticky above target, real wages squeezed</td><td class="mono" style="color:var(--cautious-bear)">−1 to −2</td></tr><tr><td class="bold">Duration Pressure</td><td>Long yields rising, real rates positive &amp; rising</td><td class="mono" style="color:var(--cautious-bear)">−1 to −2</td></tr><tr><td class="bold">Stagflation Risk</td><td>Inflation sticky + growth declining simultaneously</td><td class="mono" style="color:var(--bear)">−3</td></tr><tr><td class="bold">Recession Risk</td><td>Curve inverted, PMI &lt;47, negative surprises</td><td class="mono" style="color:var(--bear)">−2 to −3</td></tr></tbody></table></div></div></div>

  <div class="pillar"><div class="pillar-header"><div class="pillar-title"><span style="color:var(--accent);font-family:var(--mono);font-size:12px">D</span> Volatility</div><div class="pillar-weight">10%</div></div><div class="pillar-body"><p>Not the level of VIX but its trend, structure, and term premium. Low VIX at extremes is bearish (complacency). Rising VIX from panic levels scores as opportunity.</p><div class="score-legend"><span class="score-badge sb-bull">+2/+3: VIX low/falling, contango, low MOVE</span><span class="score-badge sb-bull">+1: VIX stable &lt;20</span><span class="score-badge sb-neutral">0: VIX 20–25</span><span class="score-badge sb-bear">−1: VIX 25–30, backwardation</span><span class="score-badge sb-bear">−2: VIX >30, spike</span><span class="score-badge sb-bear">−3: VIX >40 systemic</span></div></div></div>

  <div class="pillar"><div class="pillar-header"><div class="pillar-title"><span style="color:var(--accent);font-family:var(--mono);font-size:12px">E</span> Liquidity</div><div class="pillar-weight">10%</div></div><div class="pillar-body"><p>Liquidity is the oxygen of markets. A contracting liquidity environment can overwhelm even strong price structure. Monitors: Fed balance sheet · SLOOS · HY/IG spreads · TED spread · SOFR basis · M2 growth · Repo stress</p><div class="score-legend"><span class="score-badge sb-bull">+2/+3: Spreads tight, Fed accommodative, credit flowing</span><span class="score-badge sb-neutral">0: Neutral, spreads at average</span><span class="score-badge sb-bear">−2: Significant widening, credit stress</span><span class="score-badge sb-bear">−3: Funding markets stressed</span></div></div></div>

  <div class="pillar"><div class="pillar-header"><div class="pillar-title"><span style="color:var(--accent);font-family:var(--mono);font-size:12px">F</span> Positioning</div><div class="pillar-weight">10%</div></div><div class="pillar-body"><p>Extreme positioning (crowded long or short) is a contrarian signal. Heavy positioning with technical deterioration sets up violent unwinds. Monitors: CFTC COT · ICI flows · ETF creations · HF leverage · GEX · Dealer gamma</p><div class="table-wrap"><table><thead><tr><th>State</th><th>Score</th><th>Signal</th></tr></thead><tbody><tr><td class="bold">Accumulation</td><td class="mono" style="color:var(--bull)">+1 to +2</td><td>Confirms bull trend</td></tr><tr><td class="bold">Crowded Long</td><td class="mono" style="color:var(--cautious-bear)">−1</td><td>Reduce new exposure</td></tr><tr><td class="bold">Crowded Short</td><td class="mono" style="color:var(--bull)">+1</td><td>Squeeze risk</td></tr><tr><td class="bold">Distribution</td><td class="mono" style="color:var(--bear)">−1 to −2</td><td>Early warning</td></tr></tbody></table></div></div></div>

  <div class="pillar"><div class="pillar-header"><div class="pillar-title"><span style="color:var(--accent);font-family:var(--mono);font-size:12px">G</span> Sentiment</div><div class="pillar-weight">5%</div></div><div class="pillar-body"><p>Contrarian secondary signal. Low weight because extremes are infrequent but high-value. Euphoria at resistance → bearish. Panic at support → bullish. Sources: AAII · BofA FMS · CNN F&amp;G · Put/Call · Social NLP</p><div class="score-legend"><span class="score-badge sb-bull">+2/+3: Panic (contrarian buy)</span><span class="score-badge sb-neutral">0: Neutral</span><span class="score-badge sb-bear">−2/−3: Euphoria (contrarian sell)</span></div></div></div>

  <div class="pillar"><div class="pillar-header"><div class="pillar-title"><span style="color:var(--accent);font-family:var(--mono);font-size:12px">H</span> Correlation / Fragility</div><div class="pillar-weight">5%</div></div><div class="pillar-body"><p>Systemic fragility: degree to which assets move as one. In rising markets, correlation is less relevant. In stress, it is critical. BIS evidence: in high-inflation regimes equity-bond correlation turns positive, weakening classic 60/40 diversification.</p><div class="score-legend"><span class="score-badge sb-bull">+1 to +2: Low correlation, diversification functioning</span><span class="score-badge sb-neutral">0: Normal dynamics</span><span class="score-badge sb-bear">−1: Equity-bond positive correlation (risk-off)</span><span class="score-badge sb-bear">−3: Systemic lockstep</span></div></div></div>
</section>

<!-- 05 TIMEFRAME MATRIX -->
<section class="section">
  <div class="section-tag">// 05</div>
  <h2 class="section-title">Timeframe <span>Matrix</span></h2>
  <p class="section-lead">Independent scores for three timeframes. Alignment pattern determines final allocation posture and confidence. Timeframe conflicts are not noise — they are signal. AQR evidence (110 years) confirms trend following is most consistent at medium horizon (1–6 months).</p>
  <div class="tf-matrix">
    <div class="tf-cell"><div class="tf-label">Layer 1</div><div class="tf-title">Intraday / Daily</div><ul class="tf-items"><li>Price action vs prior session H/L</li><li>Intraday breadth A/D</li><li>VIX intraday behavior</li><li>Volume vs 20-day avg</li><li>Options flow (gamma, P/C)</li><li>News / event sentiment</li><li>Futures overnight positioning</li></ul></div>
    <div class="tf-cell"><div class="tf-label">Layer 2</div><div class="tf-title">Weekly</div><ul class="tf-items"><li>Weekly price structure HH/HL or LL/LH</li><li>% above MA50 (weekly)</li><li>Sector RS weekly shifts</li><li>ETF flow trends (ICI)</li><li>CFTC COT weekly positioning</li><li>EPS revision weekly</li><li>Credit spread weekly direction</li></ul></div>
    <div class="tf-cell"><div class="tf-label">Layer 3</div><div class="tf-title">Monthly</div><ul class="tf-items"><li>Monthly price structure and trend</li><li>% above MA200 monthly</li><li>Full macro regime classification</li><li>Fed meeting cycle impact</li><li>BofA FMS monthly</li><li>Street consensus updates</li><li>Yield curve monthly slope</li></ul></div>
  </div>
  <h3>Timeframe Conflict Resolution</h3>
  <div class="table-wrap"><table>
    <thead><tr><th>Monthly</th><th>Weekly</th><th>Intraday</th><th>Interpretation</th><th>Action</th><th>Confidence</th></tr></thead>
    <tbody>
      <tr><td class="state-sb">Strong Bull</td><td class="state-b">Bull</td><td class="state-b">Bull</td><td>Full alignment</td><td class="bold">Fully / Aggressively Invested</td><td class="mono" style="color:var(--bull)">High 8–10</td></tr>
      <tr><td class="state-b">Bull</td><td class="state-b">Bull</td><td class="state-cbe">Cautious Bear</td><td>ST weakness in LT uptrend</td><td class="bold">Add on Weakness</td><td class="mono" style="color:var(--bull)">High 7–8</td></tr>
      <tr><td class="state-sb">Strong Bull</td><td class="state-n">Neutral</td><td class="state-cbe">Cautious Bear</td><td>Tactical pause, LT intact</td><td class="bold">Maintain, No New Risk</td><td class="mono" style="color:var(--gold)">Medium 6–7</td></tr>
      <tr><td class="state-b">Bull</td><td class="state-cb">Cautious Bull</td><td class="state-n">Neutral</td><td>Uptrend, reduced momentum</td><td class="bold">Stay Invested with Caution, Rotate</td><td class="mono" style="color:var(--gold)">Medium 6–7</td></tr>
      <tr><td class="state-n">Neutral</td><td class="state-b">Bull</td><td class="state-b">Bull</td><td>Tactical, not structural</td><td class="bold">Partial Allocation, Tactical Only</td><td class="mono" style="color:var(--gold)">Medium 5–7</td></tr>
      <tr><td class="state-cb">Cautious Bull</td><td class="state-n">Neutral</td><td class="state-cbe">Cautious Bear</td><td>No conviction either direction</td><td class="bold">Wait for Confirmation / Barbell</td><td class="mono" style="color:var(--cautious-bear)">Low 4–5</td></tr>
      <tr><td class="state-be">Bear</td><td class="state-be">Bear</td><td class="state-b">Bull</td><td>Bear market rally</td><td class="bold">Sell Rallies</td><td class="mono" style="color:var(--bull)">High 7–8</td></tr>
      <tr><td class="state-sbe">Strong Bear</td><td class="state-be">Bear</td><td class="state-b">Bull</td><td>Oversold bounce, trap risk</td><td class="bold">Exit Risk Assets</td><td class="mono" style="color:var(--bull)">High 8–9</td></tr>
      <tr><td class="state-be">Bear</td><td class="state-cb">Cautious Bull</td><td class="state-b">Bull</td><td>Ambiguous: LT risk, tactical opp</td><td class="bold">Wait for Confirmation</td><td class="mono" style="color:var(--cautious-bear)">Low 3–5</td></tr>
    </tbody>
  </table></div>
</section>

<!-- 06 TREND STATE TAXONOMY -->
<section class="section">
  <div class="section-tag">// 06</div>
  <h2 class="section-title">Trend State <span>Taxonomy</span></h2>
  <p class="section-lead">Seven classified states, derived from the Final Score. Each carries a complete institutional definition, decision posture, and communication protocol at three audience levels. A minimum of four simultaneous confirmations is required to classify a state with high confidence.</p>

  <div class="state-block"><div class="state-header" style="background:rgba(34,197,94,0.1);border-bottom:1px solid rgba(34,197,94,0.2)"><span class="state-name" style="color:var(--bull)">● STRONG BULL</span><span class="state-range" style="color:var(--bull)">Score: +2.0 → +3.0</span></div><div class="state-content"><div><div class="state-item-label">Definition</div><div class="state-item-text">Maximum structural alignment. Price, momentum, and macro all constructive. Breadth broad, cyclicals leading. Highest risk-reward for equity exposure historically.</div></div><div><div class="state-item-label">Decision Posture</div><div class="state-item-text">Fully Invested · Maximize momentum · Aggressive sector rotation · Reduce cash to minimum</div></div><div class="state-content-full"><div class="state-item-label">JIM Headline</div><div class="state-item-text" style="color:var(--bull)">"Strong Bull: broad-based uptrend with high conviction across all timeframes."</div></div><div class="state-content-full"><div class="state-item-label">Institutional Narrative</div><div class="state-item-text">"Market conditions present maximum structural alignment across technical, momentum, and macro dimensions. Risk-reward favors full equity exposure with emphasis on momentum leaders. Primary risk is behavioral — complacency and overconcentration. Active management of sector rotation and position sizing is essential."</div></div></div></div>

  <div class="state-block"><div class="state-header" style="background:rgba(74,222,128,0.08);border-bottom:1px solid rgba(74,222,128,0.2)"><span class="state-name" style="color:#4ade80">● BULL</span><span class="state-range" style="color:#4ade80">Score: +1.0 → +2.0</span></div><div class="state-content"><div><div class="state-item-label">Definition</div><div class="state-item-text">Constructive trend with positive risk/reward. Not all pillars aligned but dominant direction is up. Price structure intact. Some secondary indicators may lag.</div></div><div><div class="state-item-label">Decision Posture</div><div class="state-item-text">Stay Fully Invested · Rotate into leaders · Trim laggards · Maintain standard risk</div></div><div class="state-content-full"><div class="state-item-label">JIM Headline</div><div class="state-item-text" style="color:#4ade80">"Bull: uptrend intact. Stay invested and rotate toward momentum leaders."</div></div></div></div>

  <div class="state-block"><div class="state-header" style="background:rgba(163,230,53,0.06);border-bottom:1px solid rgba(163,230,53,0.18)"><span class="state-name" style="color:#a3e635">◐ CAUTIOUS BULL</span><span class="state-range" style="color:#a3e635">Score: +0.3 → +1.0</span></div><div class="state-content"><div><div class="state-item-label">Definition</div><div class="state-item-text">Positive but fragile. Trend is up but with meaningful headwinds from rates, volatility, or macro uncertainty. Capital remains deployed but with elevated selectivity.</div></div><div><div class="state-item-label">Decision Posture</div><div class="state-item-text">Stay Invested · Selective rotation · Reduce weak exposures · Avoid duration · Partial cash buffer</div></div><div class="state-content-full"><div class="state-item-label">JIM Headline</div><div class="state-item-text" style="color:#a3e635">"Cautious Bull: trend constructive but conviction limited. Selective positioning required."</div></div></div></div>

  <div class="state-block"><div class="state-header" style="background:rgba(148,163,184,0.06);border-bottom:1px solid rgba(148,163,184,0.15)"><span class="state-name" style="color:var(--neutral)">◯ NEUTRAL</span><span class="state-range" style="color:var(--neutral)">Score: −0.3 → +0.3</span></div><div class="state-content"><div><div class="state-item-label">Definition</div><div class="state-item-text">No dominant trend. Risk and reward approximately balanced. Decision zone — waiting for catalyst. Patience and optionality are the appropriate posture.</div></div><div><div class="state-item-label">Decision Posture</div><div class="state-item-text">Partial Allocation · Barbell · Increase optionality · Await confirmation</div></div><div class="state-content-full"><div class="state-item-label">JIM Headline</div><div class="state-item-text" style="color:var(--neutral)">"Neutral: no dominant trend signal. Preserve optionality, await confirmation."</div></div></div></div>

  <div class="state-block"><div class="state-header" style="background:rgba(249,115,22,0.08);border-bottom:1px solid rgba(249,115,22,0.2)"><span class="state-name" style="color:var(--cautious-bear)">◑ CAUTIOUS BEAR</span><span class="state-range" style="color:var(--cautious-bear)">Score: −1.0 → −0.3</span></div><div class="state-content"><div><div class="state-item-label">Definition</div><div class="state-item-text">Dominant negative tilt. More signals point down. Risk asymmetry has shifted. Defensive action before confirmation arrives — not after.</div></div><div><div class="state-item-label">Decision Posture</div><div class="state-item-text">Reduce risk · Increase hedges · Avoid leverage · Raise cash · No new momentum positions</div></div><div class="state-content-full"><div class="state-item-label">JIM Headline</div><div class="state-item-text" style="color:var(--cautious-bear)">"Cautious Bear: risk asymmetry has shifted. Reduce exposure and increase defensive positioning."</div></div></div></div>

  <div class="state-block"><div class="state-header" style="background:rgba(239,68,68,0.08);border-bottom:1px solid rgba(239,68,68,0.2)"><span class="state-name" style="color:var(--bear)">● BEAR</span><span class="state-range" style="color:var(--bear)">Score: −2.0 → −1.0</span></div><div class="state-content"><div><div class="state-item-label">Definition</div><div class="state-item-text">Primary trend down. Sustained selling pressure. Negative macro, deteriorating price structure, rising volatility confirm the regime. Capital preservation is primary objective.</div></div><div><div class="state-item-label">Decision Posture</div><div class="state-item-text">Defensive allocation · Cash, short-duration IG, gold · Sell rallies · Avoid concentration</div></div><div class="state-content-full"><div class="state-item-label">JIM Headline</div><div class="state-item-text" style="color:var(--bear)">"Bear: primary trend is down. Defensive allocation active. Sell rallies."</div></div></div></div>

  <div class="state-block"><div class="state-header" style="background:rgba(220,38,38,0.1);border-bottom:1px solid rgba(220,38,38,0.25)"><span class="state-name" style="color:#dc2626">▼ STRONG BEAR</span><span class="state-range" style="color:#dc2626">Score: −3.0 → −2.0</span></div><div class="state-content"><div><div class="state-item-label">Definition</div><div class="state-item-text">Maximum structural deterioration. All major pillars negative. Potential systemic risk. Return of capital, not return on capital.</div></div><div><div class="state-item-label">Decision Posture</div><div class="state-item-text">Capital Preservation Mode · Exit risk assets · Maximum cash · StormGuard fully active</div></div><div class="state-content-full"><div class="state-item-label">JIM Headline</div><div class="state-item-text" style="color:#dc2626">"Strong Bear: capital preservation mode active. All risk asset exposure minimized."</div></div></div></div>
</section>

<!-- 07 RISK MODE SYSTEM -->
<section class="section">
  <div class="section-tag">// 07 — NEW</div>
  <h2 class="section-title">Risk Mode <span>System</span></h2>
  <p class="section-lead">Seven codified Risk Modes map each Trend State to a precise allocation posture, HPC11/HPC22 split, JIM tone, and execution rule. Risk Modes are the operational translation of the scoring system into capital deployment decisions.</p>

  <div class="callout callout-gold">
    <div class="callout-label">HPC Allocation Model</div>
    <p><strong>HPC11</strong> = Core ETF / diversified / lower volatility / regime-resilient. Structural exposure.<br>
    <strong>HPC22</strong> = Equity / higher return / higher volatility / alpha-seeking. Tactical exposure.<br>
    The ratio HPC11:HPC22 is the primary mechanical output of the Risk Mode. It directly feeds the Market Trends dashboard allocation bars.</p>
  </div>

  <div class="table-wrap"><table>
    <thead><tr><th>Risk Mode</th><th>Score Range</th><th>Trend State</th><th>HPC11</th><th>HPC22</th><th>Total Equity</th><th>Cash Buffer</th><th>JIM Tone</th></tr></thead>
    <tbody>
      <tr><td class="bold" style="color:var(--bull)">RISK-ON FULL</td><td class="mono">+2.0 → +3.0</td><td class="state-sb">Strong Bull</td><td class="mono">50%</td><td class="mono">50%</td><td class="mono" style="color:var(--bull)">100%</td><td class="mono">0–5%</td><td>High conviction, aggressive</td></tr>
      <tr><td class="bold" style="color:#4ade80">RISK-ON SELECTIVE</td><td class="mono">+1.0 → +2.0</td><td class="state-b">Bull</td><td class="mono">55%</td><td class="mono">40%</td><td class="mono" style="color:#4ade80">90–100%</td><td class="mono">5–10%</td><td>Constructive, disciplined</td></tr>
      <tr><td class="bold" style="color:#a3e635">CAUTIOUS GROWTH</td><td class="mono">+0.3 → +1.0</td><td class="state-cb">Cautious Bull</td><td class="mono">60%</td><td class="mono">25%</td><td class="mono" style="color:#a3e635">75–90%</td><td class="mono">10–15%</td><td>Selective, opportunity-seeking</td></tr>
      <tr><td class="bold" style="color:var(--neutral)">TRANSITION</td><td class="mono">−0.3 → +0.3</td><td class="state-n">Neutral</td><td class="mono">55%</td><td class="mono">10%</td><td class="mono" style="color:var(--neutral)">50–75%</td><td class="mono">15–25%</td><td>Balanced, patient, barbell</td></tr>
      <tr><td class="bold" style="color:var(--cautious-bear)">CAUTIOUS DEFENSE</td><td class="mono">−1.0 → −0.3</td><td class="state-cbe">Cautious Bear</td><td class="mono">50%</td><td class="mono">0%</td><td class="mono" style="color:var(--cautious-bear)">35–50%</td><td class="mono">25–40%</td><td>Defensive lean, risk-aware</td></tr>
      <tr><td class="bold" style="color:var(--bear)">DEFENSE</td><td class="mono">−2.0 → −1.0</td><td class="state-be">Bear</td><td class="mono">30%</td><td class="mono">0%</td><td class="mono" style="color:var(--bear)">15–35%</td><td class="mono">40–60%</td><td>Defensive, urgent</td></tr>
      <tr><td class="bold" style="color:#dc2626">CAPITAL PRESERVATION</td><td class="mono">−3.0 → −2.0</td><td class="state-sbe">Strong Bear</td><td class="mono">10%</td><td class="mono">0%</td><td class="mono" style="color:#dc2626">0–15%</td><td class="mono">60–100%</td><td>Protective, survival-mode</td></tr>
    </tbody>
  </table></div>

  <h3>Risk Mode — Rotation Rules by Asset Class</h3>
  <div class="table-wrap"><table>
    <thead><tr><th>Risk Mode</th><th>Equities</th><th>Fixed Income</th><th>Credit</th><th>Alternatives / Real Assets</th></tr></thead>
    <tbody>
      <tr><td class="bold" style="color:var(--bull)">RISK-ON FULL</td><td>Cyclicals, Financials, Industrials, Small Cap</td><td>Avoid long duration</td><td>HY acceptable</td><td>Commodities, EM equities</td></tr>
      <tr><td class="bold" style="color:#4ade80">RISK-ON SELECTIVE</td><td>Sector RS leaders, trim laggards</td><td>Short-duration core</td><td>IG preferred, selective HY</td><td>Selective commodities</td></tr>
      <tr><td class="bold" style="color:#a3e635">CAUTIOUS GROWTH</td><td>Quality growth, pricing power, low leverage</td><td>TIPS + short nominal</td><td>IG only, no new HY</td><td>Gold, inflation proxies</td></tr>
      <tr><td class="bold" style="color:var(--neutral)">TRANSITION</td><td>Barbell: quality defensives + high-conviction risk</td><td>Ladder: ST + MT</td><td>IG, no HY</td><td>Gold, real assets</td></tr>
      <tr><td class="bold" style="color:var(--cautious-bear)">CAUTIOUS DEFENSE</td><td>Defensives: Utilities, Healthcare, Consumer Staples</td><td>Short-duration IG, Treasuries</td><td>IG only, reduce duration</td><td>Gold, cash equivalents</td></tr>
      <tr><td class="bold" style="color:var(--bear)">DEFENSE</td><td>Minimize equity; only high-quality dividend</td><td>Short Treasuries, 2Y–5Y</td><td>Exit HY; reduce IG</td><td>Gold, cash, T-bills</td></tr>
      <tr><td class="bold" style="color:#dc2626">CAPITAL PRESERVATION</td><td>Exit all risk assets systematically</td><td>T-bills, money market</td><td>Exit all credit</td><td>Maximum gold, USD cash</td></tr>
    </tbody>
  </table></div>

  <h3>Confirmation Requirements — Minimum 4 of 6 to Validate State</h3>
  <div class="decision-list">
    <div class="decision-item"><span class="decision-tag tag-blue">REQ-1</span><div class="decision-detail"><div class="decision-title">Price Direction Aligned Across Multiple Timeframes</div><div class="decision-desc">At least 2 of 3 timeframes (intraday/weekly/monthly) must confirm the same directional bias.</div></div></div>
    <div class="decision-item"><span class="decision-tag tag-blue">REQ-2</span><div class="decision-detail"><div class="decision-title">Macro Confirms Price Direction</div><div class="decision-desc">At least 2 macro releases or 1 release + 1 nowcast/survey must be consistent with the directional signal.</div></div></div>
    <div class="decision-item"><span class="decision-tag tag-blue">REQ-3</span><div class="decision-detail"><div class="decision-title">Credit Does Not Contradict Thesis</div><div class="decision-desc">Equities can rise with spreads widening, but such moves are structurally inferior. Credit must be non-contradictory at minimum.</div></div></div>
    <div class="decision-item"><span class="decision-tag tag-blue">REQ-4</span><div class="decision-detail"><div class="decision-title">Cross-Asset Coherence</div><div class="decision-desc">Equities, bonds, dollar, and commodities must tell a coherent story — or the divergence must be explicitly explained.</div></div></div>
    <div class="decision-item"><span class="decision-tag tag-blue">REQ-5</span><div class="decision-detail"><div class="decision-title">Breadth and Leadership Expanding</div><div class="decision-desc">Sector participation must be broadening, not narrowing. Leadership concentration is a warning.</div></div></div>
    <div class="decision-item"><span class="decision-tag tag-blue">REQ-6</span><div class="decision-detail"><div class="decision-title">Crowding Not Extreme Without Strong Macro</div><div class="decision-desc">If COT/flow data shows extreme crowding, a very strong macro signal is required to sustain the state without penalty.</div></div></div>
  </div>
</section>

<!-- 08 BREAK CONDITIONS + AUTO-VETOS -->
<section class="section">
  <div class="section-tag">// 08</div>
  <h2 class="section-title">Break Conditions <span>&amp; Auto-Vetos</span></h2>
  <p class="section-lead">Explicit threshold-based overrides. When any break condition triggers, the system must: (1) flag the state, (2) downgrade Trend State by minimum one level, (3) reduce Confidence Score −2.0, and (4) generate dashboard alert. These bypass the scoring model entirely.</p>

  <div class="callout callout-red"><div class="callout-label">Override Rule</div><p>Break Conditions are not weighted inputs. They are binary triggers. When triggered, they take priority over all pillar scores. A Strong Bull with an active Break Condition must be reclassified to Cautious Bull at minimum.</p></div>

  <div class="break-item"><div class="break-title">BC-1 · VIX Spike Above Critical Threshold</div><div class="break-meta"><div class="break-meta-item"><div class="break-meta-label">Threshold</div><div class="break-meta-value">VIX > 28 (caution) | VIX > 40 (systemic)</div></div><div class="break-meta-item"><div class="break-meta-label">Score Impact</div><div class="break-meta-value">Volatility pillar → −3 immediately</div></div><div class="break-meta-item"><div class="break-meta-label">Decision</div><div class="break-meta-value">Force minimum: Defensive Allocation</div></div></div></div>

  <div class="break-item"><div class="break-title">BC-2 · 10Y Treasury Yield Breakout</div><div class="break-meta"><div class="break-meta-item"><div class="break-meta-label">Threshold</div><div class="break-meta-value">10Y > 5.2% sustained 5 sessions</div></div><div class="break-meta-item"><div class="break-meta-label">Score Impact</div><div class="break-meta-value">Macro → −2 | Liquidity → −1</div></div><div class="break-meta-item"><div class="break-meta-label">Decision</div><div class="break-meta-value">Trigger "Avoid Long Duration" + downgrade minimum one level</div></div></div></div>

  <div class="break-item"><div class="break-title">BC-3 · Breadth Collapse</div><div class="break-meta"><div class="break-meta-item"><div class="break-meta-label">Threshold</div><div class="break-meta-value">% above MA50 &lt; 40% | NH/NL ratio &lt; 0.5</div></div><div class="break-meta-item"><div class="break-meta-label">Score Impact</div><div class="break-meta-value">Price Structure → −2 regardless of index level</div></div><div class="break-meta-item"><div class="break-meta-label">Decision</div><div class="break-meta-value">Force "Reduce Weak Exposures" + breadth divergence warning</div></div></div></div>

  <div class="break-item"><div class="break-title">BC-4 · HY Credit Spread Widening</div><div class="break-meta"><div class="break-meta-item"><div class="break-meta-label">Threshold</div><div class="break-meta-value">HY OAS +100bps from recent low within 30 days</div></div><div class="break-meta-item"><div class="break-meta-label">Score Impact</div><div class="break-meta-value">Liquidity → −2 | Correlation → −1</div></div><div class="break-meta-item"><div class="break-meta-label">Decision</div><div class="break-meta-value">Raise cash buffer; avoid HY equity proxies</div></div></div></div>

  <div class="break-item"><div class="break-title">BC-5 · Equity-Bond Positive Correlation (Risk-Off)</div><div class="break-meta"><div class="break-meta-item"><div class="break-meta-label">Threshold</div><div class="break-meta-value">30-day rolling equity-bond correlation > +0.5 during decline</div></div><div class="break-meta-item"><div class="break-meta-label">Score Impact</div><div class="break-meta-value">Correlation/Fragility pillar → −3</div></div><div class="break-meta-item"><div class="break-meta-label">Decision</div><div class="break-meta-value">Diversification failing — force barbell reduction, increase cash</div></div></div></div>

  <div class="break-item"><div class="break-title">BC-6 · Drawdown Acceleration</div><div class="break-meta"><div class="break-meta-item"><div class="break-meta-label">Threshold</div><div class="break-meta-value">Drawdown > 10% in 15 trading days | > 20% from peak</div></div><div class="break-meta-item"><div class="break-meta-label">Score Impact</div><div class="break-meta-value">Price Structure → −3 | Force Bear minimum</div></div><div class="break-meta-item"><div class="break-meta-label">Decision</div><div class="break-meta-value">Mandatory StormGuard review → Capital Preservation candidate</div></div></div></div>

  <div class="break-item"><div class="break-title">BC-7 · New Highs with Deteriorating Breadth</div><div class="break-meta"><div class="break-meta-item"><div class="break-meta-label">Threshold</div><div class="break-meta-value">Index at new high while % above MA50 falling AND NH/NL declining</div></div><div class="break-meta-item"><div class="break-meta-label">Score Impact</div><div class="break-meta-value">Price Structure → −1 override (divergence penalty)</div></div><div class="break-meta-item"><div class="break-meta-label">Decision</div><div class="break-meta-value">Downgrade from Fully Invested to Stay Invested with Caution</div></div></div></div>

  <div class="break-item"><div class="break-title">BC-8 · Earnings Revision Collapse</div><div class="break-meta"><div class="break-meta-item"><div class="break-meta-label">Threshold</div><div class="break-meta-value">Net revision ratio (upgrades/downgrades) &lt; 0.7 for 3+ consecutive weeks</div></div><div class="break-meta-item"><div class="break-meta-label">Score Impact</div><div class="break-meta-value">Macro → −1 | Momentum → −1</div></div><div class="break-meta-item"><div class="break-meta-label">Decision</div><div class="break-meta-value">Reduce growth exposure; question Bull state sustainability</div></div></div></div>

  <h3>Automatic Veto Rules (from Macro Signal Conflict)</h3>
  <div class="table-wrap"><table>
    <thead><tr><th>Veto</th><th>Trigger Condition</th><th>Action</th></tr></thead>
    <tbody>
      <tr><td class="bold">VETO-1: Duration Veto</td><td>Breakevens rising + real rates rising + equity-bond correlation positive</td><td>Cut conviction in long duration; reduce long-duration equity weight</td></tr>
      <tr><td class="bold">VETO-2: Liquidity Veto</td><td>HY spreads opening + SLOOS tightening + DXY rising</td><td>Reduce beta; exit HY; reduce EM exposure</td></tr>
      <tr><td class="bold">VETO-3: Crowding Veto</td><td>Index rising + breadth deteriorating + COT/flows extreme long</td><td>Maintain asset; reduce concentration; increase realization discipline</td></tr>
      <tr><td class="bold">VETO-4: EM Risk Veto</td><td>DXY strong + US real rate high + EM liquidity tightening</td><td>Reduce EM beta; focus on US/DM quality</td></tr>
      <tr><td class="bold">VETO-5: Concentration Veto</td><td>Macro/credit/breadth/valuation partially misaligned (score 4–6)</td><td>Force diversification over concentration; reduce position sizing</td></tr>
      <tr><td class="bold">VETO-6: StormGuard Override</td><td>StormGuard activation threshold met (Volatility + Drawdown combined)</td><td>Force Capital Preservation Mode regardless of Trend State score</td></tr>
    </tbody>
  </table></div>
</section>

<!-- 09 CONFIDENCE SCORE -->
<section class="section">
  <div class="section-tag">// 09</div>
  <h2 class="section-title">Confidence <span>Score</span></h2>
  <p class="section-lead">The Confidence Score (0–10) communicates reliability of the current Trend State classification. It is not a directional signal. High confidence Bear is still bearish. It tells the advisor how much conviction to apply to the current decision posture.</p>
  <div class="code-block">
<span class="key">Confidence_Score</span> = <span class="num">10.0</span>

<span class="cmt">// Step 1: Timeframe alignment</span>
<span class="kw">IF</span> 3/3 timeframes aligned:   +0   (full baseline)
<span class="kw">IF</span> 2/3 aligned:              −1.0
<span class="kw">IF</span> 1/3 aligned:              −2.5
<span class="kw">IF</span> 0/3 aligned:              −4.0

<span class="cmt">// Step 2: Signal convergence</span>
<span class="kw">FOR EACH</span> pillar contradicting final state: −0.4 each

<span class="cmt">// Step 3: Data quality</span>
<span class="kw">FOR EACH</span> stale data source: −0.5 each

<span class="cmt">// Step 4: Break condition proximity</span>
<span class="kw">IF</span> any break condition within 20% of threshold: −0.5 each
<span class="kw">IF</span> any break condition TRIGGERED:              −2.0 mandatory

<span class="cmt">// Step 5: Volatility environment</span>
<span class="kw">IF</span> VIX > 25: −0.5
<span class="kw">IF</span> VIX > 35: −1.5 additional

<span class="cmt">// Step 6: Confirmation count (from 6-requirement check)</span>
<span class="kw">IF</span> only 4/6 confirmations met: −0.5
<span class="kw">IF</span> only 3/6 confirmations met: −1.5

<span class="key">Confidence_Score</span> = max(<span class="num">0</span>, min(<span class="num">10</span>, Confidence_Score))
  </div>
  <div class="confidence-grid">
    <div class="confidence-block" style="background:rgba(34,197,94,0.08);border-color:rgba(34,197,94,0.25)"><div class="confidence-range" style="color:var(--bull)">8 – 10</div><div class="confidence-label">High Conviction</div><div class="confidence-desc">Full alignment. Act with confidence on primary signal.</div></div>
    <div class="confidence-block" style="background:rgba(163,230,53,0.06);border-color:rgba(163,230,53,0.2)"><div class="confidence-range" style="color:#a3e635">6 – 8</div><div class="confidence-label">Moderate</div><div class="confidence-desc">Primary signal clear but divergences present. Size discipline.</div></div>
    <div class="confidence-block" style="background:rgba(249,115,22,0.08);border-color:rgba(249,115,22,0.2)"><div class="confidence-range" style="color:var(--cautious-bear)">4 – 6</div><div class="confidence-label">Mixed / Low</div><div class="confidence-desc">Conflicting signals. Reduce sizing. Await resolution.</div></div>
    <div class="confidence-block" style="background:rgba(239,68,68,0.08);border-color:rgba(239,68,68,0.2)"><div class="confidence-range" style="color:var(--bear)">0 – 4</div><div class="confidence-label">Unreliable</div><div class="confidence-desc">No reliable signal. Data stale or contradictory. Do not act on primary alone.</div></div>
  </div>
</section>

<!-- 10 MEMORY ENGINE -->
<section class="section">
  <div class="section-tag">// 10 — NEW</div>
  <h2 class="section-title">Memory <span>Engine</span></h2>
  <p class="section-lead">The Memory Engine persists market state across sessions, enabling trend change detection, narrative continuity, compliance audit trail, and JIM context-aware responses. All writes are immutable and SHA-256 hashed. Retention: 7 years (matching FINRA Books &amp; Records Rule 4511).</p>

  <div class="memory-block">
    <div class="memory-block-title">State Object — Current + Previous</div>
    <div class="code-block">
<span class="json-comment">// Persisted on every scoring computation</span>
{
  <span class="json-key">"session_id"</span>: <span class="json-str">"MTE-20260501-001"</span>,
  <span class="json-key">"computed_at"</span>: <span class="json-str">"2026-05-01T14:32:00Z"</span>,
  <span class="json-key">"current_state"</span>: {
    <span class="json-key">"trend_state"</span>: <span class="json-str">"cautious_bull"</span>,
    <span class="json-key">"risk_mode"</span>: <span class="json-str">"CAUTIOUS_GROWTH"</span>,
    <span class="json-key">"final_score"</span>: <span class="json-num">0.72</span>,
    <span class="json-key">"confidence_score"</span>: <span class="json-num">7.2</span>,
    <span class="json-key">"hpc11_weight"</span>: <span class="json-num">0.60</span>,
    <span class="json-key">"hpc22_weight"</span>: <span class="json-num">0.40</span>
  },
  <span class="json-key">"previous_state"</span>: {
    <span class="json-key">"trend_state"</span>: <span class="json-str">"bull"</span>,
    <span class="json-key">"risk_mode"</span>: <span class="json-str">"RISK_ON_SELECTIVE"</span>,
    <span class="json-key">"final_score"</span>: <span class="json-num">1.35</span>,
    <span class="json-key">"confidence_score"</span>: <span class="json-num">8.1</span>,
    <span class="json-key">"computed_at"</span>: <span class="json-str">"2026-04-17T09:15:00Z"</span>
  },
  <span class="json-key">"state_changed"</span>: <span class="json-bool">true</span>,
  <span class="json-key">"change_direction"</span>: <span class="json-str">"downgrade"</span>,
  <span class="json-key">"change_trigger"</span>: <span class="json-str">"macro_inflation_reacceleration"</span>
}
    </div>
  </div>

  <div class="memory-block">
    <div class="memory-block-title">Score History — 90-Day Rolling Window</div>
    <p style="font-size:13px;color:var(--text2)">Daily snapshots of all pillar scores, final score, confidence score, and active break conditions. Used by JIM to detect trend change velocity, persistence, and to provide context-aware responses ("the score has been declining for 3 weeks").</p>
    <div class="table-wrap"><table>
      <thead><tr><th>Field</th><th>Type</th><th>Retention</th><th>JIM Access</th></tr></thead>
      <tbody>
        <tr><td class="bold">daily_scores[]</td><td class="mono">float[]</td><td>90 days rolling</td><td>Trend velocity calculation</td></tr>
        <tr><td class="bold">pillar_history[]</td><td class="mono">object[]</td><td>90 days rolling</td><td>Divergence detection</td></tr>
        <tr><td class="bold">state_change_log[]</td><td class="mono">event[]</td><td>7 years</td><td>Compliance + narrative</td></tr>
        <tr><td class="bold">break_condition_log[]</td><td class="mono">event[]</td><td>7 years</td><td>Institutional audit</td></tr>
        <tr><td class="bold">narrative_hash[]</td><td class="mono">sha256[]</td><td>7 years</td><td>Compliance only</td></tr>
        <tr><td class="bold">confidence_evolution[]</td><td class="mono">float[]</td><td>90 days rolling</td><td>Model validation</td></tr>
      </tbody>
    </table></div>
  </div>

  <div class="memory-block">
    <div class="memory-block-title">JIM Memory Rules — Context Awareness</div>
    <div class="table-wrap"><table>
      <thead><tr><th>Condition</th><th>JIM Behavior</th></tr></thead>
      <tbody>
        <tr><td class="bold">State unchanged for &gt;30 days</td><td>JIM acknowledges persistence: "The Cautious Bull classification has been sustained for 6 weeks..."</td></tr>
        <tr><td class="bold">Score trending down 3+ sessions</td><td>JIM flags velocity: "The composite score has declined in each of the last 3 sessions, approaching [threshold]..."</td></tr>
        <tr><td class="bold">Downgrade from prior session</td><td>JIM explains change driver: "This represents a downgrade from Bull, driven by [pillar] deterioration..."</td></tr>
        <tr><td class="bold">Break condition recently triggered</td><td>JIM includes prior break event in context for 10 sessions after resolution</td></tr>
        <tr><td class="bold">Confidence score fell &gt;2 points</td><td>JIM reduces conviction language: "Evidence moderately favors..." instead of "evidence strongly supports..."</td></tr>
      </tbody>
    </table></div>
  </div>
</section>

<!-- 11 JIM NARRATIVE RULES + VALIDATION -->
<section class="section">
  <div class="section-tag">// 11</div>
  <h2 class="section-title">JIM Narrative Rules <span>&amp; Validation</span></h2>
  <p class="section-lead">Three-level output protocol, forbidden phrase registry, and complete intent coverage validation. All JIM responses for Market Trends must pass the Compliance Guardrail Engine. No output bypasses CGE.</p>

  <h3>Core Language Principles</h3>
  <div class="table-wrap"><table>
    <thead><tr><th>Rule</th><th>Instruction</th><th>Reason</th></tr></thead>
    <tbody>
      <tr><td class="bold">Probability over Certainty</td><td>"conditions favor," "evidence suggests," "higher probability of"</td><td>Never present trend as guaranteed</td></tr>
      <tr><td class="bold">Signal before Nuance</td><td>State the dominant signal first, then acknowledge counterevidence</td><td>Clarity before complexity</td></tr>
      <tr><td class="bold">Break Condition Required</td><td>Every narrative must include what would invalidate the thesis</td><td>Institutional discipline — always show the exit</td></tr>
      <tr><td class="bold">No Forecast Language</td><td>Avoid: "the market will," "we expect," "targets suggest X%"</td><td>Posture is the product, not prediction</td></tr>
      <tr><td class="bold">No Fear in Neutral</td><td>Neutral is not ominous. Do not use threatening language.</td><td>Avoid unnecessary anxiety for FO clients</td></tr>
      <tr><td class="bold">Memory Context Active</td><td>Reference state persistence, velocity, and change events from Memory Engine</td><td>Institutional context builds trust</td></tr>
    </tbody>
  </table></div>

  <h3>Three-Level Output Template</h3>
  <div class="jim-output">
    <div class="jim-header"><div class="jim-dot"></div>JIM OUTPUT — CAUTIOUS BULL · RISK MODE: CAUTIOUS GROWTH</div>
    <div class="jim-section"><div class="jim-section-label">Level A — Dashboard Headline (max 1 sentence)</div><div class="jim-section-text jim-headline">"Cautious Bull: trend remains constructive, but rates and volatility limit conviction. Stay invested, selective."</div></div>
    <div class="jim-section"><div class="jim-section-label">Level B — Institutional / CIO (Family Office — 3–5 sentences)</div><div class="jim-section-text">"The market maintains a positive structural bias across the primary and intermediate trend, supported by resilient price structure and positive sector momentum. However, elevated Treasury yields (10Y at 4.42%), persistent inflation (Core PCE 3.2%), and tightening bank credit standards (SLOOS net +5.3% tightening) prevent a full risk-on classification. Current allocation stance favors maintaining equity exposure at HPC11/HPC22 = 60%/40% while actively rotating toward momentum leaders with pricing power and avoiding long-duration and rate-sensitive assets. The primary invalidation condition is a 10Y yield breakout above 5.2% or a VIX sustained above 28, either of which would require an immediate posture review and potential downgrade to Cautious Bear."</div></div>
    <div class="jim-section"><div class="jim-section-label">Level C — Client-Ready / Advisor-to-Client (2–3 sentences)</div><div class="jim-section-text">"The market is still trending upward, but conditions are more selective than earlier in the year. We remain invested and focused on the stronger sectors, while reducing exposure to areas more sensitive to interest-rate pressure. Our positioning reflects opportunity with discipline — not fear."</div></div>
  </div>

  <h3>Forbidden Phrases by State</h3>
  <div class="table-wrap"><table>
    <thead><tr><th>State</th><th>Forbidden Language</th><th>Use Instead</th></tr></thead>
    <tbody>
      <tr><td class="state-sb">Strong Bull</td><td>"This bull market has no end in sight" / "Don't fight the tape"</td><td>"High conviction; monitor for overextension and breadth divergence."</td></tr>
      <tr><td class="state-n">Neutral</td><td>"The market is dangerous" / "Proceed with extreme caution"</td><td>"No dominant directional signal; preserve optionality."</td></tr>
      <tr><td class="state-be">Bear</td><td>"Time to sell everything" / "Crash incoming"</td><td>"Structural deterioration warrants defensive reallocation."</td></tr>
      <tr><td class="state-sbe">Strong Bear</td><td>"This is the end of the cycle" / "Expect more losses"</td><td>"Capital preservation mode active. Re-entry conditions will be monitored."</td></tr>
      <tr><td>Any</td><td>Any specific price target or percentage prediction</td><td>Directional posture language only</td></tr>
      <tr><td>Any</td><td>"The data is clear" / "No doubt about the trend"</td><td>"Evidence [strongly/moderately] favors [direction]."</td></tr>
    </tbody>
  </table></div>

  <h3>JIM Intent Coverage — Market Trends Module</h3>
  <div class="callout callout-gold"><div class="callout-label">Validation Result</div><p>Out of 30 defined JIM intents (v2 architecture), 8 are directly applicable to Market Trends. 4 are partially applicable. 8 new intents are required for full Market Trends coverage. Recommendation: define INT-031 through INT-038.</p></div>

  <div class="table-wrap"><table>
    <thead><tr><th>Intent</th><th>Description</th><th>Coverage</th><th>Market Trends Relevance</th></tr></thead>
    <tbody>
      <tr><td class="mono">INT-008</td><td>StormGuard Status</td><td class="status-full">FULL</td><td>StormGuard Override = BC-6 integration point</td></tr>
      <tr><td class="mono">INT-009</td><td>StormGuard Methodology</td><td class="status-full">FULL</td><td>Explains regime detection linked to Break Conditions</td></tr>
      <tr><td class="mono">INT-010</td><td>StormGuard Context</td><td class="status-full">FULL</td><td>Risk-off regime overlay on Trend State</td></tr>
      <tr><td class="mono">INT-011</td><td>AlphaDroid Signals</td><td class="status-partial">PARTIAL</td><td>Feeds Pillar B (Momentum) but not directly linked to state output</td></tr>
      <tr><td class="mono">INT-012</td><td>AlphaDroid Methodology</td><td class="status-partial">PARTIAL</td><td>Explains momentum input but not full Trend State</td></tr>
      <tr><td class="mono">INT-015</td><td>Hypothetical Allocation</td><td class="status-full">FULL</td><td>HPC11/HPC22 simulation maps directly to Risk Mode output</td></tr>
      <tr><td class="mono">INT-016</td><td>Stress Test / Scenario</td><td class="status-full">FULL</td><td>Break Condition scenarios are stress test instances</td></tr>
      <tr><td class="mono">INT-020</td><td>Simulation Engine</td><td class="status-full">FULL</td><td>Timeframe conflict scenarios run through simulation</td></tr>
      <tr><td class="mono">INT-021</td><td>Suitability Check</td><td class="status-partial">PARTIAL</td><td>Risk Mode output has suitability implications</td></tr>
      <tr><td class="mono">INT-022</td><td>Portfolio Approval</td><td class="status-partial">PARTIAL</td><td>Risk Mode → allocation approval pathway</td></tr>
      <tr><td class="mono" style="color:var(--bear)">INT-031 (NEW)</td><td>Current Trend State Query</td><td class="status-missing">MISSING</td><td>"What is the current market trend?" → Returns state + score + mode</td></tr>
      <tr><td class="mono" style="color:var(--bear)">INT-032 (NEW)</td><td>Trend Score Explanation</td><td class="status-missing">MISSING</td><td>"Why is the score +22 / Cautious Bull?" → Pillar breakdown</td></tr>
      <tr><td class="mono" style="color:var(--bear)">INT-033 (NEW)</td><td>Timeframe Matrix Query</td><td class="status-missing">MISSING</td><td>"What does weekly vs monthly show?" → Conflict resolution</td></tr>
      <tr><td class="mono" style="color:var(--bear)">INT-034 (NEW)</td><td>Break Condition Query</td><td class="status-missing">MISSING</td><td>"What would break the current trend?" → Active break condition list</td></tr>
      <tr><td class="mono" style="color:var(--bear)">INT-035 (NEW)</td><td>Rotation Recommendation</td><td class="status-missing">MISSING</td><td>"Where should we rotate?" → Sector RS + Risk Mode guidance</td></tr>
      <tr><td class="mono" style="color:var(--bear)">INT-036 (NEW)</td><td>Confidence Score Query</td><td class="status-missing">MISSING</td><td>"How confident is the system?" → Score + alignment explanation</td></tr>
      <tr><td class="mono" style="color:var(--bear)">INT-037 (NEW)</td><td>Macro Regime Query</td><td class="status-missing">MISSING</td><td>"What is the macro backdrop?" → 6 Signal Blocks summary</td></tr>
      <tr><td class="mono" style="color:var(--bear)">INT-038 (NEW)</td><td>Risk Mode Allocation Detail</td><td class="status-missing">MISSING</td><td>"What is the exact HPC split and why?" → Risk Mode table + rationale</td></tr>
    </tbody>
  </table></div>
</section>

<!-- 12 CURRENT REGIME READING -->
<section class="section">
  <div class="section-tag">// 12</div>
  <h2 class="section-title">Current Regime <span>Reading</span></h2>
  <p class="section-lead">Operational inference as of May 1, 2026. This section is updated on each major data release. Serves as the JIM live context reference for Market Trends queries.</p>

  <div class="regime-box" style="background:rgba(163,230,53,0.04);border-color:rgba(163,230,53,0.2)">
    <h3 style="margin-top:0;color:#a3e635">Current Classification: CAUTIOUS BULL · Risk Mode: CAUTIOUS GROWTH</h3>
    <p>Operational inference: <strong>Structural Regime neutral-positive · Tactical Trend positive · Execution mildly positive.</strong></p>
    <p>This is <em>not</em> full risk-on. It is risk-on selective with an active inflation veto. The environment calls for maintaining equity exposure, disciplined rotation, lower complacency with long duration, and greater rigor in concentration vs. diversification decisions than a classic benign disinflation regime would require.</p>
  </div>

  <div class="table-wrap"><table>
    <thead><tr><th>Signal Block</th><th>Reading (May 2026)</th><th>Score Bias</th><th>Notes</th></tr></thead>
    <tbody>
      <tr><td class="bold">Activity &amp; Growth</td><td>GDP Q1 +2.0% · Payroll +178k · PMI 52.7</td><td class="mono" style="color:var(--bull)">+1 to +2</td><td>Positive but decelerating vs. 2025 pace</td></tr>
      <tr><td class="bold">Inflation &amp; Persistence</td><td>CPI 3.3% · Core PCE 3.2% · MCT 3.2%</td><td class="mono" style="color:var(--cautious-bear)">−1 to −2</td><td>Re-acceleration is the key risk — limits Fed space</td></tr>
      <tr><td class="bold">Monetary Policy &amp; Curve</td><td>EFFR 3.64% · 2Y 3.92% · 10Y 4.42% · NFCI −0.52</td><td class="mono" style="color:var(--neutral)">0 to +1</td><td>Fed in pause; conditions still loose but yields rising</td></tr>
      <tr><td class="bold">Credit &amp; Financial Stability</td><td>HY OAS 2.83% · Baa/Tsy 1.69% · SLOOS +5.3%</td><td class="mono" style="color:var(--neutral)">0 to −1</td><td>Compressed spreads + tightening standards = caution</td></tr>
      <tr><td class="bold">Equity Fundamentals</td><td>Revisions positive · Margins pressured · Tech leading</td><td class="mono" style="color:var(--bull)">+1</td><td>Leadership narrow — AI/Tech concentrated</td></tr>
      <tr><td class="bold">Flow &amp; Positioning</td><td>VIX 22.4 · ETF inflows positive · Dollar stable</td><td class="mono" style="color:var(--neutral)">0 to +1</td><td>Not extreme crowding; dollar not a major headwind</td></tr>
    </tbody>
  </table></div>

  <h3>Break Conditions — Current Proximity</h3>
  <div class="table-wrap"><table>
    <thead><tr><th>Break Condition</th><th>Threshold</th><th>Current Value</th><th>Proximity</th><th>Status</th></tr></thead>
    <tbody>
      <tr><td class="bold">BC-1: VIX Spike</td><td class="mono">VIX > 28</td><td class="mono">22.4</td><td class="mono" style="color:#a3e635">20% buffer</td><td>WATCH</td></tr>
      <tr><td class="bold">BC-2: 10Y Breakout</td><td class="mono">10Y > 5.2%</td><td class="mono">4.42%</td><td class="mono" style="color:var(--bull)">17% buffer</td><td>MONITOR</td></tr>
      <tr><td class="bold">BC-4: HY Widening</td><td class="mono">HY OAS +100bps</td><td class="mono">2.83% (low base)</td><td class="mono" style="color:var(--bull)">Not proximate</td><td>OK</td></tr>
      <tr><td class="bold">BC-8: EPS Revision</td><td class="mono">Ratio &lt; 0.7</td><td class="mono">~0.85 est.</td><td class="mono" style="color:#a3e635">Watch Q2 season</td><td>WATCH</td></tr>
    </tbody>
  </table></div>
</section>

<!-- 13 DECISION MATRIX -->
<section class="section">
  <div class="section-tag">// 13</div>
  <h2 class="section-title">Decision <span>Matrix</span></h2>
  <p class="section-lead">Sixteen codified allocation decisions mapped to Trend States, timeframe patterns, and score thresholds. Each carries JIM language rules and forbidden phrases.</p>
  <div class="decision-list">
    <div class="decision-item"><span class="decision-tag tag-green">FULLY INVESTED</span><div class="decision-detail"><div class="decision-title">Maximum equity exposure — Strong Bull + 3/3 alignment + Confidence ≥ 8</div><div class="decision-desc">JIM says: "All indicators confirm the uptrend." JIM avoids: "This will continue indefinitely."</div></div></div>
    <div class="decision-item"><span class="decision-tag tag-green">STAY INVESTED</span><div class="decision-detail"><div class="decision-title">Maintain allocation — Bull + 2/3 or 3/3 alignment</div><div class="decision-desc">JIM says: "Primary trend remains intact." JIM avoids: "No risks present."</div></div></div>
    <div class="decision-item"><span class="decision-tag tag-green">ROTATE INTO LEADERS</span><div class="decision-detail"><div class="decision-title">Rebalance toward RS leaders — Bull/Cautious Bull + Momentum ≥ +1 + Rotation Confirmed</div><div class="decision-desc">JIM says: "Sector rotation supports reallocating toward [X]." JIM avoids: "All sectors will follow."</div></div></div>
    <div class="decision-item"><span class="decision-tag tag-green">ADD ON WEAKNESS</span><div class="decision-detail"><div class="decision-title">Use ST pullbacks in LT uptrend — Monthly Bull + Weekly Bull + Intraday Bearish</div><div class="decision-desc">JIM says: "Short-term weakness inside intact long-term uptrend creates tactical entry opportunity."</div></div></div>
    <div class="decision-item"><span class="decision-tag tag-yellow">STAY INVESTED WITH CAUTION</span><div class="decision-detail"><div class="decision-title">Maintain equity, reduce marginal risk — Cautious Bull + rate/vol headwinds active</div><div class="decision-desc">JIM says: "Trend remains constructive; secondary indicators limit conviction."</div></div></div>
    <div class="decision-item"><span class="decision-tag tag-yellow">AVOID LONG DURATION</span><div class="decision-detail"><div class="decision-title">Reduce rate-sensitive positions — Macro Pillar C ≤ −1 "Duration Pressure" + 10Y rising</div><div class="decision-desc">JIM says: "Rising real rates create headwinds for long-duration assets."</div></div></div>
    <div class="decision-item"><span class="decision-tag tag-yellow">PARTIAL ALLOCATION</span><div class="decision-detail"><div class="decision-title">50–70% target equity — Neutral + mixed timeframe + Confidence 4–6</div><div class="decision-desc">JIM says: "No dominant trend signal; partial exposure preserves optionality."</div></div></div>
    <div class="decision-item"><span class="decision-tag tag-yellow">BARBELL ALLOCATION</span><div class="decision-detail"><div class="decision-title">Quality defensive + selective risk — Neutral + high macro uncertainty</div><div class="decision-desc">JIM says: "Ambiguous signals recommend barbell — defensive quality and tactical exposure."</div></div></div>
    <div class="decision-item"><span class="decision-tag tag-orange">REDUCE WEAK EXPOSURES</span><div class="decision-detail"><div class="decision-title">Trim negative RS positions — Cautious Bull → Cautious Bear transition + Momentum ≤ −1</div><div class="decision-desc">JIM says: "Momentum deterioration in [X] warrants exposure reduction."</div></div></div>
    <div class="decision-item"><span class="decision-tag tag-orange">INCREASE CASH BUFFER</span><div class="decision-detail"><div class="decision-title">Raise cash above normal — Cautious Bear + Confidence falling + Break Conditions approaching</div><div class="decision-desc">JIM says: "Risk asymmetry favors increasing liquidity ahead of potential trend deterioration."</div></div></div>
    <div class="decision-item"><span class="decision-tag tag-orange">WAIT FOR CONFIRMATION</span><div class="decision-detail"><div class="decision-title">Pause deployment — Monthly Bear + Weekly Cautious Bull or Confidence ≤ 4</div><div class="decision-desc">JIM says: "Conflicting signals across timeframes; a confirmed directional break is required before allocation change."</div></div></div>
    <div class="decision-item"><span class="decision-tag tag-orange">NO NEW RISK</span><div class="decision-detail"><div class="decision-title">Freeze new positions — Bull → Cautious Bear transition + multiple Break Conditions</div><div class="decision-desc">JIM says: "Current environment does not support new risk additions."</div></div></div>
    <div class="decision-item"><span class="decision-tag tag-red">DEFENSIVE ALLOCATION</span><div class="decision-detail"><div class="decision-title">Cash, gold, short-duration IG — Bear + 2/3 or 3/3 bearish alignment + Liquidity ≤ −2</div><div class="decision-desc">JIM says: "Multi-factor deterioration supports defensive reallocation into capital-preserving assets."</div></div></div>
    <div class="decision-item"><span class="decision-tag tag-red">SELL RALLIES</span><div class="decision-detail"><div class="decision-title">Use bounces to reduce — Monthly Bear + Weekly Bear + Intraday Bull</div><div class="decision-desc">JIM says: "Short-term bounce inside confirmed bear trend. Use strength to reduce exposure." JIM avoids: "This could be a reversal."</div></div></div>
    <div class="decision-item"><span class="decision-tag tag-red">EXIT RISK ASSETS</span><div class="decision-detail"><div class="decision-title">Systematic liquidation — Strong Bear + StormGuard conditions met</div><div class="decision-desc">JIM says: "Structural deterioration across all timeframes warrants systematic exit from risk assets."</div></div></div>
    <div class="decision-item"><span class="decision-tag tag-red">CAPITAL PRESERVATION MODE</span><div class="decision-detail"><div class="decision-title">Maximum defensive — Strong Bear + StormGuard fully active + multiple systemic Break Conditions</div><div class="decision-desc">JIM says: "Capital preservation mode active. Return of capital is the objective." JIM avoids: any language suggesting near-term recovery.</div></div></div>
  </div>
</section>

<!-- 14 EXAMPLE SCENARIOS -->
<section class="section">
  <div class="section-tag">// 14</div>
  <h2 class="section-title">Example <span>Scenarios</span></h2>
  <p class="section-lead">Five canonical validation scenarios demonstrating the full pipeline. Scenario 5 represents the current live regime reading (May 2026).</p>

  <div class="scenario"><div class="scenario-header"><div class="scenario-title">Scenario 1 — Classic Full Alignment (Bullish)</div><div class="scenario-badge tag-green">Full Conviction</div></div><div class="scenario-body"><div class="scenario-grid"><div class="scenario-tf"><div class="scenario-tf-label">Monthly</div><div class="scenario-tf-state" style="color:var(--bull)">Strong Bull</div><div class="scenario-tf-score">+2.3</div></div><div class="scenario-tf"><div class="scenario-tf-label">Weekly</div><div class="scenario-tf-state" style="color:#4ade80">Bull</div><div class="scenario-tf-score">+1.6</div></div><div class="scenario-tf"><div class="scenario-tf-label">Intraday</div><div class="scenario-tf-state" style="color:#4ade80">Bull</div><div class="scenario-tf-score">+1.1</div></div></div><div class="scenario-arrow">→ Confluence: 3/3 · Confidence: 8.5 / 10 · Risk Mode: RISK-ON FULL</div><div class="scenario-output"><div class="scenario-output-row"><span class="scenario-output-key">State</span><span class="scenario-output-val" style="color:var(--bull)">Strong Bull · HPC11 50% / HPC22 50%</span></div><div class="scenario-output-row"><span class="scenario-output-key">Decision</span><span class="scenario-output-val">Fully Invested · Maximize Momentum · Cyclical Leaders</span></div><div class="scenario-output-row"><span class="scenario-output-key">JIM</span><span class="scenario-output-val">"Strong Bull: broad-based uptrend with high conviction across all timeframes."</span></div><div class="scenario-output-row"><span class="scenario-output-key">Watch</span><span class="scenario-output-val">Sentiment euphoria, breadth divergence, VIX complacency</span></div></div></div></div>

  <div class="scenario"><div class="scenario-header"><div class="scenario-title">Scenario 2 — ST Weakness in LT Uptrend</div><div class="scenario-badge tag-green">Add on Weakness</div></div><div class="scenario-body"><div class="scenario-grid"><div class="scenario-tf"><div class="scenario-tf-label">Monthly</div><div class="scenario-tf-state" style="color:var(--bull)">Bull</div><div class="scenario-tf-score">+1.8</div></div><div class="scenario-tf"><div class="scenario-tf-label">Weekly</div><div class="scenario-tf-state" style="color:var(--bull)">Bull</div><div class="scenario-tf-score">+1.2</div></div><div class="scenario-tf"><div class="scenario-tf-label">Intraday</div><div class="scenario-tf-state" style="color:var(--cautious-bear)">Cautious Bear</div><div class="scenario-tf-score">−0.5</div></div></div><div class="scenario-arrow">→ Confluence: 2/3 · Confidence: 7.8 / 10 · Risk Mode: RISK-ON SELECTIVE</div><div class="scenario-output"><div class="scenario-output-row"><span class="scenario-output-key">Decision</span><span class="scenario-output-val">Add on Weakness · Intraday pullback = tactical entry</span></div><div class="scenario-output-row"><span class="scenario-output-key">JIM</span><span class="scenario-output-val">"Short-term weakness inside intact long-term uptrend. Tactical add opportunity."</span></div><div class="scenario-output-row"><span class="scenario-output-key">Invalidation</span><span class="scenario-output-val">Weekly trend breaks below key support; weakness spreads to weekly frame</span></div></div></div></div>

  <div class="scenario"><div class="scenario-header"><div class="scenario-title">Scenario 3 — Bear Market Rally</div><div class="scenario-badge tag-red">Sell Rallies</div></div><div class="scenario-body"><div class="scenario-grid"><div class="scenario-tf"><div class="scenario-tf-label">Monthly</div><div class="scenario-tf-state" style="color:var(--bear)">Bear</div><div class="scenario-tf-score">−1.7</div></div><div class="scenario-tf"><div class="scenario-tf-label">Weekly</div><div class="scenario-tf-state" style="color:var(--bear)">Bear</div><div class="scenario-tf-score">−1.3</div></div><div class="scenario-tf"><div class="scenario-tf-label">Intraday</div><div class="scenario-tf-state" style="color:#4ade80">Bull</div><div class="scenario-tf-score">+0.8</div></div></div><div class="scenario-arrow">→ Bear dominant 2/3 · Confidence: 7.5 / 10 · Risk Mode: DEFENSE</div><div class="scenario-output"><div class="scenario-output-row"><span class="scenario-output-key">Decision</span><span class="scenario-output-val">Sell Rallies · Use intraday bounce to reduce exposure</span></div><div class="scenario-output-row"><span class="scenario-output-key">JIM</span><span class="scenario-output-val">"Bear market technical bounce inside confirmed downtrend. Use strength to reduce."</span></div></div></div></div>

  <div class="scenario"><div class="scenario-header"><div class="scenario-title">Scenario 4 — Break Condition Override (Systemic)</div><div class="scenario-badge tag-red">BC Active</div></div><div class="scenario-body"><div class="scenario-grid"><div class="scenario-tf"><div class="scenario-tf-label">Monthly</div><div class="scenario-tf-state" style="color:#a3e635">Cautious Bull</div><div class="scenario-tf-score">+0.6</div></div><div class="scenario-tf"><div class="scenario-tf-label">Weekly</div><div class="scenario-tf-state" style="color:var(--cautious-bear)">Cautious Bear</div><div class="scenario-tf-score">−0.4</div></div><div class="scenario-tf"><div class="scenario-tf-label">Intraday</div><div class="scenario-tf-state" style="color:var(--bear)">Bear</div><div class="scenario-tf-score">−1.8</div></div></div><div class="scenario-arrow" style="border-left-color:var(--bear)">⚠ BC-1 TRIGGERED: VIX 38 | BC-4 TRIGGERED: HY +120bps | BC-3: Breadth 32%</div><div class="scenario-output"><div class="scenario-output-row"><span class="scenario-output-key">Override</span><span class="scenario-output-val" style="color:var(--bear)">Break Conditions force downgrade → Bear | Confidence −4.0 | Risk Mode: DEFENSE</span></div><div class="scenario-output-row"><span class="scenario-output-key">Decision</span><span class="scenario-output-val">Defensive Allocation · Mandatory posture review · Raise cash immediately</span></div><div class="scenario-output-row"><span class="scenario-output-key">JIM</span><span class="scenario-output-val">"Multiple break conditions active — defensive review mandatory. Trend state downgraded."</span></div></div></div></div>

  <div class="scenario"><div class="scenario-header"><div class="scenario-title">Scenario 5 — LIVE: May 2026 Current Regime</div><div class="scenario-badge tag-yellow" style="background:rgba(163,230,53,0.1);color:#a3e635;border:1px solid rgba(163,230,53,0.3)">Cautious Bull</div></div><div class="scenario-body"><div class="scenario-grid"><div class="scenario-tf"><div class="scenario-tf-label">Monthly</div><div class="scenario-tf-state" style="color:#a3e635">Cautious Bull</div><div class="scenario-tf-score">+0.72</div></div><div class="scenario-tf"><div class="scenario-tf-label">Weekly</div><div class="scenario-tf-state" style="color:#4ade80">Bull</div><div class="scenario-tf-score">+1.2</div></div><div class="scenario-tf"><div class="scenario-tf-label">Intraday</div><div class="scenario-tf-state" style="color:var(--neutral)">Neutral / Cautious</div><div class="scenario-tf-score">−0.4</div></div></div><div class="scenario-arrow">→ Confluence: 2/3 · Confidence: 7.2 / 10 · Risk Mode: CAUTIOUS GROWTH · HPC 60/40</div><div class="scenario-output"><div class="scenario-output-row"><span class="scenario-output-key">Decision</span><span class="scenario-output-val">Stay Invested · Rotate toward Tech/Energy · Avoid Long Duration · Watch VIX and 10Y</span></div><div class="scenario-output-row"><span class="scenario-output-key">Active Watches</span><span class="scenario-output-val">VIX at 22.4 (28 threshold 20% away) · 10Y at 4.42% (5.2% threshold 17% away)</span></div><div class="scenario-output-row"><span class="scenario-output-key">JIM</span><span class="scenario-output-val">"Cautious Bull: resilient growth, but tightening financial conditions cap upside. Stay invested selectively."</span></div></div></div></div>
</section>

<!-- 15 JSON SCHEMA v2 -->
<section class="section">
  <div class="section-tag">// 15</div>
  <h2 class="section-title">JSON Schema <span>v2.0</span></h2>
  <p class="section-lead">Canonical data structure for all Market Trend state storage, API delivery, Memory Engine persistence, and JIM context injection. SHA-256 hashed on every write. Immutable audit trail.</p>
  <div class="json-block">
{
  <span class="json-key">"module"</span>: <span class="json-str">"market_trend"</span>,
  <span class="json-key">"schema_version"</span>: <span class="json-str">"2.0"</span>,
  <span class="json-key">"generated_at"</span>: <span class="json-str">"2026-05-01T14:32:00Z"</span>,
  <span class="json-key">"session_id"</span>: <span class="json-str">"MTE-20260501-001"</span>,

  <span class="json-key">"data_freshness"</span>: {
    <span class="json-key">"all_sources_fresh"</span>: <span class="json-bool">true</span>,
    <span class="json-key">"stale_sources"</span>: [],
    <span class="json-key">"last_macro_update"</span>: <span class="json-str">"2026-04-30"</span>,
    <span class="json-key">"last_price_update"</span>: <span class="json-str">"2026-05-01"</span>
  },

  <span class="json-key">"signal_blocks"</span>: {
    <span class="json-key">"activity_growth"</span>:     { <span class="json-key">"score"</span>: <span class="json-num">1.5</span>, <span class="json-key">"freshness"</span>: <span class="json-num">1.0</span>, <span class="json-key">"confidence"</span>: <span class="json-num">0.95</span> },
    <span class="json-key">"inflation_persistence"</span>: { <span class="json-key">"score"</span>: <span class="json-num">-1.5</span>, <span class="json-key">"freshness"</span>: <span class="json-num">0.85</span>, <span class="json-key">"confidence"</span>: <span class="json-num">0.90</span> },
    <span class="json-key">"monetary_liquidity_curve"</span>:{ <span class="json-key">"score"</span>: <span class="json-num">0.5</span>, <span class="json-key">"freshness"</span>: <span class="json-num">1.0</span>, <span class="json-key">"confidence"</span>: <span class="json-num">0.95</span> },
    <span class="json-key">"credit_stability"</span>:       { <span class="json-key">"score"</span>: <span class="json-num">-0.5</span>, <span class="json-key">"freshness"</span>: <span class="json-num">1.0</span>, <span class="json-key">"confidence"</span>: <span class="json-num">0.90</span> },
    <span class="json-key">"equity_fundamentals"</span>:    { <span class="json-key">"score"</span>: <span class="json-num">1.0</span>, <span class="json-key">"freshness"</span>: <span class="json-num">0.80</span>, <span class="json-key">"confidence"</span>: <span class="json-num">0.75</span> },
    <span class="json-key">"flow_volatility_positioning"</span>:{ <span class="json-key">"score"</span>: <span class="json-num">0.5</span>, <span class="json-key">"freshness"</span>: <span class="json-num">1.0</span>, <span class="json-key">"confidence"</span>: <span class="json-num">0.85</span> }
  },

  <span class="json-key">"pillar_scores"</span>: {
    <span class="json-key">"price_structure"</span>:  { <span class="json-key">"score"</span>: <span class="json-num">2</span>, <span class="json-key">"weight"</span>: <span class="json-num">0.25</span>, <span class="json-key">"contribution"</span>: <span class="json-num">0.50</span>, <span class="json-key">"stale"</span>: <span class="json-bool">false</span> },
    <span class="json-key">"momentum"</span>:          { <span class="json-key">"score"</span>: <span class="json-num">1</span>, <span class="json-key">"weight"</span>: <span class="json-num">0.20</span>, <span class="json-key">"contribution"</span>: <span class="json-num">0.20</span>, <span class="json-key">"stale"</span>: <span class="json-bool">false</span> },
    <span class="json-key">"macro_trend"</span>:       { <span class="json-key">"score"</span>: <span class="json-num">0</span>, <span class="json-key">"weight"</span>: <span class="json-num">0.15</span>, <span class="json-key">"contribution"</span>: <span class="json-num">0.00</span>, <span class="json-key">"stale"</span>: <span class="json-bool">false</span> },
    <span class="json-key">"volatility"</span>:        { <span class="json-key">"score"</span>: <span class="json-num">-1</span>, <span class="json-key">"weight"</span>: <span class="json-num">0.10</span>, <span class="json-key">"contribution"</span>: <span class="json-num">-0.10</span>, <span class="json-key">"stale"</span>: <span class="json-bool">false</span> },
    <span class="json-key">"liquidity"</span>:         { <span class="json-key">"score"</span>: <span class="json-num">1</span>, <span class="json-key">"weight"</span>: <span class="json-num">0.10</span>, <span class="json-key">"contribution"</span>: <span class="json-num">0.10</span>, <span class="json-key">"stale"</span>: <span class="json-bool">false</span> },
    <span class="json-key">"positioning"</span>:       { <span class="json-key">"score"</span>: <span class="json-num">0</span>, <span class="json-key">"weight"</span>: <span class="json-num">0.10</span>, <span class="json-key">"contribution"</span>: <span class="json-num">0.00</span>, <span class="json-key">"stale"</span>: <span class="json-bool">false</span> },
    <span class="json-key">"sentiment"</span>:         { <span class="json-key">"score"</span>: <span class="json-num">1</span>, <span class="json-key">"weight"</span>: <span class="json-num">0.05</span>, <span class="json-key">"contribution"</span>: <span class="json-num">0.05</span>, <span class="json-key">"stale"</span>: <span class="json-bool">false</span> },
    <span class="json-key">"correlation"</span>:       { <span class="json-key">"score"</span>: <span class="json-num">-1</span>, <span class="json-key">"weight"</span>: <span class="json-num">0.05</span>, <span class="json-key">"contribution"</span>: <span class="json-num">-0.05</span>, <span class="json-key">"stale"</span>: <span class="json-bool">false</span> }
  },

  <span class="json-key">"timeframe_scores"</span>: {
    <span class="json-key">"monthly"</span>:  { <span class="json-key">"raw_score"</span>: <span class="json-num">0.72</span>, <span class="json-key">"state"</span>: <span class="json-str">"cautious_bull"</span>, <span class="json-key">"weights"</span>: <span class="json-str">"monthly_default"</span> },
    <span class="json-key">"weekly"</span>:   { <span class="json-key">"raw_score"</span>: <span class="json-num">1.20</span>, <span class="json-key">"state"</span>: <span class="json-str">"bull"</span>, <span class="json-key">"weights"</span>: <span class="json-str">"weekly_adjusted"</span> },
    <span class="json-key">"intraday"</span>: { <span class="json-key">"raw_score"</span>: <span class="json-num">-0.40</span>, <span class="json-key">"state"</span>: <span class="json-str">"cautious_bear"</span>, <span class="json-key">"weights"</span>: <span class="json-str">"intraday_adjusted"</span> }
  },

  <span class="json-key">"composite"</span>: {
    <span class="json-key">"final_score"</span>: <span class="json-num">0.72</span>,
    <span class="json-key">"trend_state"</span>: <span class="json-str">"cautious_bull"</span>,
    <span class="json-key">"risk_mode"</span>: <span class="json-str">"CAUTIOUS_GROWTH"</span>,
    <span class="json-key">"hpc11_weight"</span>: <span class="json-num">0.60</span>,
    <span class="json-key">"hpc22_weight"</span>: <span class="json-num">0.40</span>,
    <span class="json-key">"equity_total"</span>: <span class="json-num">0.85</span>,
    <span class="json-key">"cash_buffer"</span>: <span class="json-num">0.10</span>,
    <span class="json-key">"confluence"</span>: <span class="json-str">"medium_2_of_3"</span>,
    <span class="json-key">"confidence_score"</span>: <span class="json-num">7.2</span>,
    <span class="json-key">"confirmations_met"</span>: <span class="json-num">5</span>
  },

  <span class="json-key">"break_conditions"</span>: {
    <span class="json-key">"any_triggered"</span>: <span class="json-bool">false</span>,
    <span class="json-key">"approaching_threshold"</span>: [<span class="json-str">"bc1_vix_watch"</span>, <span class="json-str">"bc2_10y_monitor"</span>],
    <span class="json-key">"active_overrides"</span>: [],
    <span class="json-key">"active_vetos"</span>: [<span class="json-str">"VETO-1_duration"</span>]
  },

  <span class="json-key">"decision"</span>: {
    <span class="json-key">"primary"</span>: <span class="json-str">"stay_invested_with_caution"</span>,
    <span class="json-key">"secondary"</span>: [<span class="json-str">"rotate_into_leaders"</span>, <span class="json-str">"avoid_long_duration"</span>],
    <span class="json-key">"avoid"</span>: [<span class="json-str">"leverage"</span>, <span class="json-str">"long_duration_bonds"</span>, <span class="json-str">"rate_sensitive_growth"</span>]
  },

  <span class="json-key">"memory"</span>: {
    <span class="json-key">"previous_state"</span>: <span class="json-str">"bull"</span>,
    <span class="json-key">"previous_risk_mode"</span>: <span class="json-str">"RISK_ON_SELECTIVE"</span>,
    <span class="json-key">"state_changed"</span>: <span class="json-bool">true</span>,
    <span class="json-key">"change_direction"</span>: <span class="json-str">"downgrade"</span>,
    <span class="json-key">"days_in_current_state"</span>: <span class="json-num">14</span>,
    <span class="json-key">"score_trend_7d"</span>: <span class="json-str">"declining"</span>
  },

  <span class="json-key">"narratives"</span>: {
    <span class="json-key">"headline"</span>: <span class="json-str">"Cautious Bull: resilient growth, but financial conditions tightening cap upside."</span>,
    <span class="json-key">"institutional"</span>: <span class="json-str">"[Full CIO text — 4 sentences with break conditions]"</span>,
    <span class="json-key">"client_ready"</span>: <span class="json-str">"[Advisor-to-client text — 2-3 sentences]"</span>,
    <span class="json-key">"invalidation_condition"</span>: <span class="json-str">"10Y yield above 5.2% or VIX sustained above 28."</span>,
    <span class="json-key">"output_1_sha256"</span>: <span class="json-str">"abc123..."</span>,
    <span class="json-key">"output_2_sha256"</span>: <span class="json-str">"def456..."</span>
  },

  <span class="json-key">"access_tier"</span>: {
    <span class="json-key">"headline"</span>: <span class="json-str">"all"</span>,
    <span class="json-key">"risk_mode"</span>: <span class="json-str">"fa_lite+"</span>,
    <span class="json-key">"hpc_weights"</span>: <span class="json-str">"fa_pro+"</span>,
    <span class="json-key">"institutional_narrative"</span>: <span class="json-str">"mfo+"</span>,
    <span class="json-key">"pillar_scores"</span>: <span class="json-str">"mfo+"</span>,
    <span class="json-key">"signal_blocks"</span>: <span class="json-str">"fo_inst"</span>,
    <span class="json-key">"memory_history"</span>: <span class="json-str">"fo_inst"</span>,
    <span class="json-key">"break_condition_detail"</span>: <span class="json-str">"mfo+"</span>
  }
}
  </div>
</section>

<!-- 16 IMPLEMENTATION NOTES -->
<section class="section">
  <div class="section-tag">// 16</div>
  <h2 class="section-title">Implementation <span>Notes</span></h2>
  <p class="section-lead">Build priority sequence, engineering constraints, and open questions. This section guides technical implementation from prototype to production.</p>

  <h3>Priority Build Sequence</h3>
  <div class="table-wrap"><table>
    <thead><tr><th>Phase</th><th>Component</th><th>Dependencies</th><th>Notes</th></tr></thead>
    <tbody>
      <tr><td class="mono" style="color:var(--bull)">Phase 1</td><td class="bold">Price Structure + Momentum Pillars</td><td>EOD price API</td><td>Enables basic Trend State output and dashboard display</td></tr>
      <tr><td class="mono" style="color:var(--bull)">Phase 1</td><td class="bold">Timeframe Matrix + Conflict Resolution</td><td>Phase 1 pillars</td><td>Core differentiator. Must work before any dashboard display.</td></tr>
      <tr><td class="mono" style="color:var(--bull)">Phase 1</td><td class="bold">Risk Mode System — HPC Split Output</td><td>Trend State</td><td>Directly feeds Market Trends screen allocation bars</td></tr>
      <tr><td class="mono" style="color:#a3e635">Phase 2</td><td class="bold">Volatility + Macro + Liquidity Pillars</td><td>VIX, Fed/BLS, credit APIs</td><td>Adds Break Condition monitoring capability</td></tr>
      <tr><td class="mono" style="color:#a3e635">Phase 2</td><td class="bold">Break Conditions Engine</td><td>Phase 2 pillars</td><td>Override logic; critical for institutional credibility</td></tr>
      <tr><td class="mono" style="color:var(--gold)">Phase 3</td><td class="bold">Six Signal Blocks</td><td>Macro data feeds</td><td>Full macro architecture; enables Structural Regime scoring</td></tr>
      <tr><td class="mono" style="color:var(--gold)">Phase 3</td><td class="bold">Memory Engine</td><td>Database (immutable log)</td><td>State persistence, audit trail, JIM context awareness</td></tr>
      <tr><td class="mono" style="color:var(--gold)">Phase 3</td><td class="bold">Confidence Score Computation</td><td>All pillars live</td><td>Can be approximated in earlier phases with partial data</td></tr>
      <tr><td class="mono" style="color:var(--cautious-bear)">Phase 4</td><td class="bold">JIM Narrative — INT-031 to INT-038</td><td>Full scoring engine</td><td>8 new intents required; define and add to intents_v2.json</td></tr>
      <tr><td class="mono" style="color:var(--cautious-bear)">Phase 4</td><td class="bold">AlphaDroid → Pillar B Integration</td><td>AlphaDroid API</td><td>Systematic signal feeds Momentum pillar directly</td></tr>
    </tbody>
  </table></div>

  <h3>Engineering Constraints</h3>
  <div class="card-grid">
    <div class="card"><div class="card-title" style="margin-bottom:10px">Scoring Idempotency</div><p>Same input data must produce identical output score. All randomness excluded. Timestamps of all sources stored with each computation.</p></div>
    <div class="card"><div class="card-title" style="margin-bottom:10px">Stale Data Handling</div><p>Never use cached pillar scores beyond staleness threshold. If source unavailable → set pillar to 0 + apply Confidence penalty. Log the staleness event.</p></div>
    <div class="card"><div class="card-title" style="margin-bottom:10px">Break Condition Audit</div><p>Every override must be logged: timestamp, condition name, pre-state, post-state, and the exact threshold value that triggered it. 7-year retention.</p></div>
    <div class="card"><div class="card-title" style="margin-bottom:10px">Access Tier Enforcement</div><p>Enforced at API response level, not frontend. Full JSON computed; partial JSON returned by tier. Signal blocks = FO_INST only. Memory history = FO_INST only.</p></div>
    <div class="card"><div class="card-title" style="margin-bottom:10px">Memory Engine Immutability</div><p>All Memory Engine writes are append-only. No deletion or modification allowed. SHA-256 hash on every write. Monthly integrity verification.</p></div>
    <div class="card"><div class="card-title" style="margin-bottom:10px">StormGuard Priority</div><p>StormGuard activation always overrides Trend State. When SGA active: force Capital Preservation Mode regardless of final score. This cannot be disabled by any user tier.</p></div>
  </div>

  <h3>Open Questions / Future Enhancements</h3>
  <div class="table-wrap"><table>
    <thead><tr><th>Question</th><th>Priority</th><th>Notes</th></tr></thead>
    <tbody>
      <tr><td class="bold">Dynamic pillar weights by volatility regime?</td><td><span class="badge badge-gold">High</span></td><td>In high-vol regimes, Volatility pillar weight should auto-increase. Research required.</td></tr>
      <tr><td class="bold">Brazilian market localization (SELIC, IBOVESPA, IPCA)?</td><td><span class="badge badge-gold">High</span></td><td>Brazilian FO clients need local macro block. Separate weight set for BRL portfolios.</td></tr>
      <tr><td class="bold">AlphaDroid signal as direct Pillar B input?</td><td><span class="badge badge-gold">High</span></td><td>API integration design required. Feeds systematic momentum directly.</td></tr>
      <tr><td class="bold">ML on historical pillar scores vs market outcomes?</td><td><span class="badge badge-blue">Medium</span></td><td>Backtesting weight configurations over 10+ year historical regimes to optimize empirically.</td></tr>
      <tr><td class="bold">Geopolitical black swan emergency protocol?</td><td><span class="badge badge-blue">Medium</span></td><td>Geopolitical risk cannot be scored pre-event. Manual override + emergency state classification needed.</td></tr>
      <tr><td class="bold">Confidence Score accuracy validation?</td><td><span class="badge badge-blue">Medium</span></td><td>Track Confidence Score vs subsequent trend direction correctness over 30/60/90 days.</td></tr>
    </tbody>
  </table></div>
</section>

</div><!-- /doc-body -->

<footer>
  <div class="brand">HARPIAN</div>
  <div class="note">Market Trend Decision Engine v2.0 — Consolidated · Proprietary &amp; Restricted · © HARPIAN Portfolio Engineering Terminal · May 2026</div>
</footer>

</body>
</html>"""

with open('market_trend_engine_v2.html', 'w', encoding='utf-8') as f:
    f.write(HTML)

print(f"Done. File size: {len(HTML):,} chars")
