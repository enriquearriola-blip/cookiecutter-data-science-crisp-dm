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

El comando ejecuta todos los archivos `.sql` en orden alfabético y guarda cada resultado, sin modificarlo, en `data/raw/<nombre>.parquet`. Procesa una consulta a la vez y omite los Parquet existentes; agrega `--overwrite` para reemplazarlos explícitamente. `make data` ejecuta el mismo proceso.

Si las consultas usan parámetros, pásalos una vez para todo el lote:

```bash
python -m {{ cookiecutter.module_name }}.dataset -p fecha_inicio=2025-01-01 -p fecha_fin=2026-01-01
```

Con Make, usa `make data ARGS="-p fecha_inicio=2025-01-01 -p fecha_fin=2026-01-01"`. Puedes cambiar la carpeta de salida con `--output-dir`.

**Yellowbrick:** si SQLAlchemy no reconoce la versión del servidor, `extraer()` detecta ese error específico y reintenta la conexión una sola vez con la compatibilidad necesaria. No modifica `os.environ` ni la configuración global del servidor, y no reintenta errores de consulta. No necesitas agregar código de conexión a tus scripts o notebooks.

Opcionalmente, para evitar el primer intento de detección en cada extracción, quita el `#` de esta línea de `.env`, conservando las comillas simples y la barra antes del espacio:

```dotenv
PGOPTIONS='-c override_version=PostgreSQL\ 9.5.10'
```

`config.py` carga `.env` al importar `dataset`, por lo que esta opción también se aplica a todas las extracciones. Para PostgreSQL, deja `PGOPTIONS` comentado.

Para extraer una consulta individual de forma interactiva, abre una consola Python (`python -m IPython`) o un notebook que use el ambiente del proyecto y ejecuta:

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
