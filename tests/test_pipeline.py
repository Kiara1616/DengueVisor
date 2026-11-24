from pathlib import Path
import pytest
from pipeline import build


def test_aggregation(tmp_path):
    source = tmp_path / "sample.csv"
    source.write_text("ano,semana,departamento,tipo_dx\n2024,2,Lima,C\n2024,2,Lima,C\n2024,2,Lima,P\n2024,99,Lima,C\n", encoding="utf-8")
    output = tmp_path / "weekly.csv"
    result = build(source, output)
    assert result["notifications_in_scope"] == 3
    assert result["aggregate_rows"] == 2


def test_required_columns(tmp_path):
    source = tmp_path / "invalid.csv"
    source.write_text("ano,semana\n2024,1\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Faltan columnas"):
        build(source, tmp_path / "out.csv")


def test_invalid_source_preserves_previous_output(tmp_path):
    source = tmp_path / "empty.csv"
    source.write_text("ano,semana,departamento,tipo_dx\n2024,99,LIMA,C\n", encoding="utf-8")
    output = tmp_path / "weekly.csv"
    output.write_text("previous publication", encoding="utf-8")
    with pytest.raises(ValueError, match="registros válidos"):
        build(source, output)
    assert output.read_text() == "previous publication"


def test_quality_accounting(tmp_path):
    source = tmp_path / "sample.csv"
    source.write_text("ano,semana,departamento,tipo_dx\n2024,2, Lima ,c\n2019,2,Lima,C\n2024,54,Lima,C\n2024,2,,P\n2024,2,Lima,X\n", encoding="utf-8")
    result = build(source, tmp_path / "out.csv")
    assert result["source_rows"] == 5
    assert result["excluded_rows"] == 4
    assert result["notifications_in_scope"] == 1
