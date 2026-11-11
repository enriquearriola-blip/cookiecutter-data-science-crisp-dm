import os
from importlib import import_module
from types import SimpleNamespace
from unittest.mock import MagicMock, call

import pandas as pd
import pytest
from conftest import bake_project, default_args
from sqlalchemy.engine import make_url

DATABASE_URL = "postgresql+psycopg2://user:password@localhost/test"
YELLOWBRICK_ERROR = (
    "Could not determine version from string "
    "'Yellowbrick Database version 5.2.31-43363'"
)
COMPATIBILITY_OPTION = r"-c override_version=PostgreSQL\ 9.5.10"


@pytest.fixture(scope="module")
def dataset():
    config = {
        **default_args,
        "repo_name": "extraction-test",
        "module_name": "extraction_test",
        "environment_manager": "none",
        "dependency_file": "requirements.txt",
        "pydata_packages": "none",
        "include_code_scaffold": "Yes",
        "testing_framework": "none",
        "linting_and_formatting": "ruff",
        "docs": "none",
        "open_source_license": "No license file",
    }
    with bake_project(config) as project, pytest.MonkeyPatch.context() as patch:
        patch.syspath_prepend(str(project))
        yield import_module("extraction_test.dataset")


@pytest.fixture
def extraction(dataset, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", DATABASE_URL)
    monkeypatch.delenv("PGOPTIONS", raising=False)
    engine = MagicMock()
    engine.url = make_url(DATABASE_URL)
    retry_engine = MagicMock()
    create_engine = MagicMock(side_effect=[engine, retry_engine])
    frame = pd.DataFrame({"id_cliente": [1]})
    read_sql = MagicMock(return_value=frame)
    monkeypatch.setattr(dataset, "create_engine", create_engine)
    monkeypatch.setattr(dataset.pd, "read_sql", read_sql)
    return SimpleNamespace(
        engine=engine,
        retry_engine=retry_engine,
        create_engine=create_engine,
        read_sql=read_sql,
        frame=frame,
    )


def test_normal_connection_does_not_retry(dataset, extraction):
    params = {"fecha_inicio": "2025-01-01", "fecha_fin": "2026-01-01"}

    result = dataset.extraer("01_clientes", **params)

    assert result is extraction.frame
    extraction.create_engine.assert_called_once_with(DATABASE_URL)
    extraction.read_sql.assert_called_once()
    assert extraction.read_sql.call_args.kwargs["params"] == params
    extraction.engine.connect.return_value.__exit__.assert_called_once()
    extraction.engine.dispose.assert_called_once()
    extraction.retry_engine.connect.assert_not_called()


@pytest.mark.parametrize("options_source", ["none", "environment", "url"])
def test_yellowbrick_retries_with_local_options(
    dataset, extraction, monkeypatch, options_source
):
    prefix = ""
    if options_source == "environment":
        prefix = "-c statement_timeout=1000"
        monkeypatch.setenv("PGOPTIONS", prefix)
    elif options_source == "url":
        prefix = "-c statement_timeout=2000"
        monkeypatch.setenv("PGOPTIONS", "-c application_name=environment")
        extraction.engine.url = extraction.engine.url.update_query_dict(
            {"options": prefix}
        )
        monkeypatch.setenv(
            "DATABASE_URL",
            extraction.engine.url.render_as_string(hide_password=False),
        )
    previous_options = os.environ.get("PGOPTIONS")
    extraction.engine.connect.side_effect = AssertionError(YELLOWBRICK_ERROR)

    result = dataset.extraer("01_clientes")

    assert result is extraction.frame
    assert extraction.create_engine.call_count == 2
    assert extraction.create_engine.call_args == call(
        extraction.engine.url,
        connect_args={"options": f"{prefix} {COMPATIBILITY_OPTION}".strip()},
    )
    assert os.environ.get("PGOPTIONS") == previous_options
    extraction.read_sql.assert_called_once()
    extraction.engine.dispose.assert_called_once()
    extraction.retry_engine.connect.return_value.__exit__.assert_called_once()
    extraction.retry_engine.dispose.assert_called_once()


@pytest.mark.parametrize(
    "error",
    [AssertionError("unrelated initialization failure"), ValueError(YELLOWBRICK_ERROR)],
)
def test_other_connection_errors_are_not_retried(dataset, extraction, error):
    extraction.engine.connect.side_effect = error

    with pytest.raises(type(error)) as raised:
        dataset.extraer("01_clientes")

    assert raised.value is error
    extraction.create_engine.assert_called_once_with(DATABASE_URL)
    extraction.read_sql.assert_not_called()
    extraction.engine.dispose.assert_called_once()


@pytest.mark.parametrize(
    "error",
    [AssertionError(YELLOWBRICK_ERROR), RuntimeError("retry connection failed")],
)
def test_failed_retry_propagates_and_disposes_both_engines(dataset, extraction, error):
    extraction.engine.connect.side_effect = AssertionError(YELLOWBRICK_ERROR)
    extraction.retry_engine.connect.side_effect = error

    with pytest.raises(type(error)) as raised:
        dataset.extraer("01_clientes")

    assert raised.value is error
    assert extraction.create_engine.call_count == 2
    extraction.read_sql.assert_not_called()
    extraction.engine.dispose.assert_called_once()
    extraction.retry_engine.dispose.assert_called_once()


@pytest.mark.parametrize("yellowbrick", [False, True])
def test_query_errors_are_never_retried(dataset, extraction, yellowbrick):
    if yellowbrick:
        extraction.engine.connect.side_effect = AssertionError(YELLOWBRICK_ERROR)
    error = AssertionError(YELLOWBRICK_ERROR)
    extraction.read_sql.side_effect = error

    with pytest.raises(AssertionError) as raised:
        dataset.extraer("01_clientes")

    assert raised.value is error
    assert extraction.create_engine.call_count == (2 if yellowbrick else 1)
    extraction.read_sql.assert_called_once()
    extraction.engine.dispose.assert_called_once()
    if yellowbrick:
        extraction.retry_engine.dispose.assert_called_once()
