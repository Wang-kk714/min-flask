from fastapi import APIRouter, Body
from src.service.symphony_adapter import build_messageML

adapter = APIRouter(
    prefix="/v1/adapter",
    tags=["adapter"]
)


@adapter.post("/symphony")
async def symphony_adapter(payload: dict = Body(...)):
    res = build_messageML(payload)
    return {"status_code": 200, "data": res}
