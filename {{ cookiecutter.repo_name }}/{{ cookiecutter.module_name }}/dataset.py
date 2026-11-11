from contextlib import contextmanager
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Annotated

from loguru import logger
import pandas as pd
import psycopg2
import pyarrow as pa
from pyarrow import parquet
import pyarrow.csv as arrow_csv
from sqlalchemy import text
from sqlalchemy.dialects import postgresql
from sqlalchemy.engine import make_url
from tqdm import tqdm
import typer

from {{ cookiecutter.module_name }}.config import RAW_DATA_DIR

SQL_DIR = Path(__file__).resolve().parent / "sql"

app = typer.Typer()


def _preparar_consulta(nombre, parametros):
    ruta = SQL_DIR / f"{nombre}.sql"
    sql = ruta.read_text(encoding="utf-8").strip().rstrip(";")
    consulta = text(sql).compile(dialect=postgresql.dialect())
    faltantes = set(consulta.params) - parametros.keys()
    if faltantes:
        raise ValueError(
            f"{nombre}.sql: faltan parametros {', '.join(sorted(faltantes))}. "
            "Usa --parametro nombre=valor."
        )
    return str(consulta), {clave: parametros[clave] for clave in consulta.params}


def _esquema_arrow(columnas):
    tipos = {
        16: pa.bool_(),
        20: pa.int64(),
        21: pa.int16(),
        23: pa.int32(),
        700: pa.float32(),
        701: pa.float64(),
        1082: pa.date32(),
        1114: pa.timestamp("us"),
        1184: pa.timestamp("us", tz="UTC"),
    }
    campos = []
    for columna in columnas:
        tipo = tipos.get(columna.type_code, pa.string())
        if columna.type_code == 1700:
            precision, escala = columna.precision, columna.scale
            if precision and escala is not None and 0 <= escala <= precision <= 38:
                tipo = pa.decimal128(precision, escala)
        campos.append(pa.field(columna.name, tipo))
    esquema = pa.schema(campos)
    if len(set(esquema.names)) != len(esquema.names):
        raise ValueError("Las columnas de la consulta deben tener nombres unicos.")
    return esquema


def _copiar_csv(nombre, destino, parametros):
    consulta, valores = _preparar_consulta(nombre, parametros)
    url = make_url(os.environ["DATABASE_URL"])
    if url.get_backend_name() not in {"postgres", "postgresql"}:
        raise ValueError("COPY requiere una conexion PostgreSQL o Yellowbrick.")
    opciones = url.translate_connect_args(username="user", database="dbname")
    opciones.update(url.query)
    conexion = psycopg2.connect(**opciones)
    try:
        conexion.set_client_encoding("UTF8")
        with conexion.cursor() as cursor:
            cursor.execute("SET LOCAL DateStyle TO 'ISO, YMD'")
            sql = cursor.mogrify(consulta, valores).decode("utf-8")
            cursor.execute(f"SELECT * FROM (\n{sql}\n) AS export_schema LIMIT 0")
            esquema = _esquema_arrow(cursor.description)
            with destino.open("wb") as archivo:
                cursor.copy_expert(
                    f"COPY (\n{sql}\n) TO STDOUT WITH (FORMAT CSV, HEADER TRUE)",
                    archivo,
                )
            return esquema, cursor.rowcount
    finally:
        conexion.close()


@contextmanager
def _lector_csv(ruta, esquema):
    with (
        ruta.open("rb") as fuente,
        arrow_csv.open_csv(
            fuente,
            read_options=arrow_csv.ReadOptions(block_size=8 * 1024 * 1024),
            parse_options=arrow_csv.ParseOptions(newlines_in_values=True),
            convert_options=arrow_csv.ConvertOptions(
                column_types=esquema,
                null_values=[""],
                strings_can_be_null=True,
                quoted_strings_can_be_null=False,
                true_values=["t", "true", "TRUE", "True", "1"],
                false_values=["f", "false", "FALSE", "False", "0"],
            ),
        ) as lector,
    ):
        yield lector


def _convertir_parquet(csv_path, parquet_path, esquema):
    filas = 0
    with (
        _lector_csv(csv_path, esquema) as lector,
        parquet.ParquetWriter(parquet_path, lector.schema) as escritor,
    ):
        for lote in lector:
            escritor.write_batch(lote)
            filas += lote.num_rows
    return filas


def extraer(nombre: str, **parametros) -> pd.DataFrame:
    """Usa COPY y devuelve un DataFrame completo para el trabajo interactivo.

    Para exportaciones grandes usa exportar() o el comando del modulo, que no cargan todo en RAM.
    Los parametros SQL se escriben como :nombre y se adaptan con cursor.mogrify().
    """
    with TemporaryDirectory(prefix="extraer-") as carpeta:
        ruta = Path(carpeta) / "datos.csv"
        esquema, _ = _copiar_csv(nombre, ruta, parametros)
        with _lector_csv(ruta, esquema) as lector:
            return lector.read_all().to_pandas()


def exportar(
    nombre: str,
    output_dir: Path = RAW_DATA_DIR,
    overwrite: bool = False,
    **parametros,
):
    """Exporta un CSV nativo con COPY y lo convierte a Parquet por lotes."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / f"{nombre}.csv"
    parquet_path = output_dir / f"{nombre}.parquet"
    if not overwrite and (csv_path.exists() or parquet_path.exists()):
        raise FileExistsError(f"Ya existe una salida de {nombre}; usa --overwrite.")

    with TemporaryDirectory(dir=output_dir, prefix=".exportar-") as carpeta:
        temporal_csv = Path(carpeta) / "datos.csv"
        temporal_parquet = Path(carpeta) / "datos.parquet"
        esquema, copiadas = _copiar_csv(nombre, temporal_csv, parametros)
        filas = _convertir_parquet(temporal_csv, temporal_parquet, esquema)
        if copiadas >= 0 and filas != copiadas:
            raise ValueError("El numero de filas del CSV y del Parquet no coincide.")
        if not overwrite and (csv_path.exists() or parquet_path.exists()):
            raise FileExistsError(f"Ya existe una salida de {nombre}; usa --overwrite.")
        # No publica archivos si falla COPY o la conversion.
        temporal_csv.replace(csv_path)
        temporal_parquet.replace(parquet_path)
    return filas


@app.command()
def main(
    parametro: Annotated[
        list[str],
        typer.Option(
            "--parametro",
            "-p",
            default_factory=list,
            help="Parametro SQL como nombre=valor; se puede repetir.",
        ),
    ],
    output_dir: Path = RAW_DATA_DIR,
    overwrite: Annotated[
        bool,
        typer.Option("--overwrite", help="Reemplaza los CSV y Parquet existentes."),
    ] = False,
):
    """Exporta cada consulta con COPY a CSV y convierte el CSV a Parquet por lotes."""
    parametros = {}
    for item in parametro:
        nombre, separador, valor = item.partition("=")
        if not separador or not nombre:
            raise typer.BadParameter("Usa --parametro nombre=valor.")
        parametros[nombre] = valor

    consultas = sorted(path for path in SQL_DIR.glob("*.sql") if path.is_file())
    if not consultas:
        raise typer.BadParameter(f"No se encontraron consultas SQL en {SQL_DIR}.")

    output_dir.mkdir(parents=True, exist_ok=True)
    for consulta in tqdm(consultas, desc="Extrayendo consultas"):
        salidas = [output_dir / f"{consulta.stem}.{ext}" for ext in ("csv", "parquet")]
        if any(salida.exists() for salida in salidas) and not overwrite:
            logger.info(f"Se omite {consulta.stem}; ya existe. Usa --overwrite.")
            continue

        try:
            _preparar_consulta(consulta.stem, parametros)
        except ValueError as error:
            raise typer.BadParameter(str(error)) from error
        if not os.environ.get("DATABASE_URL"):
            raise typer.BadParameter("Configura DATABASE_URL en .env antes de extraer.")

        logger.info(f"Extrayendo {consulta.name}...")
        filas = exportar(consulta.stem, output_dir, overwrite, **parametros)
        logger.success(f"{consulta.stem}: {filas:,} filas en CSV y Parquet.")

    logger.success("Extraccion terminada.")


if __name__ == "__main__":
    app()
