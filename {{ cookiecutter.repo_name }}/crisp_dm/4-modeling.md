# 4. Modeling

**Purpose:** select and apply modeling techniques and tune their parameters.

[← 3. Data preparation](3-data-preparation.md) · [CRISP-DM overview](README.md) · [Next: 5. Evaluation →](5-evaluation.md)

## 4.1 Select modeling technique

### Modeling technique

_Techniques chosen and why, and the baseline model._

### Modeling assumptions

_Assumptions each technique makes about the data (distribution, independence, missing values, monotonicity) and how they
were checked._

## 4.2 Generate test design

### Test design

_How candidate models are compared before evaluation: training and validation samples, the cross-validation scheme, the
metrics and the rule for choosing a model. Test and out-of-time data are not used to choose._

## 4.3 Build model

### Parameter settings

_Parameters tried and the values chosen, with the reason._

### Models

| Model | Technique | Parameters | Attributes | File in `models/` | Training code |
|---|---|---|---|---|---|
| | | | | | |

### Model description

_What each model learned: most important attributes, direction and shape of their effects, behavior in sub-populations,
and any problem found._

## 4.4 Assess model

### Model assessment

| Model | Metrics on validation | Meets the technical criteria of 1.3 | Notes |
|---|---|---|---|
| | | | |

### Revised parameter settings

_Changes made after the assessment and why. Repeat 4.3 and 4.4 until the best model is found._

## Exit checklist

- [ ] Baseline and candidate models trained with code in the repository
- [ ] Model chosen with the test design only, without looking at test or out-of-time data
- [ ] Chosen model and its parameters saved in `models/`
- [ ] Results reproducible from a clean environment
