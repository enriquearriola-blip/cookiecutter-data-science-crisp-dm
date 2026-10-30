# Documentación de {{ cookiecutter.project_name }}
{% if cookiecutter.project_description is not none %}
## Descripción

{{ cookiecutter.description}}
{% endif %}
## Comandos

El Makefile contiene los puntos de entrada principales para las tareas comunes de este proyecto.
{% if not cookiecutter.dataset_storage.none %}
### Sincronizar los datos con el almacenamiento en la nube

{% if cookiecutter.dataset_storage.s3 -%}
* `make sync_data_up` usa `aws s3 sync` para sincronizar recursivamente los archivos de `data/` hacia `s3://{{ cookiecutter.dataset_storage.s3.bucket }}/data/`.
* `make sync_data_down` usa `aws s3 sync` para sincronizar recursivamente los archivos de `s3://{{ cookiecutter.dataset_storage.s3.bucket }}/data/` hacia `data/`.
{% elif cookiecutter.dataset_storage.azure -%}
* `make sync_data_up` usa `az storage blob upload-batch -d` para sincronizar recursivamente los archivos de `data/` hacia `{{ cookiecutter.dataset_storage.azure.container }}/data/`.
* `make sync_data_down` usa `az storage blob download-batch -s` para sincronizar recursivamente los archivos de `{{ cookiecutter.dataset_storage.azure.container }}/data/` hacia `data/`.
{% elif cookiecutter.dataset_storage.gcs -%}
* `make sync_data_up` usa `gsutil rsync` para sincronizar recursivamente los archivos de `data/` hacia `gs://{{ cookiecutter.dataset_storage.gcs.bucket }}/data/`.
* `make sync_data_down` usa `gsutil rsync` para sincronizar recursivamente los archivos de `gs://{{ cookiecutter.dataset_storage.gcs.bucket }}/data/` hacia `data/`.
{% endif %}
{% endif %}
