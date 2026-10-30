from pathlib import Path

from loguru import logger
from tqdm import tqdm
import typer

from {{ cookiecutter.module_name }}.config import MODELS_DIR, PROCESSED_DATA_DIR

app = typer.Typer()


@app.command()
def main(
    # ---- REEMPLAZA LAS RUTAS POR DEFECTO SEGÚN CONVENGA ----
    features_path: Path = PROCESSED_DATA_DIR / "features.csv",
    labels_path: Path = PROCESSED_DATA_DIR / "labels.csv",
    model_path: Path = MODELS_DIR / "model.pkl",
    # --------------------------------------------------------
):
    # ---- REEMPLAZA ESTO CON TU PROPIO CÓDIGO ----
    logger.info("Entrenando un modelo...")
    for i in tqdm(range(10), total=10):
        if i == 5:
            logger.info("Algo pasó en la iteración 5.")
    logger.success("Entrenamiento del modelo terminado.")
    # ---------------------------------------------


if __name__ == "__main__":
    app()
