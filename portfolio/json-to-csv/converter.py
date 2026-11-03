#!/usr/bin/env python3
import argparse
import csv
import json
from pathlib import Path


def convert(input_path: str, output_path: str) -> None:
    data = json.loads(Path(input_path).read_text(encoding="utf-8"))
    if not isinstance(data, list) or any(not isinstance(row, dict) for row in data):
        raise ValueError("input JSON must be an array of objects")
    fields = []
    seen = set()
    for row in data:
        for key in row:
            if key not in seen:
                seen.add(key)
                fields.append(key)
    with open(output_path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in data:
            writer.writerow({key: row.get(key, "") for key in fields})


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert an array of flat JSON objects to CSV")
    parser.add_argument("input", help="Input JSON file")
    parser.add_argument("output", help="Output CSV file")
    args = parser.parse_args()
    convert(args.input, args.output)


if __name__ == "__main__":
    main()
