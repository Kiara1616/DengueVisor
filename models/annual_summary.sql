-- Modelo dbt: resumen anual a partir de los agregados semanales.
select year, department, diagnosis,
       sum(notifications) as notifications,
       count(distinct week) as reported_weeks
from read_csv_auto('data/processed/weekly.csv')
group by 1, 2, 3
