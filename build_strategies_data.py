"""
Parse all HPC11/HPC22 AlphaDroid CSVs and generate harpian_strategies_data.js
Run from anywhere: python build_strategies_data.py
"""
import os, csv, re, json

BASE = r"C:\Users\jfdco\OneDrive\Área de Trabalho\HARPIAN\planilhas históricas do AlphaDroid das estratégias"
OUT  = r"C:\dev\harpian-prototype\harpian_strategies_data.js"

def parse_csv(filepath):
    rows = []
    with open(filepath, encoding='utf-8-sig', errors='replace') as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append([c.strip().strip('"') for c in row])
    return rows

def extract(rows):
    d = {}
    name_row = rows[0] if rows else []
    d['full_name'] = name_row[3] if len(name_row) >= 4 else ''
    d['mode'] = rows[1][0] if len(rows) > 1 and rows[1] else ''
    for r in rows:
        if len(r) >= 5 and r[0] == 'Last Trade':
            d['last_trade'] = r[1]; d['score'] = r[4]
        if r[0] == 'BornOn Date' and len(r) >= 2 and '%' not in str(r[1]):
            d['born_on'] = r[1]
        if len(r) >= 2 and r[0] == 'Trades/Year':
            d['trades_yr'] = r[1]
        if len(r) >= 3:
            if r[0] == 'Last Week':   d['ret_1w'] = r[1];  d['spy_1w'] = r[2]
            if r[0] == 'Last Month':  d['ret_1m'] = r[1];  d['spy_1m'] = r[2]
            if r[0] == 'Half Year':   d['ret_6m'] = r[1];  d['spy_6m'] = r[2]
            if r[0] == 'BornOn Date' and '%' in str(r[1]):
                d['ret_born'] = r[1]; d['spy_born'] = r[2]
            if r[0] == 'All Years':   d['cagr_all'] = r[1]; d['spy_cagr_all'] = r[2]
            if r[0] == '10 Years':    d['cagr_10y'] = r[1]
            if r[0] == '5 Years':     d['cagr_5y']  = r[1]
            if r[0] == '3 Years':     d['cagr_3y']  = r[1]
            if r[0] == '1 Year':      d['cagr_1y']  = r[1]
            if r[0] == 'Y.T.D.':      d['ytd']      = r[1]
        if r[0] == 'Sharpe Ratio'  and 'sharpe'  not in d and len(r)>=3: d['sharpe']  = r[1]
        if r[0] == 'Max Drawdown'  and 'maxdd'   not in d and len(r)>=3: d['maxdd']   = r[1]
        if r[0] == 'Sortino Ratio' and 'sortino' not in d and len(r)>=3: d['sortino'] = r[1]
        if r[0] == 'Std.Deviation' and 'vol'     not in d and len(r)>=3: d['vol']     = r[1]
        if r[0] == 'Alt.Buy-1' and len(r) >= 5:
            d['alt1'] = r[1].strip(); d['alt2'] = r[4].strip()
        m = re.match(r'^(20\d\d|19\d\d)$', r[0])
        if m and len(r) >= 3:
            try:
                d.setdefault('years', {})[int(r[0])] = {
                    's': float(r[1]), 'spy': float(r[2])
                }
            except Exception:
                pass
    return d

HPC11_META = {
    '054': {'id': 'S21', 'label': 'US Treasuries',      'category': 'Fixed Income'},
    '055': {'id': 'S22', 'label': 'Global IG Bonds',    'category': 'Fixed Income'},
    '056': {'id': 'S23', 'label': 'Global High Yield',  'category': 'Fixed Income'},
    '057': {'id': 'S24', 'label': 'Global Equity Div.', 'category': 'Equity'},
    '058': {'id': 'S25', 'label': 'US Defensive',       'category': 'Equity'},
    '059': {'id': 'S26', 'label': 'US Large Cap',       'category': 'Equity'},
    '060': {'id': 'S27', 'label': 'Developed Countries','category': 'Equity'},
    '061': {'id': 'S28', 'label': 'Emerging Markets',   'category': 'Equity'},
    '062': {'id': 'S29', 'label': 'US Small & Mid Cap', 'category': 'Equity'},
    '063': {'id': 'S30', 'label': 'Global Innovation',  'category': 'Equity'},
    '064': {'id': 'S31', 'label': 'Alternative Inv.',   'category': 'Alternative'},
}

HPC22_META = {
    '055': {'id': 'S22',     'label': 'Global IG Bonds',       'sector': 'Fixed Income',     'act': 'Base'},
    '065': {'id': 'S32C',    'label': 'Big Tech',              'sector': 'Technology',        'act': 'Core'},
    '164': {'id': 'ACT1TE',  'label': 'Technology ACT1',       'sector': 'Technology',        'act': 'ACT1'},
    '165': {'id': 'ACT2TE',  'label': 'Technology ACT2',       'sector': 'Technology',        'act': 'ACT2'},
    '166': {'id': 'ACT1CO',  'label': 'Communication ACT1',    'sector': 'Communication',     'act': 'ACT1'},
    '167': {'id': 'ACT2CO',  'label': 'Communication ACT2',    'sector': 'Communication',     'act': 'ACT2'},
    '168': {'id': 'ACT1CD',  'label': 'Consumer Disc. ACT1',   'sector': 'Consumer Disc.',    'act': 'ACT1'},
    '169': {'id': 'ACT2CD',  'label': 'Consumer Disc. ACT2',   'sector': 'Consumer Disc.',    'act': 'ACT2'},
    '170': {'id': 'ACT1CS',  'label': 'Consumer Staples ACT1', 'sector': 'Consumer Staples',  'act': 'ACT1'},
    '171': {'id': 'ACT2CS',  'label': 'Consumer Staples ACT2', 'sector': 'Consumer Staples',  'act': 'ACT2'},
    '172': {'id': 'ACT1FIN', 'label': 'Financials ACT1',       'sector': 'Financials',        'act': 'ACT1'},
    '173': {'id': 'ACT2FIN', 'label': 'Financials ACT2',       'sector': 'Financials',        'act': 'ACT2'},
    '174': {'id': 'ACT1HE',  'label': 'Healthcare ACT1',       'sector': 'Healthcare',        'act': 'ACT1'},
    '175': {'id': 'ACT2HE',  'label': 'Healthcare ACT2',       'sector': 'Healthcare',        'act': 'ACT2'},
    '176': {'id': 'ACT1IN',  'label': 'Industrials ACT1',      'sector': 'Industrials',       'act': 'ACT1'},
    '177': {'id': 'ACT2IN',  'label': 'Industrials ACT2',      'sector': 'Industrials',       'act': 'ACT2'},
    '178': {'id': 'ACT1MA',  'label': 'Materials ACT1',        'sector': 'Materials',         'act': 'ACT1'},
    '179': {'id': 'ACT2MA',  'label': 'Materials ACT2',        'sector': 'Materials',         'act': 'ACT2'},
    '180': {'id': 'ACT1RE',  'label': 'Real Estate ACT1',      'sector': 'Real Estate',       'act': 'ACT1'},
    '181': {'id': 'ACT2RE',  'label': 'Real Estate ACT2',      'sector': 'Real Estate',       'act': 'ACT2'},
    '182': {'id': 'ACT1EN',  'label': 'Energy ACT1',           'sector': 'Energy',            'act': 'ACT1'},
    '183': {'id': 'ACT2EN',  'label': 'Energy ACT2',           'sector': 'Energy',            'act': 'ACT2'},
}

def process_dir(folder, meta):
    result = []
    for fname in sorted(os.listdir(folder)):
        if not fname.endswith('.csv'): continue
        prefix = fname[:3]
        if prefix not in meta: continue
        rows = parse_csv(os.path.join(folder, fname))
        d = extract(rows)
        m = meta[prefix]
        entry = {
            'id':           m['id'],
            'label':        m['label'],
            'full_name':    d.get('full_name', ''),
            'mode':         d.get('mode', ''),
            'born_on':      d.get('born_on', ''),
            'last_trade':   d.get('last_trade', ''),
            'score':        d.get('score', ''),
            'trades_yr':    d.get('trades_yr', ''),
            'alt1':         d.get('alt1', ''),
            'alt2':         d.get('alt2', ''),
            'cagr_all':     d.get('cagr_all', ''),
            'cagr_10y':     d.get('cagr_10y', ''),
            'cagr_5y':      d.get('cagr_5y', ''),
            'cagr_3y':      d.get('cagr_3y', ''),
            'cagr_1y':      d.get('cagr_1y', ''),
            'ytd':          d.get('ytd', ''),
            'sharpe':       d.get('sharpe', ''),
            'maxdd':        d.get('maxdd', ''),
            'sortino':      d.get('sortino', ''),
            'vol':          d.get('vol', ''),
            'spy_cagr_all': d.get('spy_cagr_all', ''),
            'ret_1w':       d.get('ret_1w', ''),
            'spy_1w':       d.get('spy_1w', ''),
            'ret_1m':       d.get('ret_1m', ''),
            'spy_1m':       d.get('spy_1m', ''),
            'ret_6m':       d.get('ret_6m', ''),
            'spy_6m':       d.get('spy_6m', ''),
            'ret_born':     d.get('ret_born', ''),
            'spy_born':     d.get('spy_born', ''),
            'years':        {str(k): v for k, v in sorted(d.get('years', {}).items())},
        }
        for key in ('category', 'sector', 'act'):
            if key in m: entry[key] = m[key]
        result.append(entry)
    return result

hpc11 = process_dir(os.path.join(BASE, 'HPC11'), HPC11_META)
hpc22 = process_dir(os.path.join(BASE, 'HPC22'), HPC22_META)

js = (
    "// HARPIAN Strategy Database — auto-generated from AlphaDroid CSVs\n"
    "// Generated: 2026-05-02  |  DO NOT EDIT MANUALLY\n"
    "// Source: planilhas historicas do AlphaDroid das estrategias\n\n"
    "const HPC11_STRATEGIES = " + json.dumps(hpc11, indent=2, ensure_ascii=False) + ";\n\n"
    "const HPC22_STRATEGIES = " + json.dumps(hpc22, indent=2, ensure_ascii=False) + ";\n"
)

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(js)

print(f"OK  {OUT}")
print(f"HPC11: {len(hpc11)} strategies | HPC22: {len(hpc22)} strategies")
for s in hpc11:
    print(f"  HPC11 {s['id']:5s} {s['label']:25s} CAGR-all={s['cagr_all']:>6}% | 5Y={s['cagr_5y']:>6}% | Sharpe={s['sharpe']} | MaxDD={s['maxdd']}")
