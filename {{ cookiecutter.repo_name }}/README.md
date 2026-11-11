# {{cookiecutter.project_name}}

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

{{cookiecutter.description}}

{% if cookiecutter.include_code_scaffold == "Yes" %}
## Extracción de datos

Configura `DATABASE_URL` en `.env` y guarda tus consultas en `{{ cookiecutter.module_name }}/sql/`, una por archivo.

Con el ambiente activado, ejecuta en la terminal:

```bash
python -m {{ cookiecutter.module_name }}.dataset
```

El comando ejecuta los archivos `.sql` en orden alfabético. Usa `psycopg2.copy_expert()` para escribir un CSV nativo y convierte ese CSV a Parquet por lotes de lectura de 8 MiB, sin cargar todo en RAM. Conserva ambos archivos: `data/raw/<nombre>.csv` y `data/raw/<nombre>.parquet`. `make data` ejecuta el mismo proceso.

Si ya existe cualquiera de las dos salidas, omite la consulta. Usa `--overwrite` solo para volver a exportar y reemplazar ambos archivos. Los archivos no se publican si falla COPY o la conversión. Prevé espacio para CSV, Parquet y los temporales durante un reemplazo.

La conversión usa los tipos del servidor para preservar texto (incluidos ceros iniciales), nulos, fechas y decimales con precisión conocida. Los tipos no reconocidos y los numéricos sin precisión fija se guardan como texto.

Si las consultas usan parámetros, pásalos una vez para todo el lote:

```bash
python -m {{ cookiecutter.module_name }}.dataset -p fecha_inicio=2025-01-01 -p fecha_fin=2026-01-01
```

Con Make, usa `make data ARGS="-p fecha_inicio=2025-01-01 -p fecha_fin=2026-01-01"`. Puedes cambiar la carpeta de salida con `--output-dir`.

**PostgreSQL y Yellowbrick:** la conexión usa `psycopg2` directamente y no necesita `PGOPTIONS` ni un ajuste de versión. SQLAlchemy solo analiza la URL y los parámetros; no abre conexiones. No se reintentan consultas.

Para obtener un DataFrame completo de forma interactiva, abre una consola Python (`python -m IPython`) o un notebook que use el ambiente del proyecto y ejecuta (esta función también usa COPY, pero sí carga todo el resultado en RAM):

```python
from {{ cookiecutter.module_name }}.dataset import extraer

clientes = extraer("01_clientes", fecha_inicio="2025-01-01", fecha_fin="2026-01-01")
clientes.head()
```

Después de editar `.env`, reinicia la consola o el kernel si ya estaba abierto. Para una prueba rápida, agrega `LIMIT 5` a la consulta SQL: `head()` solo limita la visualización, no la extracción.
{% endif %}

## Organización del proyecto

```
├── LICENSE            <- Licencia de código abierto, si se eligió una
├── Makefile           <- Makefile con comandos útiles como `make data` o `make train`
├── README.md          <- El README principal para quienes desarrollan este proyecto.
├── crisp_dm           <- Metodología CRISP-DM: un documento por fase; empieza en crisp_dm/README.md
│
├── data
│   ├── external       <- Datos de fuentes externas.
│   ├── interim        <- Datos intermedios que ya se transformaron.
│   ├── processed      <- Los conjuntos de datos finales y canónicos para el modelado.
│   └── raw            <- Los datos originales, sin modificar.
│
├── docs               <- Un proyecto de mkdocs por defecto; consulta www.mkdocs.org
│
├── models             <- Modelos entrenados y serializados, predicciones o resúmenes de los modelos
│
├── notebooks          <- Jupyter notebooks. La convención de nombres es un número (para ordenarlos),
│                         las iniciales de quien lo crea y una descripción corta separada por `-`,
│                         p. ej. `1.0-jqp-exploracion-inicial-de-datos`.
│
├── pyproject.toml     <- Archivo de configuración del proyecto con los metadatos del paquete
│                         {{ cookiecutter.module_name }} y la configuración de herramientas como black
│
├── references         <- Diccionarios de datos, manuales y todo el material explicativo.
│
├── reports            <- Análisis generados en HTML, PDF, LaTeX, etc.
│   └── figures        <- Gráficas y figuras generadas para los reportes
│
├── requirements.txt   <- El archivo de requerimientos para reproducir el ambiente de análisis,
│                         p. ej. generado con `pip freeze > requirements.txt`
│
├── setup.cfg          <- Archivo de configuración de flake8
│
└── {{ cookiecutter.module_name }}   <- Código fuente de este proyecto.
    │
    ├── __init__.py             <- Hace de {{ cookiecutter.module_name }} un módulo de Python
    │
    ├── config.py               <- Variables útiles y configuración
    │
    ├── dataset.py              <- Scripts para descargar o generar datos
    │
    ├── features.py             <- Código para crear variables para el modelado
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Código para hacer inferencia con los modelos entrenados
    │   └── train.py            <- Código para entrenar modelos
    │
    ├── plots.py                <- Código para crear visualizaciones
    │
    └── sql                     <- Consultas SQL de extracción, una por archivo; las ejecuta dataset.py
```

--------
