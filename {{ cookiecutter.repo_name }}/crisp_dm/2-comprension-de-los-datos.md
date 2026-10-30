# 2. Comprensión de los datos

**Propósito:** recolectar los datos iniciales, familiarizarse con ellos, encontrar problemas de calidad y descubrir los
primeros hallazgos.

[← 1. Comprensión del negocio](1-comprension-del-negocio.md) · [Resumen de CRISP-DM](README.md) ·
[Siguiente: 3. Preparación de los datos →](3-preparacion-de-los-datos.md)

## 2.1 Recolectar los datos iniciales

### Informe de recolección de los datos iniciales

| Fuente | Descripción | Responsable | Ubicación o consulta | Periodo | Granularidad | Registros | Método de acceso |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

_Problemas encontrados al recolectar los datos y cómo se resolvieron. Guarda las consultas de extracción en
`{{ cookiecutter.module_name }}/sql/` (en la columna "Ubicación o consulta", enlaza el archivo) y las extracciones
crudas, sin modificar, en `data/raw/`._

## 2.2 Describir los datos

### Informe de descripción de los datos

_Formato y volumen de cada fuente, identificadores y llaves, y el significado de cada campo (enlaza el diccionario de
datos en `references/`). ¿Los datos cubren lo que necesitan los objetivos de minería de datos de la fase 1?_

## 2.3 Explorar los datos

### Informe de exploración de los datos

_Primeros hallazgos: distribuciones, relaciones entre los atributos clave y la variable objetivo, subpoblaciones,
cambios en el tiempo. Enlaza los notebooks de exploración (`notebooks/0.xx-*`)._

| Hallazgo | Evidencia (notebook, figura) | Implicación para las siguientes fases |
|---|---|---|
| | | |

## 2.4 Verificar la calidad de los datos

### Informe de calidad de los datos

_Valores faltantes, errores, duplicados, códigos inconsistentes, valores fuera de rango, huecos de cobertura en el
tiempo._

| Problema | Campos | Registros afectados | Tratamiento propuesto |
|---|---|---|---|
| | | | |

## Lista de verificación de cierre

- [ ] Todas las fuentes de datos identificadas, accesibles y documentadas
- [ ] Extracciones crudas guardadas en `data/raw/` y reproducibles con código del repositorio
- [ ] Diccionario de datos en `references/`
- [ ] Problemas de calidad de los datos listados, cada uno con un tratamiento propuesto
- [ ] Los datos pueden responder a los objetivos de minería de datos de la fase 1 (si no, regresa a la fase 1)
