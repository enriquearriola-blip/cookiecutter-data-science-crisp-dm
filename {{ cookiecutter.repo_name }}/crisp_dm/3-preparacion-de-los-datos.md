# 3. Preparación de los datos

**Propósito:** construir el conjunto de datos final para el modelado a partir de los datos crudos.

[← 2. Comprensión de los datos](2-comprension-de-los-datos.md) · [Resumen de CRISP-DM](README.md) ·
[Siguiente: 4. Modelado →](4-modelado.md)

## 3.1 Seleccionar los datos

### Justificación de inclusión y exclusión

_Qué registros (población, periodo, filtros) y qué atributos entran al análisis, y por qué. Anota los atributos que se
dejan fuera porque no están disponibles al momento de la predicción (fuga de información), por razones legales o éticas,
o por su calidad._

| Registros o atributo | Incluido | Razón |
|---|---|---|
| | | |

## 3.2 Limpiar los datos

### Informe de limpieza de los datos

| Problema (de 2.4) | Decisión | Implementación (archivo o función) | Registros afectados |
|---|---|---|---|
| | | | |

## 3.3 Construir los datos

### Atributos derivados

| Atributo | Definición | Campos de origen | Disponible al momento de la predicción |
|---|---|---|---|
| | | | |

### Registros generados

_Registros creados para el análisis (por ejemplo, periodos sin actividad), si los hay._

## 3.4 Integrar los datos

### Datos combinados

_Cómo se unen las tablas (llaves, cardinalidad, alineación en el tiempo) y las verificaciones de que no se duplican ni se
pierden registros._

## 3.5 Formatear los datos

### Datos reformateados

_Cambios que necesitan las herramientas de modelado y que no cambian el significado de los datos (tipos, codificaciones,
orden)._

## Salidas

### Conjunto de datos

_Ubicación del conjunto de datos final en `data/processed/` y el código que lo construye
(`{{ cookiecutter.module_name }}/dataset.py`, `{{ cookiecutter.module_name }}/features.py`)._

### Descripción del conjunto de datos

_Definición de la variable objetivo, número de registros y atributos, y las muestras (entrenamiento, validación, prueba,
fuera de tiempo) con sus periodos._

| Muestra | Periodo | Registros | Eventos | Tasa de eventos |
|---|---|---|---|---|
| | | | | |

## Lista de verificación de cierre

- [ ] El conjunto de datos se reconstruye de principio a fin desde `data/raw/` con código del repositorio, sin pasos
      manuales
- [ ] Cada grupo de registros y cada atributo excluido tiene una razón
- [ ] Ningún atributo usa información que no esté disponible al momento de la predicción
- [ ] Muestras definidas antes del modelado, con los datos de prueba y fuera de tiempo apartados
