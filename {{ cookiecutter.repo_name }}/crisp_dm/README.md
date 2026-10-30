# CRISP-DM: {{ cookiecutter.project_name }}

This folder documents the project with **CRISP-DM** (Cross-Industry Standard Process for Data Mining). There is one
document per phase. Each one lists the CRISP-DM tasks of the phase, the output each task produces and an exit checklist.

CRISP-DM is iterative: going back to an earlier phase when something new is learned is expected, not a failure. Record
each return in the [iteration log](#iteration-log).

```
 1. Business understanding ◄────────────────┐
        │  ▲                                │
        ▼  │                                │
 2. Data understanding                      │
        │                                   │
        ▼                                   │
 3. Data preparation ◄──────┐               │
        │                   │               │
        ▼                   │               │
 4. Modeling ───────────────┘               │
        │                                   │
        ▼                                   │
 5. Evaluation ─────────────────────────────┘
        │
        ▼
 6. Deployment
```

## Status

| Phase | Document | Status | Owner | Last updated |
|---|---|---|---|---|
| 1. Business understanding | [1-business-understanding.md](1-business-understanding.md) | Not started | {{ cookiecutter.author_name }} | |
| 2. Data understanding | [2-data-understanding.md](2-data-understanding.md) | Not started | {{ cookiecutter.author_name }} | |
| 3. Data preparation | [3-data-preparation.md](3-data-preparation.md) | Not started | {{ cookiecutter.author_name }} | |
| 4. Modeling | [4-modeling.md](4-modeling.md) | Not started | {{ cookiecutter.author_name }} | |
| 5. Evaluation | [5-evaluation.md](5-evaluation.md) | Not started | {{ cookiecutter.author_name }} | |
| 6. Deployment | [6-deployment.md](6-deployment.md) | Not started | {{ cookiecutter.author_name }} | |

Status values: Not started, In progress, Done, Revisited.

## Where each phase lives in this project

| Phase | Notebooks (`notebooks/`) | Code (`{{ cookiecutter.module_name }}/`) | Data and outputs |
|---|---|---|---|
| 1. Business understanding | | | `references/`: requirements, glossary, stakeholder material |
| 2. Data understanding | `0.xx-*`: data exploration | `dataset.py` | `data/raw/`, `data/external/`, `references/`: data dictionaries |
| 3. Data preparation | `1.xx-*`: cleaning and feature creation | `dataset.py`, `features.py` | `data/interim/`, `data/processed/` |
| 4. Modeling | `3.xx-*`: modeling | `modeling/train.py` | `models/` |
| 5. Evaluation | `2.xx-*`: visualizations | `modeling/predict.py`, `plots.py` | `reports/`, `reports/figures/` |
| 6. Deployment | `4.xx-*`: publication | the `{{ cookiecutter.module_name }}` package | `models/`, `reports/`, `docs/` |
{% if cookiecutter.include_code_scaffold == "No" %}
The code scaffold was not generated for this project; the file names above are where Cookiecutter Data Science
suggests putting that code.
{% endif %}
## How to use these documents

1. Start with phase 1 before touching the data, and agree on the success criteria with the people who will use the
   results.
2. Fill in each document while doing the work, not at the end. Replace the text in _italics_ with the answer; when a
   task does not apply, write "Not applicable" and why.
3. Link to the evidence (notebooks, figures, reports, code) instead of copying results into the documents.
4. A phase is done when its exit checklist is complete. Update the status table above.
5. When the work sends you back to an earlier phase, add a row to the iteration log and set that phase to Revisited.

## Iteration log

| Date | From phase | Back to phase | What was learned | Decision |
|---|---|---|---|---|
| | | | | |
