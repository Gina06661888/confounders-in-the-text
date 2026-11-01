# Data availability and access

## Included in this initial package

Only aggregate reported results needed for Table 1 and Figure 2 are included. No firm-level Compustat records or financial analysis tables are distributed here.

## SEC filings and metadata

The study uses Item 1 of 10-K filings organized by filing year 2010–2026. A filing-year folder is not the same as the financial year. SEC metadata linking uses CIK and accession number. A later package will document source URLs, the input inventory, extraction rules, and download snapshots. Public accessibility does not by itself establish redistribution rights for every original document or third-party source archive.

## Compustat

Financial statements are obtained from Compustat North America through WRDS. Access requires the relevant institutional/vendor entitlement. Raw extracts and merged firm-level financial data are excluded pending confirmation of the applicable license. ROA and other derived financial fields are not assumed to be freely redistributable.

The full replication package will include the query specification, variable list, filters, access dates, and construction programs so entitled users can reconstruct the financial inputs. Researchers without access will need a separately provided, fully synthetic demonstration dataset; it is not included in this initial package.

## Embedding models

- MiniLM: `sentence-transformers/all-MiniLM-L6-v2`.
- Llama-based: `nvidia/llama-nemotron-embed-1b-v2`.
- OpenAI: `text-embedding-3-small`.

Model revisions, preprocessing, chunking, pooling, precision, and vector/index checksums must be recorded in the final package. OpenAI access requires an API key and may incur charges. Redistribution of model weights and derived embeddings will be reviewed against the applicable terms before release.

## Simulations

The current research simulations are semi-synthetic: they retain real embeddings and observed characteristics while generating treatment and outcome. They are not automatically unrestricted synthetic data. A fully synthetic quick-start dataset must be generated independently of licensed firm-level inputs.

## Credentials and local files

Do not commit passwords, API keys, WRDS credentials, local raw data, or cache databases. Local paths belong in `configs/paths.local.json`, which is ignored by Git.
