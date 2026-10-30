# CRISP-DM: {{ cookiecutter.project_name }}

Esta carpeta documenta el proyecto con **CRISP-DM** (Cross-Industry Standard Process for Data Mining, proceso estándar
intersectorial para minería de datos). Hay un documento por fase. Cada uno enumera las tareas CRISP-DM de la fase, el
resultado que produce cada tarea y una lista de verificación de cierre.

CRISP-DM es iterativo: regresar a una fase anterior cuando se aprende algo nuevo es lo esperado, no un fracaso.
Anota cada regreso en el [registro de iteraciones](#registro-de-iteraciones).

```
 1. Comprensión del negocio ◄────────────────────┐
        │  ▲                                     │
        ▼  │                                     │
 2. Comprensión de los datos                     │
        │                                        │
        ▼                                        │
 3. Preparación de los datos ◄───┐               │
        │                        │               │
        ▼                        │               │
 4. Modelado ────────────────────┘               │
        │                                        │
        ▼                                        │
 5. Evaluación ──────────────────────────────────┘
        │
        ▼
 6. Despliegue
```

## Estado

| Fase | Documento | Estado | Responsable | Última actualización |
|---|---|---|---|---|
| 1. Comprensión del negocio | [1-comprension-del-negocio.md](1-comprension-del-negocio.md) | Sin iniciar | {{ cookiecutter.author_name }} | |
| 2. Comprensión de los datos | [2-comprension-de-los-datos.md](2-comprension-de-los-datos.md) | Sin iniciar | {{ cookiecutter.author_name }} | |
| 3. Preparación de los datos | [3-preparacion-de-los-datos.md](3-preparacion-de-los-datos.md) | Sin iniciar | {{ cookiecutter.author_name }} | |
| 4. Modelado | [4-modelado.md](4-modelado.md) | Sin iniciar | {{ cookiecutter.author_name }} | |
| 5. Evaluación | [5-evaluacion.md](5-evaluacion.md) | Sin iniciar | {{ cookiecutter.author_name }} | |
| 6. Despliegue | [6-despliegue.md](6-despliegue.md) | Sin iniciar | {{ cookiecutter.author_name }} | |

Valores de estado: Sin iniciar, En curso, Terminada, Revisitada.

## Dónde está cada fase en este proyecto

| Fase | Notebooks (`notebooks/`) | Código (`{{ cookiecutter.module_name }}/`) | Datos y salidas |
|---|---|---|---|
| 1. Comprensión del negocio | | | `references/`: requerimientos, glosario, material de los interesados |
| 2. Comprensión de los datos | `0.xx-*`: exploración de datos | `dataset.py` | `data/raw/`, `data/external/`, `references/`: diccionarios de datos |
| 3. Preparación de los datos | `1.xx-*`: limpieza y creación de variables | `dataset.py`, `features.py` | `data/interim/`, `data/processed/` |
| 4. Modelado | `3.xx-*`: modelado | `modeling/train.py` | `models/` |
| 5. Evaluación | `2.xx-*`: visualizaciones | `modeling/predict.py`, `plots.py` | `reports/`, `reports/figures/` |
| 6. Despliegue | `4.xx-*`: publicación | el paquete `{{ cookiecutter.module_name }}` | `models/`, `reports/`, `docs/` |
{% if cookiecutter.include_code_scaffold == "No" %}
En este proyecto no se generó el código base; los nombres de archivo de arriba indican dónde sugiere Cookiecutter Data
Science poner ese código.
{% endif %}
## Cómo usar estos documentos

1. Empieza por la fase 1 antes de tocar los datos y acuerda los criterios de éxito con quienes usarán los resultados.
2. Llena cada documento mientras haces el trabajo, no al final. Reemplaza el texto en _cursiva_ con la respuesta; cuando
   una tarea no aplique, escribe "No aplica" y por qué.
3. Enlaza la evidencia (notebooks, figuras, reportes, código) en lugar de copiar resultados en los documentos.
4. Una fase está terminada cuando su lista de verificación de cierre está completa. Actualiza la tabla de estado.
5. Cuando el trabajo te regrese a una fase anterior, agrega una fila al registro de iteraciones y marca esa fase como
   Revisitada.

## Registro de iteraciones

| Fecha | Desde la fase | Regreso a la fase | Qué se aprendió | Decisión |
|---|---|---|---|---|
| | | | | |
