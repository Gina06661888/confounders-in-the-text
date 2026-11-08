# Preparing the research inputs

## Two entry points

For the existing submitted results, use the frozen analysis sample and the three
report embedding exports, then run notebooks 06a–07. See `RUNNING_MODELS.md`.
The public Zenodo embeddings alone do not contain the financial sample.

To reconstruct inputs, notebooks 01–05 now contain the supplied upstream
programs with local configuration and cleared outputs. Their inclusion is not
evidence that the complete pipeline has been independently rerun.

## Local configuration

Copy `configs/preparation.example.json` to `configs/preparation.local.json`.
Set `source_project_root` to the downloaded project folder containing the annual
10-K ZIPs, `10K_compustat`, and `10K_competition_lean16_recovered`.
Leave other fields null to use the original frozen run layout. Set explicit
paths when your local layout differs. All relative paths resolve from the repo.
Keep outputs outside the source project. The loader rejects overlapping paths.

The source inputs are:

| Input | Default location under the source project |
|---|---|
| Annual filing archives | `10K_2010.zip` through `10K_2026.zip` |
| Frozen extraction | `10K_competition_lean16_recovered/all_years/cache_manifest.jsonl` and referenced `cache/` files |
| Authorized Compustat extract | `10K_compustat/raw/fxzpe8jifm2g4jh7.csv.zip` |
| Financial panel receipt | `10K_compustat/processed/financial_preparation/f210213cef87860ef86d/financial_snapshot.json` |
| SEC report dates | `10K_compustat/sec_metadata/runs/20261029T184230_97d76974/` |
| MiniLM export | `10K_three_model_embeddings/minilm/fa8fc124c14a1ca97e34/4bbe3e612630a585888e/latest_snapshot.json` |

These names identify the supplied frozen versions; new runs need not reproduce
the same directory names. Do not place licensed financial data in the public repo.

## Execution sequence

Start Jupyter from the repository root. Run selected notebooks top to bottom.

| Step | Notebook | Result and next configuration change |
|---|---|---|
| 1 | `01_Extract_Competition` | New `all_years/` manifest and cached paragraphs/sentences. Set `extraction_dir` to the new extraction output root. Skip this step to retain the original manifest and IDs. |
| 2 | `02_Prepare_Financials` | Financial panel, checksums, exclusions and `latest_financial_run.json`. Set `financial_run_dir` to the newly printed run directory. |
| 3 | `03_SEC_Filing_Dates` | SEC dates and match audit. Set `SEC_CONTACT_EMAIL` locally, then set `sec_run_dir` to the newly created run directory. |
| 4a | `04a_Encode_MiniLM` | Shared corpus database, paragraph vectors and report export. Set `minilm_snapshot` to the new `latest_snapshot.json`. |
| 4b | `04b_Encode_OpenAI` | OpenAI export from that same shared corpus. Optional if using precomputed report vectors. API execution is disabled by a zero cost ceiling until explicitly configured. |
| 4c | `04c_Encode_Llama` | Llama export from that same shared corpus. A suitable CUDA device is recommended. |
| 5 | `05_Build_Analysis_Sample` | Frozen analysis CSV, aligned MiniLM matrix, `dataset_snapshot.json`, and exclusion/matching audits. |
| 6 | `06a`, `06b`, `06c`, then `07` | Benchmarks, sensitivity runs, and semi-synthetic experiments. Configure `paths.local.json` to use the completed step-5 sample and chosen report exports. |

Steps 2 and 3 can use the supplied frozen outputs instead of rebuilding.
For steps 4a–4c, use the same `extraction_dir` and `embedding_output_root` across
all three encoders. The OpenAI and Llama notebooks require the shared corpus
created by MiniLM. Existing public report exports do not include that paragraph
database. For SEC/step-5 cross-checking of a new MiniLM export, point
`embedding_root` to its output root.

### Corpus identity and partial source coverage

The original extraction uses source paths, archive timestamps and members in
cache/identifier construction. Rebuilding under another path may create new
report IDs. Its manifest hash also defines the encoder corpus ID. **Do not mix
newly extracted IDs with old embeddings.** For an exact snapshot attempt,
retain the frozen manifest byte-for-byte and move caches without editing it;
the encoding notebooks resolve moved cache paths locally. A fresh corpus must
be encoded and matched consistently, and expected corpus/count settings in
steps 3, 5 and the research configuration must be updated explicitly.

The original coverage file records zero sources for 2026 Q4. Annual ZIP presence
does not prove a complete filing universe. Preserve the coverage and source
inventory; do not describe 2010–2026 as complete annual coverage.

### Financial query and eligibility

`data/queries/compustat_funda.sql` preserves the supplied WRDS query, including
the date range 2008-01-01 through 2026-10-31, active/inactive firms, INDL/FS,
STD, consolidated records and USD/CAD. Financial preparation subsequently keeps
INDL; analysis alignment keeps USD and complete required fields. These later
filters are deliberate and differ from the broader initial query.
Record the actual download date when obtaining a new extract. Database updates
can change values even with identical SQL. The frozen extract is identified by
SHA256 `e9c40b475595832871df2e9789e56733e1e346f080087f9de89fdf25a3c5d227`.

CIK-to-GVKEY historical identity remains unverified in the original snapshot.
The next fiscal-year outcome may include months before filing. The preparation
code preserves these limitations; it does not resolve causal identification.

## Environment and execution time

Use Python 3.10+ and stage-specific environments. Install the appropriate PyTorch
build separately for encoding/training. `environment/requirements-preparation.txt`
lists supporting packages; the original extraction dependency suggestions are
retained in notebook 01. Original financial/model version receipts are documented
in the validation record. No single fully pinned environment has been verified
for every original stage.

Encoding device defaults to CPU in the portable notebooks; set
`ENCODING_DEVICE=cuda` for local CUDA encoding. Inspect the notebook settings
before execution. OpenAI encoding uses `OPENAI_API_KEY`, a configurable price
estimate and an explicit spending ceiling. Verify current pricing independently
before raising the zero ceiling; the package never needs API calls when using
the existing report vectors.

Runtime depends on the raw collection, paragraph counts, model downloads and
hardware. Full extraction, encoding and neural timings have not been measured
in this packaging environment. Notebook progress and original per-fold logs are
available; cached runs are not valid estimates of fresh execution time.

## Check saved results separately from refitting

With the supplied original results available locally:

```bash
python scripts/verify_original_results.py --processed-root /path/to/10K_compustat/processed
```

This verifies Table 1, Figure 2 inputs, sensitivity comparisons and simulation
summaries against saved original outputs. It does not rerun neural estimation.
After refitting, use the same checks as a reference, retaining new run identities
and recording numerical tolerances and hardware.
