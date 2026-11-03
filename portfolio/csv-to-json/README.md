# CSV to JSON converter sample

Self-produced AgenteRenda portfolio sample. This is **not** presented as a completed paid contract.

Python 3.10+ command-line utility for converting CSV files to JSON.

## Usage

```bash
python converter.py input.csv output.json
python converter.py input.csv output.json --delimiter ";"
python converter.py input.csv output.json --indent 4
```

The converter auto-detects comma, semicolon, tab and pipe delimiters, supports an explicit delimiter override and configurable JSON indentation. It preserves quoted multiline fields, emits UTF-8 JSON without ASCII-escaping Unicode, and rejects malformed row widths instead of silently reshaping data.

## Verification

```bash
python -m pytest -q
```

Preflight on the AgenteRenda workspace: **5 tests passed**.
