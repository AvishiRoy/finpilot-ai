from fastapi import FastAPI

from app.core.config import settings
from app.api.user import router as user_router
from app.api.auth import router as auth_router
from app.api import user, auth, categories, transactions, budgets, dashboard
from app.repositories.category_repository import CategoryRepository
from app.db.session import SessionLocal


# Create FastAPI app FIRST
app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    debug=settings.debug,
)


# Startup event
@app.on_event("startup")
def seed_default_categories():
    """Seed system categories once at startup if they don't exist yet."""
    db = SessionLocal()
    try:
        CategoryRepository(db).seed_defaults()
    finally:
        db.close()


# Routers
app.include_router(user_router)
app.include_router(auth_router)

app.include_router(categories.router, prefix="/api")
app.include_router(transactions.router, prefix="/api")
app.include_router(budgets.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")


@app.get("/", tags=["root"])
def read_root():
    return {
        "message": f"Welcome to {settings.app_name}",
        "status": "running",
    }


@app.get("/health", tags=["monitoring"])
def health_check():
    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.app_env,
    }