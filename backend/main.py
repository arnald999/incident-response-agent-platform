from fastapi import FastAPI

from backend.api.incident_routes import router as incident_router

app = FastAPI(
    title="Incident Response Agent Platform",
    version="0.1.0",
)

app.include_router(incident_router)


@app.get("/health")
async def health():
    return {"status": "healthy"}