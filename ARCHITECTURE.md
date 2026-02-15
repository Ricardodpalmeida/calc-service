# calc-service Architecture

## System Overview

```mermaid
flowchart TB
    subgraph "Agent Layer"
        A[Any Agent]
    end
    
    subgraph "Interface Layer"
        B[CLI Tool<br/>calc-service.py]
        C[Skill Interface<br/>skill:calc-service]
    end
    
    subgraph "API Layer"
        D[FastAPI Backend<br/>Port 8000]
        E[API Endpoints<br/>/calculate /operations /health]
    end
    
    subgraph "Core Engine"
        F[CalculatorEngine<br/>decimal.Decimal]
        G[Operations<br/>add subtract multiply<br/>divide modulo power sqrt]
    end
    
    subgraph "Validation"
        H[Pydantic Schemas<br/>Request/Response]
        I[Error Handler<br/>DivisionByZero<br/>InvalidInput]
    end
    
    A -->|skill:calc-service| C
    A -->|calc-service calc| B
    B -->|HTTP| D
    C -->|HTTP| D
    D --> E
    E --> H
    E --> I
    E --> F
    F --> G
```

## Data Flow

```mermaid
sequenceDiagram
    participant User as Agent/User
    participant CLI as CLI Tool
    participant API as FastAPI
    participant Engine as CalculatorEngine
    participant Decimal as decimal.Decimal

    User->>CLI: calc-service calc -o add -a "0.1" -b "0.2"
    CLI->>API: POST /api/v1/calculate
    Note over API: Request Validation
    API->>Engine: calculate(Operation.ADD, "0.1", "0.2")
    Engine->>Decimal: Decimal("0.1") + Decimal("0.2")
    Decimal-->>Engine: Decimal("0.3")
    Engine-->>API: result
    API-->>CLI: {"result": "0.3", ...}
    CLI-->>User: 0.3
```

## Component Details

| Component | Purpose | Technology |
|-----------|---------|------------|
| **CLI Tool** | Command-line interface for agents | Python + argparse |
| **Skill Interface** | OpenClaw skill wrapper | SKILL.md + Python |
| **FastAPI** | HTTP API server | Python + FastAPI |
| **CalculatorEngine** | Core calculation logic | decimal.Decimal |
| **Pydantic** | Request/response validation | Pydantic v2 |
| **Error Handler** | Custom exceptions | Python classes |

## Precision Guarantee

```mermaid
flowchart LR
    A[Input:<br/>0.1 + 0.2] -->|float| B[Regular Calc<br/>0.30000000000000004]
    A -->|string| C[calc-service]
    C -->|Decimal| D[Exact Result<br/>0.3]
    
    style B fill:#fbb,stroke:#333
    style D fill:#bfb,stroke:#333
```

## API Contract

### Request
```json
{
  "operation": "add",
  "operand_a": "0.1",
  "operand_b": "0.2",
  "precision": 28
}
```

### Response
```json
{
  "result": "0.3",
  "operation": "add",
  "precision": 28,
  "success": true
}
```

### Error Response
```json
{
  "error": {
    "code": "E4001",
    "message": "Divisão por zero não permitida",
    "field": "operand_b"
  },
  "success": false
}
```

## File Structure

```
calc-service/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── config.py            # Settings
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── calculator.py  # Endpoints
│   │   ├── services/
│   │   │   └── calculator.py      # Decimal engine
│   │   └── schemas/
│   │       └── calculation.py     # Pydantic models
│   └── tests/
│       └── test_calculator.py
├── cli/
│   └── calc-service.py          # CLI tool
└── docs/
    └── SKILL.md                 # Agent interface
```

---

**Default for diagrams: Mermaid**  
*Image generation only when explicitly requested*