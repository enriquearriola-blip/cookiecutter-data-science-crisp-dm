import os
from importlib import import_module
from types import SimpleNamespace
from unittest.mock import MagicMock, call

import pandas as pd
import pytest
from conftest import bake_project, default_args
from sqlalchemy.engine import make_url
from typer.testing import CliRunner

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


@pytest.fixture
def batch(dataset, tmp_path, monkeypatch):
    sql_dir = tmp_path / "sql"
    sql_dir.mkdir()
    monkeypatch.setattr(dataset, "SQL_DIR", sql_dir)
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    monkeypatch.delenv("PGOPTIONS", raising=False)
    return SimpleNamespace(
        sql_dir=sql_dir,
        output_dir=tmp_path / "raw",
        runner=CliRunner(),
    )


def test_batch_extracts_queries_in_order_and_saves_parquet(dataset, batch, monkeypatch):
    (batch.sql_dir / "02_segunda.sql").write_text("SELECT 2 AS id", encoding="utf-8")
    (batch.sql_dir / "01_primera.sql").write_text("SELECT 1 AS id", encoding="utf-8")
    (batch.sql_dir / "README.txt").write_text("Not a query", encoding="utf-8")
    extract = MagicMock(wraps=dataset.extraer)
    monkeypatch.setattr(dataset, "extraer", extract)

    result = batch.runner.invoke(dataset.app, ["--output-dir", str(batch.output_dir)])

    assert result.exit_code == 0, result.output
    assert extract.call_args_list == [call("01_primera"), call("02_segunda")]
    assert sorted(path.name for path in batch.output_dir.iterdir()) == [
        "01_primera.parquet",
        "02_segunda.parquet",
    ]
    for name, value in (("01_primera", 1), ("02_segunda", 2)):
        pd.testing.assert_frame_equal(
            pd.read_parquet(batch.output_dir / f"{name}.parquet"),
            pd.DataFrame({"id": [value]}),
        )


def test_batch_passes_repeated_parameters_to_queries(dataset, batch):
    (batch.sql_dir / "01_parametros.sql").write_text(
        "SELECT :fecha_inicio AS fecha_inicio, :etiqueta AS etiqueta",
        encoding="utf-8",
    )
    (batch.sql_dir / "02_sin_parametros.sql").write_text(
        "SELECT 2 AS id", encoding="utf-8"
    )

    result = batch.runner.invoke(
        dataset.app,
        [
            "--output-dir",
            str(batch.output_dir),
            "-p",
            "fecha_inicio=2025-01-01",
            "-p",
            "etiqueta=a=b",
        ],
    )

    assert result.exit_code == 0, result.output
    pd.testing.assert_frame_equal(
        pd.read_parquet(batch.output_dir / "01_parametros.parquet"),
        pd.DataFrame({"fecha_inicio": ["2025-01-01"], "etiqueta": ["a=b"]}),
    )
    assert (batch.output_dir / "02_sin_parametros.parquet").is_file()


@pytest.mark.parametrize("parameter", ["fecha_inicio", "=2025-01-01"])
def test_batch_rejects_malformed_parameters(dataset, batch, monkeypatch, parameter):
    extract = MagicMock()
    monkeypatch.setattr(dataset, "extraer", extract)

    result = batch.runner.invoke(dataset.app, ["-p", parameter])

    assert result.exit_code == 2
    assert "nombre=valor" in result.output
    extract.assert_not_called()


def test_batch_reports_missing_sql_parameters(dataset, batch, monkeypatch):
    (batch.sql_dir / "01_parametros.sql").write_text(
        "SELECT :fecha_inicio AS fecha_inicio", encoding="utf-8"
    )
    extract = MagicMock()
    monkeypatch.setattr(dataset, "extraer", extract)

    result = batch.runner.invoke(dataset.app, ["--output-dir", str(batch.output_dir)])

    assert result.exit_code == 2
    assert "fecha_inicio" in result.output
    extract.assert_not_called()
    assert not list(batch.output_dir.iterdir())


def test_batch_reports_missing_database_configuration(dataset, batch, monkeypatch):
    (batch.sql_dir / "01_datos.sql").write_text("SELECT 1 AS id", encoding="utf-8")
    monkeypatch.delenv("DATABASE_URL", raising=False)
    extract = MagicMock()
    monkeypatch.setattr(dataset, "extraer", extract)

    result = batch.runner.invoke(dataset.app, ["--output-dir", str(batch.output_dir)])

    assert result.exit_code == 2
    assert "DATABASE_URL" in result.output
    extract.assert_not_called()


def test_batch_reports_empty_sql_directory(dataset, batch):
    result = batch.runner.invoke(dataset.app, ["--output-dir", str(batch.output_dir)])

    assert result.exit_code == 2
    assert "No se encontraron" in result.output
    assert not batch.output_dir.exists()


def test_batch_skips_existing_outputs_unless_overwrite_is_requested(
    dataset, batch, monkeypatch
):
    (batch.sql_dir / "01_datos.sql").write_text("SELECT 1 AS id", encoding="utf-8")
    batch.output_dir.mkdir()
    output = batch.output_dir / "01_datos.parquet"
    pd.DataFrame({"id": [99]}).to_parquet(output, index=False)
    extract = MagicMock(wraps=dataset.extraer)
    monkeypatch.setattr(dataset, "extraer", extract)
    args = ["--output-dir", str(batch.output_dir)]

    result = batch.runner.invoke(dataset.app, args)

    assert result.exit_code == 0, result.output
    extract.assert_not_called()
    assert pd.read_parquet(output)["id"].tolist() == [99]

    result = batch.runner.invoke(dataset.app, [*args, "--overwrite"])

    assert result.exit_code == 0, result.output
    extract.assert_called_once_with("01_datos")
    assert pd.read_parquet(output)["id"].tolist() == [1]


@pytest.mark.parametrize("existing_output", [False, True])
def test_batch_write_failure_preserves_outputs_and_cleans_temporary_files(
    dataset, batch, monkeypatch, existing_output
):
    (batch.sql_dir / "01_datos.sql").write_text("SELECT 1 AS id", encoding="utf-8")
    batch.output_dir.mkdir()
    output = batch.output_dir / "01_datos.parquet"
    if existing_output:
        output.write_bytes(b"existing output")
    monkeypatch.setattr(
        dataset, "extraer", MagicMock(return_value=pd.DataFrame({"id": [1]}))
    )

    def fail_write(frame, path, **kwargs):
        path.write_bytes(b"incomplete parquet")
        raise OSError("write failed")

    monkeypatch.setattr(pd.DataFrame, "to_parquet", fail_write)

    result = batch.runner.invoke(
        dataset.app, ["--output-dir", str(batch.output_dir), "--overwrite"]
    )

    assert result.exit_code != 0
    assert isinstance(result.exception, OSError)
    if existing_output:
        assert output.read_bytes() == b"existing output"
    assert list(batch.output_dir.iterdir()) == ([output] if existing_output else [])


def test_batch_query_failure_stops_without_publishing_output(
    dataset, batch, monkeypatch
):
    (batch.sql_dir / "01_invalid.sql").write_text(
        "SELECT * FROM missing_table", encoding="utf-8"
    )
    (batch.sql_dir / "02_valida.sql").write_text("SELECT 2 AS id", encoding="utf-8")
    extract = MagicMock(wraps=dataset.extraer)
    monkeypatch.setattr(dataset, "extraer", extract)

    result = batch.runner.invoke(dataset.app, ["--output-dir", str(batch.output_dir)])

    assert result.exit_code != 0
    extract.assert_called_once_with("01_invalid")
    assert not list(batch.output_dir.iterdir())
