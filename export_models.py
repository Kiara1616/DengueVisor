"""Exporta y concilia el modelo anual dbt para consumo público."""
from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parent

def export():
    with duckdb.connect(str(ROOT / "data/dengue.duckdb"), read_only=True) as db:
        total = db.sql("select sum(notifications) from annual_summary").fetchone()[0]
        expected = db.execute("select sum(notifications) from read_csv_auto(?)", [str(ROOT / "data/processed/weekly.csv")]).fetchone()[0]
        if total != expected:
            raise ValueError("El total dbt no coincide con el agregado semanal")
        db.sql("select * from annual_summary order by year, department, diagnosis").write_csv(str(ROOT / "data/processed/annual.csv"), header=True)
        print(f"Modelo dbt exportado; {total:,} notificaciones conciliadas")

if __name__ == "__main__":
    export()
