# Technical methods and replication notes

## Measurements and alignment

The treatment is 100 times the share of retained Item 1 sentences satisfying the competition dictionary and exclusion rule. It measures competition language. Report representations are equal-weight means of retained paragraph vectors followed by L2 normalization. Embedding computation deduplicates identical texts but report aggregation counts each retained paragraph ID.

The outcome is next-fiscal-year net income divided by mean beginning/end total assets. Financial controls are current ROA, log assets, debt/assets, and cash/assets, plus year and two-digit SIC indicators. Exact financial-period matching, authorized input construction, and historical identity review are separate upstream steps. Next-fiscal-year outcomes are not automatically wholly after the filing date.

## Benchmarks

Five outer folds keep companies together. Training-only scalers and inner company validation are used for the learned representation. The encoder has hidden layers 256 and 128 and outputs 64 coordinates. The outcome head has hidden layers 128 and 64; the treatment adversary has layers 64 and 32. The matched no-adversary comparator disables the adversarial objective. Settings include dropout 0.1, learning rate 0.001, weight decay 0.00001, up to 40 epochs, and patience 6 after at least 10 epochs.

The treatment adversary uses gradient reversal strength 0.05 and objective weight 0.005. These are distinct factors; treatment unpredictability is an objective, not a guarantee of confounder retention or identification.

Each representation is combined with observed controls for Ridge (alpha 10) and RF (300 trees, maximum depth 12, minimum leaf 20, maximum features 0.5). Fold-specific representation coordinates are never pooled as a common coordinate system across independently fitted encoders. Out-of-fold treatment and outcome residuals enter a no-intercept residual slope. Approximate inference clusters influence scores by company. Company deletion diagnostics keep predictions fixed and do not refit the pipeline.

## Semi-synthetic design

Real Llama representations and observed characteristics supply the design. A separate 1,500-company calibration group defines PCA-based factors: shared confounder C, outcome-only M, treatment-only L, and an observed-control score W. Each replication samples 1,000 evaluation companies and one report per company. Treatment and outcome are generated as:

T = gamma_C C + gamma_L L + 0.3 W + error_T

Y = 1.0 T + C + 0.5 M + 0.3 W + error_Y

Independent errors have standard deviation 1. Confounding strengths are 0.15, 0.60, and 1.20 with gamma_L = 1, plus a boundary setting gamma_C = 1.20 and gamma_L = 0. Each setting has 50 replications with paired samples/noise across settings. Simulation representations use the same architecture with a smaller common budget: two folds, 20 epochs, and 60 RF trees. The true effect is in synthetic units, not empirical ROA units. Oracle controls are included as references. This is not the fully synthetic quick-start demo.

## Reproduction boundary

The review adaptation changes labels, path configuration, and checkpoint namespaces. It does not promise bitwise equality across GPU builds. Full neural training has not been rerun in the packaging environment; complete input-to-paper verification remains pending. Upstream extraction, embedding, and financial alignment integration is not complete.
