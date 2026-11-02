# Data availability and access

## Included in this initial package

Aggregate results for the 5%-restricted main Table 1, unrestricted estimates, Adjustment Z asset-sensitivity comparisons, Figure 2 diagnostics, and Figure 3 simulation summaries are included. No firm-level Compustat records or financial analysis tables are distributed here.

## SEC filings and metadata

The study uses Item 1 of 10-K filings organized by filing year 2010–2026. A filing-year folder is not the same as the financial year. SEC metadata linking uses CIK and accession number. A later package will document source URLs, the input inventory, extraction rules, and download snapshots. Public accessibility does not by itself establish redistribution rights for every original document or third-party source archive.

## Compustat

Financial statements are obtained from Compustat North America through WRDS. Access requires the relevant institutional/vendor entitlement. Raw extracts and merged firm-level financial data are excluded pending confirmation of the applicable license. ROA and other derived financial fields are not assumed to be freely redistributable.

The full replication package will include the query specification, variable list, filters, access dates, and construction programs so entitled users can reconstruct the financial inputs. Researchers without access can run `scripts/run_synthetic_demo.py`, which generates fully artificial observations locally. This CPU demonstration is distinct from the paper's semi-synthetic simulation and does not reproduce its empirical findings.

## Embedding models

- MiniLM: `sentence-transformers/all-MiniLM-L6-v2`.
- Llama-based: `nvidia/llama-nemotron-embed-1b-v2`.
- OpenAI: `text-embedding-3-small`.

Anonymous receipts now record the model revisions where available, chunking, pooling, precision and matrix/index checksums in `data/embedding_metadata/`. The report-vector archive and its current access status are documented in [embedding downloads](docs/EMBEDDING_DOWNLOADS.md). Creating new OpenAI embeddings requires an API key and may incur charges; reading the precomputed vectors does not. Model weights and paragraph vectors are not bundled. No general redistribution license for third-party source data or model weights is asserted.

## Simulations

The current research simulations are semi-synthetic: they retain real embeddings and observed characteristics while generating treatment and outcome. They are not automatically unrestricted synthetic data. A fully synthetic quick-start dataset must be generated independently of licensed firm-level inputs.

## Credentials and local files

Do not commit passwords, API keys, WRDS credentials, local raw data, or cache databases. Local paths belong in `configs/paths.local.json`, which is ignored by Git.
