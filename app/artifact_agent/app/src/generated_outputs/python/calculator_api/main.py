from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from datetime import datetime
from typing import Literal, Optional
import uuid

app = FastAPI()

class CalculationCreateRequest(BaseModel):
    operand1: float
    operand2: float
    operation: Literal["add", "subtract", "multiply", "divide"]

class CalculationResponse(BaseModel):
    id: str
    operand1: float
    operand2: float
    operation: str
    result: float
    createdAt: datetime

class ErrorResponse(BaseModel):
    error: str
    message: str
    statusCode: int

@app.post("/calculations", response_model=CalculationResponse, status_code=status.HTTP_201_CREATED)
async def create_calculation(request: CalculationCreateRequest):
    try:
        result = 0.0
        if request.operation == "add":
            result = request.operand1 + request.operand2
        elif request.operation == "subtract":
            result = request.operand1 - request.operand2
        elif request.operation == "multiply":
            result = request.operand1 * request.operand2
        elif request.operation == "divide":
            if request.operand2 == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "error": "Bad Request",
                        "message": "Division by zero is not allowed",
                        "statusCode": status.HTTP_400_BAD_REQUEST
                    }
                )
            result = request.operand1 / request.operand2

        return {
            "id": str(uuid.uuid4()),
            "operand1": request.operand1,
            "operand2": request.operand2,
            "operation": request.operation,
            "result": result,
            "createdAt": datetime.now()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Internal Server Error",
                "message": str(e),
                "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR
            }
        )
