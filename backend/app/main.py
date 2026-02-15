"""Main FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from app.api.v1.calculator import router as calculator_router
from app.config import settings
from app.schemas.calculation import HealthCheck


def create_application() -> FastAPI:
    """Application factory pattern."""
    
    app = FastAPI(
        title="Calc Service API",
        description="High-precision decimal calculator API for agents",
        version=settings.VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # API routes
    app.include_router(
        calculator_router,
        prefix=settings.API_PREFIX
    )
    
    return app


app = create_application()
start_time = datetime.utcnow()


@app.get("/health", response_model=HealthCheck)
async def health_check():
    """
    Health check endpoint.
    Returns service status, version, and uptime.
    """
    now = datetime.utcnow()
    uptime = int((now - start_time).total_seconds())
    
    return HealthCheck(
        status="healthy",
        timestamp=now.isoformat() + "Z",
        version=settings.VERSION,
        uptime=uptime,
        checks={
            "calculator": "ok",
            "api": "ok"
        }
    )


@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "name": "Calc Service API",
        "version": settings.VERSION,
        "docs": "/docs",
        "health": "/health"
    }
