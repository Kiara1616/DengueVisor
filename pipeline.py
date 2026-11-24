"""Ingesta por filas de notificaciones públicas MINSA, con validación y trazabilidad."""
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import argparse
import csv
import hashlib
import io
import json
import os
import tempfile
import urllib.request

SOURCE = "https://www.datosabiertos.gob.pe/sites/default/files/datos_abiertos_vigilancia_dengue_2000_2025_0.csv"
ROOT = Path(__file__).resolve().parent
OUT = ROOT / "data/processed/weekly.csv"
REQUIRED = {"ano", "semana", "departamento", "tipo_dx"}


def publish(reader, output=OUT, source=SOURCE):
    if not REQUIRED.issubset(reader.fieldnames or []):
        raise ValueError(f"Faltan columnas: {sorted(REQUIRED - set(reader.fieldnames or []))}")
    counts, reasons = Counter(), Counter()
    total = 0
    for row in reader:
        total += 1
        try:
            year, week = int(row["ano"]), int(row["semana"])
        except (ValueError, TypeError):
            reasons["invalid_year_or_week"] += 1
            continue
        department = (row["departamento"] or "").strip().upper()
        diagnosis = (row["tipo_dx"] or "").strip().upper()
        if not 2020 <= year <= 2025:
            reasons["outside_year_scope"] += 1
        elif not 1 <= week <= 53:
            reasons["invalid_week"] += 1
        elif not department:
            reasons["missing_department"] += 1
        elif diagnosis not in {"C", "P", "S"}:
            reasons["unsupported_diagnosis"] += 1
        else:
            counts[year, week, department, diagnosis] += 1
    if not counts:
        raise ValueError("La fuente no contiene registros válidos; se conserva la publicación anterior.")
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="", dir=output.parent, delete=False) as staged:
        writer = csv.writer(staged)
        writer.writerow(["year", "week", "department", "diagnosis", "notifications"])
        writer.writerows([*key, count] for key, count in sorted(counts.items()))
        staged_path = Path(staged.name)
    os.replace(staged_path, output)
    metadata = {"source": source, "generated_at_utc": datetime.now(timezone.utc).isoformat(), "source_rows": total,
                "notifications_in_scope": sum(counts.values()), "excluded_rows": sum(reasons.values()),
                "exclusions": dict(reasons), "aggregate_rows": len(counts),
                "aggregate_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
                "scope": "2020-2025; weeks 1-53; C/P/S; nonempty department"}
    output.with_name("metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(metadata, ensure_ascii=False))
    return metadata


def build(source, output=OUT):
    with Path(source).open(encoding="utf-8-sig", newline="") as stream:
        return publish(csv.DictReader(stream), output, str(source))


def build_remote(output=OUT):
    request = urllib.request.Request(SOURCE, headers={"User-Agent": "DengueVisor/1.0 educational open-data pipeline"})
    with urllib.request.urlopen(request, timeout=120) as response:
        with io.TextIOWrapper(response, encoding="utf-8-sig", newline="") as stream:
            return publish(csv.DictReader(stream), output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="CSV local opcional")
    args = parser.parse_args()
    build(args.input) if args.input else build_remote()
