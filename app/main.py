
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.services.tools import (
    calculate_total,
    get_server_status,
)

app = FastAPI(
    title="AI Chatbot Tool Server",
    version="1.0.0",
)


class CalculateRequest(BaseModel):
    price: float = Field(ge=0)
    quantity: int = Field(ge=0)


@app.get("/")
async def home():
    return {"message": "AI Chatbot Tool Server is running"}


@app.post("/calculate")
async def calculate(request: CalculateRequest):
    return calculate_total(
        request.price,
        request.quantity,
    )


@app.get("/server-status/{service_name}")
async def server_status(service_name: str):
    try:
        return get_server_status(service_name)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
