"""Pydantic schemas for Calc Service API."""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal, List
from datetime import datetime
from enum import Enum


class Operation(str, Enum):
    """Supported mathematical operations."""
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"
    MODULO = "modulo"
    POWER = "power"
    SQRT = "sqrt"


class CalculateRequest(BaseModel):
    """Request schema for calculation endpoint."""
    operation: Operation = Field(..., description="Operação matemática a executar")
    operand_a: str = Field(..., pattern=r"^-?[0-9]+\.?[0-9]*$", description="Primeiro operando como STRING")
    operand_b: Optional[str] = Field(None, pattern=r"^-?[0-9]+\.?[0-9]*$", description="Segundo operando como STRING")
    precision: int = Field(default=28, ge=0, le=28, description="Precisão decimal (0-28)")
    
    @field_validator("operand_b")
    @classmethod
    def validate_operand_b(cls, v: Optional[str], info) -> Optional[str]:
        """Validate that operand_b is provided for non-sqrt operations."""
        values = info.data
        if values.get("operation") != Operation.SQRT and v is None:
            raise ValueError("operand_b é obrigatório para esta operação")
        return v


class CalculateResponse(BaseModel):
    """Response schema for successful calculation."""
    success: Literal[True] = True
    result: str = Field(..., description="Resultado do cálculo em formato STRING")
    operation: Operation
    operand_a: str
    operand_b: Optional[str]
    precision: int
    timestamp: str
    request_id: str


class OperationInfo(BaseModel):
    """Information about a supported operation."""
    id: str
    name: str
    symbol: str
    description: str
    operands: int
    example: str


class OperationsResponse(BaseModel):
    """Response schema for operations list."""
    success: Literal[True] = True
    operations: List[OperationInfo]
    count: int
    timestamp: str


class ErrorDetail(BaseModel):
    """Error detail information."""
    code: str = Field(..., pattern=r"^E[0-9]{4}$")
    message: str
    field: Optional[str] = None
    details: Optional[dict] = None


class ErrorResponse(BaseModel):
    """Response schema for errors."""
    success: Literal[False] = False
    error: ErrorDetail
    timestamp: str
    request_id: str


class HealthCheck(BaseModel):
    """Health check response."""
    status: str
    timestamp: str
    version: str
    uptime: int
    checks: dict
