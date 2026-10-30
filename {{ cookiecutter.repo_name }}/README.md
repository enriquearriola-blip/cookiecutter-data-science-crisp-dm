# {{cookiecutter.project_name}}

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

{{cookiecutter.description}}

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

