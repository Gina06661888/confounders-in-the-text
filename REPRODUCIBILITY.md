# Reproducibility guide

## What runs now

`python scripts/plot_figure1.py`, `plot_figure2.py`, and `plot_figure3.py` reproduce the proposal workflow and aggregate diagnostic/simulation figures. The aggregate simulation CSV retains all evaluated methods and scenarios. `results/table1_full_sample.csv` transcribes the verified full-sample estimates. These files do not independently reproduce model estimation.

## Full workflow to integrate

| Stage | Inputs | Output | Availability here |
|---|---|---|---|
| Item 1 extraction and measurement | Filing inventory and HTML | Paragraph/sentence tables and audit logs | Pending integration |
| Embeddings | Accepted paragraph corpus | Paragraph/report vectors and indexes | Pending integration |
| SEC linking | CIK and accession | Filing/report dates and match statuses | Pending integration |
| Financial preparation | Authorized Compustat extract | ROA, controls, period audit | Pending integration |
| Analysis alignment | Text, dates, financial periods, vector index | Company-report table and aligned matrix | Pending integration |
| Benchmarks | Same analysis reports for each encoder | Eight specifications, out-of-fold predictions, diagnostics | Three adapted notebooks included; requires local inputs |
| Simulation | Real representations/characteristics and generated treatment/outcome | Known-effect recovery metrics | Adapted notebook included; requires local inputs |
| Industry effects | Llama representation and financial/text sample | Held-out effect predictions and industry summaries | Future direction; separate development branch |

The four adapted research notebooks have cleared outputs and use a local configuration instead of personal paths. Label/checkpoint renaming creates new run identities. Syntax and CPU estimator tests have passed; the adapted full neural pipelines have not been trained again in the packaging environment. See `docs/RUNNING_MODELS.md` and `docs/TECHNICAL_APPENDIX.md`.

## Population and units

The unrestricted matched sample has 56,345 reports and 8,094 companies. Table 1 uses current ROA, log assets, leverage, cash holdings, fiscal-year indicators, and two-digit SIC indicators. Nuisance prediction models are ridge regression and random forest. Comparisons use observed controls only, raw text, a learned representation without adversarial training, and an adversarial adjustment representation.

Treatment is measured in percentage points (100 times sentence share). Outcome ROA is in decimal units during estimation. Reported effects multiply the slope by 100, yielding ROA percentage points per one-percentage-point increase in competition language. Intervals use approximate company-clustered standard errors.

Figure 2 reports held-out treatment prediction R-squared, from the raw representation or the adjustment representation alone. These probes are distinct from treatment nuisance prediction using representation plus observed controls.

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
