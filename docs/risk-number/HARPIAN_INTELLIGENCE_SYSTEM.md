# HARPIAN INTELLIGENCE SYSTEM

## Nitrogen / Riskalyze Intelligence Dossier

This file is the central Harpian reference for the Nitrogen/Riskalyze archive and reverse-engineering work completed on 2026-04-27.

## Local Archive

Primary folders:

- `nitrogen_site_archive/`
  - Public Nitrogen/Riskalyze mirror.
  - 878 sitemap URLs scanned.
  - 1,793 public assets downloaded.
  - 87 PDFs extracted into searchable text.
  - Main technical model: `nitrogen_site_archive/risk_number_model.md`
  - Estimator script: `nitrogen_site_archive/risk_number_estimator.js`
- `nitrogen_authenticated_capture/`
  - Sanitized authenticated reports-page capture.
  - Visible reports page was the report template builder, not a direct list of downloadable reports.
  - Session/HAR/JWT/passcode artifacts were removed after analysis.

Important files:

- `nitrogen_site_archive/risk_number_model.md`
- `nitrogen_site_archive/risk_number_estimator.js`
- `nitrogen_site_archive/extracted_text/926087680ba5ddfe_nitrogenwealth.com__wp-content__uploads__2022__12__The-Math-Behind-Nitrogen.txt`
- `nitrogen_site_archive/extracted_text/4d34a6e868a4c334_strongvalley.com__wp-content__uploads__2020__12__The-Math-Behind-Riskalyze.txt`
- `nitrogen_site_archive/extracted_text/f3b9d0b67342ff7b_nitrogenwealth.com__wp-content__uploads__2022__12__StatsOverviewExample.txt`
- `nitrogen_authenticated_capture/ffb6b41e94af8cab6e9b78f3fdd52bdc05a134e3.json`

## Core Findings

Nitrogen's Risk Number is proprietary, but public and authenticated materials reveal the broad portfolio-risk method:

- A portfolio receives a six-month return and volatility scenario.
- Holding-level return, volatility, and correlation feed a covariance matrix.
- The portfolio's 95% Historical/Probability Range is based on standard deviation.
- Nitrogen/Riskalyze describes using Value at Risk with a normal distribution at `1.64` sigmas.
- They state that Monte Carlo is not used for this range.

Working formula:

```text
six_month_downside = six_month_expected_return - 1.64 * six_month_volatility
six_month_upside   = six_month_expected_return + 1.64 * six_month_volatility
```

Risk Number is then mapped from downside risk. Disclosed approximate anchors:

| Six-month downside | Approximate Risk Number |
|---:|---:|
| -2% | low 20s |
| -5% | low 30s |
| -7% | low 40s |
| -12% | low 60s |
| -18% | low 80s |

Additional examples found:

| Source | Risk Number | Six-month range |
|---|---:|---:|
| Public Stats Overview example | 45 | -8.21% to +14% |
| Public IPS/example report | 91 | about -27% to +33% |
| Authenticated benchmark data | SPY 70 | benchmark Risk Number |
| Authenticated benchmark data | AGG 29 | benchmark Risk Number |
| Authenticated benchmark data | 70/30 Blend 52 | benchmark Risk Number |
| Authenticated benchmark data | 50/50 Blend 42 | benchmark Risk Number |

## Harpian Transparency Model

The client question was:

> If a client wants 100% profit in three years, what would his Risk Number and volatility be?

The transparent answer:

```text
100% total return in 3 years = 2.0x starting wealth
Required annual compound return = 2^(1/3) - 1 = 25.99%
Required six-month compound return = 2^(1/6) - 1 = 12.25%
```

A return target alone does not determine the Risk Number. Risk Number depends on downside risk, and downside risk depends on volatility.

Using the Nitrogen-style 6-month VaR equation with `r6 = 12.25%`:

| Annual volatility assumption | Six-month downside | Approx Risk Number |
|---:|---:|---:|
| 18% | -8.63% | ~49 |
| 25% | -16.75% | ~78 |
| 35% | -28.34% | ~92 |
| 50% | -45.74% | ~99 |
| 56% | -52.69% | ~99 |

Practical conclusion:

- A 100% target over 3 years requires about `26%` annualized return.
- If pursued through public-market beta or leverage, it is likely a `Risk Number 99` style objective.
- If someone claims this target with low Risk Number, the missing variable is the assumed volatility/downside.
- Harpian should present this as a transparency calculation, not a guarantee.

## Harpian Use

This can become part of the Harpian Intelligence System as:

- A risk-expectation translation layer.
- A client transparency calculator.
- A competitive-methodology reference.
- A suitability control for aggressive return targets.
- A benchmark comparison layer for Harpian simulator charts.

Recommended Harpian phrasing:

```text
Target return is not risk tolerance. Harpian separates destination risk from journey risk:
the desired outcome, the volatility required to pursue it, and the downside a client must be able to withstand.
```

## Run The Estimator

From the project root:

```powershell
node nitrogen_site_archive\risk_number_estimator.js
```

Current output:

```text
Target total return: 100.00% in 3 years
Required CAGR: 25.99%
Required 6-month compound return: 12.25%

Annual vol 18.00% -> downside -8.63% -> approx RN 49
Annual vol 25.00% -> downside -16.75% -> approx RN 78
Annual vol 35.00% -> downside -28.34% -> approx RN 92
Annual vol 50.00% -> downside -45.74% -> approx RN 99
Annual vol 56.00% -> downside -52.69% -> approx RN 99
```

## Asset Benchmark Table

The first simulator benchmark table is saved in:

- `harpian_asset_benchmarks/harpian_asset_benchmark_table.csv`
- `harpian_asset_benchmarks/harpian_asset_benchmark_table_raw.csv`
- `harpian_asset_benchmarks/harpian_asset_benchmark_table.md`

The table includes:

- US Treasury proxies: `SHY`, `IEF`, `TLT`
- US aggregate bonds: `AGG`, `BND`
- US equities: `SPY`, `DIA`, `QQQ`, `IWM`
- International equities: `EFA`, `EEM`
- Real estate: `IYR`
- Gold: `GLD`
- Single-stock technology: `NVDA`
- Leveraged ETFs: `UPRO`, `TQQQ`

Metric definitions:

- `risk_number`: captured from Nitrogen where available; otherwise estimated from the Nitrogen downside anchors.
- `annualized_return_since_2008_or_inception`: daily-price CAGR from 2008-01-01 or first available history.
- `trailing_3y_annualized_return`: 3-year CAGR through latest available market close.
- `annualized_volatility`: daily-return standard deviation annualized by `sqrt(252)`.
- `six_month_95_downside`: Nitrogen-style downside estimate using `six_month_return - 1.64 * six_month_volatility`.
- `six_month_95_upside`: Nitrogen-style upside estimate using `six_month_return + 1.64 * six_month_volatility`.

## Data Handling Note

Sensitive authentication materials were not retained in this dossier. The working archive preserves research sources, public documents, extracted text, and sanitized findings.
