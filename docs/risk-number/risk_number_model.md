# Nitrogen / Riskalyze Risk Number - working model

## What was archived

- Public Nitrogen site mirror: `nitrogen_site_archive/`
  - 878 sitemap URLs scanned.
  - 1,793 public assets downloaded.
  - 87 PDFs extracted to text in `nitrogen_site_archive/extracted_text/`.
- Authenticated capture: `nitrogen_authenticated_capture/`
  - Login reached `https://pro.riskalyze.com/reports/`.
  - Saved sanitized HTML/screenshot and non-sensitive API/cache artifacts.
  - Session/HAR/token artifacts were removed after analysis.
  - Visible reports page is a report template builder, not a direct PDF download list.

## Methodology evidence

The most useful sources are:

- `extracted_text/926087680ba5ddfe_..._The-Math-Behind-Nitrogen.txt`
- `extracted_text/4d34a6e868a4c334_..._The-Math-Behind-Riskalyze.txt`
- `extracted_text/f3b9d0b67342ff7b_..._StatsOverviewExample.txt`
- `nitrogen_authenticated_capture/ffb6b41e94af8cab6e9b78f3fdd52bdc05a134e3.json`

Key findings:

- Nitrogen says Risk Number is proprietary, but the portfolio math uses:
  - return scenario,
  - volatility,
  - correlations/covariance matrix,
  - 6-month Value at Risk,
  - normal distribution at `1.64` sigmas for a 95% downside threshold.
- Portfolio 95% Historical/Probability Range:
  - downside = six-month expected return - `1.64 * six-month volatility`
  - upside = six-month expected return + `1.64 * six-month volatility`
- They say the range is based on standard deviation via covariance matrix and does not use Monte Carlo.
- They disclose examples mapping six-month downside to approximate Risk Number:
  - `-2%` downside: low 20s
  - `-5%` downside: low 30s
  - `-7%` downside: low 40s
  - `-12%` downside: low 60s
  - `-18%` downside: low 80s
- Authenticated benchmark data captured:
  - `SPY` Risk Number: `70`
  - `AGG` Risk Number: `29`
  - `70/30 Blend` Risk Number: `52`
  - `50/50 Blend` Risk Number: `42`
- Public report examples:
  - Risk Number `45`: 6-month range about `-8.21%` to `+14%`.
  - Risk Number `91`: 6-month range about `-27.42%` to `+33.18%`.

## Important limitation

The question "what is the Risk Number for a client who wants 100% profit in 3 years?" has no single mathematically valid answer.

Reason: a target return is not a risk measure. The same 100% target could be paired with:

- a very low probability speculative path,
- a concentrated equity/leveraged portfolio,
- an illiquid/private investment with smoothed marks,
- an options strategy,
- or an impossible marketing claim.

Nitrogen's Risk Number depends primarily on the 6-month downside risk, not on the 3-year target return by itself.

## Transparent calculation for 100% in 3 years

Target total return:

```text
100% total return in 3 years means ending wealth = 2.0x starting wealth.
Required annual compound return = 2^(1/3) - 1 = 25.99%
Required six-month compound return = 2^(1/6) - 1 = 12.25%
```

If a portfolio has expected six-month return `r6` and six-month volatility `sigma6`, Nitrogen-style downside is:

```text
downside6 = r6 - 1.64 * sigma6
```

Rearranged:

```text
sigma6 = (r6 - downside6) / 1.64
annualized_volatility ~= sigma6 * sqrt(2)
```

Using `r6 = 12.25%`, illustrative volatility by downside:

| Six-month downside | Approx Risk Number | Six-month vol | Annualized vol |
|---:|---:|---:|---:|
| -8.21% | ~45 | 12.48% | 17.65% |
| -12.00% | low 60s | 14.79% | 20.92% |
| -18.00% | low 80s | 18.45% | 26.10% |
| -27.42% | ~91 | 24.19% | 34.21% |

These rows answer a better question: "If the portfolio is expected to compound to 100% in 3 years, what volatility corresponds to a given Nitrogen downside/Risk Number?"

## Practical answer

Under a conservative public-market assumption, a 25.99% annual target is far above Nitrogen's disclosed long-term S&P 500 assumption of 7.5%. If we scale market exposure linearly, that target is about `3.47x` the S&P return assumption. Using `SPY` Risk Number `70` as a market-risk anchor, the implied portfolio would almost certainly be at or above Nitrogen's maximum Risk Number range, effectively `99`, with very high annualized volatility.

So the honest answer is:

- **Client target:** 100% in 3 years.
- **Required annual return:** about `26.0%`.
- **Risk Number:** not determinable from the target alone.
- **If implemented through leveraged/public-market beta:** likely `99` or beyond the platform's useful scale.
- **Volatility:** depends on the downside assumption; a Risk Number around `91` with that target implies roughly `34%` annualized volatility, while a leveraged S&P-style assumption can easily push annualized volatility above `50%`.
