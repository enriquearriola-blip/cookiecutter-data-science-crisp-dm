# 3. Data preparation

**Purpose:** build the final dataset for modeling from the raw data.

[← 2. Data understanding](2-data-understanding.md) · [CRISP-DM overview](README.md) · [Next: 4. Modeling →](4-modeling.md)

## 3.1 Select data

### Rationale for inclusion and exclusion

_Which records (population, period, filters) and which attributes enter the analysis, and why. Note attributes left out
because they are not available at prediction time (leakage), for legal or ethical reasons, or because of quality._

| Records or attribute | Included | Reason |
|---|---|---|
| | | |

## 3.2 Clean data

### Data cleaning report

| Issue (from 2.4) | Decision | Implementation (file or function) | Affected records |
|---|---|---|---|
| | | | |

## 3.3 Construct data

### Derived attributes

| Attribute | Definition | Source fields | Available at prediction time |
|---|---|---|---|
| | | | |

### Generated records

_Records created for the analysis (for example, periods with no activity), if any._

## 3.4 Integrate data

### Merged data

_How the tables are joined (keys, cardinality, alignment in time) and the checks that no records are duplicated or
lost._

## 3.5 Format data

### Reformatted data

_Changes the modeling tools need that do not change the meaning of the data (types, encodings, ordering)._

## Outputs

### Dataset

_Location of the final dataset in `data/processed/` and the code that builds it (`{{ cookiecutter.module_name }}/dataset.py`,
`{{ cookiecutter.module_name }}/features.py`)._

### Dataset description

_Target definition, number of records and attributes, and the samples (training, validation, test, out-of-time) with
their periods._

| Sample | Period | Records | Events | Event rate |
|---|---|---|---|---|
| | | | | |

## Exit checklist

- [ ] The dataset is rebuilt end to end from `data/raw/` with code in the repository, with no manual steps
- [ ] Every excluded record group and attribute has a reason
- [ ] No attribute uses information that is not available at prediction time
- [ ] Samples defined before modeling, with the test and out-of-time data set aside
