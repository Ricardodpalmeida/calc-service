"""API v1 endpoints for calculator operations."""

from fastapi import APIRouter, HTTPException, status
from datetime import datetime
import uuid

from app.schemas.calculation import (
    CalculateRequest,
    CalculateResponse,
    OperationsResponse,
    OperationInfo,
    ErrorResponse,
    ErrorDetail
)
from app.services.calculator import CalculatorEngine, CalculatorError, Operation
from app.config import settings


router = APIRouter()
calculator = CalculatorEngine()

# Operation definitions for /operations endpoint
OPERATIONS = [
    OperationInfo(
        id="add",
        name="Adição",
        symbol="+",
        description="Soma dois números",
        operands=2,
        example="0.1 + 0.2 = 0.3"
    ),
    OperationInfo(
        id="subtract",
        name="Subtração",
        symbol="-",
        description="Subtrai o segundo do primeiro",
        operands=2,
        example="5 - 3 = 2"
    ),
    OperationInfo(
        id="multiply",
        name="Multiplicação",
        symbol="*",
        description="Multiplica dois números",
        operands=2,
        example="4 * 3 = 12"
    ),
    OperationInfo(
        id="divide",
        name="Divisão",
        symbol="/",
        description="Divide o primeiro pelo segundo",
        operands=2,
        example="10 / 3 = 3.333..."
    ),
    OperationInfo(
        id="modulo",
        name="Módulo",
        symbol="%",
        description="Resto da divisão inteira",
        operands=2,
        example="10 % 3 = 1"
    ),
    OperationInfo(
        id="power",
        name="Potência",
        symbol="^",
        description="Eleva à potência",
        operands=2,
        example="2^3 = 8"
    ),
    OperationInfo(
        id="sqrt",
        name="Raiz Quadrada",
        symbol="√",
        description="Calcula a raiz quadrada",
        operands=1,
        example="√16 = 4"
    ),
]


@router.post(
    "/calculate",
    response_model=CalculateResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Calculation error"},
        422: {"model": ErrorResponse, "description": "Validation error"}
    }
)
async def calculate(request: CalculateRequest):
    """
    Execute a mathematical calculation with decimal precision.
    
    - **operation**: Mathematical operation to perform
    - **operand_a**: First operand (as string to preserve precision)
    - **operand_b**: Second operand (optional for sqrt)
    - **precision**: Decimal precision (0-28, default 28)
    """
    request_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    try:
        # Set precision for this calculation
        calculator.set_precision(request.precision)
        
        # Execute calculation (operation is already validated by Pydantic)
        result = calculator.calculate(
            operation=Operation(request.operation.value),
            operand_a=request.operand_a,
            operand_b=request.operand_b
        )
        
        return CalculateResponse(
            result=str(result),  # Return as string to preserve precision
            operation=request.operation,
            operand_a=request.operand_a,
            operand_b=request.operand_b,
            precision=request.precision,
            timestamp=timestamp,
            request_id=request_id
        )
    
    except CalculatorError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "error": {
                    "code": e.code,
                    "message": e.message,
                    "field": e.field,
                    "details": e.details
                },
                "timestamp": timestamp,
                "request_id": request_id
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error": {
                    "code": "E5000",
                    "message": "Erro interno do servidor",
                    "field": None,
                    "details": str(e)
                },
                "timestamp": timestamp,
                "request_id": request_id
            }
        )


@router.get("/operations", response_model=OperationsResponse)
async def list_operations():
    """List all supported mathematical operations with metadata."""
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    return OperationsResponse(
        operations=OPERATIONS,
        count=len(OPERATIONS),
        timestamp=timestamp
    )
