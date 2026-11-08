# Reproducibility guide

## What runs now

`python scripts/plot_figure1.py`, `plot_figure2.py`, and `plot_figure3.py` reproduce the proposal workflow and aggregate diagnostic/simulation figures. The aggregate simulation CSV retains all evaluated methods and scenarios. `results/table1_asset_restricted.csv` transcribes the supplied 5%-restricted main estimates; `results/table1_full_sample.csv` preserves the earlier unrestricted estimates. `results/asset_sensitivity_adjustment.csv` compares Adjustment Z across 0%, 1%, and 5% restrictions. These files do not independently reproduce model estimation.

## Included workflow and validation scope

| Stage | Inputs | Output | Availability here |
|---|---|---|---|
| Item 1 extraction and measurement | Filing inventory and HTML | Paragraph/sentence tables and audit logs | Portable notebook included; full stage rerun pending |
| Embeddings | Accepted paragraph corpus | Paragraph/report vectors and indexes | Portable notebook included; full stage rerun pending |
| SEC linking | CIK and accession | Filing/report dates and match statuses | Portable notebook included; full stage rerun pending |
| Financial preparation | Authorized Compustat extract | ROA, controls, period audit | Adapted notebook rerun; financial panel matches supplied output |
| Analysis alignment | Text, dates, financial periods, vector index | Company-report table and aligned matrix | Rerun from saved SEC dates, rebuilt financial panel and public embeddings; matched original |
| Benchmarks | Same analysis reports for each encoder | Eight specifications, out-of-fold predictions, diagnostics | Three adapted notebooks included; requires local inputs |
| Simulation | Real representations/characteristics and generated treatment/outcome | Known-effect recovery metrics | Adapted notebook included; requires local inputs |
| Industry effects | Llama representation and financial/text sample | Held-out effect predictions and industry summaries | Future direction; separate development branch |

All included research notebooks have cleared outputs and use local configuration instead of personal paths. Upstream configuration and execution order are in `docs/PREPARING_DATA.md`; completed checks are in `docs/VALIDATION.md`. Label/checkpoint renaming creates new run identities. Syntax and CPU estimator tests have passed; the adapted full neural pipelines have not been trained again in the packaging environment. See `docs/RUNNING_MODELS.md` and `docs/TECHNICAL_APPENDIX.md`.

## Population and units

The unrestricted matched sample has 56,345 reports and 8,094 companies. The 1% restriction retains 55,781 reports and 8,015 companies; the 5% main restriction retains 53,527 reports and 7,679 companies. Thresholds use current assets across unrestricted report-period observations, not future ROA. Table 1 uses current ROA, log assets, leverage, cash holdings, fiscal-year indicators, and two-digit SIC indicators. Nuisance prediction models are ridge regression and random forest. Comparisons use observed controls only, raw text, a learned representation without adversarial training, and an adversarial adjustment representation.

Treatment is measured in percentage points (100 times sentence share). Outcome ROA is in decimal units during estimation. Reported effects multiply the slope by 100, yielding ROA percentage points per one-percentage-point increase in competition language. Intervals use approximate company-clustered standard errors.

Figure 2 uses the 5% main sample and reports held-out treatment prediction R-squared, from the raw representation or the adjustment representation alone. These probes are distinct from treatment nuisance prediction using representation plus observed controls.

## Validation before a submission release

- Record source inventory, financial query, download dates, and all exclusions.
- Pin software and model versions; specify API dependencies and CPU/GPU requirements.
- Join by stable report/paragraph identifiers; verify matrix/index snapshots and checksums.
- Keep companies together in folds and document preprocessing fitted within training partitions.
- Preserve 0%, 1%, and 5% asset-selection settings as separate runs.
- Freeze the manuscript tables/figures and their exact generating run configurations.
- Test the completed package from a clean checkout and environment.
- Report expected execution times and numerical reproducibility tolerances after measurement.

Do not describe this initial documentation release as an independently verified end-to-end replication.
