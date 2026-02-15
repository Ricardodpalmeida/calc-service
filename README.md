# calc-service

> High-precision decimal calculator for OpenClaw agents.

---

## Quick Start

```bash
# Add to PATH
export PATH="$HOME/.openclaw/workspace/calc-service/cli:$PATH"

# Calculate
calc-service calculate --operation add --a "0.1" --b "0.2"
# → 0.3

calc-service calc -o multiply -a "10.5" -b "2" --json
# → {"result": "21.0", ...}
```

---

## Features

- **Decimal precision** — Uses `decimal.Decimal`, no floating-point errors
- **7 operations** — add, subtract, multiply, divide, modulo, power, sqrt
- **CLI tool** — Easy command-line interface
- **JSON output** — Machine-parseable results
- **Skill integration** — Available to all OpenClaw agents

---

## Operations

| Operation | Symbol | Example |
|-----------|--------|---------|
| add | + | `0.1 + 0.2 = 0.3` |
| subtract | - | `10 - 3 = 7` |
| multiply | * | `10.5 * 2 = 21.0` |
| divide | / | `10 / 3 = 3.333...` |
| modulo | % | `10 % 3 = 1` |
| power | ^ | `2 ^ 10 = 1024` |
| sqrt | √ | `√2 = 1.414...` |

---

## Backend API

FastAPI backend with OpenAPI docs:
- `GET /health` — Health check
- `GET /api/v1/operations` — List operations  
- `POST /api/v1/calculate` — Calculate

Start server:
```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --port 8000
```

---

## Project Structure

```
calc-service/
├── backend/          # FastAPI API
│   ├── app/
│   │   ├── api/v1/calculator.py
│   │   ├── services/calculator.py  # Decimal engine
│   │   └── schemas/calculation.py
│   └── tests/
├── cli/              # Command-line tool
│   └── calc-service.py
└── docs/             # Documentation
```

---

## Documentation

Full specification in Obsidian:  
`4. Projects/[OpenClaw] 20260215 calc-service/`

---

**Created**: 2026-02-15  
**Version**: 1.0.0