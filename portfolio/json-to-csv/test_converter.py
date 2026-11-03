import csv
import json
from pathlib import Path
from converter import convert


def test_missing_keys_are_empty(tmp_path: Path):
    source = tmp_path / "input.json"
    target = tmp_path / "output.csv"
    source.write_text(json.dumps([{"name": "Ana", "age": 30}, {"name": "Beto", "city": "Cotia"}]), encoding="utf-8")
    convert(str(source), str(target))
    with target.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert rows == [
        {"name": "Ana", "age": "30", "city": ""},
        {"name": "Beto", "age": "", "city": "Cotia"},
    ]


def test_invalid_shape_raises(tmp_path: Path):
    source = tmp_path / "input.json"
    target = tmp_path / "output.csv"
    source.write_text(json.dumps({"name": "not-an-array"}), encoding="utf-8")
    try:
        convert(str(source), str(target))
    except ValueError as exc:
        assert "array of objects" in str(exc)
    else:
        raise AssertionError("ValueError was not raised")
