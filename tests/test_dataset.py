from datetime import date
from decimal import Decimal
from importlib import import_module
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pandas as pd
import pyarrow as pa
import pyarrow.csv as arrow_csv
import pyarrow.parquet as parquet
import pytest
from conftest import bake_project, default_args
from typer.testing import CliRunner

DATABASE_URL = "postgresql+psycopg2://user:password@localhost/test"


def column(name, oid=23, precision=None, scale=None):
    return SimpleNamespace(name=name, type_code=oid, precision=precision, scale=scale)


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
def export(dataset, tmp_path, monkeypatch):
    sql_dir = tmp_path / "sql"
    sql_dir.mkdir()
    (sql_dir / "01_datos.sql").write_text("SELECT 1 AS id;", encoding="utf-8")
    monkeypatch.setattr(dataset, "SQL_DIR", sql_dir)
    monkeypatch.setenv("DATABASE_URL", DATABASE_URL)
    monkeypatch.delenv("PGOPTIONS", raising=False)
    connection = MagicMock()
    cursor = connection.cursor.return_value.__enter__.return_value
    cursor.description = [column("id")]
    cursor.rowcount = 2
    cursor.mogrify.return_value = b"SELECT 1 AS id"
    state = SimpleNamespace(
        sql_dir=sql_dir,
        output_dir=tmp_path / "raw",
        connection=connection,
        cursor=cursor,
        payload=b"id\n1\n2\n",
        runner=CliRunner(),
    )

    def copy(command, output):
        assert not hasattr(output, "getvalue")
        output.write(state.payload)

    cursor.copy_expert.side_effect = copy
    state.connect = MagicMock(return_value=connection)
    monkeypatch.setattr(dataset.psycopg2, "connect", state.connect)
    monkeypatch.setattr(
        pd, "read_sql", MagicMock(side_effect=AssertionError("not COPY"))
    )
    return state


def test_copy_uses_psycopg2_and_preserves_connection_options(
    dataset, export, monkeypatch
):
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql+psycopg2://user:pa%40ss@server:5432/db?sslmode=require&connect_timeout=7",
    )
    monkeypatch.setenv("PGOPTIONS", "-c statement_timeout=1000")

    assert dataset.exportar("01_datos", export.output_dir) == 2

    export.connect.assert_called_once_with(
        user="user",
        password="pa@ss",
        host="server",
        port=5432,
        dbname="db",
        sslmode="require",
        connect_timeout="7",
    )
    export.cursor.copy_expert.assert_called_once()
    command = export.cursor.copy_expert.call_args.args[0]
    assert (
        command == "COPY (\nSELECT 1 AS id\n) TO STDOUT WITH (FORMAT CSV, HEADER TRUE)"
    )
    assert "LIMIT 0" in export.cursor.execute.call_args.args[0]
    export.cursor.fetchall.assert_not_called()
    export.connection.set_client_encoding.assert_called_once_with("UTF8")
    export.connection.close.assert_called_once()
    export.connection.cursor.return_value.__exit__.assert_called_once()
    assert dataset.os.environ["PGOPTIONS"] == "-c statement_timeout=1000"
    assert (export.output_dir / "01_datos.csv").read_bytes() == export.payload
    assert parquet.read_table(export.output_dir / "01_datos.parquet")[
        "id"
    ].to_pylist() == [1, 2]


def test_parameters_are_compiled_and_passed_to_mogrify(dataset, export):
    (export.sql_dir / "01_datos.sql").write_text(
        "SELECT :value AS id WHERE '100%' LIKE '%';", encoding="utf-8"
    )
    value = "O'Brien'); SELECT dangerous(); --"

    dataset.exportar("01_datos", export.output_dir, value=value)

    sql, params = export.cursor.mogrify.call_args.args
    assert "%(value)s" in sql
    assert "100%%" in sql
    assert params == {"value": value}
    assert not sql.endswith(";")
    assert value not in export.cursor.copy_expert.call_args.args[0]


def test_interactive_extraer_uses_copy_and_returns_dataframe(dataset, export):
    result = dataset.extraer("01_datos")

    assert isinstance(result, pd.DataFrame)
    assert result["id"].tolist() == [1, 2]
    export.cursor.copy_expert.assert_called_once()
    copied_path = Path(export.cursor.copy_expert.call_args.args[1].name)
    assert not copied_path.exists()
    assert not export.output_dir.exists()


def test_csv_conversion_preserves_text_nulls_decimals_and_dates(dataset, export):
    export.cursor.description = [
        column("id", 1043),
        column("amount", 1700, 18, 2),
        column("flag", 16),
        column("day", 1082),
        column("note", 1043),
        column("nullable", 1043),
        column("empty", 1043),
    ]
    export.payload = (
        "id,amount,flag,day,note,nullable,empty\n"
        '0001,9007199254740993.12,t,2026-11-11,"caf\u00e9, ""hola""\nlinea",,""\n'
        "0002,,f,2026-11-12,NA,x,plain\n"
    ).encode("utf-8")

    dataset.exportar("01_datos", export.output_dir)

    table = parquet.read_table(export.output_dir / "01_datos.parquet")
    assert table["id"].to_pylist() == ["0001", "0002"]
    assert table["amount"].to_pylist() == [Decimal("9007199254740993.12"), None]
    assert table["flag"].to_pylist() == [True, False]
    assert table["day"].to_pylist() == [date(2026, 11, 11), date(2026, 11, 12)]
    assert table["note"].to_pylist() == ['caf\u00e9, "hola"\nlinea', "NA"]
    assert table["nullable"].to_pylist() == [None, "x"]
    assert table["empty"].to_pylist() == ["", "plain"]
    assert (export.output_dir / "01_datos.csv").read_bytes() == export.payload


def test_empty_result_keeps_header_and_parquet_schema(dataset, export):
    export.payload = b"id\n"
    export.cursor.rowcount = 0

    assert dataset.exportar("01_datos", export.output_dir) == 0

    table = parquet.read_table(export.output_dir / "01_datos.parquet")
    assert table.num_rows == 0
    assert table.schema == pa.schema([("id", pa.int32())])


def test_parquet_conversion_writes_multiple_batches(dataset, export, monkeypatch):
    export.payload = ("id\n" + "".join(f"{i}\n" for i in range(100))).encode()
    export.cursor.rowcount = 100
    monkeypatch.setattr(
        dataset,
        "_lector_csv",
        lambda path, schema: arrow_csv.open_csv(
            path,
            read_options=arrow_csv.ReadOptions(block_size=64),
            convert_options=arrow_csv.ConvertOptions(column_types=schema),
        ),
    )

    dataset.exportar("01_datos", export.output_dir)

    metadata = parquet.read_metadata(export.output_dir / "01_datos.parquet")
    assert metadata.num_rows == 100
    assert metadata.num_row_groups > 1


@pytest.mark.parametrize("suffixes", [("csv",), ("parquet",), ("csv", "parquet")])
def test_existing_outputs_are_skipped_without_copy(dataset, export, suffixes):
    export.output_dir.mkdir()
    for suffix in suffixes:
        (export.output_dir / f"01_datos.{suffix}").write_bytes(b"existing")

    result = export.runner.invoke(dataset.app, ["--output-dir", str(export.output_dir)])

    assert result.exit_code == 0, result.output
    export.connect.assert_not_called()
    for suffix in suffixes:
        assert (export.output_dir / f"01_datos.{suffix}").read_bytes() == b"existing"

    result = export.runner.invoke(
        dataset.app, ["--output-dir", str(export.output_dir), "--overwrite"]
    )

    assert result.exit_code == 0, result.output
    assert (export.output_dir / "01_datos.csv").read_bytes() == export.payload
    assert parquet.read_table(export.output_dir / "01_datos.parquet").num_rows == 2


@pytest.mark.parametrize("phase", ["copy", "conversion", "rowcount"])
def test_failures_preserve_existing_files_and_remove_staging(
    dataset, export, monkeypatch, phase
):
    export.output_dir.mkdir()
    for suffix in ("csv", "parquet"):
        (export.output_dir / f"01_datos.{suffix}").write_bytes(b"existing")
    if phase == "copy":
        export.cursor.copy_expert.side_effect = RuntimeError("COPY failed")
    elif phase == "conversion":
        monkeypatch.setattr(
            dataset, "_convertir_parquet", MagicMock(side_effect=OSError("full"))
        )
    else:
        export.cursor.rowcount = 999

    with pytest.raises((RuntimeError, OSError, ValueError)):
        dataset.exportar("01_datos", export.output_dir, overwrite=True)

    assert sorted(path.name for path in export.output_dir.iterdir()) == [
        "01_datos.csv",
        "01_datos.parquet",
    ]
    for suffix in ("csv", "parquet"):
        assert (export.output_dir / f"01_datos.{suffix}").read_bytes() == b"existing"
    export.cursor.copy_expert.assert_called_once()
    export.connection.close.assert_called_once()


def test_connection_failure_is_not_retried(dataset, export):
    error = RuntimeError("connection failed")
    export.connect.side_effect = error

    with pytest.raises(RuntimeError) as raised:
        dataset.exportar("01_datos", export.output_dir)

    assert raised.value is error
    export.connect.assert_called_once()
    assert not list(export.output_dir.iterdir())


def test_duplicate_column_names_fail_before_copy(dataset, export):
    export.cursor.description = [column("id"), column("id")]

    with pytest.raises(ValueError, match="unicos"):
        dataset.exportar("01_datos", export.output_dir)

    export.cursor.copy_expert.assert_not_called()
    export.connection.close.assert_called_once()


def test_batch_runs_sql_files_in_order_without_dataframe(dataset, export, monkeypatch):
    (export.sql_dir / "02_datos.sql").write_text("SELECT 2 AS id", encoding="utf-8")
    monkeypatch.setattr(
        dataset, "extraer", MagicMock(side_effect=AssertionError("DataFrame"))
    )
    actual = dataset.exportar
    exporter = MagicMock(wraps=actual)
    monkeypatch.setattr(dataset, "exportar", exporter)

    result = export.runner.invoke(dataset.app, ["--output-dir", str(export.output_dir)])

    assert result.exit_code == 0, result.output
    assert [call.args[0] for call in exporter.call_args_list] == [
        "01_datos",
        "02_datos",
    ]
    assert sorted(path.name for path in export.output_dir.iterdir()) == [
        "01_datos.csv",
        "01_datos.parquet",
        "02_datos.csv",
        "02_datos.parquet",
    ]


@pytest.mark.parametrize("parameter", ["bad", "=value"])
def test_cli_rejects_malformed_parameters(dataset, export, parameter):
    result = export.runner.invoke(dataset.app, ["-p", parameter])

    assert result.exit_code == 2
    export.connect.assert_not_called()


def test_missing_parameters_fail_before_connection(dataset, export):
    (export.sql_dir / "01_datos.sql").write_text("SELECT :missing", encoding="utf-8")

    result = export.runner.invoke(dataset.app, ["--output-dir", str(export.output_dir)])

    assert result.exit_code == 2
    assert "missing" in result.output
    export.connect.assert_not_called()


def test_cli_requires_database_configuration(dataset, export, monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)

    result = export.runner.invoke(dataset.app, ["--output-dir", str(export.output_dir)])

    assert result.exit_code == 2
    assert "DATABASE_URL" in result.output
    export.connect.assert_not_called()


def test_unknown_database_types_are_kept_as_text(dataset):
    schema = dataset._esquema_arrow(
        [
            column("unknown", 99999),
            column("numeric", 1700),
            column("small", 21),
            column("big", 20),
            column("float", 700),
            column("double", 701),
            column("timestamp", 1114),
            column("zoned", 1184),
        ]
    )

    assert schema.types == [
        pa.string(),
        pa.string(),
        pa.int16(),
        pa.int64(),
        pa.float32(),
        pa.float64(),
        pa.timestamp("us"),
        pa.timestamp("us", tz="UTC"),
    ]
