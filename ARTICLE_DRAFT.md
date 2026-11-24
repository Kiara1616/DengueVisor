# DengueVisor: ingeniería de datos para explorar notificaciones de dengue en Perú

**Autoría:** Kiara1616 (proyecto individual). Borrador para Dev.to, Medium o Hashnode; completar los enlaces públicos antes de publicar.

## Problema
La fuente oficial publica notificaciones de dengue, pero explorar una región y semana requiere descargar y procesar un archivo grande. Construí DengueVisor para consultar los registros mediante filtros y gráficos, manteniendo el origen y las limitaciones de la información. El propósito es convertir un archivo abierto en un producto reproducible y fácil de consultar.

## Datos y arquitectura
Fuente: [Vigilancia Epidemiológica de dengue](https://www.datosabiertos.gob.pe/dataset/vigilancia-epidemiol%C3%B3gica-de-dengue). Python procesa el CSV remoto por filas y genera agregados; dbt sobre DuckDB construye y prueba un resumen anual; GitHub Actions actualiza los datos; Streamlit muestra gráficos.

## Transformación
Seleccioné 2020–2025, semanas 1–53, departamentos informados y tipos C/P/S. Agrupé por año, semana, departamento y tipo de diagnóstico. El CSV original no se publica en el repositorio; el dashboard usa agregados. La descarga usa `TextIOWrapper` y `csv.DictReader`, lo que permite leer el CSV por filas y respetar campos entrecomillados. Un contador acumula cada combinación sin almacenar todos los registros individuales en memoria.

Cada exclusión tiene una razón registrada: año fuera del alcance, semana inválida, departamento ausente o diagnóstico no admitido. Una fuente sin columnas requeridas o sin registros válidos provoca un error y conserva la publicación anterior.

## Transformación SQL con dbt

DuckDB permite trabajar con una base local, sin administrar un servidor. dbt construye el modelo `annual_summary`, con notificaciones y semanas registradas por año, departamento y diagnóstico. El núcleo del modelo es:

```sql
select year, department, diagnosis,
       sum(notifications) as notifications,
       count(distinct week) as reported_weeks
from read_csv_auto('data/processed/weekly.csv')
group by 1, 2, 3
```

Las pruebas dbt revisan nulos, valores diagnósticos admitidos y conteos positivos. Antes de exportar el resumen anual, verifico que su total coincida con el CSV semanal. La aplicación muestra ese resumen en su sección de datos, con una aclaración: el modelo anual no aplica el filtro de semanas del gráfico.

## Verificación
El procesamiento local leyó 1 065 274 filas de la fuente y generó 6 573 agregados semanales; 719 965 notificaciones quedaron dentro del alcance definido. Se excluyeron 345 309 registros por corresponder a años fuera del periodo seleccionado. La suma de registros incluidos y excluidos coincide con las filas leídas.

La ejecución local de `dbt build` construyó un modelo y superó seis pruebas de datos. Las cinco pruebas Python cubren agregación, columnas requeridas, preservación del archivo anterior, contabilidad de exclusiones y carga de la aplicación con ambos temas y una búsqueda sin resultados. Estas comprobaciones locales no sustituyen la evidencia de ejecución en GitHub: [añadir captura de Actions cuando se publique].

## Resultados
En el snapshot utilizado, 2024 reúne 271 531 notificaciones entre las clasificaciones incluidas. Para ese año, Lima aporta 87 864 registros y La Libertad 49 931. Son conteos absolutos de registros del archivo, no tasas ajustadas por población.

En todo el periodo filtrado se contabilizan 687 684 registros confirmados y 32 281 probables; no aparecen sospechosos dentro de este alcance. La opción de filtro se conserva para explicar la clasificación y admitir fuentes posteriores que la incluyan. No interpreto automáticamente el menor número de 2025 como una reducción: la cobertura del archivo puede ser parcial.

## Automatización y publicación

El workflow de calidad ejecuta pruebas Python, `dbt build` y la conciliación del resumen anual. Un segundo workflow actualiza la fuente los lunes a las 07:17 de Perú, o bajo demanda, y solo hace commit de los agregados si el procesamiento y las validaciones terminan correctamente.

La publicación prevista es Streamlit Community Cloud: se conecta el repositorio, la rama `main` y `app.py` una sola vez. El servicio observa cambios posteriores de GitHub y actualiza la aplicación. En el artículo publicado debo incluir una captura de una actualización real y la URL pública, para demostrar la automatización. La solución no requiere una cuenta ni credenciales de AWS.

## Limitaciones
Son notificaciones provisionales, sujetas a cambios. Los conteos no equivalen a tasas poblacionales ni a una predicción individual. Sin un identificador de caso no deduplico automáticamente registros con atributos iguales. La fecha de procesamiento indica cuándo ejecuté el pipeline, no cuándo el MINSA actualizó cada registro. El alcance llega a 2025, incluso si la aplicación se ejecuta en 2026.

## Enlaces
- Repositorio previsto: https://github.com/Kiara1616/DengueVisor (verificar publicación).
- Aplicación: pendiente de despliegue; añadir URL real.
- Video: pendiente de grabación y publicación; añadir URL real.
