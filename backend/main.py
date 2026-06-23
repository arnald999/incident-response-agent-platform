from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.api.incident_routes import router as incident_router
from backend.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="Incident Response Agent Platform",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(incident_router)


@app.get("/health")
async def health():
    return {"status": "healthy"}