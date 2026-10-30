from pathlib import Path

from loguru import logger
from tqdm import tqdm
import typer

from {{ cookiecutter.module_name }}.config import PROCESSED_DATA_DIR, RAW_DATA_DIR

app = typer.Typer()


@app.command()
def main(
    # ---- REEMPLAZA LAS RUTAS POR DEFECTO SEGÚN CONVENGA ----
    input_path: Path = RAW_DATA_DIR / "dataset.csv",
    output_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
    # --------------------------------------------------------
):
    # ---- REEMPLAZA ESTO CON TU PROPIO CÓDIGO ----
    logger.info("Procesando el conjunto de datos...")
    for i in tqdm(range(10), total=10):
        if i == 5:
            logger.info("Algo pasó en la iteración 5.")
    logger.success("Procesamiento del conjunto de datos terminado.")
    # ---------------------------------------------


if __name__ == "__main__":
    app()
