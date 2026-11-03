#!/usr/bin/env python3
import argparse
import csv
import io
import json
from pathlib import Path


def _dialect(sample: str, delimiter: str | None):
    if delimiter:
        class Custom(csv.excel):
            pass
        Custom.delimiter = delimiter
        return Custom
    try:
        return csv.Sniffer().sniff(sample, delimiters=",;\t|")
    except csv.Error:
        return csv.excel


def convert(input_path: str, output_path: str, delimiter: str | None = None, indent: int | None = 2) -> None:
    text = Path(input_path).read_text(encoding="utf-8-sig")
    if not text.strip():
        raise ValueError("CSV input is empty")
    dialect = _dialect(text[:8192], delimiter)
    try:
        reader = csv.DictReader(io.StringIO(text, newline=""), dialect=dialect, strict=True)
        if not reader.fieldnames or any(name is None or name == "" for name in reader.fieldnames):
            raise ValueError("CSV header is required")
        rows = []
        for line_number, row in enumerate(reader, start=2):
            if None in row:
                raise ValueError(f"Invalid CSV row {line_number}: too many fields")
            if any(value is None for value in row.values()):
                raise ValueError(f"Invalid CSV row {line_number}: too few fields")
            rows.append(row)
    except csv.Error as exc:
        raise ValueError(f"Invalid CSV: {exc}") from exc
    Path(output_path).write_text(json.dumps(rows, ensure_ascii=False, indent=indent), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert CSV data to JSON")
    parser.add_argument("input", help="Input CSV file")
    parser.add_argument("output", help="Output JSON file")
    parser.add_argument("--delimiter", help="Optional delimiter override, for example ';' or '|'")
    parser.add_argument("--indent", type=int, default=2, help="JSON indentation; use 0 for compact-ish output")
    args = parser.parse_args()
    convert(args.input, args.output, delimiter=args.delimiter, indent=args.indent)


if __name__ == "__main__":
    main()
