# Cookiecutter Data Science + CRISP-DM

_Una estructura de proyecto lógica, razonablemente estandarizada y flexible para hacer y compartir trabajo de ciencia de datos._

[![PyPI - Version](https://img.shields.io/pypi/v/cookiecutter-data-science)](https://pypi.org/project/cookiecutter-data-science/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cookiecutter-data-science)](https://pypi.org/project/cookiecutter-data-science/)
<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>
[![tests](https://github.com/drivendataorg/cookiecutter-data-science/actions/workflows/tests.yml/badge.svg)](https://github.com/drivendataorg/cookiecutter-data-science/actions/workflows/tests.yml)

> **Este repositorio es un fork de [Cookiecutter Data Science](https://github.com/drivendataorg/cookiecutter-data-science), creado y mantenido por [DrivenData](https://www.drivendata.org/).** Todo el crédito de la plantilla es de DrivenData y sus colaboradores. Este fork traduce la plantilla al español y agrega a cada proyecto generado una carpeta con la metodología CRISP-DM y otra para las consultas SQL de extracción (consulta [Este fork](#este-fork) y [Créditos y licencia](#créditos-y-licencia)). Para empezar, sigue la [Guía rápida](#guía-rápida).

**Cookiecutter Data Science (CCDS)** es una herramienta para crear una plantilla de proyecto de ciencia de datos que incorpora buenas prácticas. Para conocer la filosofía de CCDS, visita la [página del proyecto](https://cookiecutter-data-science.drivendata.org/) (en inglés).

> ℹ️ Cookiecutter Data Science v2 cambió respecto a v1. Ahora requiere instalar el nuevo paquete de Python cookiecutter-data-science, que extiende la funcionalidad de la herramienta de plantillas [cookiecutter](https://cookiecutter.readthedocs.io/en/stable/README.html). Usa el programa de línea de comandos `ccds` en lugar de `cookiecutter`.

## Este fork

Este repositorio es CCDS v2.3.0 con tres cambios:

- **Español.** Está en español todo lo que lee quien usa la plantilla: este README, y en cada proyecto generado el README, la ayuda y los mensajes del Makefile, los comentarios y mensajes del código base y la documentación de mkdocs. Los nombres de carpetas, archivos, variables y opciones se quedan en inglés, porque son el estándar de CCDS y el paquete `ccds` depende de ellos. Las preguntas que hace `ccds` al generar un proyecto (por ejemplo, `project_name` o `Select docs`) también salen en inglés, porque vienen del paquete instalado.
- **CRISP-DM.** Cada proyecto generado incluye la carpeta `crisp_dm/` con un documento por fase de CRISP-DM (comprensión del negocio, comprensión de los datos, preparación de los datos, modelado, evaluación y despliegue). Cada documento enumera las tareas CRISP-DM de la fase, el resultado de cada tarea y una lista de verificación de cierre. `crisp_dm/README.md` lleva el estado de cada fase, relaciona las fases con las carpetas de CCDS y registra cada regreso a una fase anterior.
- **Consultas SQL.** El código base incluye la carpeta `sql/` para las consultas de extracción, una por archivo, y la función `extraer()` en `dataset.py`, que ejecuta una consulta con sus parámetros y regresa un DataFrame. La conexión se define en `.env` como `DATABASE_URL`; por defecto se instalan `sqlalchemy`, el driver de PostgreSQL (`psycopg2-binary`), `pandas` y `pyarrow`. Para otra base de datos, cambia el driver en las dependencias del proyecto y la URL.

**Definir tu metodología.** Haz un fork o clona este repositorio y edita los archivos de `{{ cookiecutter.repo_name }}/crisp_dm/`. Cada proyecto que generes después tendrá tu versión; los proyectos ya generados no cambian. Los archivos son plantillas Jinja, así que pueden usar las variables de CCDS, como `{{ cookiecutter.project_name }}` o `{{ cookiecutter.author_name }}`, y las llaves dobles literales del texto se deben escapar. Para generar un proyecto desde una copia local, pasa su ruta; se usan los archivos tal como están en disco:

```bash
ccds ruta/a/cookiecutter-data-science-crisp-dm
```

**Actualizar desde el repositorio original.** Los cambios están en la rama `crisp-dm`, la rama por defecto de este repositorio. Al integrar una versión nueva del original, los archivos traducidos pueden tener conflictos: resuélvelos conservando la traducción y traduciendo lo nuevo, y después corre las pruebas.

```bash
git remote add upstream https://github.com/drivendataorg/cookiecutter-data-science.git  # una sola vez
git fetch upstream --tags
git merge v2.4.0                                       # la versión nueva
pipx install --force cookiecutter-data-science==2.4.0  # mantén el paquete al día con la plantilla
```

## Guía rápida

Pasos para crear un proyecto desde cero en cualquier computadora. El repositorio es público, así que no necesitas iniciar sesión en GitHub.

### 1. Instala los requisitos

Necesitas Python 3.9 o superior, `git`, `make` y el paquete `ccds` en la versión 2.3.0, instalado con [pipx](https://pipx.pypa.io/). La versión tiene que ser exactamente esa, porque los hooks de la plantilla importan funciones del paquete `ccds` instalado.

**Ubuntu/Debian**

```bash
sudo apt install python3 python3-venv git make pipx
pipx ensurepath          # después cierra y vuelve a abrir la terminal
pipx install cookiecutter-data-science==2.3.0
```

**macOS** (`make` viene con las herramientas de línea de comandos de Xcode)

```bash
brew install python git pipx
pipx ensurepath          # después cierra y vuelve a abrir la terminal
pipx install cookiecutter-data-science==2.3.0
```

**Windows** (PowerShell)

```powershell
py -m pip install --user pipx
py -m pipx ensurepath             # después vuelve a abrir PowerShell
pipx install cookiecutter-data-science==2.3.0
```

Anota la versión de Python de la computadora (`python3 --version`, o `py --version` en Windows); la necesitas en el paso 2.

### 2. Genera el proyecto

```bash
cd ~/Documentos            # la carpeta donde guardas tus proyectos
ccds https://github.com/enriquearriola-blip/cookiecutter-data-science-crisp-dm -c crisp-dm
```

La opción `-c crisp-dm` es necesaria: sin ella, `ccds` usa la etiqueta de la versión instalada (`v2.3.0`), que es la plantilla original, en inglés y sin CRISP-DM ni `sql/`. Si `ccds` pregunta si puede borrar y volver a descargar la plantilla, responde que sí (`yes`) para usar la versión más reciente.

Las preguntas salen en inglés; las de opciones son menús numerados:

| Pregunta | Respuesta sugerida |
|---|---|
| `project_name` | Por ejemplo, `Proyecto Prueba` (la carpeta se llamará `proyecto_prueba`) |
| `repo_name`, `module_name` | Enter, para aceptar el valor propuesto |
| `author_name`, `description` | Tu nombre y una frase sobre el proyecto |
| `python_version_number` | **La versión de Python de la computadora** (por ejemplo, `3.12`); si no coincide, la instalación falla con "requires a different Python" |
| `dataset_storage` | `none` |
| `environment_manager` | `none` si creas el ambiente tú (paso 3); `virtualenv` necesita virtualenvwrapper instalado |
| `dependency_file` | `requirements.txt` |
| `pydata_packages` | `basic` (agrega numpy, scikit-learn, matplotlib y Jupyter) |
| `testing_framework` | `pytest` |
| `linting_and_formatting` | `ruff` |
| `open_source_license` | `No license file`, para trabajo interno |
| `docs` | `mkdocs` |
| `include_code_scaffold` | **`Yes`**; sin él no se generan `sql/` ni `extraer()` |

### 3. Crea el ambiente e instala las dependencias

**Linux/macOS**

```bash
cd proyecto_prueba
python3 -m venv .venv
source .venv/bin/activate
make requirements
```

**Windows**: `make` no viene instalado, así que ejecuta los comandos directamente. Si PowerShell bloquea la activación del ambiente, ejecuta antes `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

```powershell
cd proyecto_prueba
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 4. Verifica que funcione

```bash
make              # ayuda: "Reglas disponibles: ..."
make lint         # "All checks passed!"
make data         # "Procesamiento del conjunto de datos terminado."
```

`make test` falla a propósito hasta que escribas tus propias pruebas: la prueba de ejemplo de `tests/` es `assert False`.

### 5. Conecta tu base de datos

1. En `.env`, quita el `#` de `DATABASE_URL` y llena tus datos:
   `DATABASE_URL=postgresql+psycopg2://usuario:contraseña@servidor:5432/base_de_datos`
2. Reemplaza `proyecto_prueba/sql/01_clientes.sql` por una consulta real.
3. Pruébala en Python, con el ambiente activado:

   ```python
   from proyecto_prueba.dataset import extraer

   clientes = extraer("01_clientes", fecha_inicio="2025-01-01", fecha_fin="2026-01-01")
   clientes.head()
   ```

### 6. Empieza el proyecto

- Abre `crisp_dm/README.md` y empieza por `crisp_dm/1-comprension-del-negocio.md`.
- Pon el proyecto bajo control de versiones. `.env`, `.venv/` y `data/` ya están en `.gitignore`, así que tus credenciales, el ambiente y los datos no entran a git:

  ```bash
  git init && git add . && git commit -m "Proyecto inicial desde la plantilla"
  ```

## La estructura de carpetas resultante

La estructura de carpetas de tu proyecto nuevo se verá más o menos así (según las opciones que elijas):

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

## Usar otras versiones de la plantilla

Por defecto, `ccds` usa la versión de la _plantilla_ que corresponde a la versión del _paquete `ccds` instalado_ (por ejemplo, si instalaste `ccds` v2.0.1, usarás la versión v2.0.1 de la plantilla). Para usar otra versión, pasa con la opción `-c/--checkout` la rama (o etiqueta o hash de commit) que quieras. Por ejemplo, para usar la plantilla original desde su rama `master`:

```bash
ccds -c master
```

## Usar v1

Si quieres usar la plantilla anterior, v1, necesitas tener instalado el paquete cookiecutter-data-science o el paquete cookiecutter. Después usa cualquiera de los dos programas con la opción `-c v1`:

```bash
ccds https://github.com/drivendataorg/cookiecutter-data-science -c v1
# o, de forma equivalente
cookiecutter https://github.com/drivendataorg/cookiecutter-data-science -c v1
```

## Contribuir

Las contribuciones a Cookiecutter Data Science se hacen en el [repositorio original](https://github.com/drivendataorg/cookiecutter-data-science); [consulta su guía](https://cookiecutter-data-science.drivendata.org/contributing/) (en inglés).

### Instalar los requisitos de desarrollo

```bash
pip install -r dev-requirements.txt
```

### Correr las pruebas

```bash
pytest tests
```

## Créditos y licencia

Cookiecutter Data Science es creado y mantenido por [DrivenData](https://www.drivendata.org/) y sus [colaboradores](https://github.com/drivendataorg/cookiecutter-data-science/graphs/contributors). El repositorio original es [drivendataorg/cookiecutter-data-science](https://github.com/drivendataorg/cookiecutter-data-science) y su documentación está en [cookiecutter-data-science.drivendata.org](https://cookiecutter-data-science.drivendata.org/). Todo lo que contiene este repositorio, salvo los cambios de este fork (la traducción, CRISP-DM y las consultas SQL), es obra suya y se usa bajo la licencia MIT. El aviso de copyright original se conserva sin cambios en [LICENSE](LICENSE), y los cambios de este fork se distribuyen bajo la misma licencia.

Los documentos de CRISP-DM siguen las fases, tareas y salidas de la _CRISP-DM 1.0 Step-by-step data mining guide_ (Chapman et al., 2000), escrita por el consorcio CRISP-DM.
