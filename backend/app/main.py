import os
from contextlib import asynccontextmanager

from pillow_heif import register_heif_opener
register_heif_opener()  # enables Pillow to open HEIC/HEIF images from iPhone

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
    # Create all tables — checkfirst=True skips tables that already exist
    Base.metadata.create_all(bind=engine, checkfirst=True)
    yield


app = FastAPI(
    title=settings.APP_NAME,
    description="Intelligent wardrobe management & outfit recommendation API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

_raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000")
_allowed_origins = [o.strip() for o in _raw_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
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
