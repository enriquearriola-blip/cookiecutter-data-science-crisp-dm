from pathlib import Path

from loguru import logger
from tqdm import tqdm
import typer

from {{ cookiecutter.module_name }}.config import FIGURES_DIR, PROCESSED_DATA_DIR

app = typer.Typer()


@app.command()
def main(
    # ---- REEMPLAZA LAS RUTAS POR DEFECTO SEGÚN CONVENGA ----
    input_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
    output_path: Path = FIGURES_DIR / "plot.png",
    # --------------------------------------------------------
):
    # ---- REEMPLAZA ESTO CON TU PROPIO CÓDIGO ----
    logger.info("Generando la gráfica a partir de los datos...")
    for i in tqdm(range(10), total=10):
        if i == 5:
            logger.info("Algo pasó en la iteración 5.")
    logger.success("Generación de la gráfica terminada.")
    # ---------------------------------------------


if __name__ == "__main__":
    app()
