# JSON to CSV converter sample

Self-produced AgenteRenda portfolio sample. This is **not** presented as a completed paid contract.

Python 3.10+ command-line utility for converting an array of flat JSON objects to CSV.

## Usage

```bash
python converter.py input.json output.csv
```

Keys are collected in stable encounter order across all objects. Missing keys are emitted as empty CSV fields. Invalid top-level shapes are rejected.

## Verification

```bash
python -m pytest -q
```

Preflight on the AgenteRenda workspace: **2 tests passed**.
