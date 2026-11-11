-- Consulta de ejemplo: reemplázala por tus consultas de extracción.
--
-- Una consulta por archivo, numerada en orden de ejecución. dataset.extraer("01_clientes", ...) la
-- ejecuta; el comando del modulo guarda 01_clientes.csv y 01_clientes.parquet en data/raw/.
-- Los parámetros se escriben con dos puntos antes del nombre, como en el WHERE de abajo, y sus valores
-- se pasan desde Python; no pegues los valores en el texto. SQLAlchemy toma como parámetro cualquier
-- palabra con dos puntos pegados al inicio, incluso en los comentarios: evita escribirlas aquí.
SELECT
    id_cliente,
    fecha_alta
FROM clientes
WHERE fecha_alta >= :fecha_inicio
  AND fecha_alta < :fecha_fin
