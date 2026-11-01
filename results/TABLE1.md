# Table 1 Estimated effect of competition language on next year ROA

Main sample: exclude the bottom 5% of report-period observations by current total assets; 53,527 reports from 7,679 firms.

| Specification | MiniLM | Llama | OpenAI |
|---|---:|---:|---:|
| (1) W-only — Ridge | 0.5558 [0.2305, 0.8811] | 0.5558 [0.2305, 0.8811] | 0.5558 [0.2305, 0.8811] |
| (2) W-only — RF | 0.1909 [0.0767, 0.3051] | 0.1909 [0.0767, 0.3051] | 0.1909 [0.0767, 0.3051] |
| (3) Raw H — Ridge | 0.3140 [0.0816, 0.5465] | 0.2094 [-0.0528, 0.4717] | 0.4798 [0.1694, 0.7903] |
| (4) Raw H — RF | 0.0869 [-0.0505, 0.2242] | 0.1160 [-0.0161, 0.2480] | 0.1281 [0.0002, 0.2560] |
| (5) NoAdv — Ridge | 0.3356 [0.1030, 0.5681] | 0.3709 [0.1470, 0.5949] | 0.4104 [0.2166, 0.6042] |
| (6) NoAdv — RF | 0.2042 [0.0497, 0.3587] | 0.1701 [0.0287, 0.3114] | 0.2068 [0.0453, 0.3682] |
| (7) Adjustment Z — Ridge | 0.3802 [0.1169, 0.6436] | 0.4147 [0.2149, 0.6145] | 0.4219 [0.1868, 0.6570] |
| (8) Adjustment Z — RF | 0.2262 [0.0651, 0.3874] | 0.1686 [0.0255, 0.3118] | 0.2493 [0.0963, 0.4024] |

Entries are ROA percentage points per one-percentage-point increase in competition language. Brackets contain approximate 95% company-clustered confidence intervals. All specifications include four financial controls and fiscal-year and SIC2 indicators. Company-disjoint five-fold cross-fitting is used. Four decimal places preserve the small positive lower limit for OpenAI Raw H–RF.

The unrestricted and 1% restriction Adjustment Z estimates are negative with intervals including zero. The 5% estimates are positive with intervals excluding zero. These are different analysis populations; significance does not identify which estimate is causally more accurate.

Source: supplied completed asset-sensitivity comparisons. The aggregate transcription is not a new model run.
