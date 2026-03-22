import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .core.config import get_settings
from .core.database import engine, Base
from .models import User, ClothingItem, Outfit, WearLog  # noqa: F401 — register models
from .routers import auth, items, outfits, recommendations, wear_logs, stats

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure upload directory exists
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    # Create all tables (dev convenience — Alembic handles prod migrations)
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.APP_NAME,
    description="Intelligent wardrobe management & outfit recommendation API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

app.include_router(auth.router)
app.include_router(items.router)
app.include_router(outfits.router)
app.include_router(wear_logs.router)
app.include_router(recommendations.router)
app.include_router(stats.router)


@app.get("/health", tags=["system"])
def health_check():
    return {"status": "ok", "app": settings.APP_NAME, "version": "0.1.0"}
