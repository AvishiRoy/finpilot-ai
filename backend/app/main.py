from fastapi import FastAPI

from app.core.config import settings

# The FastAPI app instance is the core of the application.
# title/version here automatically populate the Swagger UI at /docs.
app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    debug=settings.debug,
)


@app.get("/", tags=["root"])
def read_root() -> dict:
    """
    Root endpoint.

    Confirms the API is reachable and identifies the service.
    Useful as a quick sanity check (e.g. when hitting the base deployment URL).
    """
    return {
        "message": f"Welcome to {settings.app_name}",
        "status": "running",
    }


@app.get("/health", tags=["monitoring"])
def health_check() -> dict:
    """
    Health check endpoint.

    Used by load balancers, container orchestrators (e.g. Docker, ECS, Kubernetes),
    and uptime monitors to verify the service is alive. Intentionally lightweight —
    no database or external calls — so it responds fast and doesn't itself become
    a point of failure.
    """
    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.app_env,
    }