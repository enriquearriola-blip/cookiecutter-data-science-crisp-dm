#################################################################################
# VARIABLES GLOBALES                                                            #
#################################################################################

PROJECT_NAME = {{ cookiecutter.repo_name }}
PYTHON_VERSION = {{ cookiecutter.python_version_number }}
PYTHON_INTERPRETER = python

#################################################################################
# COMANDOS                                                                      #
#################################################################################

{% if cookiecutter.dependency_file != 'none' %}
## Instala las dependencias de Python
.PHONY: requirements
requirements:
	{% if "requirements.txt" == cookiecutter.dependency_file -%}
	{% if "uv" == cookiecutter.environment_manager -%}
	uv pip install -r requirements.txt
	{% else -%}
	$(PYTHON_INTERPRETER) -m pip install -U pip
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt
	{% endif -%}
	{% elif "pyproject.toml" == cookiecutter.dependency_file -%}
	{% if "uv" == cookiecutter.environment_manager -%}
	uv sync
	{% elif "pixi" == cookiecutter.environment_manager -%}
	pixi install
	{% elif "poetry" == cookiecutter.environment_manager -%}
	poetry install
	{% else -%}
	pip install -e .
	{% endif -%}
	{% elif "environment.yml" == cookiecutter.dependency_file -%}
	conda env update --name $(PROJECT_NAME) --file environment.yml --prune
	{% elif "Pipfile" == cookiecutter.dependency_file -%}
	pipenv install
	{% elif "pixi.toml" == cookiecutter.dependency_file -%}
	pixi install
{% endif %}
{% endif %}


## Borra todos los archivos compilados de Python
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

{% if cookiecutter.linting_and_formatting == 'ruff' %}
## Revisa el estilo con ruff (usa `make format` para dar formato)
.PHONY: lint
lint:
	ruff format --check
	ruff check

## Da formato al código fuente con ruff
.PHONY: format
format:
	ruff check --fix
	ruff format
{% elif cookiecutter.linting_and_formatting == 'flake8+black+isort' %}
## Revisa el estilo con flake8, black e isort (usa `make format` para dar formato)
.PHONY: lint
lint:
	flake8 {{ cookiecutter.module_name }}
	isort --check --diff {{ cookiecutter.module_name }}
	black --check {{ cookiecutter.module_name }}

## Da formato al código fuente con black
.PHONY: format
format:
	isort {{ cookiecutter.module_name }}
	black {{ cookiecutter.module_name }}
{% endif %}

{% if cookiecutter.testing_framework != 'none' %}
## Corre las pruebas
.PHONY: test
test:
{%- if cookiecutter.testing_framework == 'unittest' %}
	python -m unittest discover -s tests
{%- elif cookiecutter.testing_framework == 'pytest' %}
	python -m pytest tests
{%- endif -%}
{%- endif -%}

{% if not cookiecutter.dataset_storage.none %}
## Descarga los datos del almacenamiento en la nube
.PHONY: sync_data_down
sync_data_down:
	{% if cookiecutter.dataset_storage.s3 -%}
	aws s3 sync s3://{{ cookiecutter.dataset_storage.s3.bucket }}/data/ \
		data/ {% if cookiecutter.dataset_storage.s3.aws_profile != 'default' %} --profile {{ cookiecutter.dataset_storage.s3.aws_profile }}{% endif %}
	{% elif cookiecutter.dataset_storage.azure -%}
	az storage blob download-batch -s {{ cookiecutter.dataset_storage.azure.container }}/data/ \
		-d data/
	{% elif cookiecutter.dataset_storage.gcs -%}
	gsutil -m rsync -r gs://{{ cookiecutter.dataset_storage.gcs.bucket }}/data/ data/
	{% endif %}

## Sube los datos al almacenamiento en la nube
.PHONY: sync_data_up
sync_data_up:
	{% if cookiecutter.dataset_storage.s3 -%}
	aws s3 sync data/ \
		s3://{{ cookiecutter.dataset_storage.s3.bucket }}/data {% if cookiecutter.dataset_storage.s3.aws_profile != 'default' %} --profile {{ cookiecutter.dataset_storage.s3.aws_profile }}{% endif %}
	{% elif cookiecutter.dataset_storage.azure -%}
	az storage blob upload-batch -d {{ cookiecutter.dataset_storage.azure.container }}/data/ \
		-s data/
	{% elif cookiecutter.dataset_storage.gcs -%}
	gsutil -m rsync -r data/ gs://{{ cookiecutter.dataset_storage.gcs.bucket }}/data/
	{% endif %}
{% endif %}

{% if cookiecutter.environment_manager != 'none' %}
## Crea el ambiente del intérprete de Python
.PHONY: create_environment
create_environment:
	{% if cookiecutter.environment_manager == 'conda' -%}
	{% if cookiecutter.dependency_file != 'environment.yml' %}
	conda create --name $(PROJECT_NAME) python=$(PYTHON_VERSION) -y
	{% else -%}
	conda env create --name $(PROJECT_NAME) -f environment.yml
	{% endif %}
	@echo ">>> Ambiente de conda creado. Actívalo con:\nconda activate $(PROJECT_NAME)"
	{% elif cookiecutter.environment_manager == 'virtualenv' -%}
	@bash -c "if [ ! -z `which virtualenvwrapper.sh` ]; then source `which virtualenvwrapper.sh`; mkvirtualenv $(PROJECT_NAME) --python=$(PYTHON_INTERPRETER); else mkvirtualenv.bat $(PROJECT_NAME) --python=$(PYTHON_INTERPRETER); fi"
	@echo ">>> Nuevo virtualenv creado. Actívalo con:\nworkon $(PROJECT_NAME)"
	{% elif cookiecutter.environment_manager == 'pipenv' -%}
	pipenv --python $(PYTHON_VERSION)
	@echo ">>> Nuevo ambiente de pipenv creado. Actívalo con:\npipenv shell"
	{% elif cookiecutter.environment_manager == 'uv' -%}
	uv venv --python $(PYTHON_VERSION)
	@echo ">>> Nuevo ambiente virtual de uv creado. Actívalo con:"
	@echo ">>> Windows: .\\\\.venv\\\\Scripts\\\\activate"
	@echo ">>> Unix/macOS: source ./.venv/bin/activate"
	{% elif cookiecutter.environment_manager == 'pixi' -%}
	{% if cookiecutter.dependency_file == 'pixi.toml' %}
	@echo ">>> El ambiente de Pixi se creará al ejecutar 'make requirements'"
	{% else %}
	@echo ">>> Ambiente de Pixi configurado en pyproject.toml. Ejecuta 'make requirements' para instalar las dependencias."
	{% endif %}
	@echo ">>> Actívalo con:\npixi shell"
	{% elif cookiecutter.environment_manager == 'poetry' -%}
	poetry env use $(PYTHON_VERSION)
	@echo ">>> Ambiente de Poetry creado. Actívalo con: "
	@echo '$$(poetry env activate)'
	@echo ">>> O ejecuta comandos con:\npoetry run <comando>"
{% endif %}
{% endif %}


#################################################################################
# REGLAS DEL PROYECTO                                                           #
#################################################################################

{% if cookiecutter.include_code_scaffold == 'Yes' %}
## Genera el conjunto de datos
.PHONY: data
data: requirements
	$(PYTHON_INTERPRETER) {{ cookiecutter.module_name }}/dataset.py
{% endif %}

#################################################################################
# Comandos autodocumentados                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
sys.stdin.reconfigure(encoding='utf-8'); \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Reglas disponibles:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON_INTERPRETER) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)
