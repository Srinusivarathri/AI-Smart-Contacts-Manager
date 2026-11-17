from fastapi import FastAPI

from app.routes import health, search

app = FastAPI(title="AI Service")

app.include_router(health.router)
app.include_router(search.router)


@app.get("/")
def root():
    return {"service": "AI Service", "status": "running"}