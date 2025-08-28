from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from src.api.init import api_router
from src.core.config import ADDRESS_FRONT

app = FastAPI(title="Deepbot API")

origins = [ADDRESS_FRONT,]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)
