# Confounders in the Text
## Generative AI–Assisted Causal Inference for Organizational Research

Anonymous research artifact under preparation for peer review.

This project studies text-based adjustment for the relationship between competition language in business descriptions (Item 1) of 10-K filings and next-fiscal-year return on assets (ROA).

## Current release status

This initial repository contains documentation, transcription of verified aggregate full-sample results, and a runnable Figure 2 plotting script. The end-to-end extraction, financial matching, representation learning, simulation, and industry analysis programs have **not yet been integrated into this repository**. It is not yet a complete replication package.

The unrestricted analysis sample contains 56,345 reports from 8,094 companies. The extraction corpus contains 106,877 accepted reports. These are different populations.

## Quick start: reproduce Figure 2

Python 3.10 or newer is recommended for this plotting-only example. From the repository root:

```bash
python -m venv .venv
# Windows PowerShell:
.venv\\Scripts\\Activate.ps1
# macOS/Linux alternative:
# source .venv/bin/activate
python -m pip install -r requirements-figures.txt
python scripts/plot_figure2.py
```

The script reads the checked-in aggregate diagnostics and writes PNG, PDF, and SVG files to `outputs/figures/`. It does not train models or require financial data, an API key, or a GPU.

## Repository contents

- [Full-sample Table 1](results/table1_full_sample.csv): effect estimates and approximate confidence limits.
- [Figure 2 input](results/figure2_treatment_diagnostics.csv): out-of-fold treatment prediction diagnostics.
- [Reproduction plan](REPRODUCIBILITY.md): workflow, inputs, and current availability.
- [Data access](DATA_AVAILABILITY.md): public-source and licensed-data dependencies.
- [Configuration template](configs/paths.example.json): portable input/output paths.

## Analysis overview

1. Extract and validate Item 1 paragraphs and sentences.
2. Measure competition language using a sentence-level adaptation of the competition word list and exclusion rule.
3. Encode paragraphs with MiniLM, a Llama-based embedding model, or OpenAI embeddings; aggregate paragraph vectors to report vectors.
4. Match SEC metadata using CIK and accession number.
5. Match financial periods, construct ROA and controls, and align representations by report identifier.
6. Fit company-grouped cross-fitted benchmarks and examine representation and influence diagnostics.
7. Evaluate known-effect recovery in semi-synthetic simulations and explore industry variation.

## Interpretation

Competition language is the share of retained Item 1 sentences satisfying the dictionary rules. It is not automatically a measure of an exogenous change in competitive conditions. Table 1 reports continuous-treatment slopes, not binary-treatment average effects. All displayed approximate 95% intervals include zero. Reduced treatment predictability alone does not establish valid confounder adjustment.

## Anonymous review and licensing

Files in this package omit author names and institutional identifiers. The hosting account and Git commit metadata are separate from artifact anonymity. No code license or citation authorship is asserted in this initial version; a license and named citation will be added when approved by the authors.
