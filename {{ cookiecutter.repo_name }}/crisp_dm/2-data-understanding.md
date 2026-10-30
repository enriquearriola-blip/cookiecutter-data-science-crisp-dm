# 2. Data understanding

**Purpose:** collect the initial data, get familiar with it, find data quality problems and discover first insights.

[← 1. Business understanding](1-business-understanding.md) · [CRISP-DM overview](README.md) ·
[Next: 3. Data preparation →](3-data-preparation.md)

## 2.1 Collect initial data

### Initial data collection report

| Source | Description | Owner | Location or query | Period | Granularity | Records | Access method |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

_Problems found while collecting the data and how they were solved. Keep the extraction queries and scripts in the
repository and the raw extracts, unchanged, in `data/raw/`._

## 2.2 Describe data

### Data description report

_Format and volume of each source, identifiers and keys, and the meaning of each field (link the data dictionary in
`references/`). Does the data cover what the data mining goals of phase 1 need?_

## 2.3 Explore data

### Data exploration report

_First findings: distributions, relationships between key attributes and the target, sub-populations, changes over
time. Link the exploration notebooks (`notebooks/0.xx-*`)._

| Finding | Evidence (notebook, figure) | Implication for the next phases |
|---|---|---|
| | | |

## 2.4 Verify data quality

### Data quality report

_Missing values, errors, duplicates, inconsistent codes, values out of range, gaps in coverage over time._

| Issue | Fields | Affected records | Proposed treatment |
|---|---|---|---|
| | | | |

## Exit checklist

- [ ] All data sources identified, accessible and documented
- [ ] Raw extracts saved in `data/raw/` and reproducible from code in the repository
- [ ] Data dictionary in `references/`
- [ ] Data quality issues listed, each with a proposed treatment
- [ ] The data can answer the data mining goals of phase 1 (if not, go back to phase 1)
