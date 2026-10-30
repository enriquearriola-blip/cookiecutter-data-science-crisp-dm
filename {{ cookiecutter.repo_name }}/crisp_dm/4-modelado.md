# 4. Modelado

**Propósito:** seleccionar y aplicar técnicas de modelado y ajustar sus parámetros.

[← 3. Preparación de los datos](3-preparacion-de-los-datos.md) · [Resumen de CRISP-DM](README.md) ·
[Siguiente: 5. Evaluación →](5-evaluacion.md)

## 4.1 Seleccionar la técnica de modelado

### Técnica de modelado

_Técnicas elegidas y por qué, y el modelo de línea base._

### Supuestos del modelado

_Supuestos que cada técnica hace sobre los datos (distribución, independencia, valores faltantes, monotonicidad) y cómo
se verificaron._

## 4.2 Generar el diseño de prueba

### Diseño de prueba

_Cómo se comparan los modelos candidatos antes de la evaluación: muestras de entrenamiento y validación, el esquema de
validación cruzada, las métricas y la regla para elegir un modelo. Los datos de prueba y fuera de tiempo no se usan para
elegir._

## 4.3 Construir el modelo

### Configuración de parámetros

_Parámetros probados y los valores elegidos, con la razón._

### Modelos

| Modelo | Técnica | Parámetros | Atributos | Archivo en `models/` | Código de entrenamiento |
|---|---|---|---|---|---|
| | | | | | |

### Descripción de los modelos

_Qué aprendió cada modelo: atributos más importantes, dirección y forma de sus efectos, comportamiento en subpoblaciones
y cualquier problema encontrado._

## 4.4 Evaluar el modelo

### Evaluación del modelo

| Modelo | Métricas en validación | Cumple los criterios técnicos de 1.3 | Notas |
|---|---|---|---|
| | | | |

### Configuración de parámetros revisada

_Cambios hechos después de la evaluación y por qué. Repite 4.3 y 4.4 hasta encontrar el mejor modelo._

## Lista de verificación de cierre

- [ ] Modelo de línea base y modelos candidatos entrenados con código del repositorio
- [ ] Modelo elegido solo con el diseño de prueba, sin ver los datos de prueba ni fuera de tiempo
- [ ] Modelo elegido y sus parámetros guardados en `models/`
- [ ] Resultados reproducibles desde un ambiente limpio
