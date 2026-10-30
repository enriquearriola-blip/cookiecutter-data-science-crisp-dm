import os
from pathlib import Path

from loguru import logger
import pandas as pd
from sqlalchemy import create_engine, text
from tqdm import tqdm
import typer

from {{ cookiecutter.module_name }}.config import PROCESSED_DATA_DIR, RAW_DATA_DIR

SQL_DIR = Path(__file__).resolve().parent / "sql"

app = typer.Typer()


def extraer(nombre: str, **parametros) -> pd.DataFrame:
    """Ejecuta la consulta sql/<nombre>.sql y regresa el resultado.

    Los parámetros se pasan a la consulta como :nombre_del_parametro. La conexión se lee de la
    variable de entorno DATABASE_URL, definida en .env.
    """
    consulta = text((SQL_DIR / f"{nombre}.sql").read_text(encoding="utf-8"))
    motor = create_engine(os.environ["DATABASE_URL"])
    try:
        with motor.connect() as conexion:
            return pd.read_sql(consulta, conexion, params=parametros)
    finally:
        motor.dispose()


@app.command()
def main(
    # ---- REEMPLAZA LAS RUTAS POR DEFECTO SEGÚN CONVENGA ----
    input_path: Path = RAW_DATA_DIR / "dataset.csv",
    output_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
    # --------------------------------------------------------
):
    # ---- REEMPLAZA ESTO CON TU PROPIO CÓDIGO ----
    # Para extraer de la base de datos, ejecuta las consultas de sql/ y guarda cada resultado,
    # sin modificarlo, en data/raw/. Por ejemplo:
    #   clientes = extraer("01_clientes", fecha_inicio="2025-01-01", fecha_fin="2026-01-01")
    #   clientes.to_parquet(RAW_DATA_DIR / "01_clientes.parquet")
    logger.info("Procesando el conjunto de datos...")
    for i in tqdm(range(10), total=10):
        if i == 5:
            logger.info("Algo pasó en la iteración 5.")
    logger.success("Procesamiento del conjunto de datos terminado.")
    # ---------------------------------------------


if __name__ == "__main__":
    app()
