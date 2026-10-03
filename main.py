"""LegalEase FastAPI backend."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import router

app = FastAPI(
    title="LegalEase API",
    description="Educational legal document drafting demo",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)
app.include_router(router)


@app.get("/")
def home():
    return {"app": "LegalEase", "status": "running", "docs": "/docs"}
