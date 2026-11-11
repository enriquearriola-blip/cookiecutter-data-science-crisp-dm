import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Annotated

from loguru import logger
import pandas as pd
from sqlalchemy import create_engine, text
from tqdm import tqdm
import typer

from {{ cookiecutter.module_name }}.config import RAW_DATA_DIR

SQL_DIR = Path(__file__).resolve().parent / "sql"

app = typer.Typer()


def extraer(nombre: str, **parametros) -> pd.DataFrame:
    """Ejecuta la consulta sql/<nombre>.sql y regresa el resultado.

    Los parámetros se pasan a la consulta como :nombre_del_parametro. La conexión se lee de la
    variable de entorno DATABASE_URL, definida en .env. Si SQLAlchemy no reconoce la versión de
    Yellowbrick, reintenta la conexión una vez con compatibilidad local, sin reintentar consultas.
    """
    consulta = text((SQL_DIR / f"{nombre}.sql").read_text(encoding="utf-8"))
    motor = create_engine(os.environ["DATABASE_URL"])
    try:
        try:
            conexion = motor.connect()
        except AssertionError as error:
            if not str(error).startswith(
                "Could not determine version from string 'Yellowbrick Database version "
            ):
                raise
            opciones = motor.url.query.get("options", os.environ.get("PGOPTIONS", ""))
            opciones = f"{opciones} -c override_version=PostgreSQL\\ 9.5.10".strip()
            motor.dispose()
            motor = create_engine(motor.url, connect_args={"options": opciones})
            conexion = motor.connect()

        with conexion:
            return pd.read_sql(consulta, conexion, params=parametros)
    finally:
        motor.dispose()


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
        bool, typer.Option("--overwrite", help="Reemplaza los Parquet existentes.")
    ] = False,
):
    """Ejecuta todos los archivos SQL en orden y guarda sus resultados como Parquet."""
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
        salida = output_dir / f"{consulta.stem}.parquet"
        if salida.exists() and not overwrite:
            logger.info(f"Se omite {salida.name}; ya existe. Usa --overwrite.")
            continue

        requeridos = text(consulta.read_text(encoding="utf-8")).compile().params or {}
        faltantes = set(requeridos) - parametros.keys()
        if faltantes:
            raise typer.BadParameter(
                f"{consulta.name}: faltan parametros {', '.join(sorted(faltantes))}. "
                "Usa --parametro nombre=valor."
            )
        if not os.environ.get("DATABASE_URL"):
            raise typer.BadParameter("Configura DATABASE_URL en .env antes de extraer.")

        logger.info(f"Extrayendo {consulta.name}...")
        datos = extraer(consulta.stem, **parametros)
        # Publica el archivo solo al terminar; una falla no deja un Parquet incompleto.
        with NamedTemporaryFile(dir=output_dir, delete=False) as archivo:
            temporal = Path(archivo.name)
        try:
            datos.to_parquet(temporal, index=False)
            temporal.replace(salida)
        finally:
            temporal.unlink(missing_ok=True)
        logger.success(f"{consulta.name}: {len(datos):,} filas guardadas en {salida}.")
        del datos

    logger.success("Extraccion terminada.")


if __name__ == "__main__":
    app()
