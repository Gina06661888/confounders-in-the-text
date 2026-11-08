# Validation status

The following checks were completed using the supplied original project files.
They distinguish reconstruction from comparison with previously saved results.

| Check | Outcome | Scope |
|---|---|---|
| Public embedding ZIP | Passed | Entire ZIP MD5 matches the published archive; all three matrices and index pass SHA256, dimensions, finite-value and report-ID checks. |
| Financial preparation rerun | Passed | Notebook 02 rebuilt 212,875 records and 81 columns from the original authorized CSV ZIP. The reconstructed panel matches the supplied panel, with numerical tolerance 1e-12. |
| Analysis alignment rerun | Passed | Notebook 05 joined the saved SEC dates, rebuilt financial panel and public MiniLM export, producing 56,345 reports from 8,094 companies. All 75 shared columns match the original table at numerical tolerance 1e-12; the personal `source_path` column is absent. |
| Aligned MiniLM matrix | Passed | Byte-level SHA256 equals the original `cb048f53eebf55d51dc0f13bc3bd849a444e0cf50b827612262285ea32af40b8`. |
| Main-sample selection | Passed | The 5% current-log-assets restriction retains 53,527 reports and 7,679 companies. |
| Original saved results vs package | Passed | 24 main-table rows, 24 unrestricted rows, 18 sensitivity rows, 6 Figure 2 diagnostic rows, and 40 simulation rows. Displayed rounding and GENI/Adjustment label changes are accounted for. |
| Notebook/code checks | Passed | All notebook code cells and embedded worker programs compile; saved outputs and execution counts are cleared. Configuration protection and existing CPU/component tests pass. |
| Proposal figure scripts | Passed | Workflow and figures generated from the included aggregate CSVs. This is plotting verification, not a new empirical estimate. |

The numerical tolerance applies to reconstructed table contents. The rebuilt
analysis CSV has a different byte hash because the public index omits
`source_path`. Its new receipt records its actual hash; do not replace that hash
with the historical one. The matrix is unchanged byte-for-byte.

## Remaining checks

- The full HTML extraction, shared paragraph corpus and three encoders have not
  been rerun in this packaging environment. Their adapted programs are included.
- The SEC network download was not repeated; the supplied dates were read and
  their receipt/checksum verified during analysis alignment.
- Original archive acquisition URLs/download dates and the Compustat download
  date have not been established. The actual query and extraction coverage are
  preserved. The recorded 2026 Q4 source count is zero.
- Historical company linking and outcome-period timing limitations in the
  original analysis remain. These checks establish software/data agreement,
  not validity of causal identification.

See `PREPARING_DATA.md` for the ordered reconstruction steps and
`RUNNING_MODELS.md` for model execution instructions.
