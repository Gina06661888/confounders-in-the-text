# Alignment with the current Stage 1 proposal

## Scope

The submission branch follows the supplied Stage 1 proposal: competition measurement; three text encoders; Table 1; treatment-predictability diagnostics (Figure 2); and four-scenario semi-synthetic evidence (Figure 3). Figure 1 presents the four-step workflow. The current main sample excludes the bottom 5% of report-period observations by current assets; completed unrestricted and 1% restrictions provide sensitivity comparisons. Industry heterogeneity remains a development extension. Completed industry-extension code is preserved on the `development-industry-extension` branch, outside this proposal package.

## Terminology

Use **Generative AI–Assisted Causal Inference**, **causal adjustment representation**, and **Adjustment Z**. W-only, Raw H, and NoAdv retain their meanings. Internal keys may use `Adjustment`; figure legends and Table 1 use `Adjustment Z`. Renaming does not change numerical results.

## Result provenance

Table 1 now uses the supplied completed 5% results for 53,527 reports and 7,679 companies, stored in `results/table1_asset_restricted.csv`. The earlier 0% table remains unchanged in `results/table1_full_sample.csv`; `results/asset_sensitivity_adjustment.csv` preserves the three-population comparison. Figure 2 uses the corresponding 5% raw/adjusted treatment R-squared values (MiniLM 0.454216/0.191111; Llama 0.546029/0.196419; OpenAI 0.553073/0.171278). Its former unrestricted values are archived in `results/figure2_treatment_diagnostics_unrestricted.csv`. Figure 3 uses the supplied simulation summary: four scenarios, 50 replications, 1,000 evaluation companies, and true synthetic effect 1. All summary rows are retained. Its main plot displays the six methods described by the proposal; raw and oracle reference rows remain in the CSV.

This synchronization transcribes existing supplied results and redraws Figure 2; it does not rerun model training. The 5% sample was selected after diagnostics and sensitivity analyses, and is not described as prespecified. The sign change across samples remains explicit. The simulation was not recalibrated or rerun on the 5% empirical sample. The supplied proposal explicitly discusses the simulation bias/coverage results and the similarity of the adversarial and non-adversarial representations. The corresponding values and computations are retained. A reduction in prediction R-squared comparing H and Z is not, by itself, an isolated test of the adversarial component; the NoAdv comparison supplies that ablation.

## Future code changes

For each model update: identify changed scripts and settings; rerun affected analyses; regenerate the tables/figures from the same output snapshot; record data/model/code identities; compare the outputs with the proposal; then create a new submission version. A label-only plotting edit does not require model retraining. Changes to estimation, filtering, seeds, or model settings do require rerunning affected results. Historical results are not overwritten or represented as newly estimated results.

The full upstream replication pipeline remains under integration. Public financial-data redistribution is not assumed.
