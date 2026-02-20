"""FastAPI REST API exposing the calculator module over HTTP."""

import logging
from enum import Enum

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from calculator import add, subtract, multiply, divide

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Calculator API",
    description="A REST API for basic arithmetic operations.",
    version="1.0.0",
)


class Operation(str, Enum):
    """Supported arithmetic operations."""

    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"


class CalculationRequest(BaseModel):
    """Request body for a calculation.

    Attributes:
        operation: The arithmetic operation to perform.
        a: First operand.
        b: Second operand.
    """

    operation: Operation
    a: float = Field(..., description="First operand")
    b: float = Field(..., description="Second operand")


class CalculationResponse(BaseModel):
    """Response body for a successful calculation.

    Attributes:
        operation: The operation that was performed.
        a: First operand.
        b: Second operand.
        result: The computed result.
    """

    operation: str
    a: float
    b: float
    result: float


class ErrorResponse(BaseModel):
    """Response body for an error.

    Attributes:
        error: Error type identifier.
        detail: Human-readable error message.
    """

    error: str
    detail: str


_OPERATIONS = {
    Operation.ADD: add,
    Operation.SUBTRACT: subtract,
    Operation.MULTIPLY: multiply,
    Operation.DIVIDE: divide,
}


@app.get("/health")
def health_check() -> dict:
    """Return service health status.

    Returns:
        Dictionary with status key.
    """
    return {"status": "healthy"}


@app.post(
    "/calculate",
    response_model=CalculationResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Division by zero"},
        422: {"model": ErrorResponse, "description": "Validation error"},
    },
)
def calculate(request: CalculationRequest) -> CalculationResponse:
    """Perform an arithmetic calculation.

    Args:
        request: The calculation request containing operation and operands.

    Returns:
        CalculationResponse with the computed result.

    Raises:
        HTTPException: 400 if division by zero is attempted.
    """
    func = _OPERATIONS[request.operation]

    try:
        result = func(request.a, request.b)
    except ZeroDivisionError:
        logger.warning(
            "Division by zero attempted: %s / %s", request.a, request.b
        )
        raise HTTPException(
            status_code=400,
            detail={"error": "division_by_zero", "detail": "Cannot divide by zero"},
        )

    logger.info(
        "Calculated %s(%s, %s) = %s",
        request.operation.value,
        request.a,
        request.b,
        result,
    )

    return CalculationResponse(
        operation=request.operation.value,
        a=request.a,
        b=request.b,
        result=result,
    )
