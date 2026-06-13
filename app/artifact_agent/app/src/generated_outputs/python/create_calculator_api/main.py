from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Union

app = FastAPI()

class CalculationRequest(BaseModel):
    operation: str
    operands: List[Union[int, float]]

class ErrorResponse(BaseModel):
    message: str
    code: int

@app.post('/calculator')
async def perform_calculation(request: CalculationRequest):
    if request.operation not in ['add', 'subtract', 'multiply', 'divide']:
        raise HTTPException(status_code=400, detail=ErrorResponse(message='Invalid operation', code=400).dict())
    if len(request.operands) < 2:
        raise HTTPException(status_code=400, detail=ErrorResponse(message='At least two operands are required', code=400).dict())
    result = None
    if request.operation == 'add':
        result = sum(request.operands)
    elif request.operation == 'subtract':
        result = request.operands[0] - sum(request.operands[1:])
    elif request.operation == 'multiply':
        result = 1
        for operand in request.operands:
            result *= operand
    elif request.operation == 'divide':
        try:
            result = request.operands[0]
            for operand in request.operands[1:]:
                result /= operand
        except ZeroDivisionError:
            raise HTTPException(status_code=500, detail=ErrorResponse(message='Division by zero', code=500).dict())
    return {'result': result}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)