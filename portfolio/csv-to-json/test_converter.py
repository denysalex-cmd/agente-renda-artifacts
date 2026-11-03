import json
from pathlib import Path
from converter import convert


def test_semicolon_delimiter_is_detected(tmp_path: Path):
    source = tmp_path / "input.csv"
    target = tmp_path / "output.json"
    source.write_text('name;note\nAna;"hello, world"\nBeto;"quote ""inside"""\n', encoding="utf-8")
    convert(str(source), str(target))
    data = json.loads(target.read_text(encoding="utf-8"))
    assert data[0] == {"name": "Ana", "note": "hello, world"}
    assert data[1]["note"] == 'quote "inside"'


def test_custom_pipe_delimiter(tmp_path: Path):
    source = tmp_path / "input.csv"
    target = tmp_path / "output.json"
    source.write_text("a|b\n1|2\n", encoding="utf-8")
    convert(str(source), str(target), delimiter="|")
    assert json.loads(target.read_text(encoding="utf-8")) == [{"a": "1", "b": "2"}]


def test_unicode_is_not_ascii_escaped(tmp_path: Path):
    source = tmp_path / "input.csv"
    target = tmp_path / "output.json"
    source.write_text("city,name\nCotia,João\n", encoding="utf-8")
    convert(str(source), str(target))
    assert "João" in target.read_text(encoding="utf-8")


def test_multiline_quoted_field_is_preserved(tmp_path: Path):
    source = tmp_path / "input.csv"
    target = tmp_path / "output.json"
    source.write_text('id,note\n1,"first line\nsecond line"\n', encoding="utf-8")
    convert(str(source), str(target))
    assert json.loads(target.read_text(encoding="utf-8")) == [{"id": "1", "note": "first line\nsecond line"}]


def test_invalid_row_width_raises(tmp_path: Path):
    source = tmp_path / "input.csv"
    target = tmp_path / "output.json"
    source.write_text("a,b\n1,2,3\n", encoding="utf-8")
    try:
        convert(str(source), str(target))
    except ValueError as exc:
        assert "too many fields" in str(exc)
    else:
        raise AssertionError("ValueError was not raised")
