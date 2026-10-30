# Cookiecutter Data Science + CRISP-DM

_A logical, reasonably standardized but flexible project structure for doing and sharing data science work._

[![PyPI - Version](https://img.shields.io/pypi/v/cookiecutter-data-science)](https://pypi.org/project/cookiecutter-data-science/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cookiecutter-data-science)](https://pypi.org/project/cookiecutter-data-science/)
<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>
[![tests](https://github.com/drivendataorg/cookiecutter-data-science/actions/workflows/tests.yml/badge.svg)](https://github.com/drivendataorg/cookiecutter-data-science/actions/workflows/tests.yml)

> **This is a fork of [Cookiecutter Data Science](https://github.com/drivendataorg/cookiecutter-data-science), created and maintained by [DrivenData](https://www.drivendata.org/).** All credit for the template goes to DrivenData and its contributors. The only change is a CRISP-DM methodology folder added to every generated project (see [This fork](#this-fork-crisp-dm-methodology) and [Credits and license](#credits-and-license)).

**Cookiecutter Data Science (CCDS)** is a tool for setting up a data science project template that incorporates best practices. To learn more about CCDS's philosophy, visit the [project homepage](https://cookiecutter-data-science.drivendata.org/).

> ℹ️ Cookiecutter Data Science v2 has changed from v1. It now requires installing the new cookiecutter-data-science Python package, which extends the functionality of the [cookiecutter](https://cookiecutter.readthedocs.io/en/stable/README.html) templating utility. Use the provided `ccds` command-line program instead of `cookiecutter`.

## This fork: CRISP-DM methodology

This repository is CCDS v2.3.0 with one addition: every generated project gets a `crisp_dm/` folder with one document per CRISP-DM phase (business understanding, data understanding, data preparation, modeling, evaluation and deployment). Each document lists the CRISP-DM tasks of the phase, the output of each task and an exit checklist. `crisp_dm/README.md` tracks the status of each phase, maps the phases to the CCDS folders and logs each return to an earlier phase.

**Generating a project.** The hooks import helper functions from the installed `ccds` package, so install the version that matches this template. Pass the `crisp-dm` branch: by default `ccds` checks out the tag of the installed version (`v2.3.0`), which is the original template without CRISP-DM.

```bash
pipx install cookiecutter-data-science==2.3.0
ccds https://github.com/enriquearriola-blip/cookiecutter-data-science-crisp-dm -c crisp-dm
```

**Defining your methodology.** Fork or clone this repository and edit the files in `{{ cookiecutter.repo_name }}/crisp_dm/`. Every project generated afterwards gets your version; projects already generated are not affected. The files are Jinja templates, so they can use the CCDS variables, such as `{{ cookiecutter.project_name }}` or `{{ cookiecutter.author_name }}`, and literal double braces in the text must be escaped. To generate from a local copy, pass its path, which uses the files as they are on disk:

```bash
ccds path/to/cookiecutter-data-science-crisp-dm
```

**Updating from upstream.** The addition lives on the `crisp-dm` branch, the default branch of this repository. It touches only `{{ cookiecutter.repo_name }}/crisp_dm/` (new), the directory trees in `{{ cookiecutter.repo_name }}/README.md` and in this README, the title and fork notes of this README, and the expected files in `tests/test_creation.py`.

```bash
git remote add upstream https://github.com/drivendataorg/cookiecutter-data-science.git  # once
git fetch upstream --tags
git merge v2.4.0                                       # the new release
pipx install --force cookiecutter-data-science==2.4.0  # keep the package in step with the template
```

## Installation

Cookiecutter Data Science v2 requires Python 3.9+. Since this is a cross-project utility application, we recommend installing it with [pipx](https://pypa.github.io/pipx/). Installation command options:

```bash
# With pipx from PyPI (recommended)
pipx install cookiecutter-data-science

# With pip from PyPI
pip install cookiecutter-data-science

# With conda from conda-forge (coming soon)
# conda install cookiecutter-data-science -c conda-forge
```

## Starting a new project

To start a new project, run:

```bash
ccds
```

### The resulting directory structure

The directory structure of your new project will look something like this (depending on the settings that you choose):

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── crisp_dm           <- CRISP-DM methodology: one document per phase; start at crisp_dm/README.md
│
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         {{ cookiecutter.module_name }} and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── {{ cookiecutter.module_name }}   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes {{ cookiecutter.module_name }} a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations   
```

## Using unreleased changes

By default, `ccds` will use the _project template_ version that corresponds to the _installed `ccds` package_ version (e.g., if you have installed `ccds` v2.0.1, you'll use the v2.0.1 version of the project template by default). To use a specific version of the project template, use the `-c/--checkout` flag to provide the branch (or tag or commit hash) of the version you'd like to use. For example to use the project template from the `master` branch:

```bash
ccds -c master
```

## Using v1

If you want to use the old v1 project template, you need to have either the cookiecutter-data-science package or cookiecutter package installed. Then, use either command-line program with the `-c v1` option:

```bash
ccds https://github.com/drivendataorg/cookiecutter-data-science -c v1
# or equivalently
cookiecutter https://github.com/drivendataorg/cookiecutter-data-science -c v1
```

## Contributing

We welcome contributions! [See the docs for guidelines](https://cookiecutter-data-science.drivendata.org/contributing/).

### Installing development requirements

```bash
pip install -r dev-requirements.txt
```

### Running the tests

```bash
pytest tests
```

## Credits and license

Cookiecutter Data Science is created and maintained by [DrivenData](https://www.drivendata.org/) and its [contributors](https://github.com/drivendataorg/cookiecutter-data-science/graphs/contributors). The original repository is [drivendataorg/cookiecutter-data-science](https://github.com/drivendataorg/cookiecutter-data-science) and its documentation is at [cookiecutter-data-science.drivendata.org](https://cookiecutter-data-science.drivendata.org/). Everything in this repository except the CRISP-DM addition is their work, used under the MIT license; the original copyright notice is kept unchanged in [LICENSE](LICENSE), and the CRISP-DM addition is distributed under the same license.

The CRISP-DM documents follow the phases, tasks and outputs of the _CRISP-DM 1.0 Step-by-step data mining guide_ (Chapman et al., 2000), written by the CRISP-DM consortium.
