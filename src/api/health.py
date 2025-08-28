from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from src.core.config import HEALTH_SECRET_KEY

router = APIRouter(tags=["health"])


@router.get("/health")
async def health(request: Request):
    key = request.headers.get("X-Health-Key")
    if key != HEALTH_SECRET_KEY:
        raise HTTPException(status_code=403, detail="Forbidden")
    return JSONResponse({"status": "ok"})


