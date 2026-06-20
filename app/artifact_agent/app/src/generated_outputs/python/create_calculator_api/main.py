from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid

app = FastAPI()

class CalculationCreateRequest(BaseModel):
    operation: str
    operands: List[float]

class CalculationUpdateRequest(BaseModel):
    operation: Optional[str] = None
    operands: Optional[List[float]] = None

class CalculationResponse(BaseModel):
    id: str
    result: float
    createdAt: str
    updatedAt: str

class ErrorResponse(BaseModel):
    message: str
    code: int

calculations = {}

@app.post('/calculator', response_model=CalculationResponse, status_code=201)
async def create_calculation(request: CalculationCreateRequest):
    calc_id = str(uuid.uuid4())
    result = eval(f"{request.operands[0]} {request.operation} {request.operands[1]}")
    calculations[calc_id] = {
        'id': calc_id,
        'result': result,
        'createdAt': '2023-10-01T00:00:00Z',
        'updatedAt': '2023-10-01T00:00:00Z'
    }
    return calculations[calc_id]

@app.put('/calculator/{id}', response_model=CalculationResponse)
async def update_calculation(id: str, request: CalculationUpdateRequest):
    if id not in calculations:
        raise HTTPException(status_code=404, detail='Calculation not found')
    if request.operation:
        calculations[id]['operation'] = request.operation
    if request.operands:
        calculations[id]['operands'] = request.operands
    calculations[id]['result'] = eval(f"{calculations[id]['operands'][0]} {calculations[id]['operation']} {calculations[id]['operands'][1]}")
    calculations[id]['updatedAt'] = '2023-10-01T00:00:00Z'
    return calculations[id]

@app.delete('/calculator/{id}', status_code=204)
async def delete_calculation(id: str):
    if id not in calculations:
        raise HTTPException(status_code=404, detail='Calculation not found')
    del calculations[id]

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return ErrorResponse(message=exc.detail, code=exc.status_code)
