# HRIE Implementation Plan v1.0

**Companion to:** `HRIE_Technical_Specification_v1_0.md`
**Audience:** Claude Code (autonomous coding agent) and JP (review)
**Format:** Sequential sprints with atomic tasks, acceptance criteria, and ready-to-paste prompts.

---

## How to Use This Document

This plan decomposes the HRIE specification into **8 sprints × 3-5 atomic tasks each**. Each task is sized so a single Claude Code session can complete it end-to-end (code + tests + commit).

For each task you will find:
- **Goal** — what the task produces
- **Inputs** — files / context the agent needs
- **Acceptance criteria** — what must be true at the end
- **Suggested prompt** — paste this verbatim into Claude Code

**Execution rule:** complete every task in a sprint and pass its acceptance criteria before advancing. Do not interleave sprints. The dependency graph assumes strict sequencing.

---

## Sprint 0 — Repository Bootstrap

### Task 0.1 — Initialize the repository

**Goal:** Create the `harpian/hrie` package with the directory structure from §4 of the spec.

**Acceptance criteria:**
- `pyproject.toml` configured with Python 3.11+, dependencies from §3.3 of the spec.
- `harpian/hrie/` and all submodules from §4 created with empty `__init__.py`.
- `tests/{unit,integration,golden_vectors,property}/` created.
- `make install`, `make test`, `make lint` targets working.
- Pre-commit hooks: `ruff`, `black`, `mypy --strict`.
- CI pipeline (GitHub Actions) running `make test` on push.

**Suggested prompt:**
> Read `HRIE_Technical_Specification_v1_0.md` sections 3 and 4. Initialize a Python 3.11+ project at the repository root with the exact directory structure from §4. Use Pydantic v2, NumPy, SciPy, pandas, pyarrow, FastAPI. Set up pyproject.toml with strict mypy, ruff, and black. Add a Makefile with `install`, `test`, `lint`, `typecheck` targets. Add a GitHub Actions workflow that runs all of these on push. Do NOT add any business logic yet — just the skeleton.

### Task 0.2 — Configure persistence layer

**Goal:** PostgreSQL schema for asset master, proxy registry, audit log; Redis cache wiring.

**Acceptance criteria:**
- `harpian/hrie/persistence/asset_master.py` with SQLAlchemy 2.0 models for `assets`, `proxy_registry`, `audit_log`.
- Alembic configured with initial migration creating these tables.
- `harpian/hrie/persistence/cache.py` with Redis async client and TTL configuration.
- `docker-compose.yml` for local Postgres + Redis.
- Connection pool configurable via env vars (`HRIE_DB_URL`, `HRIE_REDIS_URL`).

**Suggested prompt:**
> Read §13 (audit log), §3.3 (deployment), and §17 (integration). Build the persistence layer: SQLAlchemy 2.0 models, Alembic initial migration, Redis cache wrapper. Asset master has columns for canonical identifiers from §5.1. Proxy registry stores the table from §7.3. Audit log is append-only with chain hashing (§13.2). Add docker-compose for local dev. No engine logic yet — only persistence.

---

## Sprint 1 — Domain Model & Contracts

### Task 1.1 — Implement domain types

**Goal:** All Pydantic v2 models and frozen dataclasses from §5.

**Acceptance criteria:**
- `harpian/hrie/contracts/inputs.py`: `AssetIdentifier`, `IngestionRequest`, `PortfolioInput`, `PortfolioPosition`.
- `harpian/hrie/contracts/outputs.py`: `AssetRiskOutput`, `PortfolioRiskOutput`, `RiskContribution`, `CorrelationCluster`, `Alert`.
- `harpian/hrie/contracts/errors.py`: all exception classes from §16.4.
- `harpian/hrie/classification/taxonomy.py`: `AssetClass` enum.
- All models validate via `model_validate` round-trip tests.

**Suggested prompt:**
> Read §5 and §16.4 of the spec. Implement every domain type as Pydantic v2 models in `harpian/hrie/contracts/`. Use `Decimal` for monetary fields, `date` for dates, `Enum` subclasses for closed sets. Add a `tests/unit/test_contracts.py` that round-trips every model through `model_dump_json` → `model_validate_json` and asserts equality. No business logic yet.

### Task 1.2 — Configuration module

**Goal:** Single source of truth for all engine constants.

**Acceptance criteria:**
- `harpian/hrie/config.py` with versioned constants: `RN_ANCHORS`, `DEFAULT_RAF`, `RAF_WEIGHTS`, `LAMBDA_PENALTY`, `STRESS_SCENARIOS`.
- Constants are immutable (`Final[...]` annotations).
- A `__VERSION__` string tags each constant group; bumping it requires test updates.

**Suggested prompt:**
> Read §7.2, §9.3, §10.2, §10.5, §14.1. Create `harpian/hrie/config.py` containing all calibration constants. Use `typing.Final` for immutability and version each group with a string constant (e.g., `RAF_WEIGHTS_VERSION = "1.0.0"`). The version strings will be embedded in every output payload. Add tests asserting that the constants match the values in the spec.

---

## Sprint 2 — Statistics Layer (L3)

### Task 2.1 — Returns and volatility

**Goal:** §8.1 and §8.2 implemented.

**Acceptance criteria:**
- `harpian/hrie/statistics/returns.py`: `simple_return`, `log_return`, `cagr`, `compute_returns_series`.
- `harpian/hrie/statistics/volatility.py`: `annualized_volatility` with the frequency map from §8.2.
- Property tests via `hypothesis`: monotonicity, non-negativity, frequency invariance under aggregation.
- Golden vector: a synthetic geometric brownian motion series produces the analytically expected vol within 1%.

**Suggested prompt:**
> Read §8.1 and §8.2. Implement returns and volatility computation. Use NumPy throughout. Add unit tests with hand-computed expected values for small series. Add hypothesis-based property tests for monotonicity and scale invariance. Add a golden test using a 10-year GBM series with known sigma=0.20 and assert the computed vol is within 1% of 0.20.

### Task 2.2 — Downside deviation and drawdown

**Goal:** §8.3 and §8.4 implemented.

**Acceptance criteria:**
- `harpian/hrie/statistics/downside.py`: `downside_deviation` accepting MAR.
- `harpian/hrie/statistics/drawdown.py`: `drawdown_series`, `max_drawdown`, `recovery_time_days`, `average_drawdown`, `rolling_drawdown_max`.
- Tests cover: monotonic series (no drawdown), single-trough series (known recovery), unrecovered series (returns -1).
- All functions accept `np.ndarray` and return scalars or arrays — no pandas in the hot path.

**Suggested prompt:**
> Read §8.3 and §8.4. Implement downside deviation and the full drawdown surface. Hot path must be NumPy-only (no pandas). Test cases: monotonic series, V-shaped series with hand-computed drawdown, series that never recovers (recovery_time_days returns -1). Add hypothesis tests asserting `max_drawdown <= 0` and `recovery_time >= 0 or == -1`.

### Task 2.3 — Ratios, VaR, CVaR

**Goal:** §8.5 and §8.6 implemented.

**Acceptance criteria:**
- `harpian/hrie/statistics/ratios.py`: `sharpe`, `sortino`, `calmar`, `var_95_6m`, `cvar_95_6m`.
- Historical method primary; Cornish-Fisher fallback for series with < 5y history flagged in output.
- Method actually used is recorded in a returned `ComputationMethod` field.
- Edge cases: zero volatility → 0.0, not Inf or NaN.

**Suggested prompt:**
> Read §8.5 and §8.6. Implement ratios and tail-risk measures. Historical VaR/CVaR is primary; add a Cornish-Fisher parametric fallback for short series (< 5y). The function signature returns the chosen method as a tagged enum. All zero-vol edge cases return 0.0 instead of Inf/NaN. Add tests with known distributions (normal — Cornish-Fisher should match historical within tolerance).

---

## Sprint 3 — Risk Number & RAF (L4)

### Task 3.1 — Risk Number computer

**Goal:** §9 implemented.

**Acceptance criteria:**
- `harpian/hrie/risk_number/anchors.py`: `RN_ANCHORS` with version stamp.
- `harpian/hrie/risk_number/computer.py`: `map_downside_to_rn`, `compute_rn_base_from_metrics`.
- Tests: every anchor maps to its exact RN, midpoints interpolate correctly, downside ≤ 0 returns 1, downside ≥ 27.42% returns 99.
- Property test: monotonicity in downside.

**Suggested prompt:**
> Read §9. Implement the Risk Number computer with the anchor table from §9.3 and linear interpolation from §9.4. Tests must verify every anchor point maps exactly, midpoints interpolate linearly, and edge cases (≤0, ≥0.2742) clamp correctly. Add a hypothesis test asserting `map_downside_to_rn` is monotonically non-decreasing.

### Task 3.2 — RAF components

**Goal:** §10.3 implemented as five independent component functions.

**Acceptance criteria:**
- `harpian/hrie/raf/components.py` with one function per component: `volatility_acceleration`, `correlation_expansion`, `liquidity_stress_listed`, `liquidity_stress_fund`, `macro_sensitivity`, `drawdown_convexity`.
- Each function returns a float in `[0, 1]`.
- Each has a docstring citing the relevant spec section.
- Unit tests with hand-computed expected values for each component.

**Suggested prompt:**
> Read §10.3 carefully. Implement each RAF component as a separate function. Each must clamp output to [0, 1]. The two liquidity stress functions are mutually exclusive — listed assets use the order-book version, fund vehicles use the redemption-period version. Use the asset class taxonomy to dispatch. Tests: for each component, build a small synthetic input where the expected output is hand-computable (e.g., for vol_accel, use a series where vol_21d / vol_252d = 2.0 exactly).

### Task 3.3 — RAF aggregator and RN adjustment

**Goal:** §10.4 and §10.5 implemented.

**Acceptance criteria:**
- `harpian/hrie/raf/aggregator.py`: `compute_raf` with weights from `config.py`.
- `harpian/hrie/raf/adjuster.py`: `adjust_rn_with_raf` implementing the λ formula.
- Outlier detection per §10.6 with `raf_outlier` warning emission.
- Tests: RAF=1 → no adjustment, RAF=10 → +35% adjustment (capped at 99).

**Suggested prompt:**
> Read §10.4, §10.5, §10.6. Implement the aggregator and adjuster. The λ=0.35 default lives in config. Tests: at RAF=1, RN_adjusted == RN_base; at RAF=10, RN_adjusted == round(RN_base * 1.35) capped at 99. Add a test for the outlier detection: when bottom-up RAF deviates from default by >3.0, a warning is recorded.

---

## Sprint 4 — Correlation Engine (L5)

### Task 4.1 — Rolling correlations

**Goal:** §11.1 implemented.

**Acceptance criteria:**
- `harpian/hrie/correlation/rolling.py`: `rolling_correlation` and `rolling_correlation_matrix`.
- Windows: 21d, 63d, 126d, 252d.
- Handles aligned and misaligned date indices (raises on misalignment).
- Tests with known synthetic series (perfect correlation, zero correlation, anti-correlation).

**Suggested prompt:**
> Read §11.1. Implement rolling correlation for both pairwise and full matrix cases. The matrix function must be vectorized — no Python loops over asset pairs. Misaligned date indices raise `ValueError`. Tests with synthetic series: two identical series → ρ=1.0, two independent gaussian series with N=10000 → |ρ|<0.05.

### Task 4.2 — Stress correlations

**Goal:** §11.2 implemented.

**Acceptance criteria:**
- `harpian/hrie/correlation/stress.py`: `stress_correlation`, `stress_correlation_matrix`.
- Stress days defined by benchmark return percentile.
- Insufficient stress observations (< 30) returns NaN; the caller decides how to handle.
- Tests: synthetic series where stress regime has known correlation different from normal.

**Suggested prompt:**
> Read §11.2. Implement stress correlation. The stress mask is defined as days where the benchmark series returned below its 10th percentile in the lookback window. If fewer than 30 stress days exist, return NaN — the caller in §12 will fall back to normal correlation. Test with a constructed series: in days where benchmark return < threshold, asset A and B move together (ρ=0.9); otherwise ρ=0.1. Verify stress correlation ≈ 0.9, normal ≈ 0.1.

### Task 4.3 — Dynamic blending and PSD projection

**Goal:** §11.3 and §11.4 implemented.

**Acceptance criteria:**
- `harpian/hrie/correlation/dynamic.py`: `dynamic_correlation_matrix`, `nearest_psd`.
- Implements Higham's nearest-PSD projection.
- PSD projection is idempotent (verified via property test).
- Blending γ = portfolio_systemic_RAF / 10, clamped to [0, 1].

**Suggested prompt:**
> Read §11.3 and §11.4. Implement the dynamic correlation blender and Higham's nearest-PSD projection (eigh decomposition, clip negative eigenvalues, reconstruct). Property tests: nearest_psd is idempotent, output is symmetric, output has all eigenvalues >= -1e-10. Test the blend with γ=0 (pure normal), γ=1 (pure stress), γ=0.5 (linear midpoint).

---

## Sprint 5 — Ingestion & Classification (L1, L2)

### Task 5.1 — Identifier resolver

**Goal:** §6.1 and §6.4 implemented.

**Acceptance criteria:**
- `harpian/hrie/ingestion/resolver.py`: `IdentifierResolver` class.
- Implements the source hierarchy from §6.1.
- Records every fallback in `proxy_chain`.
- Brazilian-specific resolution from §6.4 implemented per asset class.
- Adapter pattern: each provider implements `Provider.has_asset()` and `Provider.fetch()`.

**Suggested prompt:**
> Read §6.1, §6.2, §6.4. Implement the identifier resolver as an orchestrator over a list of `Provider` adapters. The provider interface is `has_asset(identifier) -> bool` and `fetch(identifier) -> MarketDataBundle`. Implement stub providers for AlphaDroid, B3, ANBIMA, Yahoo, Manual — they can return mock data for now (real integrations come later). Every fallback is recorded in `proxy_chain`. Test the full hierarchy with mocked providers.

### Task 5.2 — Calendar and currency normalization

**Goal:** §6.3 implemented.

**Acceptance criteria:**
- `harpian/hrie/ingestion/normalizer.py`: `normalize_calendar`, `synthesize_brl_series`.
- Forward-fill is **prohibited** — gaps > 5d trigger `confidence_score` degradation.
- BRL synthesis multiplies USD price by USD/BRL FX, with explicit FX rolldown.
- Tests with deliberate gaps and currency conversion edge cases.

**Suggested prompt:**
> Read §6.3. Implement calendar normalization (B3 trading calendar for BRL assets, NYSE for USD) and BRL synthesis for dual-currency assets. Forward-fill is prohibited; gaps > 5 trading days reduce confidence. Test with a series that has a 7-day gap and verify the normalizer flags it but does not interpolate.

### Task 5.3 — Classifier and proxy registry

**Goal:** §7 implemented.

**Acceptance criteria:**
- `harpian/hrie/classification/classifier.py`: rule-based router from §7.1.
- `harpian/hrie/classification/proxy_registry.py`: lookup against the persistence-backed registry.
- `harpian/hrie/classification/raf_defaults.py`: imports from `config.py`.
- 95%+ accuracy on a curated test set of 50 Brazilian assets.

**Suggested prompt:**
> Read §7. Implement the deterministic classifier with the priority order from §7.1 (no ML in v1.0). Build a curated test fixture of 50 Brazilian assets with their expected `AssetClass` and assert 95%+ classification accuracy. The proxy registry is a Postgres lookup — use the asset master table created in Sprint 0.

---

## Sprint 6 — Portfolio Aggregation & Confidence (L6)

### Task 6.1 — Portfolio aggregator

**Goal:** §12 implemented end to end.

**Acceptance criteria:**
- `harpian/hrie/portfolio/covariance.py`: dynamic covariance from §12.2.
- `harpian/hrie/portfolio/aggregator.py`: `compute_portfolio_risk` orchestrator implementing §12.3 through §12.6.
- `harpian/hrie/portfolio/contributors.py`: marginal contributions from §12.7 and clusters from §12.8.
- Total contribution percentages sum to 1.0 ± 1e-6.
- Cluster detection uses scipy hierarchical clustering.

**Suggested prompt:**
> Read §12 in full. Implement the portfolio aggregator. The orchestrator takes per-asset outputs (already computed) and the two correlation matrices, then computes dynamic covariance, portfolio downside, RN_portfolio_base, RAF_portfolio with overlay, RN_portfolio_adjusted, marginal contributions, and clusters. Tests: a 3-asset portfolio with known weights, vols, and correlations should produce a hand-computable σ_p — verify within 1e-6.

### Task 6.2 — Confidence scoring

**Goal:** §13 implemented.

**Acceptance criteria:**
- `harpian/hrie/scoring/confidence.py` with the formula from §13.1.
- Provenance record persistence per §13.2 (audit log table).
- `VERY_LOW` confidence emits an alert and flags the output as non-primary.

**Suggested prompt:**
> Read §13. Implement the confidence scoring and provenance logger. Provenance is written to the audit_log table with a chain hash linking to the previous entry for the same asset_id. Test the formula: a 5y daily series from AlphaDroid scores HIGH; a 1y monthly proxy chain of depth 3 scores LOW.

### Task 6.3 — Stress scenarios and alerts

**Goal:** §14 implemented.

**Acceptance criteria:**
- `harpian/hrie/alerts/rules.py`: alert rule engine.
- Stress scenarios from §14.1 implemented as linear shock propagation.
- All five alert codes from §14.2 evaluable.
- Tests for each alert trigger condition.

**Suggested prompt:**
> Read §14. Implement stress scenarios as linear shock propagation (non-linear repricing is v1.1). Implement all alert rules from §14.2. Test that each alert code can be triggered by a constructed input. The `portfolio_exceeds_behavioral_tolerance` alert requires a `ClientContext` parameter — make it optional.

---

## Sprint 7 — Public API & Adapters

### Task 7.1 — REST API

**Goal:** §16 implemented.

**Acceptance criteria:**
- `harpian/hrie/api/routes.py`: all endpoints from §16.1 wired to the orchestrators.
- `harpian/hrie/api/schemas.py`: request and response Pydantic models.
- Idempotency-Key header handling per §16.3.
- RFC 7807 error responses per §16.4.
- OpenAPI spec auto-generated and lives at `/hrie/v1/docs`.

**Suggested prompt:**
> Read §16. Implement the FastAPI routes. Use the contracts from `harpian.hrie.contracts` directly (Pydantic v2 is compatible with FastAPI). Idempotency-Key cached in Redis with 24h TTL. Error responses follow RFC 7807. Add integration tests using `httpx.AsyncClient` that hit each endpoint with both happy-path and error inputs.

### Task 7.2 — Python SDK

**Goal:** §16.2 implemented.

**Acceptance criteria:**
- `harpian/hrie/sdk.py`: `HRIEClient` class with both sync and async methods.
- Auto-retry with exponential backoff on transient failures.
- Built-in idempotency key generation (UUID4 unless caller provides one).
- Tests against a local FastAPI test server.

**Suggested prompt:**
> Read §16.2. Build a thin async-first client wrapper over httpx. Sync methods are generated via `asgiref.sync_to_async` inversion. Auto-retry on 5xx with exponential backoff (max 3 retries). Tests use a fixture that spins up the FastAPI app and points the client at it.

### Task 7.3 — HRD Engine adapter

**Goal:** §17.2 implemented — the bridge that lets the HRD Engine consume HRIE.

**Acceptance criteria:**
- `harpian/hrie/adapters/hrd_adapter.py`: `HRIEAdapter` class.
- Translation layer: HRD's `Position` → HRIE's `AssetIdentifier`.
- `get_portfolio_risk_number` returns `RN_portfolio_adjusted` as integer.
- `get_full_risk_breakdown` returns the complete `PortfolioRiskOutput`.
- Integration test: feed a real HRD `Portfolio` and assert HRIE produces a sane `RN_portfolio`.

**Suggested prompt:**
> Read §17.2. Build the HRD adapter. The translation layer maps each HRD `Position` to an HRIE `AssetIdentifier` using whatever fields are available (ticker, name, asset_class hint). When ambiguous, raise `IdentifierUnresolvedError` with the position name in the message. Integration test: construct an HRD Portfolio with three positions (one BR equity, one FII, one international ETF) and verify HRIE returns valid metrics.

---

## Sprint 8 — Hardening, Golden Vectors, Documentation

### Task 8.1 — Golden vector suite

**Goal:** §18.2 implemented with the six required vectors.

**Acceptance criteria:**
- `tests/golden_vectors/` contains: `IVVB11_5y.json`, `PATL11_3y.json`, `tesouro_selic.json`, `multimercado_macro_xpm_30.json`, `previdência_brz_target_2040.json`, `family_office_balanced_50_30_20.json`.
- Each vector includes input data and expected outputs.
- Test harness reruns the engine on each vector and asserts byte-identical output.
- Drift CI step blocks PRs that change golden outputs without an explicit migration commit signed by COO + CIO.

**Suggested prompt:**
> Read §18.2. Build the golden vector suite. For each of the six vectors, capture real or representative input data and run the current engine to capture expected outputs. The test harness uses `pytest-golden` or similar. Add a CI step that diffs golden outputs and fails the PR unless the commit message contains `GOLDEN_MIGRATION:` followed by an issue ID.

### Task 8.2 — Property-based test suite

**Goal:** §18.3 implemented.

**Acceptance criteria:**
- `tests/property/` contains hypothesis-based tests for: RN monotonicity, RAF bounds, portfolio RN bounded by max asset RN under low correlation, PSD projection idempotence, permutation invariance.
- All property tests run in CI with at least 1000 examples each.

**Suggested prompt:**
> Read §18.3. Implement all five property tests using hypothesis. Each test runs at least 1000 examples in CI. The "permutation invariance" test reorders portfolio positions and asserts the output is bit-identical (excluding ordered fields like `dominant_risk_contributors` which should also be reordered consistently).

### Task 8.3 — Performance benchmarks

**Goal:** §18.5 and §19 verified.

**Acceptance criteria:**
- `tests/performance/` contains benchmarks for: single asset cold/warm, 100-asset portfolio, 500-asset portfolio.
- pytest-benchmark integration; CI runs benchmarks and posts results to a tracked metric.
- All P95 targets from §19 met on a reference machine (4 vCPU, 8GB RAM).

**Suggested prompt:**
> Read §18.5 and §19. Build performance benchmarks using pytest-benchmark. Targets: single asset < 200ms cold / < 50ms cached; 100-asset portfolio < 500ms; 500-asset portfolio < 2s. Run on a reference fixture machine in CI. If a target is missed, the build fails with an actionable message.

### Task 8.4 — Operator documentation

**Goal:** Generate human-readable docs from the codebase.

**Acceptance criteria:**
- `docs/` directory with: architecture overview, API reference (auto-generated from OpenAPI), runbook (deploy, recompute on anchor bump, audit log inspection), troubleshooting guide.
- All docstrings cite the relevant spec section.
- `make docs` builds with mkdocs-material.

**Suggested prompt:**
> Build operator documentation under `docs/` using mkdocs-material. The architecture page mirrors §3 of the spec. The API reference is auto-generated from the OpenAPI schema. The runbook covers: how to deploy a new version, how to handle an anchor or RAF weight migration (with the COO+CIO sign-off requirement), how to inspect the audit log, how to investigate a divergence alert from the AlphaDroid shadow comparison.

---

## Cross-Cutting Conventions

These rules apply to every task. Claude Code must respect them.

### Code Style
- Type hints everywhere (`mypy --strict` clean).
- Docstrings cite the spec section (e.g., `"""Implements §10.4 — RAF aggregation."""`).
- No magic numbers — all calibration in `config.py`.
- No silent fallbacks — every fallback emits a structured warning.

### Testing Discipline
- Every public function has a unit test.
- Every external boundary has an integration test with mocked dependencies.
- Property tests for invariants that must always hold.
- Golden vectors for end-to-end regression.

### Determinism
- Same input + same engine version + same calibration version = byte-identical output.
- Seed any randomness; record the seed in the audit log.

### Auditability
- Every output payload includes engine version, anchor table version, RAF weights version.
- Every fallback or warning is recorded in the audit log.
- Every calibration change is a versioned migration with a sign-off requirement.

### Performance
- NumPy-only in hot paths (returns, vol, drawdown, correlation).
- Pandas allowed only at ingestion boundaries.
- Async I/O for all provider calls.
- Pre-warm the cache on startup with the top-100 most-queried assets.

---

## Sprint Schedule

| Sprint | Duration | Cumulative |
| --- | --- | --- |
| 0 — Bootstrap | 1 week | 1 |
| 1 — Domain & Config | 0.5 week | 1.5 |
| 2 — Statistics | 1 week | 2.5 |
| 3 — RN & RAF | 1 week | 3.5 |
| 4 — Correlation | 1 week | 4.5 |
| 5 — Ingestion & Classification | 1 week | 5.5 |
| 6 — Portfolio & Confidence | 1 week | 6.5 |
| 7 — API & Adapters | 1 week | 7.5 |
| 8 — Hardening & Docs | 0.5 week | 8 |

Total: **8 weeks** for v1.0 production-ready core.

After v1.0 ships, the v1.1 academic depth layer (HMM, LPPL, Kalman, Cornish-Fisher, structured product Greeks) becomes the next planning cycle.

---

## Definition of Done — v1.0

The HRIE v1.0 ships when **all** of these are true:

- [ ] All 24 tasks above are complete and merged.
- [ ] All six golden vectors pass.
- [ ] All five property tests pass with 1000+ examples.
- [ ] Performance targets from §19 met on the reference machine.
- [ ] HRD Engine successfully consumes HRIE for `RN_portfolio` in a smoke test against three real client portfolios.
- [ ] AlphaDroid shadow reconciliation runs daily for one week with no divergence > 5%.
- [ ] Operator runbook reviewed and signed by JP.
- [ ] CIO + COO sign-off on the calibration constants and stress scenarios.

When that checklist clears, the engine is production-grade and the Harpian Terminal can route any portfolio — Brazilian or international, in or out of AlphaDroid — through a single coherent risk computation layer.

---

*— End of Implementation Plan v1.0 —*
