# Revisión técnica — DengueVisor

Verificación local realizada sobre un entorno Python 3.12 independiente en D:, el 24 de noviembre de 2026 (Perú).

## Evidencia verificada

- Fuente real MINSA: 1 065 274 filas procesadas.
- Alcance 2020–2025: 719 965 registros incluidos, 345 309 excluidos por año fuera de alcance.
- Agregado semanal: 6 573 filas, sin registros individuales publicados.
- dbt: un modelo construido y seis pruebas de datos aprobadas.
- Conciliación de totales entre resumen anual dbt y agregado semanal: correcta.
- pytest: cinco pruebas aprobadas, incluyendo UI con ambos temas y búsqueda sin resultados.
- El servidor local de Streamlit arranca desde D: en el puerto 8501.

## Correcciones respecto de la primera versión

- Se unificó la transformación usada por la ingesta real y las pruebas locales.
- Se eliminó la ruta redundante que descargaba el archivo completo y la opción `--force` sin efecto.
- Se añadió lectura CSV correcta con `TextIOWrapper`, huella SHA-256 y contabilidad de exclusiones.
- Una fuente vacía o inválida no sustituye los agregados previos.
- El modelo dbt ahora se exporta y consume en el dashboard.
- Los años se tratan como categorías en gráficos para evitar colores continuos confusos.
- El indicador de máximo identifica año y semana; el ranking declara su alcance nacional.
- Se fijaron versiones directas, se separaron herramientas de desarrollo y dependencias de la app.
- Se documentaron la cobertura histórica, la posible cobertura parcial, la atribución y las publicaciones pendientes.

## Pendientes externos

Repositorio público bajo Kiara1616, ejecuciones CI públicas, despliegue SaaS, artículo publicado, video público, envío a Telegram y ZIP final. No se acreditan estos requisitos con pruebas locales.

No hay configuraciones, SDK, llaves ni recursos de AWS en este proyecto. No se revisaron ni modificaron recursos AWS ajenos al proyecto.
